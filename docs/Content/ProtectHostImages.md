# Protect Host Images

_ProtectHostImages_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It protects certain sandboxed processes whose main executable image comes from the host from executable content originating inside the sandbox.

```ini
[DefaultBox]
ProtectHostImages=y
```

The setting is disabled by default and requires a currently applicable Support Certificate.

## Behavior

When the setting is enabled, the driver identifies sandboxed processes whose executable was loaded from the host rather than from the sandbox. For those processes, it blocks executable image mappings from boxed paths during normal image loading. This is intended to prevent a DLL or other executable image placed in the sandbox from being loaded into a host-installed program that is running sandboxed.

The current driver also prevents a process whose own executable comes from the sandbox from obtaining write access to a protected host-image process, even within the same box, and prevents that boxed-image process from starting a host-image child through the protected path.

This setting does not prevent every DLL or image load, every form of code injection, or every interaction with host processes. The executable-image mapping check has a limited exception for mappings required during process creation; separate `ProtectHostImages` process-creation checks still apply. Application compatibility can also require file-migration exceptions.

`ProtectHostImages` is disabled for an [Application Compartment](../PlusContent/compartment-mode.md) box (`NoSecurityIsolation=y`). It is independent of [ConfidentialBox](ConfidentialBox.md): one restricts image and related process operations inside the sandbox, while the other restricts process/thread handles opened from the host.

## Compatibility

Blocking boxed executable images can expose applications that expect their installed modules to be copied into and loaded from the sandbox. Current default templates include migration exceptions for common installation locations of Firefox-family browsers. Custom installation paths may need equivalent `DontCopy` rules if affected.

When notification is enabled, Sandboxie issues message 1305 for a blocked executable-image load. The related `NotifyImageLoadDenied` setting is enabled by default while its SandMan control is available.

## SandMan configuration

The control is under:

**Sandbox Options > Advanced Options > Dlls & Extensions > Image Protection**

Its current label is:

**Prevent sandboxed programs installed on the host from loading DLLs from the sandbox**

The adjacent **Issue message 1305 when a program tries to load a sandboxed dll** checkbox controls `NotifyImageLoadDenied`. SandMan supports a global `ProtectHostImages` default with a per-box override.

The driver records `ProtectHostImages` when a sandboxed process is initialized. Restart the affected sandboxed process tree after changing it.

## Version history

`ProtectHostImages` and `NotifyImageLoadDenied` were introduced in Sandboxie Plus 1.9.0 / Classic 5.64.0. Compatibility fixes for Firefox-family browsers followed in Sandboxie Plus 1.15.4 / Classic 5.70.4.

## Related pages

- [Confidential Box](ConfidentialBox.md)
- [Box Encryption](../PlusContent/BoxEncryption.md)
