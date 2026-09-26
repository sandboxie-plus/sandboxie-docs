# Open Protected Storage

The current way to open the host's legacy Windows [Protected Storage](ProtectedStorage.md) (PStore) endpoints is to select Sandboxie's **Open Protected Storage** template for a box:

```ini
[DefaultBox]
Template=OpenProtectedStorage
```

The older `OpenProtectedStorage=y` Boolean remains in setting metadata and may appear in old configurations, but it is **not** the current configuration method. Sandboxie Plus 1.8.0 / Classic 5.63.0 replaced it with the template. Legacy configuration migration can convert the old Boolean to template selection; the old driver consumers visible in current source are commented out. Do not edit the shipped template to enable this option.

## What the template does

The shipped template opens these system paths:

```ini
OpenFilePath=|\Device\NamedPipe\protected_storage
OpenIpcPath=*\BaseNamedObjects*\PS_SERVICE_STARTED
OpenIpcPath=\RPC Control\protected_storage
```

In an ordinary sandbox, Sandboxie normally hooks `PStoreCreateInstance` and supplies its own `IPStoreImpl` compatibility implementation. When the effective IPC policy opens `\RPC Control\protected_storage`, Sandboxie's PStore initialization skips that hook. The template opens that endpoint, allowing the native PStore path instead of Sandboxie's replacement through this mechanism. The historical `FuncSkipHook=PStoreCreateInstance` line in the shipped template is commented out, not an active rule.

The same endpoint check runs before Sandboxie's [Open Credentials](OpenCredentials.md) setting is checked. With this template selected, Sandboxie also skips its user-mode WinCred hooks; supported native credential API calls can pass through. By contrast, `OpenCredentials=y` alone leaves the separate PStore hook in place. PStore and the Windows Credential APIs are related here but are not the same facility.

## SandMan and scope

SandMan exposes this template at **Sandbox Options > General Options > Restrictions > Other restrictions > Open System Protected Storage**. When selected, its separate **Open Windows Credentials Store (user mode)** checkbox appears checked and disabled. SandMan saves the template selection, not `OpenProtectedStorage=y` or an automatic `OpenCredentials=y` value.

In [Application Compartment](../PlusContent/compartment-mode.md), Sandboxie already skips its replacement PStore hook. That does not, by itself, establish whether the separate WinCred hooks are installed; their own endpoint and `OpenCredentials` checks still matter.

The hook decisions are made as relevant modules initialize in sandboxed processes. Restart affected sandboxed applications and their child processes after changing the template. A Windows reboot or routine driver/service restart is not normally necessary solely for these user-mode hooks.
