# Normal Ipc Path

_Normal Ipc Path_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for which Sandboxie will apply the default sandboxing scheme. This setting is most useful in combination with [Rule Specificity](../PlusContent/RuleSpecificity.md) where it allows to restore default sandboxing behaviour for paths whose parents have been configured as Open, WriteOnly, or even Closed.

Example:

```
   .
   .
   .
   [DefaultBox]
   NormalIpcPath=\RPC Control\AudioSrv
```

Related Sandboxie Plus setting: Sandbox Options > Resource Access > IPC > Add IPC Path > Access column > Normal
