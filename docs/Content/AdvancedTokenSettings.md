# Advanced Token Settings

The settings on this page alter how Sandboxie filters or reconstructs Windows access tokens. Most are advanced compatibility or debugging options that preserve properties Sandboxie would normally remove or restrict. They should generally be used only when required for compatibility or specialized testing.

These settings affect token-based isolation only. File-system and registry virtualization, IPC controls, network restrictions, GUI isolation, and other independent Sandboxie mechanisms remain separate.

## Token processing stages

The relevant part of token processing can be simplified as follows:

```text
original primary token
    |
    v
preliminary filtering
    |
    |-- UnfilteredToken can skip this stage
    |
    v
restriction / reconstruction
    |
    |-- UnrestrictedToken can skip this stage
    |
    |-- the normal modern path reconstructs the token
    |
    v
sandbox primary token
```

The preliminary filter and the later restriction or reconstruction stage are separate. Consequently, *UnfilteredToken* does not mean that the token is unrestricted, and *UnrestrictedToken* does not restore properties removed by preliminary filtering. Enabling both preserves substantially more characteristics of the source token than enabling either one alone.

Sandboxie has a modern token-construction path and a legacy filtering path. Current normal configurations commonly use the modern `Token_CreateToken` path because *SandboxieAllGroup* has a runtime default of enabled; *UseCreateToken* can also select that path. This distinction is particularly important for *UnstrippedToken*, whose behavior differs between the two paths.

This is a conceptual outline of token processing, not the complete Sandboxie isolation model.

## Common syntax and scope

All settings on this page are box-wide Boolean settings:

```ini
SettingName=y
SettingName=n
```

Current runtime lookups are not executable-qualified, so syntax such as `SettingName=program.exe,y` is not supported for these settings. Normal Sandboxie configuration and template inheritance can still affect the effective configuration of a box.

## NoUntrustedToken

```ini
NoUntrustedToken=y
```

```ini
NoUntrustedToken=n
```

*NoUntrustedToken* defaults to `n` in both the setting metadata and the current runtime. The normal restricted sandbox token uses the Windows **Untrusted** integrity level. When *NoUntrustedToken* is enabled, Sandboxie uses **Low** integrity instead.

This setting does not disable token replacement or restriction, preserve the source integrity level, or disable security isolation. It changes the sandbox token's lowered integrity level from Untrusted to Low while leaving the remaining token-isolation steps active.

If *KeepTokenIntegrity* is enabled, the normal integrity reduction is skipped, making the Untrusted-versus-Low choice irrelevant. The setting is also redundant when [`NoSecurityIsolation=y`](NoSecurityIsolation.md) bypasses normal primary-token replacement.

SandMan exposes this setting at:

**Sandbox Options > Security Options > Advanced Security**

The checkbox is labeled **Use LOW integrity token instead of UNTRUSTED (reduces isolation)**.

## UnfilteredToken

```ini
UnfilteredToken=y
```

```ini
UnfilteredToken=n
```

*UnfilteredToken* defaults to `n`. It skips Sandboxie's preliminary token-filtering stage. That stage normally removes a fixed set of sensitive privileges and also applies [`DropAdminRights`](DropAdminRights.md) filtering when configured.

Later restriction or reconstruction still occurs. The resulting token can therefore still receive a substituted token user or lower integrity level, have groups converted to deny-only, lose privileges during reconstruction, and receive Sandboxie-specific token groups.

In short, *UnfilteredToken* skips the preliminary filtering stage; later token-restriction or reconstruction steps may still modify the token. Current code also consults this behavior during relevant impersonation-token validation and WTS token handling.

Because *DropAdminRights* participates in the preliminary filter, *UnfilteredToken* can bypass that preliminary removal of administrator-related groups and selected privileges. It does not remove the later Sandboxie restrictions.

## UnrestrictedToken

```ini
UnrestrictedToken=y
```

```ini
UnrestrictedToken=n
```

*UnrestrictedToken* defaults to `n`. It skips the heavy token-restriction or reconstruction stage, causing Sandboxie to duplicate the token received from the earlier stage.

That token may already have been modified by preliminary filtering. Enabling *UnrestrictedToken* alone does not restore groups, privileges, or other properties removed earlier.

*UnrestrictedToken* skips the normal heavy token-restriction stage, but other Sandboxie isolation mechanisms remain active and earlier token filtering may already have modified the token. It does not disable file-system or registry virtualization and isolation, IPC controls, network restrictions, or other independent sandbox mechanisms.

## UnfilteredToken versus UnrestrictedToken

| Configuration | Preliminary filter | Restriction/reconstruction |
|---|---|---|
| Normal | Applied | Applied |
| `UnfilteredToken=y` | Skipped | Still applied |
| `UnrestrictedToken=y` | Still applied | Skipped |
| Both enabled | Skipped | Skipped |

Using both options preserves substantially more characteristics of the source token than either option alone. It does not completely disable Sandboxie because the other isolation layers remain independent.

## ReplicateToken

```ini
ReplicateToken=y
```

```ini
ReplicateToken=n
```

*ReplicateToken* defaults to `n` and applies specifically to the modern `Token_CreateToken` reconstruction path. It creates a new token while preserving substantially more properties from the source token; it does not simply duplicate the original token object.

The reconstructed token preserves or reuses the source token user, groups, privileges, token type, impersonation level, authentication ID, expiration, owner, primary group, default DACL, token source, device groups, and token security attributes. It also avoids several normal transformations, including Sandboxie or Anonymous token-user substitution, conversion of groups to deny-only, normal privilege reduction, and normal addition of the *SandboxieAll* group.

The source token passed to this stage may already have undergone preliminary filtering unless *UnfilteredToken* is also enabled. *ReplicateToken* therefore does not necessarily restore groups or privileges removed earlier.

The implementation does not explicitly copy every token information class. Research did not establish explicit copying of `TokenRestrictedSids`, `TokenOrigin`, `TokenSessionId`, or AppContainer capabilities. *ReplicateToken* reconstructs the sandbox token while preserving substantially more properties of its source token; it should not be treated as an exact clone of every token field.

## CopyTokenAttributes

```ini
CopyTokenAttributes=y
```

```ini
CopyTokenAttributes=n
```

*CopyTokenAttributes* applies to the modern `Token_CreateToken` path and refers specifically to `TokenSecurityAttributes`. Sandboxie reads these security attributes from the source token and adds them to the newly created token. The setting does not copy every token information class and does not mean that AppContainer capabilities are copied.

There is an important difference between the metadata and current runtime defaults:

- the setting metadata lists a default of `n`;
- the current `Token_CreateToken` implementation uses `true` as the runtime default when the setting is absent.

As a result, token security attributes are copied by default on that path in the current implementation. Setting `CopyTokenAttributes=n` explicitly disables this optional copy. Enabling *ReplicateToken* forces the copy behavior regardless of the explicit *CopyTokenAttributes* value.

Attribute copying occurs after the new token is created and is best effort. Failure while querying, allocating, or applying `TokenSecurityAttributes` does not invalidate an otherwise successfully created token.

## KeepTokenIntegrity

```ini
KeepTokenIntegrity=y
```

```ini
KeepTokenIntegrity=n
```

*KeepTokenIntegrity* defaults to `n`. Sandboxie normally replaces the source integrity SID with a lowered sandbox integrity level. Enabling this setting preserves the source token's integrity level instead, so a token that begins at High integrity can remain at High integrity.

Integrity level, group membership, and privileges are separate token properties. *KeepTokenIntegrity* preserves the source integrity level; token groups and privileges are filtered independently. It does not undo *DropAdminRights* and does not change the compatibility behavior of [`FakeAdminRights`](FakeAdminRights.md).

Enabling this setting makes *NoUntrustedToken* irrelevant. It is also redundant when normal primary-token replacement is bypassed by *NoSecurityIsolation*.

## KeepUserGroup

```ini
KeepUserGroup=y
```

```ini
KeepUserGroup=n
```

*KeepUserGroup* defaults to `n`. Here, "user group" means the token group entry whose SID matches the token's `TokenUser`. It does not specifically mean `BUILTIN\Users`, the *SandboxieAll* group, or the logon SID.

During normal group restriction, Sandboxie can disable groups or convert them to deny-only. With *KeepUserGroup* enabled, the group matching the token user SID is preserved instead of receiving that normal treatment. The `TokenUser` identity itself can still be substituted later by the normal Anonymous Logon or Sandboxie SID path.

## UnstrippedToken

```ini
UnstrippedToken=y
```

```ini
UnstrippedToken=n
```

*UnstrippedToken* defaults to `n`. It skips selected stripping operations, but the exact preserved properties depend on the token-construction path.

### Modern token-construction path

On the modern `Token_CreateToken` path, enabling *UnstrippedToken* skips the normal group-restriction transformations and integrity-level replacement. Normal token-user substitution still occurs, and privileges are still reduced to the modern path's restricted privilege set, which normally retains `SeChangeNotifyPrivilege`.

It therefore does not preserve every token component.

### Legacy filtering path

On the legacy path, integrity handling occurs before the *UnstrippedToken* early return. Later group stripping and restriction steps are skipped. Consequently, the setting does not imply *KeepTokenIntegrity* uniformly across both implementations.

*UnstrippedToken* acts later and more narrowly than *UnfilteredToken*, is less comprehensive than *UnrestrictedToken*, and is not an alias for either one. The modern behavior is the most relevant to current normal configurations, but the legacy distinction still exists under other configurations or platform conditions.

## Interaction with NoSecurityIsolation

When [`NoSecurityIsolation=y`](NoSecurityIsolation.md), Sandboxie normally bypasses primary-token replacement. The settings described on this page are therefore generally redundant or not reached for the normal primary token:

- *NoUntrustedToken*
- *ReplicateToken*
- *CopyTokenAttributes*
- *UnfilteredToken*
- *UnrestrictedToken*
- *KeepTokenIntegrity*
- *KeepUserGroup*
- *UnstrippedToken*

See [No Security Isolation](NoSecurityIsolation.md) for the wider effects of that mode.

## Interaction with administrative-rights settings

[`DropAdminRights`](DropAdminRights.md) performs real token filtering, including disabling administrator-related groups and removing selected privileges. *UnfilteredToken* can bypass its preliminary filtering stage, while *UnrestrictedToken* alone does not restore properties already removed there. *KeepTokenIntegrity* can preserve a High integrity level without restoring administrative groups or privileges.

[`FakeAdminRights`](FakeAdminRights.md) is different: its current implementation primarily uses compatibility hooks to make selected administrator checks appear successful. It does not restore real administrator groups or privileges removed by token filtering.

## SandMan configuration

Among the settings on this page, only *NoUntrustedToken* has a dedicated current SandMan control:

**Sandbox Options > Security Options > Advanced Security > Use LOW integrity token instead of UNTRUSTED (reduces isolation)**

The remaining settings are advanced manual [`Sandboxie.ini`](SandboxieIni.md) options.

## Sandboxie Plus and Classic

Token processing is implemented in shared Sandboxie components. SandMan exposes the *NoUntrustedToken* control, while the other settings on this page use manual configuration. Current source does not contain equivalent dedicated Sandboxie Control Classic controls, but compatible manual INI settings can be consumed by the shared runtime where applicable.

## Applying configuration changes

These settings are primarily consulted while Sandboxie prepares, filters, or creates a process token. Changing them does not retroactively rebuild an already assigned primary token. Restart affected sandboxed processes after changing the settings; recreating the sandboxed process tree provides consistent behavior. A SandMan, service, or driver restart is not normally required.

*UnfilteredToken* is also consulted during relevant later impersonation-token handling, but this does not remove the need to restart processes when changing primary-token policy.

## Failure behavior

Essential token-filtering, construction, or assignment failures cause process initialization to fail rather than deliberately falling back to a less-restricted host token. Exact errors depend on the failed operation.

The optional *CopyTokenAttributes* step is different: failure to copy `TokenSecurityAttributes` does not invalidate an otherwise successfully created token.

## Version history

- *UnfilteredToken* and *UnrestrictedToken* date to Sandboxie Plus 0.2.1 / Classic 5.41.1.
- *KeepTokenIntegrity* dates to Sandboxie Plus 0.3.0 / Classic 5.42.
- *KeepUserGroup* and *UnstrippedToken* date to Sandboxie Plus 1.0.6 / Classic 5.55.6.
- The setting metadata records *NoUntrustedToken*, *ReplicateToken*, and *CopyTokenAttributes* as added in Sandboxie Plus 1.14.1.
- The dedicated *NoUntrustedToken* SandMan control was documented in the Sandboxie Plus 1.17.0 / Classic 5.72.0-era changes.

## Related pages

- [Isolation Mechanism](IsolationMechanism.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Drop Admin Rights](DropAdminRights.md)
- [Fake Admin Rights](FakeAdminRights.md)
- [Sandboxie Ini](SandboxieIni.md)
