# SandMan Triggers

SandMan supports commands that run automatically in response to selected sandbox events. The following settings use this mechanism:

* `OnBoxDelete`
* `OnBoxTerminate`
* `OnFileRecovery`

> **Security note:** SandMan triggers are trusted management automation configured by the user. `SandMan.exe` launches their commands on the host, outside the sandbox that caused the event.

Trigger commands are not callbacks to sandboxed applications. They run in SandMan's current user and security context and are not automatically elevated. If SandMan is already elevated, the command inherits that elevated context. Restrictions applied to the originating sandbox, such as its `StartRunAccess` rules, do not contain the host-side command.

## Configuration

```ini
OnBoxDelete=<command line>
OnBoxTerminate=<command line>
OnFileRecovery=<command line>
```

Each setting may be repeated. Commands are executed sequentially in the effective order returned by the configuration. Do not rely on a particular ordering between entries inherited from several templates and `GlobalSettings`.

For example:

```ini
OnBoxTerminate="C:\Tools\box-audit.exe" --box "%BoxName%"
OnBoxTerminate="C:\Tools\cleanup-log.exe" "%BoxPath%"
```

Useful Sandboxie expansions include:

* `%SbieHome%` — the Sandboxie installation directory;
* `%BoxPath%` — the sandbox file root;
* `%BoxName%` — the sandbox name.

Normal Sandboxie configuration expansion also applies to other supported `%...%` variables. See [Expandable Variables](ExpandableVariables.md) for related configuration concepts.

SandMan launches the configured command line directly. There is no implicit `cmd.exe` shell, so batch files and shell operators require an explicit command interpreter where applicable:

```ini
OnBoxDelete=cmd.exe /c "C:\Scripts\cleanup.cmd"
```

Executable paths containing spaces should be quoted. The command inherits SandMan's environment and current working directory; no particular working directory, such as the Sandboxie installation directory, should be assumed.

## OnBoxDelete

`OnBoxDelete` runs configured host-side commands before SandMan cleans the contents of a sandbox. It applies to:

* manual **Delete Contents** operations;
* [AutoDelete](AutoDelete.md) cleanup;
* equivalent SandMan content-cleanup operations;
* silent or asynchronous cleanup paths.

Removing the sandbox definition itself does not normally invoke this trigger. `OnBoxDelete` describes automation before content cleanup, not removal of the sandbox configuration.

When AutoDelete follows the closing of a box, the relevant order is:

1. `OnBoxTerminate` runs first.
2. SandMan may offer recovery handling.
3. If cleanup proceeds, `OnBoxDelete` runs.
4. SandMan performs the resulting snapshot-aware cleanup action.

If AutoDelete recovery is cancelled before cleanup begins, `OnBoxTerminate` may already have run, but `OnBoxDelete` does not run.

`OnBoxDelete` runs before SandMan performs snapshot-aware cleanup. Depending on the cleanup selection and configuration, SandMan may return to the active snapshot state, return to the default snapshot state, or perform full cleanup when snapshots are removed. The trigger does not automatically receive snapshot information. See [Box Snapshots](../PlusContent/BoxSnapshots.md) for general snapshot behavior.

`OnBoxDelete` is available since Sandboxie Plus 1.0.10.

## OnBoxTerminate

`OnBoxTerminate` normally runs when SandMan observes that a sandbox which had active processes now has no remaining active processes. It does not run for every individual process exit.

```text
active process count > 0
        ↓
active process count = 0
        ↓
OnBoxTerminate
```

This can occur after:

* the last process exits naturally;
* **Terminate All**, once all processes are actually gone;
* forced termination that leaves the box empty.

If the box later starts processes and becomes empty again, the trigger can run again. `LingerProcess` and `LeaderProcess` do not directly fire it, although they can influence when the box eventually reaches zero active processes.

`OnBoxTerminate` runs before SandMan's AutoDelete handling. Trigger exit status should not be treated as a prerequisite for AutoDelete.

As an edge case, SandMan's startup cleanup mode can invoke box-closed handling for a box that is already empty, which can also cause `OnBoxTerminate` to run.

`OnBoxTerminate` is available since Sandboxie Plus 1.13.1.

## OnFileRecovery

For each file, `OnFileRecovery` runs configured checker commands before SandMan attempts to move that file to its host recovery destination. It is a per-file check, not a callback after the complete recovery operation.

SandMan expands the configured command and appends the quoted physical path of the file inside sandbox storage. For example:

```ini
OnFileRecovery="C:\Tools\scan.exe" --check
```

is executed conceptually as:

```text
"C:\Tools\scan.exe" --check "<physical sandbox file path>"
```

The sandbox-file path is the final automatically appended argument when the configured command already contains arguments. SandMan does not automatically append the recovery destination, recovery method, or box name. `%BoxName%` can be used when the checker needs the box name.

The checker applies to recovery operations that use SandMan's normal recovery engine, including:

* normal and [Quick Recovery](QuickRecovery.md) flows;
* recovery from Auto/Instant Recovery prompts;
* recovery initiated from SandMan's file view.

This does not guarantee coverage of external drag-and-drop or other mechanisms that do not use SandMan's recovery engine.

An exit code of zero allows recovery to continue. A nonzero exit code or failure to start the checker causes SandMan to ask whether the file should be recovered anyway or skipped. The decision can be applied to the remaining files in the current operation. Files already recovered are not rolled back.

A checker is therefore a user-assisted compatibility and safety step, not a mandatory security boundary. A long-running checker can delay the recovery operation.

`OnFileRecovery` was introduced in Sandboxie Plus 1.7.0. Although current setting metadata lists 1.4.0, source history and the changelog identify 1.7.0 as its introduction.

## Failure behavior

Trigger failure handling is not uniform and should not be treated as a transactional policy mechanism.

For `OnBoxDelete` and `OnBoxTerminate`, do not assume that a nonzero command exit code cancels the cleanup, termination, or subsequent AutoDelete action. These triggers are intended for automation rather than enforcement. If cleanup later fails, commands that already ran are not rolled back.

`OnFileRecovery` is different because its result is explicitly considered by the recovery workflow, which lets the user continue or skip the affected file.

## Inheritance, imports, and configuration trust

Trigger entries can come from the sandbox section, enabled templates, or `GlobalSettings`. SandMan can also disable inherited trigger entries. Saved changes generally apply to the next corresponding event; sandboxed applications do not need to restart solely because a trigger definition changed. Changes made after an operation has already captured its command list do not alter that running operation.

> **Review trigger settings when importing or enabling configuration from an untrusted source, because these entries can launch host-side commands through SandMan.**

Imported sandbox configurations can contain trigger settings, as can templates received from another source. This does not make importing configurations unsafe by definition, but it makes reviewing their trigger entries important before enabling or using them. See [Import Box](ImportBox.md) for import information.

Normal [Configuration Protection](ConfigurationProtection.md) can restrict who may change Sandboxie configuration. It does not make an arbitrary imported command trustworthy.

## SandMan interface

The controls are located under:

**Sandbox Options > Advanced Options > Triggers**

The current user-facing actions are:

* **On Delete Content** — **Run Command**;
* **On Box Terminate** — **Run Command**;
* **On File Recovery** — **Run File Checker**.

SandMan accepts free-form command lines and supports multiple entries.

## Sandboxie Plus and Classic

`OnBoxDelete`, `OnBoxTerminate`, and `OnFileRecovery` are currently consumed by SandMan. Sharing the same Sandboxie configuration file does not cause Sandboxie Control Classic to execute them, and Classic does not provide equivalent support for these SandMan triggers.

`OnBoxDelete` is SandMan's modern pre-cleanup trigger. The legacy [DeleteCommand](DeleteCommand.md) setting remains in use by Sandboxie Control Classic and `Start.exe`, where it selects the command that performs directory deletion.

The two settings are not equivalent:

* `OnBoxDelete` runs user-configured automation before SandMan cleanup.
* `DeleteCommand` selects the legacy deletion command used by Classic and `Start.exe` to remove prepared sandbox directories.
