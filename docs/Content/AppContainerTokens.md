# AppContainer Token Compatibility

Sandboxie handles AppContainer-related requests at several distinct stages: profile and token API calls, process-creation attributes, a caller-supplied child token, and the later sandbox primary-token path. Changing a token argument before Windows creates a child is different from disabling Sandboxie's subsequent primary-token replacement. These advanced settings address particular compatibility paths; they do not form one AppContainer on/off switch.

In a standard sandbox, Sandboxie substitutes selected AppContainer creation behavior for compatibility rather than preserving the native Windows AppContainer model unchanged. A real Windows AppContainer token, Sandboxie's substitute compatibility token, and an AppContainer-like SID returned by a profile API are different things.

## Standard sandbox and Application Compartment

| Behavior | Standard sandbox | Application Compartment |
| --- | --- | --- |
| Normal Sandboxie restricted primary-token replacement | Normally active | Bypassed |
| `CreateAppContainerToken` compatibility hook | Installed on Windows 8.1 and later | Not installed |
| AppContainer-related process-creation attributes | Suppressed by the compatibility hook | Not suppressed through that branch |
| `CreateAppContainerProfile` compatibility SID hook | Installed on Windows 8 and later | Not installed |
| `DropAppContainerToken` runtime default | `y` | `n` |
| `UnRestrictAppContainerToken` substitute path | Applicable through the installed hook | Not used through that hook |

Application Compartment permits native Windows AppContainer handling to participate more directly, while also bypassing Sandboxie's normal restricted primary-token replacement. Other sandbox policies remain separate. See [Application Compartment](../PlusContent/compartment-mode.md), [No Security Isolation](NoSecurityIsolation.md), and [Access Token Isolation](AccessTokenIsolation.md).

## AppContainer API compatibility

For a standard sandbox on Windows 8.1 and later, Sandboxie hooks `CreateAppContainerToken`. Normally it opens the current process token and returns a restricted compatibility substitute, using `DISABLE_MAX_PRIVILEGE` and disabling groups supplied to `CreateRestrictedToken`. The result is not a real AppContainer token containing the requested AppContainer SID and capabilities.

The standard-box process-creation compatibility hook also suppresses `PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES` and `PROC_THREAD_ATTRIBUTE_ALL_APPLICATION_PACKAGES_POLICY`: it reports success without forwarding those attributes. This behavior is selected by sandbox mode, not by the current `FakeAppContainerToken` value.

Sandboxie's standard-box `CreateAppContainerProfile` hook returns a locally allocated SID shaped like `S-1-15-2-...`. It does not call the original Windows profile-creation function or create a normal AppContainer profile. The current fixed compatibility SID is not built from the requested profile name or capabilities.

Sandboxie can separately detect a process token that really is an AppContainer token through `TokenAppContainerSid`. That detection does not mean that the standard-box substitute token or the profile hook's synthetic SID has native AppContainer isolation semantics.

### FakeAppContainerToken: historical setting

`FakeAppContainerToken` remains in setting metadata, with an introduction version of 1.8.2, and appears in historical release notes. Current source no longer uses it to enable or disable the AppContainer compatibility substitutions: the former configuration test around process-attribute handling is commented out. The relevant standard-box behavior is currently selected by sandbox mode. Do not rely on `FakeAppContainerToken=n` to disable these hooks.

## Caller-supplied tokens during child creation

`DropAppContainerToken` and [Drop Child Process Token](DropChildProcessToken.md) act on the token supplied by the calling process when it creates a child. Neither removes an AppContainer SID from an existing token or directly disables Sandboxie's later primary-token replacement.

### DropAppContainerToken

```ini
DropAppContainerToken=browser.exe,n
```

When this setting is effective and the `hToken` supplied to `CreateProcessInternalW` is an AppContainer token, Sandboxie clears that token argument (`hToken = NULL`) and emits **Dropped AppContainer Token** to its trace path. The child is then created without that caller-supplied token argument; no existing token object is rewritten.

The runtime default is `y` in a standard sandbox and `n` in Application Compartment. The setting is image-aware: `browser.exe` in the example selects the sandboxed **caller** making the child-creation request, not the child executable. With `n`, this particular setting does not drop an AppContainer token supplied by `browser.exe`.

In a standard sandbox, the driver normally still applies `Token_ReplacePrimary()` to the child after creation. Dropping a caller-supplied AppContainer token and applying Sandboxie's normal restricted primary token are separate stages.

In Application Compartment, native AppContainer handling is otherwise allowed more directly and the normal restricted-primary-token replacement is bypassed. Explicitly setting `DropAppContainerToken=program.exe,y` can therefore remove a Windows token restriction that would otherwise apply to the child. This reduces token isolation; it does not automatically grant elevation.

### UnRestrictAppContainerToken

```ini
UnRestrictAppContainerToken=program.exe,y
```

This image-aware setting controls the standard-box `CreateAppContainerToken` substitute path. For most images its runtime default is `n`, so Sandboxie creates the restricted compatibility substitute. With `y`, Sandboxie instead calls `NtDuplicateToken` and returns a primary-token duplicate of the `TokenHandle` supplied to that hook. The supplied token may already be restricted; `y` does not guarantee a full or unrestricted user token. It preserves more of that supplied token than Sandboxie's restricted substitute path.

For `msedge.exe` specifically, the runtime default is `y`. This compatibility exception addresses newer Edge versions that do not work with the restricted substitute; it is not a default for other browsers. Application Compartment does not install the current substitute hook, so this setting is not a normal control for that mode.

### Other child-token compatibility paths

`DropChildProcessToken` defaults to `n` and can clear any caller-supplied child token for a selected calling image. The same clearing behavior is hardcoded for images classified as Acrobat Reader or plugin containers. A separate Firefox branch can clear a token for child command lines containing `-sandboxingKind`. These are distinct paths; the old Flash-specific condition is commented out. See [Drop Child Process Token](DropChildProcessToken.md) for the setting's scope.

`DeprecatedTokenHacks` is still queried for a legacy Chromium/Edge compatibility branch, but only outside Application Compartment mode and when `OriginalToken` is disabled. When enabled, this branch can clear the caller-supplied token for a child process if the calling process is classified as Chrome and the child command line contains `--service-sandbox-type`. It does not re-enable `FakeAppContainerToken` or act as a blanket switch for every historical token workaround.

## Security and configuration

These settings change particular Windows token choices, which can materially change access checks. They do not by themselves disable file or registry virtualization, network restrictions, IPC policy, or sandbox membership, and they do not grant administrator privileges. [Original Token](OriginalToken.md) and [Advanced Token Settings](AdvancedTokenSettings.md) describe separate choices later in the token pipeline.

No dedicated current SandMan controls were identified for `DropAppContainerToken`, `FakeAppContainerToken`, `UnRestrictAppContainerToken`, or `DropChildProcessToken`. Configure applicable active settings through [Sandboxie.ini](SandboxieIni.md) for a specific compatibility or debugging need.

These paths are selected during SbieDll initialization, AppContainer API hooking, or child-process creation. Changes do not rebuild tokens already assigned to running processes. Restart affected sandboxed process trees after changing the settings; a Windows reboot or routine service/driver restart is not normally required.

Current setting metadata lists `DropAppContainerToken` as added in 1.7.2, `FakeAppContainerToken` in 1.8.2, `UnRestrictAppContainerToken` in 1.8.4, and `DropChildProcessToken` in 1.15.6. `FakeAppContainerToken` is residual in current code despite its historical introduction; no exact removal version is established.

## Related pages

- [Drop Child Process Token](DropChildProcessToken.md)
- [Original Token](OriginalToken.md)
- [Advanced Token Settings](AdvancedTokenSettings.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Application Compartment](../PlusContent/compartment-mode.md)
- [Sandboxie Ini](SandboxieIni.md)
