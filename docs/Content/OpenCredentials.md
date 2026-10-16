# Open Credentials

`OpenCredentials` is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) for Sandboxie's user-mode Windows Credential API (WinCred) compatibility layer. It is disabled (`n`) by default. It is a box/effective Boolean setting, not an executable-qualified rule.

Windows Credential APIs let applications store and retrieve user names, passwords, and related sign-in information, including credentials for network resources. This setting concerns Sandboxie's handling of its intercepted WinCred calls, not every Windows credential mechanism.

```ini
[DefaultBox]
OpenCredentials=y
```

When enabled, Sandboxie does not install its WinCred hooks for the affected sandboxed process, so calls in that hook set use the native Windows implementation. This does **not** by itself disable Sandboxie's separate legacy [Protected Storage](ProtectedStorage.md) (PStore) hook. It does not describe every Windows credential, authentication, or password-storage mechanism.

## Behavior when disabled in a standard sandbox

Unless the effective IPC policy opens `\RPC Control\protected_storage` (for example, through the [Open Protected Storage](OpenProtectedStorage.md) template), Sandboxie intercepts `CredWriteA/W`, `CredReadA/W`, `CredWriteDomainCredentialsA/W`, `CredReadDomainCredentialsA/W`, `CredDeleteA/W`, and `CredEnumerateA/W`. This is the implemented WinCred hook set, not a guarantee of coverage for every credential-related API.

The default compatibility layer primarily virtualizes modifications while retaining read-through behavior:

- Intercepted credential and domain-credential writes are serialized into Sandboxie's PStore-backed storage rather than directly updating the native credential through those hooked calls.
- `CredReadW` checks the sandboxed representation first, then can fall back to native `CredReadW` when no valid sandboxed item is found. `CredReadDomainCredentialsW` similarly falls back to the native domain-credential read when no matching sandboxed item is found.
- `CredEnumerateW` can combine sandboxed entries with results from native credential enumeration. A sandboxed process may therefore see host credential entries through this API.
- An intercepted delete writes a local deletion marker instead of calling the native credential-delete API through that path.

Application Compartment differs at the PStore layer. In that mode, Sandboxie does not install its replacement `PStoreCreateInstance` hook, while the WinCred hooks can still be installed if neither the protected-storage endpoint nor `OpenCredentials=y` bypasses them. In that case, their backing-store initialization reaches the native PStore provider rather than Sandboxie's `IPStoreImpl`, so the standard-sandbox storage description above should not be generalized to Application Compartment.

These behaviors are not a complete confidentiality boundary for host credentials. They also do not establish what happens through APIs outside Sandboxie's hook set.

## Interaction with Open Protected Storage

The `Template=OpenProtectedStorage` template adds a rule to open the protected-storage IPC endpoint. When the effective IPC policy opens that endpoint, Sandboxie skips both its PStore hook and its WinCred hooks. Thus the template has a broader effect than `OpenCredentials=y` alone. The template does not merely set the old `OpenProtectedStorage` Boolean internally.

In SandMan, the current control is **Sandbox Options > General Options > Restrictions > Other restrictions > Open Windows Credentials Store (user mode)**. Selecting **Open System Protected Storage** displays this credential control as checked and disabled. It does not automatically save `OpenCredentials=y`; deselecting the PStore control restores the stored credential-setting state.

Hook installation is decided as the relevant modules initialize in a sandboxed process. Restart affected sandboxed applications and their child processes after changing this setting or the template; a Windows reboot or routine Sandboxie driver/service restart is not normally needed solely for these hooks.

See [Protected Storage](ProtectedStorage.md), [Open Protected Storage](OpenProtectedStorage.md), and [SBIE2213](SBIE2213.md).
