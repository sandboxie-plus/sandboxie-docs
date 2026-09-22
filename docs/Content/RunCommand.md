# RunCommand

`RunCommand` adds custom entries to a sandbox's **Run** menu in SandMan. Selecting an entry starts its configured command in that sandbox. Defining an entry does not start a program automatically, at sandbox startup, or on another sandbox event.

This is a SandMan menu feature, not a driver-enforced execution rule. The current Sandboxie Control Classic code does not provide the corresponding custom Run Menu consumer.

## Configuration formats

Each `RunCommand` line defines one menu entry. The simple format separates the displayed name from the command line with the first `|`:

```ini
[DefaultBox]
RunCommand=Notepad|"C:\Windows\notepad.exe"
RunCommand=Config\Open win.ini|"C:\Windows\notepad.exe" "C:\Windows\win.ini"
```

The command may include arguments. Quote executable paths containing spaces and quote arguments as required by the launched program. SandMan passes the command line to its normal sandbox launcher; `RunCommand` does not provide a separate shell-command parser.

A backslash in the name creates a menu hierarchy. For example, `Config\Open win.ini` appears under **Run > Config**. Multiple levels can be written as `Tools\Editors\Notepad`.

The legacy format also accepts an optional icon after the first comma in the name portion: `Name,icon|command`. Because the first comma and first `|` are separators, use JSON for menu names that need those characters.

For an icon or working directory, use a JSON value with `Command`, `Name`, optional `Icon`, and optional `WorkingDir` fields:

```ini
RunCommand={"Command":"\"C:\\Windows\\notepad.exe\" \"C:\\Windows\\win.ini\"","Name":"Config\\Open win.ini","Icon":"C:\\Windows\\System32\\notepad.exe,0","WorkingDir":"C:\\Windows"}
```

JSON requires backslashes and embedded quotation marks to be escaped as shown. SandMan's editor writes the compact legacy form when neither icon nor working directory is set; otherwise it writes JSON. It removes double quotes from `WorkingDir` when serializing an entry.

`Icon` can specify an icon file and index as `path,index`, or just an index to use with the command's executable. Without an explicit icon, SandMan tries the command executable's icon. If a specified icon cannot be loaded, it uses a fallback icon. The special index `-1` selects SandMan's Internet icon.

## Working directory and sandbox paths

`WorkingDir` is optional. When present, SandMan passes it as the working directory for the `Start.exe` launcher; when empty, SandMan does not set a working directory for that launch. Use a path appropriate for the program you start.

SandMan recognizes `%BoxRoot%` in the command and working-directory strings and replaces it with that sandbox's file-root path before launching. Pinning a program may create such a path. Do not treat this substitution as general environment-variable expansion.

## Global, sandbox, and template entries

Entries may be placed in `[GlobalSettings]` for all sandboxes or in an individual sandbox section. Applicable templates can also contribute entries. When SandMan builds a sandbox's Run menu, it requests local, template, and global values together. These entries are combined rather than treated as a single overriding value: adding a box-specific entry does not replace a global entry with the same name, and duplicate menu actions are possible.

The sandbox's **Run Menu** editor shows its own entries, not the complete effective list from global settings and templates. The global editor manages global entries separately. Because the effective list can combine entries from the sandbox, applicable templates, and global settings, do not rely on the relative order of entries from different configuration sources as a stable menu order.

## SandMan interface

For one sandbox, open **Sandbox Options > General Options > Run Menu**. The editor lists **Name** and **Command Line**, with controls to add a program or command, remove an entry, and move it up or down. **Add program** also offers **Browse for Program**.

For entries available to all sandboxes, open **Options > Global Settings > General Config > Run Menu**. This is a separate editor for `[GlobalSettings]` entries.

You can also use a running sandboxed process's **Preset > Pin to Run Menu** action. SandMan records its executable and working directory in a box-local entry. A shortcut shown under the sandbox's **Run from Start Menu** submenu can likewise be pinned, preserving its command, arguments, icon, and working directory when available. That submenu represents the sandbox's Start Menu items, not the host Windows Start Menu.

A Run Menu item can also be used to create a desktop shortcut. The `RunCommand` value itself is not a Windows `.lnk` file.

## Execution and changes

When a custom entry is selected, SandMan expands `%BoxRoot%` in its command and working directory, then calls its normal `RunStart` path with the selected box and default start flags. That path invokes `Start.exe` for the box. `RunCommand` does not request elevation or bypass the box's normal restrictions.

SandMan rebuilds the Run menu from configuration when updating the selected sandbox's menu. After saving changes, reopen the menu if necessary; existing sandboxed processes do not need to be restarted. If you edit `Sandboxie.ini` outside SandMan, reload the configuration first.

`RunCommand` is distinct from automatic startup settings such as `StartCommand` and `StartSystemBox`, and from host-side [SandMan triggers](SandManTriggers.md) such as `OnBoxDelete` or `OnBoxTerminate`. A separate `CSbieUtils::RunCommand()` helper executes other SandMan commands and is not the consumer of `RunCommand=` menu entries.

## Version history

The changelog records custom per-sandbox Run Menu commands and process pinning in the Sandboxie Plus 0.5.0 / Classic 5.45.0 release pair. This establishes the SandMan UI milestone, not the original introduction date of the `RunCommand` setting, whose current metadata has no `AddedVersion`.

Later milestones include global Run Menu entries in 1.6.1 / 5.61.1, menu folders in 1.8.0 / 5.63.0, and custom icons in 1.9.0 / 5.64.0. Subsequent releases fixed working-directory handling for Run Menu entries.

## Related pages

- [Sandboxie Ini](SandboxieIni.md)
- [Start Command Line](StartCommandLine.md)
- [Start System Box](StartSystemBox.md)
- [SandMan Triggers](SandManTriggers.md)
