# Program Forcing Controls

Automatic forcing determines how a **new process start** is handled when a program would otherwise start outside a sandbox. The driver makes the core selection in `Process_GetForcedStartBox()`. Configured force rules, global program alerts, and the temporary **Pause Forcing Programs** state serve different purposes; none is a general switch for all Sandboxie isolation.

## How a start is evaluated

Sandboxie considers whether a process is already associated with a sandbox path, then evaluates configured force rules for boxes enabled for the current user and session. Each box can contribute [Force Folder](ForceFolder.md), [Force Process](ForceProcess.md), and [Force Children](ForceChildren.md) rules; there is no single global destination box. [Disable Force Rules](DisableForceRules.md) excludes a box from the force data built for those rules.

For normal configured rules, the existing detailed order is: executable-directory `ForceFolder` → `ForceProcess` / configured `ForceChildren` → working-directory `ForceFolder` → document-argument `ForceFolder`. The linked setting pages cover matching syntax and exceptions.

If normal forcing has not selected a box, the driver checks global `AlertFolder` and then `AlertProcess` entries. An ordinary alert-list match reports or denies an unsandboxed start; it does **not** select a sandbox. Other independent paths, including Mark-of-the-Web forcing, may be evaluated later. A successful normal force selection does not also pass through this ordinary alert-list branch.

| Mechanism | Scope | Persistence | Effect on new starts |
| --- | --- | --- | --- |
| `DisableForceRules=y` | One box | Configuration | Excludes that box from normal force-data participation. |
| **Pause Forcing Programs** | Windows session | Temporary, timed state | Skips assignment for a matching normal force rule while active. |
| `AlertFolder` / `AlertProcess` | Global | Configuration | Matches starts outside sandboxes for notification or denial; does not select a box. |
| `StartRunAlertDenied=y` | Global | Configuration | Makes normal alert-list matches deny the start. |
| `AllowForceSystem=y` | Global | Configuration | Removes a default identity-based exclusion from the main force/alert evaluation; a rule must still match. |

These mechanisms are not substitutes for one another. SandMan may also retain unchecked individual force entries as disabled UI entries; those are neither active forcing rules nor the same as `DisableForceRules` or the session pause.

## Global program alerts and blocking

`AlertFolder` and `AlertProcess` are global lists under `[GlobalSettings]`, not per-box destination rules:

```ini
[GlobalSettings]
AlertFolder=C:\Example
AlertProcess=example.exe
```

[Alert Folder](AlertFolder.md) tests the executable's own path/directory at process start. Unlike `ForceFolder`, it does not inspect the working directory or document argument for its alert match. Ordinary folder entries match recursively under that folder; wildcard entries use pattern matching. [Alert Process](AlertProcess.md) matches ordinary entries as image names; an entry containing `*` is treated as a case-insensitive pattern against the normalized executable path. Neither list watches arbitrary file access or activity after launch.

By default, `StartRunAlertDenied=n`: a normal alert-list match can generate [SBIE1301](SBIE1301.md) without this mechanism blocking the start. With `StartRunAlertDenied=y`, a normal alert-list match instead denies the start. `AlertStartRunAccessDenied` defaults to `y` and controls whether that denial reports [SBIE1308](SBIE1308.md); it does not control the denial itself. This global alert policy is separate from a sandbox's **Start/Run Access** restrictions.

SandMan exposes the lists under **Global Settings > Program Control > Program Alerts**, with **Add Program** and **Add Folder**. **Prevent the listed programs from starting on this system** maps to `StartRunAlertDenied`; **Issue message 1308 when a program fails to start** maps to `AlertStartRunAccessDenied` for this global path.

## Temporary pause and persistent per-box disabling

SandMan's **Pause Forcing Programs** command asks for a duration when starting a pause. The driver stores the pause timestamp for the relevant Windows session; it does not set `DisableForceRules=y` on boxes or suspend already-running processes. A matching `ForceFolder`, `ForceProcess`, or `ForceChildren` rule is skipped for a new launch while the pause is effective.

A skipped force match retains its paused-force status: `StartRunAlertDenied` does **not** turn that match into a blocked start. If `NotifyForceProcessDisabled=y`, it can instead generate SBIE1301. If no force rule matched, the ordinary `AlertFolder` / `AlertProcess` checks still run and may block under `StartRunAlertDenied=y`. Pausing forcing does not disable the global alert/block list.

[Force Disable Seconds](ForceDisableSeconds.md) supplies the duration and defaults to 10 seconds. A configured global `ForceDisableSeconds=0` makes the timed pause ineffective; zero does not mean an indefinite pause or permanently disable forcing. SandMan's API writes a positive duration when supplied, so entering zero in its prompt should not be described as necessarily saving a zero-valued INI setting. The pause state remains temporary even if a positive duration is saved as configuration.

[Force Disable Admin Only](ForceDisableAdminOnly.md) defaults to `n`. With global `ForceDisableAdminOnly=y`, the pause API is restricted to Administrator accounts; it does not always require an elevated administrator token. SandMan labels this **Only Administrator user accounts can use Pause Forcing Programs command**. The underlying driver also verifies that the control caller is trusted.

## System service identities

`AllowForceSystem` is an advanced, manual global Boolean that defaults to `n`. The default guard skips the main force-rule, alert-rule, and Mark-of-the-Web evaluation for target processes running as `S-1-5-18` (LocalSystem), `S-1-5-19` (LocalService), or `S-1-5-20` (NetworkService). A process with one of these identities whose parent is identified as DcomLaunch is an explicit compatibility exception to this guard; this does not generalize to every SYSTEM-parented process.

```ini
[GlobalSettings]
AllowForceSystem=y
```

Enabling it permits those identities to participate in normal evaluation; it does not automatically force every service or change other processing outside this gate. The setting was added in Sandboxie Plus 1.16.0 / Classic 5.71.0. No dedicated current SandMan control was identified for it.

## Notifications, lifecycle, and limits

In the same global **Program Alerts** area, **Issue message 1301 when forced processes has been disabled** maps to `NotifyForceProcessDisabled`, and **Issue message 1321 when a process has been forced into a sandbox** maps to `NotifyForceProcessEnabled`. Both default to `n`. The first reports a skipped force match during a temporary pause; the second reports successful forced assignment. Neither notification setting enables, disables, or pauses forcing. See [Notification Settings](NotificationSettings.md).

Force and alert configuration affects subsequent process-start decisions after configuration is applied or reloaded. The session pause is live driver state and expires according to its duration. These controls do not retroactively move, terminate, or suspend processes; disable file or registry isolation or Sandboxie itself; replace sandbox Start/Run restrictions; or grant elevation. A Windows reboot is not normally required solely for these controls.
