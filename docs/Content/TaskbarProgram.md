# Taskbar Program

`TaskbarProgram` is an inactive setting for choosing a different launcher in a taskbar relaunch command. It concerns which executable starts the relaunch, not which application the taskbar relaunches. [^1]

## Syntax

`TaskbarProgram=<executable-path>`

> [!NOTE]
> The path is read only in code guarded by `CUSTOM_APPUSERMODELID`. The checked-in standard build does not define that flag and ignores this entry. [^1]

## Standard behavior

Sandboxie builds its relaunch command using the `Start.exe` from its installation, followed by `/box:` with the sandbox name and then the application to relaunch. It does not use a launcher path from the INI. [^1]

## See also

- [Taskbar Name](TaskbarName.md)
- [Taskbar Unique](TaskbarUnique.md)

[^1]: [Conditional reader and standard relaunch command](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/dll/taskbar.c#L696-L727).
