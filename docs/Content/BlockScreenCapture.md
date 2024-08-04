# Block Screen Capture

_BlockScreenCapture_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.13.6 / 5.68.6. If enabled, it will prevent sandboxed processes from accessing the images of the window outside the sandbox. For example:
```
   .
   .
   .
   [DefaultBox]
   BlockScreenCapture=y
```
A setting similar to _BlockScreenCapture_ is [CoverBoxedWindows](CoverBoxedWindows.md).

Related Sandboxie Plus setting: Sandbox Options > General Options > Restrictions > Prevent sandboxed processes from capturing window images
