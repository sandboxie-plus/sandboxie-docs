# Sandboxie Logon

Sandboxie normally substitutes the identity represented by a sandboxed process's access token as part of its [token isolation](IsolationMechanism.md). The default path uses the Windows Anonymous Logon identity. The optional *SandboxieLogon* setting uses a virtual SID associated with the sandbox instead.

This behavior is part of access-token isolation, not Windows user-account management. It does not create a local or domain account, sign a user in to Windows, create a separate interactive login, or give the sandbox its own user profile or password.

## SandboxieLogon

```ini
SandboxieLogon=y
```

```ini
SandboxieLogon=n
```

*SandboxieLogon* is a box-wide Boolean setting and defaults to `n`. It does not support executable-qualified matching at runtime. Like other box settings, it can be inherited through normal Sandboxie configuration and templates.

When the setting is enabled, the Sandboxie service creates or resolves a virtual SID mapping associated with the sandbox. Sandboxie supplies that SID to the token-construction machinery and uses it as the sandbox token's `TokenUser`. In practical terms, *SandboxieLogon* replaces the normal anonymous sandbox token identity with a virtual SID associated with the sandbox.

The virtual SID can give a sandbox a distinguishable identity for Windows access checks. It remains a token identity used for isolation, however; it is not a normal Windows account or a separate logon session, and it does not by itself create a user profile.

## AnonymousLogon

```ini
AnonymousLogon=y
```

```ini
AnonymousLogon=n
```

*AnonymousLogon* is a box-wide Boolean setting and defaults to `y`. There is no dedicated SandMan control for it, so it is an advanced manual configuration setting. It does not support executable-qualified matching at runtime.

When the anonymous identity path is active and no sandbox-specific SID is used, Sandboxie substitutes the Windows **ANONYMOUS LOGON** SID (`S-1-5-7`) as the token user. On relevant current Windows paths, Sandboxie may also use the anonymous authentication LUID as part of token construction.

The normal configuration is:

```ini
SandboxieLogon=n
AnonymousLogon=y
```

Enabling *SandboxieLogon* causes the box-specific Sandboxie SID to be used in place of the normal anonymous user identity. These are therefore alternative roles in the normal token-construction path, rather than two independent user-identity substitutions applied one after the other.

*AnonymousLogon* changes the identity represented in the sandbox token. It does not by itself guarantee anonymous network authentication. SSPI, stored or explicitly supplied credentials, SMB, browsers, Windows Credential Manager, and other application or Windows authentication mechanisms can have behavior beyond this token-user substitution.

## KeepLogonSession

```ini
KeepLogonSession=y
```

```ini
KeepLogonSession=n
```

*KeepLogonSession* is a box-wide Boolean setting, defaults to `n`, and has no dedicated SandMan control. It does not support executable-qualified matching at runtime.

Despite its name, this setting does not preserve every property of the original Windows logon session. Sandboxie normally restricts token groups during token construction. With *KeepLogonSession* enabled, Sandboxie preserves the token group marked with `SE_GROUP_LOGON_ID` instead of applying the normal disabling or deny-only treatment to that logon SID group.

The implementation has not been shown to preserve or restore the token's `AuthenticationId`, `TokenOrigin`, `TokenSessionId`, LSA credentials, DPAPI state, SSPI context, or network credentials.

## Token user and logon SID

The token user and logon SID are separate Windows token concepts:

- *SandboxieLogon* and *AnonymousLogon* select the identity represented by `TokenUser` in the normal sandbox token path.
- *KeepLogonSession* preserves a token group marked as the logon SID during Sandboxie's group-restriction step.

Preserving the logon SID group does not undo the Sandboxie or Anonymous Logon `TokenUser` substitution. Conversely, changing `TokenUser` is not the same as creating, preserving, or removing an LSA logon session.

## Security isolation and advanced modes

The default anonymous identity and the optional sandbox-specific SID are parts of Sandboxie's token identity isolation. *SandboxieLogon* changes which sandbox identity is represented in access checks, while *KeepLogonSession* preserves one group that Sandboxie would normally restrict. Other Sandboxie isolation mechanisms continue to apply separately.

When [`NoSecurityIsolation=y`](NoSecurityIsolation.md), Sandboxie normally bypasses replacement of the process's primary token. The identity transformations described on this page are therefore generally not part of that primary-token path. SandMan also disables and clears the *SandboxieLogon* control when security isolation is disabled.

The advanced *ReplicateToken* token-construction mode preserves the source token user rather than performing the normal Sandboxie or Anonymous Logon user substitution. Other advanced token-filtering settings are outside the scope of this page.

## SandMan configuration

SandMan exposes *SandboxieLogon* at:

**Sandbox Options > Security Options > Advanced Security**

The checkbox is labeled **Use a Sandboxie login instead of an anonymous token**. The New Box Wizard also exposes the Sandboxie-logon choice where applicable.

There are no dedicated SandMan controls for *AnonymousLogon* or *KeepLogonSession*; configure them manually in [`Sandboxie.ini`](SandboxieIni.md) when needed.

## Sandboxie Plus and Classic

Runtime support is implemented in shared Sandboxie components. SandMan provides the current *SandboxieLogon* interface. Current source does not contain equivalent dedicated Sandboxie Control Classic controls, but compatible manual INI settings can be consumed by the shared runtime where applicable.

## Applying changes and failure behavior

The settings on this page are used while Sandboxie prepares or constructs a process token. They do not retroactively rebuild a primary token that has already been assigned. Restart affected sandboxed processes after changing them; recreating the sandboxed process tree gives predictable results. A SandMan, service, or driver restart is not normally required.

Essential token-construction or assignment failures cause process startup to fail rather than deliberately falling back to a less-restricted host token. If the service cannot create or resolve the sandbox-specific SID, it can continue without that SID, leaving the normal anonymous identity path available. This should not be treated as a guarantee for every possible token-creation failure.

## Version history

- The original *SandboxieLogon* mechanism dates to the Sandboxie Plus 0.2.2 / Classic 5.41.2 era.
- Sandboxie Plus 1.2.0 / Classic 5.57 introduced the modern per-box SID behavior and temporarily enabled it by default.
- Sandboxie Plus 1.2.7 / Classic 5.57.7 changed the default back to disabled.
- Sandboxie Plus 1.4.0 / Classic 5.59 added the SandMan interface.
- *KeepLogonSession* was added to the setting metadata in Sandboxie Plus 1.14.1.

The current metadata does not identify a reliable introduction version for *AnonymousLogon*.

## Related pages

- [Isolation Mechanism](IsolationMechanism.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Sandboxie Ini](SandboxieIni.md)
