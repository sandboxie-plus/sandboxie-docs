# Block IE Embedding

_BlockIEEmbedding_ is a global setting in [Sandboxie Ini](SandboxieIni.md). It enables a narrow compatibility workaround for certain host-side requests to access the Internet Explorer CLSID Registry path; it is not a general browser or COM blocking control.

```ini
[GlobalSettings]
BlockIEEmbedding=y
```

Without an effective global value, the workaround is off. A value only in an individual sandbox section does not control it; applicable globally merged templates can also supply the effective value.

## Scope

When enabled, Sandboxie's driver denies Registry key open/create requests if the key name supplied to the callback contains `CLSID\{0002DF01-0000-0000-C000-000000000046}` and the caller is not tracked as a sandboxed process by this driver path. The comparison is case-insensitive and matches a substring, so a supplied subkey path can match too. It does not guarantee coverage of every equivalent way to access the Registry key. On Windows 10 Creators Update and later, requests originating from kernel mode are not subject to this check.

The denial applies only when the caller's executable basename exactly matches one of these names, ignoring case:

- `winword.exe`
- `powerpnt.exe`
- `excel.exe`
- `explorer.exe`
- `svchost.exe`

The matching open/create request is denied with `STATUS_ACCESS_DENIED` before ordinary sandbox Registry filtering. A Registry access rule such as `OpenKeyPath` cannot override that particular denial. Callers with a tracked Sandboxie process record are not denied by `BlockIEEmbedding`; subsequent Registry handling follows the normal path applicable to that caller. This setting does not directly intercept value queries, value writes, key enumeration, or deletion.

If the setting is off, the key name or executable does not match, or the process name cannot be obtained, this special denial does not occur. The request may still fail under other Sandboxie rules or Windows permissions.

## Compatibility context

The option originated in the Sandboxie 5.19.1 beta / 5.20 era as a workaround for an Office hyperlink scenario involving embedded Internet Explorer and a separately forced browser. That historical outcome is not guaranteed on current Windows or Office versions. _BlockIEEmbedding_ neither starts Internet Explorer nor enables [program forcing](ForceProcess.md) by itself.

## Configuration availability

This is a manual INI setting; neither SandMan nor Sandboxie Control Classic has a dedicated control for it. The driver checks the effective global value on each relevant Registry request. After a successful Sandboxie configuration reload, later requests can use the changed value without restarting the application; Registry handles already obtained are not revoked.
