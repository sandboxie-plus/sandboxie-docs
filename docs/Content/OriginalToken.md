# Original Token

*OriginalToken* is an advanced, unsafe compatibility and debugging setting. It prevents Sandboxie from replacing a sandboxed process's primary Windows access token through its normal restricted-token path. It also relaxes selected token and impersonation handling elsewhere. It does **not** run the process outside its sandbox.

> [!WARNING]
> `OriginalToken=y` substantially weakens Sandboxie's token-based isolation. Groups, privileges, and integrity characteristics that Sandboxie would normally reduce can remain available from the incoming token. An application started with an elevated token may therefore retain that elevation; the setting does not grant administrator privileges to a standard user. A more powerful token can increase access to host resources even while other sandbox mechanisms remain active. Sandboxie classifies this as an insecure debug option.

## Configuration

```ini
[DefaultBox]
OriginalToken=y
```

The runtime default is `n` (disabled). This is a box-level Boolean setting; normal configuration resolution can also supply it through an applicable template or global settings. Current consumers do not select *OriginalToken* by executable name. Do not use an executable-qualified form such as `OriginalToken=program.exe,y` to configure this behavior.

SandMan has no dedicated *OriginalToken* checkbox or entry in its usual Advanced Options list. Configure it through [Sandboxie Ini](SandboxieIni.md) when a specific compatibility or debugging need warrants it. Current shipped templates do not enable it automatically.

## Primary-token behavior

For a normal sandboxed process, Sandboxie obtains the initial primary token, applies preliminary filtering where configured, then constructs or restricts and assigns a sandbox-managed primary token. Depending on the configuration, these steps can reduce privileges, change group access, and lower integrity.

With `OriginalToken=y`, the driver returns before that normal primary-token filtering, restriction, and assignment path. The process keeps the Windows token supplied to that path rather than receiving Sandboxie's normally restricted replacement. This does not mean that every original privilege is always present: the incoming token may already be limited, and other Windows or Sandboxie paths can still affect particular token operations. See [Access Token Isolation](AccessTokenIsolation.md) for the normal token model.

### Distinction from other token settings

| Configuration | Preliminary filtering in the normal primary-token path | Later restricted-token construction and assignment |
| --- | --- | --- |
| Default | Applied | Applied |
| `UnfilteredToken=y` | Skipped | Still applied |
| `UnrestrictedToken=y` | Still involved | A less-restricted token is duplicated and assigned through Sandboxie's token path |
| `OriginalToken=y` | Normal primary-token replacement path is skipped | No restricted primary token is assigned through that path |

*UnfilteredToken* and *UnrestrictedToken* are therefore not aliases for *OriginalToken*. In the primary-token replacement path, *OriginalToken* returns before the branches for options such as *ReplicateToken*, *CopyTokenAttributes*, *UnstrippedToken*, *KeepTokenIntegrity*, and preliminary *DropAdminRights* filtering. This does not make every separate consumer of those settings irrelevant. [Advanced Token Settings](AdvancedTokenSettings.md) explains their individual stages. *FakeAdminRights* also has separate compatibility behavior during child-process creation.

## What remains sandboxed

The process remains registered with its sandbox, and Sandboxie's normal process initialization still sets up independently configured file, registry, IPC, GUI, and network handling. SbieDll injection and sandbox identity are not disabled merely by *OriginalToken*. File and registry virtualization, applicable filters, and other sandbox rules can therefore remain active.

An active filter is not a promise of the same host-access result as a normally restricted-token process. Windows access checks can observe the stronger token preserved by *OriginalToken*. Treat the setting as a substantial reduction in token-based protection, **not** as either complete removal of the sandbox or preservation of every other protection at identical strength.

## Application Compartment

[Application Compartment](NoSecurityIsolation.md) and *OriginalToken* share some runtime branches that bypass restricted primary-token replacement and use a more direct child-process creation path. Application Compartment does not automatically write or enable `OriginalToken=y`, and the two configurations are not equivalent. Application Compartment has additional path-policy, filtering, and Job Object behavior that *OriginalToken* alone does not select.

## Child processes and AppContainer tokens

For child creation, *OriginalToken* skips Sandboxie's later suspended-creation and token-replacement sequence and passes the resulting token choice to Windows. It does **not** guarantee that every child receives an exact copy of its parent's token. In particular, [Drop Child Process Token](DropChildProcessToken.md) can clear a caller-supplied token **before** the *OriginalToken* branch runs. *DropAppContainerToken* is also evaluated before that branch, and other special-case handling can affect the token passed to Windows.

*OriginalToken* does not disable all AppContainer compatibility handling. [AppContainer Token Compatibility](AppContainerTokens.md) explains those separate API, process-attribute, and caller-supplied-token stages.

## Impersonation and related effects

The setting is broader than primary-token replacement. The driver relaxes a Sandboxie-specific impersonation-token validation path, and SbieDll omits selected impersonation hooks and token-compatibility handling. Other IPC namespace and security hooks remain installed. This does not mean impersonation always succeeds or that all IPC isolation is disabled; Windows checks and other Sandboxie controls still apply.

*OriginalToken* also changes selected token choices and checks made by Sandboxie's service. It does **not**, by itself, cause sandboxed RpcSs to run as SYSTEM: the current automatic SYSTEM-source path also requires settings such as *MsiInstallerExemptions* or *RunServicesAsSystem*. See [Sandboxed Services](SandboxedServices.md) and [RPC Compatibility](RpcCompatibility.md) for those separate behaviors.

The setting can omit basic UI restrictions on Sandboxie's root Job Object without removing the process from that Job Object or automatically disabling its resource limits. See [Job Objects](JobObjects.md).

## Applying changes

Primary-token replacement and several hook-installation decisions occur as sandboxed processes start. Changing *OriginalToken* does not rebuild an existing process's token or reinstall hooks in that process. Restart affected sandboxed processes after a change; restarting the sandboxed process tree gives a consistent test. A Windows reboot or routine SandMan, service, or driver restart is not normally required.

## Version history

The current settings metadata lists `AddedVersion=0.2.1`, while the changelog describes *OriginalToken* as an experimental testing/debug option in Sandboxie Plus 0.4.5 / Classic 5.44.1. These sources do not establish one unambiguous introduction version. The changelog later calls it an insecure debug option.

## Related pages

- [Access Token Isolation](AccessTokenIsolation.md)
- [Advanced Token Settings](AdvancedTokenSettings.md)
- [Drop Child Process Token](DropChildProcessToken.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Sandboxie Ini](SandboxieIni.md)
