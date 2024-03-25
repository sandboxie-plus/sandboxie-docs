# Notify Direct Disk Access

_NotifyDirectDiskAccess_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It is typically specified as _NotifyDirectDiskAccess=y_.

Usage:
```
   .
   .
   .
   [DefaultBox]
   NotifyDirectDiskAccess=y
```

Note that the default behavior of Sandboxie is to deny all direct access requests, unless explicit direct access is given to the hard disk device through the [OpenFilePath](OpenFilePath.md) or [OpenPipePath](OpenPipePath.md) settings. Normally, a message is not issued when such access is denied.

This setting can not be altered using [Sandboxie Control](SandboxieControl.md) and must be edited in [Sandboxie Ini](SandboxieIni.md).
