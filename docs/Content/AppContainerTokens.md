# AppContainer Token Compatibility

Sandboxie handles AppContainer-related requests at several distinct stages: profile and token API calls, process-creation attributes, a caller-supplied child token, and the later sandbox primary-token path. Changing a token argument before Windows creates a child is different from disabling Sandboxie's subsequent primary-token replacement. These advanced settings address particular compatibility paths; they do not form one AppContainer on/off switch.

In a standard sandbox, Sandboxie substitutes selected AppContainer creation behavior for compatibility rather than preserving the native Windows AppContainer model unchanged. A real Windows AppContainer token, Sandboxie's substitute compatibility token, and an AppContainer-like SID returned by a profile API are different things.

## Standard sandbox and Application Compartment

The following behavior applies to Sandboxie Plus 1.18.8 / Classic 5.73.8 and later.

| Behavior | Standard sandbox | Application Compartment |
| --- | --- | --- |
| Normal Sandboxie restricted primary-token replacement | Normally active | Bypassed |
| `CreateAppContainerToken` compatibility hook | Installed on Windows 8.1 and later | Not installed |
| Direct `NtCreateLowBoxToken` compatibility hook | Installed on Windows 8.1 and later | Not installed |
| AppContainer-related process-creation attributes | Suppressed by default; `FakeAppContainerToken=n` passes them through | Always passed through this branch |
| `CreateAppContainerProfile` compatibility SID hook | Installed on Windows 8 and later | Not installed |
| `DropAppContainerToken` runtime default | `y` | `n` |
| `UnRestrictAppContainerToken` substitute path | Applicable through the installed hook | Not used through that hook |

Application Compartment permits native Windows AppContainer handling to participate more directly, while also bypassing Sandboxie's normal restricted primary-token replacement. Other sandbox policies remain separate. See [Application Compartment](../PlusContent/compartment-mode.md), [No Security Isolation](NoSecurityIsolation.md), and [Access Token Isolation](AccessTokenIsolation.md).

## AppContainer API compatibility

For a standard sandbox on Windows 8.1 and later, Sandboxie hooks `CreateAppContainerToken`. Normally it opens the current process token and returns a restricted compatibility substitute, using `DISABLE_MAX_PRIVILEGE` and disabling selected groups through `CreateRestrictedToken`. Since 1.18.8, the default keeps four broad groups out of that disabling list; see [KeepBroadGroupsInAppContainerToken](#keepbroadgroupsinappcontainertoken). The result is not a real AppContainer token containing the requested AppContainer SID and capabilities.

The standard-box process-creation compatibility hook can suppress `PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES` and `PROC_THREAD_ATTRIBUTE_ALL_APPLICATION_PACKAGES_POLICY` by reporting success without forwarding them. Since 1.18.8, [FakeAppContainerToken](#fakeappcontainertoken) controls this behavior. Direct `NtCreateLowBoxToken` calls have a separate [NeutralizeLowBoxToken](#neutralizelowboxtoken) control.

Sandboxie's standard-box `CreateAppContainerProfile` hook returns a locally allocated SID shaped like `S-1-15-2-...`. It does not call the original Windows profile-creation function or create a normal AppContainer profile. The current fixed compatibility SID is not built from the requested profile name or capabilities.

Sandboxie can separately detect a process token that really is an AppContainer token through `TokenAppContainerSid`. That detection does not mean that the standard-box substitute token or the profile hook's synthetic SID has native AppContainer isolation semantics.

<div id="fakeappcontainertoken-historical-setting"></div>

### FakeAppContainerToken {#fakeappcontainertoken}

```ini
FakeAppContainerToken=program.exe,n
```

Since 1.18.8, this image-aware setting is evaluated again in the standard-box process-attribute path. Its runtime default is `y`, which suppresses the two attributes listed above. With `n`, Sandboxie forwards them to Windows, allowing native AppContainer process attributes to participate in child creation. Application Compartment always forwards them through this branch and does not consult the setting.

This controls process-creation attributes, not the separate profile-SID hook, `CreateAppContainerToken` substitute, or direct LowBox-token hook. Setting it to `n` does not disable all AppContainer compatibility handling or guarantee that every child runs with a native AppContainer token.

In 1.18.6 and 1.18.7, the configuration test in this path was commented out, so changing the value did not affect attribute suppression. The setting's historical introduction version in metadata is 1.8.2; that is distinct from its renewed effect in 1.18.8.

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

This image-aware setting controls the standard-box `CreateAppContainerToken` substitute path. Since 1.18.8, its runtime default is `n` for all images, including `msedge.exe`, so Sandboxie creates the restricted compatibility substitute. With `y`, Sandboxie instead calls `NtDuplicateToken` and returns a primary-token duplicate of the `TokenHandle` supplied to that hook. The supplied token may already be restricted; `y` does not guarantee a full or unrestricted user token. It preserves more of that supplied token than Sandboxie's restricted substitute path.

In 1.18.6 and 1.18.7, `msedge.exe` had a runtime default of `y` for compatibility. The 1.18.8 broad-group change made the restricted substitute usable for Edge again, and this default exception was removed. An explicit `UnRestrictAppContainerToken=msedge.exe,y` still selects the duplicate path. Application Compartment does not install the substitute hook, so this setting is not a normal control for that mode.

### KeepBroadGroupsInAppContainerToken {#keepbroadgroupsinappcontainertoken}

```ini
KeepBroadGroupsInAppContainerToken=program.exe,n
```

Introduced in 1.18.8, this image-aware setting defaults to `y`. It applies when the standard-box `CreateAppContainerToken` hook constructs its restricted substitute (`UnRestrictAppContainerToken=n`). Sandboxie leaves Everyone, Users, Authenticated Users, and INTERACTIVE out of the list of groups to disable. Their existing state in the source token is retained; the setting does not re-enable groups that were already disabled there. Other groups are passed to the restriction operation, and `DISABLE_MAX_PRIVILEGE` still applies.

Setting it to `n` restores the earlier behavior of passing every queried group to `CreateRestrictedToken` for disabling. That behavior could prevent a child from opening resources such as `\KnownDlls`. This is a compatibility/debugging choice, not a general recommendation to change the default. It does not control the duplicate path selected by `UnRestrictAppContainerToken=y` or the separate direct LowBox-token hook.

### NeutralizeLowBoxToken {#neutralizelowboxtoken}

```ini
NeutralizeLowBoxToken=program.exe,n
```

Since 1.18.8, Sandboxie also hooks direct `NtCreateLowBoxToken` calls in standard sandboxes on Windows 8.1 and later. This image-aware setting defaults to `y`: the hook returns a primary-token duplicate of `ExistingTokenHandle` instead of creating the requested native LowBox token with its package SID and capabilities. The supplied token may already be restricted.

With `n`, the hook forwards the original call and its arguments to Windows. Windows access checks and failures still apply. Application Compartment does not install this hook. This setting is separate from `UnRestrictAppContainerToken`, `KeepBroadGroupsInAppContainerToken`, and process-attribute suppression; changing one does not configure the others.

### Other child-token compatibility paths

`DropChildProcessToken` defaults to `n` and can clear any caller-supplied child token for a selected calling image. The same clearing behavior is hardcoded for images classified as Acrobat Reader or plugin containers. A separate Firefox branch can clear a token for child command lines containing `-sandboxingKind`. These are distinct paths; the old Flash-specific condition is commented out. See [Drop Child Process Token](DropChildProcessToken.md) for the setting's scope.

`DeprecatedTokenHacks` is still queried for a legacy Chromium/Edge compatibility branch, but only outside Application Compartment mode and when `OriginalToken` is disabled. When enabled, this branch can clear the caller-supplied token for a child process if the calling process is classified as Chrome and the child command line contains `--service-sandbox-type`. It does not control `FakeAppContainerToken` or act as a blanket switch for every historical token workaround.

## Existing boxes and AppContainer permissions {#existing-boxes-and-appcontainer-permissions}

Version 1.18.8 adds AppContainer access-control entries (ACEs) to security descriptors used for sandbox roots and boxed objects. These help native AppContainer children access the boxed resources they need. An existing box can retain an older filesystem discretionary access-control list (DACL), so updating the descriptor used for new objects does not itself repair every existing box.

For affected existing boxes, 1.18.8 adds the following command. Run it from the Sandboxie installation directory with permission to change the box folders' DACLs; an administrator can perform this repair:

```cmd
KmdUtil.exe fixboxdacls
```

The tool enumerates boxes enabled for the invoking account and session, resolves existing file-root directories, and adds inheritable full-access entries for `ALL APPLICATION PACKAGES` (`S-1-15-2-1`) and `ALL RESTRICTED APPLICATION PACKAGES` (`S-1-15-2-2`) when its checks find those grants missing. Disabled boxes and boxes unavailable to that account are not processed. The command is not limited to a selected box. The existing `fixdacls` command also invokes this box-folder repair in 1.18.8.

This changes stored filesystem permissions; it is not a read-only diagnostic. The driver must be available for box enumeration and path queries. Unresolved or nonexistent roots are skipped, and custom permissions or inheritance can affect the result. Do not assume that running the command guarantees AppContainer access to every existing child object, or that an unavailable image-backed root was repaired. Review custom ACL requirements before using it. This repair is separate from the token settings above.

## Security and configuration

These settings change particular Windows token choices, which can materially change access checks. They do not by themselves disable file or registry virtualization, network restrictions, IPC policy, or sandbox membership, and they do not grant administrator privileges. [Original Token](OriginalToken.md) and [Advanced Token Settings](AdvancedTokenSettings.md) describe separate choices later in the token pipeline.

No dedicated current SandMan controls were identified for the token settings on this page. Configure them through [Sandboxie.ini](SandboxieIni.md) for a specific compatibility or debugging need. An optional [Program Name Prefix](ProgramNamePrefix.md) selects the sandboxed process making the relevant API call, not its child executable.

These paths are selected during SbieDll initialization, AppContainer API hooking, or child-process creation. Changes do not rebuild tokens already assigned to running processes. Restart affected sandboxed process trees after changing the settings; a Windows reboot or routine service/driver restart is not normally required.

Current setting metadata lists `DropAppContainerToken` as added in 1.7.2, `FakeAppContainerToken` in 1.8.2, `UnRestrictAppContainerToken` in 1.8.4, and `DropChildProcessToken` in 1.15.6. The renewed `FakeAppContainerToken` check, uniform `UnRestrictAppContainerToken=n` default, `KeepBroadGroupsInAppContainerToken`, `NeutralizeLowBoxToken`, and `fixboxdacls` command are 1.18.8 changes.

## Related pages

- [Drop Child Process Token](DropChildProcessToken.md)
- [Original Token](OriginalToken.md)
- [Advanced Token Settings](AdvancedTokenSettings.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Application Compartment](../PlusContent/compartment-mode.md)
- [Sandboxie Ini](SandboxieIni.md)
