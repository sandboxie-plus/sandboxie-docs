# IContextMenu CLSID

`IContextMenuClsid` selects which shell extensions receive a data-object compatibility wrapper in sandboxed Windows Explorer. The value identifies the extension's COM class; it does not register the class or allow otherwise blocked access. [^1]

## Syntax

`IContextMenuClsid={<extension-clsid>}`

In [Sandboxie.ini](SandboxieIni.md), put the extension's class ID inside literal braces. Use a separate entry for each class. Sandboxie checks the current sandbox's list, including entries it inherits from templates and `[GlobalSettings]`. [^1] [^2]

## Usage

This example uses the class ID from the legacy Microsoft Security Essentials template and adds the wrapper for this extension in one sandbox. It does not enable the rest of that template. [^3]

```ini
[DefaultBox]
IContextMenuClsid={09A47860-11B0-4DA5-AFA5-26D86198A780}
```

Reload the configuration and restart sandboxed Explorer to try it with a newly created extension object. The wrapper applies after Explorer successfully creates an object for the listed class with the `IContextMenu` interface. It wraps the `IDataObject` passed to `IShellExtInit::Initialize`; it does not change other context-menu classes. [^1]

## See also

- [Use Fake Shell Dispatch](UseFakeShellDispatch.md)

[^1]: [COM activation check](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/dll/com.c#L693-L701) and [shell extension wrapper and CLSID lookup](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/dll/sh.c#L2126-L2207).
[^2]: [Lookup in the sandbox, templates, and global settings](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/drv/conf.c#L1443-L1468).
[^3]: [Microsoft Security Essentials compatibility template](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/install/Templates.ini#L2546-L2554).
