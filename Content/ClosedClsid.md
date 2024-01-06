# Closed Clsid

The _ClosedClsid_ setting in [Sandboxie Ini](SandboxieIni.md) (available since v0.5.3a / 5.45.2) is employed to specify COM class identifiers for unsandboxed COM objects that should be restricted from access by sandboxed programs.

To utilize this setting, you can include it in the [DefaultBox] section, as shown below:

```ini
[DefaultBox]
ClosedClsid={8BC3F05E-D86B-11D0-A075-00C04FB68820}
```

In this example, the _Windows Management and Instrumentation_ is designated as not accessible to sandboxed programs.

Additionally, it is related to the Sandboxie Plus setting found under:

Sandbox Options > Resource Access > COM
