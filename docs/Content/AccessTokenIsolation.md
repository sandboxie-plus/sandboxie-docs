# Access Token Isolation

Sandboxie uses a heavily restricted primary access token as one layer of sandbox isolation. This token limits what a sandboxed process can do through direct Windows access checks. File, registry, IPC, and other sandbox rules are separate layers of the broader isolation model.

Sandboxie Plus 1.14.1 introduced the `UseCreateToken` and `SandboxieAllGroup` settings. Their behavior and defaults have evolved since their introduction.

## Current behavior

Although `UseCreateToken` itself defaults to `n`, `SandboxieAllGroup` defaults to `y` and also selects the new-token construction path. As a result, creating a new sandboxed token is the normal current behavior even when `UseCreateToken` is not explicitly present.

## UseCreateToken

```ini
UseCreateToken=y
```

This setting explicitly selects Sandboxie's token-construction path, which builds a new primary token instead of using the historical `SepFilterToken` filtering path. `SepFilterToken` is an internal Windows kernel routine that Sandboxie historically locates through implementation-specific analysis; it is not a public, documented Windows API.

The effective behavior is as follows:

- `UseCreateToken=y` selects the new-token path regardless of `SandboxieAllGroup`.
- `UseCreateToken=n` alone does not select the historical path when `SandboxieAllGroup=y`.
- When both `UseCreateToken=n` and `SandboxieAllGroup=n`, Sandboxie can use the historical filtering path if it can locate the internal routine.
- If the internal routine cannot be located, Sandboxie falls back to constructing a new token.

## SandboxieAllGroup

```ini
SandboxieAllGroup=y
```

This setting enables the shared Sandboxie SID:

```text
S-1-5-100-0
```

Windows displays this SID as:

```text
Sandboxie\All Sandboxes
```

Sandboxie adds the SID as a normal enabled group in the sandboxed token. The group is shared by processes from all sandboxes, so Windows access-control or auditing policies can use it to match sandboxed processes collectively. The SID does not grant access by itself; an ACL or another policy must refer to it. It also does not identify an individual sandbox or isolate one sandbox from another.

## Effective settings

| `UseCreateToken` | `SandboxieAllGroup` | Effective behavior                                                     |
| ---------------- | ------------------- | ---------------------------------------------------------------------- |
| default / absent | default / absent    | New-token path with the shared Sandboxie group                         |
| `n`              | `y`                 | New-token path with the shared group                                   |
| `y`              | `y`                 | New-token path with the shared group                                   |
| `y`              | `n`                 | New-token path without the shared group                                |
| `n`              | `n`                 | Historical filtering path when available; otherwise new-token fallback |

Global settings can affect the effective value when a setting is absent from an individual sandbox.

## SandMan control

In SandMan, the control is available under **Sandbox Options > Security Options > Advanced Security > Sandboxie token** and is labeled **Create a new sandboxed token instead of stripping down the original token**.

| UI state          | Meaning                                                                             |
| ----------------- | ----------------------------------------------------------------------------------- |
| Checked           | Create a new sandboxed token and include the shared `Sandboxie\All Sandboxes` group |
| Partially checked | Create a new sandboxed token without the shared group                               |
| Unchecked         | Disable both options, allowing the historical filtering path when available         |

SandMan may remove a setting instead of writing a literal `y` or `n` when defaults or global inheritance already produce the selected state. A separate global option also controls whether the shared group is enabled.

## Token restrictions

In the normal new-token path, Sandboxie constructs a heavily restricted primary access token that, among other restrictions:

- reduces the privileges that the process can use;
- generally converts ordinary groups to deny-only so they cannot grant access;
- applies a low or untrusted integrity policy, depending on configuration;
- substitutes the sandbox identity used by Sandboxie's isolation model.

The exact token contents can also be affected by other advanced settings.

### Shared group and per-sandbox identity

`Sandboxie\All Sandboxes` is common to every sandbox and is useful when a policy needs to match all sandboxed processes. The per-sandbox identity used with SandboxieLogon identifies a specific sandbox and serves a different purpose.

## Security implications

The restricted primary token helps ensure that direct Windows access attempts do not simply execute with the original unrestricted identity. Sandboxie's driver-mediated paths can then enforce file, registry, IPC, and other resource-access rules separately.

The new-token and historical filtering paths differ primarily in their implementation and token contents. Both participate in Sandboxie's broader isolation design; neither should be treated as the entire security model, and the new-token path is not categorically more secure in every configuration.

## Administrator and elevation behavior

Running an application elevated does not mean that the primary token used by the sandboxed process retains the full administrator group and privilege set. Sandboxie still applies its token restrictions. [Drop Admin Rights](DropAdminRights.md) is a separate setting that further affects administrator and elevation behavior.

## NoSecurityIsolation interaction

These token-isolation settings are not used for normal token replacement when the following setting is active:

```ini
NoSecurityIsolation=y
```

See [No Security Isolation](NoSecurityIsolation.md) for the broader effects of that mode.

## Compatibility and failure behavior

The new-token path avoids relying on `SepFilterToken` as the normal implementation path and became the normal behavior in later Sandboxie Plus releases. The historical path remains available when both settings effectively disable the new path and the internal routine is available.

If the historical filtering routine cannot be located, Sandboxie falls back to constructing a new token. A runtime failure while actually constructing or applying a sandboxed token can prevent the process from initializing.

## Version history

- Sandboxie Plus 1.14.1 introduced `UseCreateToken` and `SandboxieAllGroup`.
- Subsequent releases included compatibility and security fixes for the implementation.
- From Sandboxie Plus 1.17.0, `SandboxieAllGroup` became enabled by default, making the new-token path the normal behavior.

## Related settings

- [Sandboxie Ini](SandboxieIni.md)
- [Drop Admin Rights](DropAdminRights.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Isolation Mechanism](IsolationMechanism.md)
- [SandboxieDrv Token Internals](TokenMagic.md)
