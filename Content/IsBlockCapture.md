# Is Block Capture

_IsBlockCapture_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.13.4 / 5.68.4. If enabled, it will prevent sandboxed processes from accessing the images of the window outside the sandbox. For example:
```
   .
   .
   .
   [DefaultBox]
   IsBlockCapture=y
```
A setting similar to _IsBlockCapture_ is [IsProtectScreen](IsProtectScreen.md).

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Restriction](RestrictionsSettings.md)

Related Sandboxie Plus setting: Sandbox Options > General Options > Restrictions > Prevent sandboxed processes from using public methods to capture window images
