# Protect Host Images

_ProtectHostImages_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.9.0 / 5.64.0. This setting can be enabled to prevent processes located outside the sandbox from loading boxed DLLs.

```
   .
   .
   .
   [DefaultBox]
   ProtectHostImages=y
```

Related Sandboxie Plus setting: Sandbox Options > Various Options > Dlls & Extensions > Prevent sandboxed programs installed on host from loading DLLs from the sandbox
