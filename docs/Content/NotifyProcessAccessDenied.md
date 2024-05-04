# Notify Process Access Denied

_NotifyProcessAccessDenied_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) since v1.0.16 / 5.55.16. It is typically specified as _NotifyProcessAccessDenied=y_, and indicates that Sandboxie should issue message [SBIE2111](SBIE2111.md) when programs are denied reading from the address space of the process.

Usage:
```
   .
   .
   .
   [DefaultBox]
   NotifyProcessAccessDenied=y
```

Related Sandboxie Plus setting: Sandbox Options > General Options > Restrictions > Other restrictions > Issue message 2111 when a process access is denied

For more information, see [SBIE2111](SBIE2111.md).
