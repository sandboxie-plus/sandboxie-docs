# ARM64 and CHPE Compatibility

Sandboxie supports several process architectures on Windows on ARM64, but they do not all use the same injection path. Its CHPE workaround is primarily about making x86 processes, including programs selected by force rules, compatible with Sandboxie's x86 hooks. It is not a security-hardening setting.

## Supported architectures

| Process on Windows on ARM64 | Current Sandboxie behavior |
| --- | --- |
| Native ARM64 | Supported by the ARM64 driver, low-level injection, syscall hooks, and SbieDll build. |
| x64 process on ARM64 | Detected as an AMD64 target and handled by Sandboxie through its ARM64EC-specific low-level injection path and ARM64EC SbieDll build. This is distinct from native ARM64 and does not guarantee every application is compatible. |
| Emulated x86 without CHPE binaries | Supported through the x86/WoW64 path and x86 SbieDll. |
| ARM32 | Not implemented; an attempted sandbox injection reports `SBIE2338` and the process cannot start in the sandbox. ARM32 is not x86. |

Sandboxie detects the target process architecture during injection. For an x64 target on ARM64, Sandboxie uses its internal ARM64EC-specific injection data and ARM64EC SbieDll build. This describes Sandboxie's implementation path; it should not be read as saying that x64 emulation and ARM64EC are interchangeable architecture terms. Users do not select a separate ARM64EC mode in Sandbox Options. This path is also distinct from the x86 CHPE workaround below.

## Why x86 CHPE matters

CHPE uses hybrid system binaries for some x86 processes on Windows on ARM64. Sandboxie's current x86 injection path expects the ordinary x86 `ntdll.dll` from `SysWOW64`, not a CHPE-only `ntdll.dll` from `SyChpe32`. When the ordinary x86 module is absent, injection fails with the CHPE form of `SBIE2338`.

For this reason, Sandboxie normally arranges for new x86 processes to use non-CHPE system binaries. This matters especially to [forced programs](ForceProcess.md) and [forced folders](ForceFolder.md): a host process selected for forcing may already have begun with CHPE binaries before Sandboxie attempts injection.

## DisableCHPE and its global scope

On an ARM64 build, SbieSvc reads the Boolean `DisableCHPE` from global configuration during startup. Its default is `y`. When enabled and the service's driver-assist startup succeeds, SbieSvc sets `LoadCHPEBinaries=0` under this **host** registry key:

```text
HKLM\SOFTWARE\Microsoft\Wow64\x86\xtajit
```

That key is global to x86 process creation on the host. The default workaround can therefore affect new x86 processes **outside** sandboxes while SbieSvc runs; it is not a per-box setting or a change to one application's image options. It does not retroactively change processes that are already running.

To opt out of the service's host-wide registry change, use:

```ini
[GlobalSettings]
DisableCHPE=n
```

This is an advanced compatibility trade-off, not a recommended general configuration. A value in an individual sandbox section does not control the service's global lookup. The setting is not an independent ARM64EC toggle.

### Backup, restoration, and failures

When enabling the workaround, SbieSvc opens or creates the host key. If `LoadCHPEBinaries_old` is absent and an existing `LoadCHPEBinaries` value can be read, it saves that value as `LoadCHPEBinaries_old`; it does not overwrite an existing backup. It then attempts to write `LoadCHPEBinaries=0`. If the original value was absent, there is no old value to save.

On a normal service stop or shutdown with the workaround enabled, SbieSvc attempts to restore the saved value and deletes the backup. If no backup exists, it deletes `LoadCHPEBinaries` instead. These operations are attempted, not guaranteed: failure to open the key prevents the change or restoration, and the code does not check every read, write, or delete result. Partial registry failures or an abnormal shutdown can leave the host CHPE configuration different from its original state, including leaving `LoadCHPEBinaries=0`. A later start with the workaround still enabled preserves an existing backup and can restore it on a later normal stop; starting with `DisableCHPE=n` does not run that restoration path. Do not assume automatic recovery after a crash.

## What happens with `DisableCHPE=n`

`DisableCHPE=n` stops SbieSvc from applying its startup-wide `xtajit` write. Ordinary new x86 host processes can then use CHPE when Windows and their other configuration permit it. If such a process matches `ForceProcess` or `ForceFolder` and starts with CHPE binaries, Sandboxie's injection cannot find the expected ordinary x86 `ntdll.dll`: it reports `SBIE2338 (CHPE)` and the driver marks the process for termination instead of successfully forcing it into the box. The same injection failure is possible for any x86 target that reaches Sandboxie's injection step with the CHPE `ntdll.dll` already loaded; the error is not exclusive to force rules.

This opt-out does **not** disable Sandboxie's per-process CHPE handling. Separate from the host-wide registry write, SbieSvc installs SbieDll's image-option hook in the service process, SbieDll installs the corresponding hook during process initialization, and the ARM64 low-level x86 path installs its own equivalent handling. These paths report `LoadCHPEBinaries=0` for the relevant process-creation queries and are not gated by the `DisableCHPE` configuration value. Consequently, a sandboxed process or child may still be created without CHPE; `DisableCHPE=n` does not promise that every x86 process will use it.

## Architecture failures and `SBIE2338`

The current ARM64 injection path emits `SBIE2338` for two distinct conditions: an unsupported ARM32 target (`ARM32`) and an x86 target whose ordinary `SysWOW64` `ntdll.dll` cannot be found (`CHPE`). In either case the failed injection is reported to the driver, which marks the process for termination. The ARM64EC path is implemented separately; its other initialization failures are not these two `SBIE2338` cases.

## Applying changes

The global `DisableCHPE` value is read during SbieSvc driver-assist startup. Reloading Sandboxie.ini while SbieSvc remains running does not reapply or undo the host registry change. Restart SbieSvc after changing the global value, and start new affected x86 processes to observe the changed process-creation behavior. The code does not require a Windows reboot or a separate driver restart solely for this setting. Changing the value cannot rebuild an already running process's architecture or injected hooks.

SandMan has no dedicated `DisableCHPE` control in its current options interface. Configure it manually in the global section of [Sandboxie Ini](SandboxieIni.md).

## Version history

Sandboxie Plus 1.5.0 / Classic 5.60.0 introduced Windows on ARM64 support, including ARM64/ARM64EC injection and hooks, the CHPE workaround, and the ARM32 limitation. Later releases fixed specific ARM64 compatibility problems, including an ARM64 FFS-hook issue and x64-process startup on ARM64. The 1.18.5 source change hardens ARM64 hook-target scanning for Chromium/Firefox-style interceptors; it does not change `DisableCHPE` configuration or the CHPE lifecycle described here.

## Related pages

- [Advanced Loader and SxS Compatibility](AdvancedLoaderCompatibility.md) covers the separate ARM64 template use of `DisableBoxedWinSxS`.
- [Host Injection](HostInjection.md) covers the separate `HostInjectDllARM64` list.
- [Feature Comparison](FeatureComparison.md) summarizes product availability rather than per-architecture injection details.
