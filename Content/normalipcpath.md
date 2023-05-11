# Normal Ipc Path

_Normal Ipc Path_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for which Sandboxie will apply the defualt sandboxing scheme. This setting is most usefull in combination with [Rule Specificity](rulespecificity.md) where it allows to restore defaul sandboxing behavioure for paths which parents have been configured as Open, WriteOnly, or even Closed.

Example:

```
   .
   .
   .
   [DefaultBox]
   NormalIpcPath=\RPC Control\AudioSrv
```
