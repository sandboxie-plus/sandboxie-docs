# Normal IPC Path

_NormalIpcPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It restores Sandboxie's normal/default IPC handling for matching named IPC objects. It does not grant direct host access.

With [Rule Specificity](../PlusContent/RuleSpecificity.md) enabled, a more-specific Normal rule can override a broader Open or Closed IPC path rule when the matcher selects it.

```ini
[DefaultBox]
NormalIpcPath=\RPC Control\AudioSrv
```

IPC path rules do not receive the implicit trailing `*` that Sandboxie normally adds to File and Registry rules without a wildcard. The example therefore matches according to the configured IPC pattern itself. If broader matching is intended, add the wildcard explicitly.

Related Sandboxie Plus setting: **Sandbox Options > Resource Access > IPC > Add IPC Path > Access column > Normal**
