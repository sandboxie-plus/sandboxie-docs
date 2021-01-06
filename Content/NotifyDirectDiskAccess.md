# Notify Direct Disk Access

_NotifyDirectDiskAccess_ is a sandbox setting in [Sandboxie Ini](SandboxieIni). It is typically specified as _NotifyDirectDiskAccess=y_, and indicates that Sandboxie should issue message [SBIE1313](SBIE1313) when programs are denied direct access to a hard disk device.

Usage:
```
   .
   .
   .
   [DefaultBox]
   NotifyDirectDiskAccess=y
```

Note that the default behavior of Sandboxie is to deny all direct access requests, unless explicit direct access is given to the hard disk device through the [OpenFilePath](OpenFilePath) or [OpenPipePath](OpenPipePath) settings. Normally, a message is not issued when such access is denied. Use the _NotifyDirectDiskAccess_ setting to have Sandboxie issue message [SBIE1313](SBIE1313) when access is denied. Note that message [SBIE1313](SBIE1313) does not necessarily indicate malicious behavior.

This setting can not be altered using [Sandboxie Control](SandboxieControl) and must be edited in [Sandboxie Ini](SandboxieIni).
