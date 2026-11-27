# Is Virtual

`IsVirtual` reports whether the Sandboxie driver marks a configuration section as virtual. It is a read-only section property, introduced in 1.16.0 / 5.71.0. [^1]

## Syntax

There is no INI assignment. Query `IsVirtual` as a property of a named configuration section. The driver returns `Y` for a virtual section and `N` for an existing nonvirtual section. If the section does not exist, the query returns no value. [^2]

## How it is used

The driver marks a section as virtual when an in-memory configuration update creates it. The Plus configuration API reads this property to decide whether to send later writes directly to the driver instead of through the INI service. [^2] [^3]

To check whether SandMan is staging edits, see [Is Shadow](IsShadow.md). To find an imported section's path, see [INI Location](IniLocation.md). Neither question is answered by `IsVirtual` alone. [^2]

## See also

- [Import Box](ImportBox.md)

[^1]: [Release 1.16.0 / 5.71.0](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.16.0) and [tagged driver section-property lookup](https://github.com/sandboxie-plus/Sandboxie/blob/v1.16.0/Sandboxie/core/drv/conf.c#L1475-L1511).
[^2]: [Driver section-property lookup](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/drv/conf.c#L1379-L1405) and [virtual section creation](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/Sandboxie/core/drv/conf.c#L1900-L1912).
[^3]: [Plus configuration API property lookup](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/QSbieAPI/Sandboxie/SbieIni.cpp#L30-L36) and [write dispatch](https://github.com/sandboxie-plus/Sandboxie/blob/affd54ff7a4575a2c811e64dba80593cffe7e52e/SandboxiePlus/QSbieAPI/Sandboxie/SbieIni.cpp#L370-L378).
