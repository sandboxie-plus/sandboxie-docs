# Taskbar Name

`TaskbarName` is an inactive setting for changing the bracketed sandbox name in a taskbar relaunch label. It does not rename the sandbox. [^1]

## Syntax

`TaskbarName=<label-prefix>`

> [!NOTE]
> The reader is guarded by `CUSTOM_APPUSERMODELID`, which the checked-in standard build does not define. An INI entry has no effect in that build. [^1]

## Standard behavior

When Sandboxie supplies a relaunch label, it puts the real sandbox name in brackets in front of the application label, for example `[DefaultBox] Application`. The bracketed name does not come from `TaskbarName`. [^1]

## See also

- [Taskbar Program](TaskbarProgram.md)
- [Taskbar Unique](TaskbarUnique.md)

[^1]: [Conditional reader and standard taskbar label](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/dll/taskbar.c#L734-L751).
