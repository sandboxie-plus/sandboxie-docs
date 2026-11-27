# Taskbar Unique

`TaskbarUnique` is an inactive setting for adding text to the prefix Sandboxie uses for taskbar application IDs (`AppUserModelID`). It is not an on/off setting for taskbar grouping. [^1]

## Syntax

`TaskbarUnique=<text>`

> [!NOTE]
> The checked-in standard build does not define `CUSTOM_APPUSERMODELID`, so it does not read this entry. The destination buffer and the formatter that would add that text to the prefix are also commented out. Defining the flag alone would not restore the feature. [^1]

## Standard behavior

When Sandboxie prefixes a taskbar application ID, the prefix is `Sandbox.<box>.` with the actual sandbox name in place of `<box>`. It does not include a value from `TaskbarUnique`. [^1]

## See also

- [Taskbar Name](TaskbarName.md)
- [Taskbar Program](TaskbarProgram.md)

[^1]: [Taskbar ID prefix construction](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/dll/taskbar.c#L173-L202).
