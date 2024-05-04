# Normal Key Path

_Normal Key Path_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for which Sandboxie will apply the default sandboxing scheme. This setting is most useful in combination with [Rule Specificity](../PlusContent/RuleSpecificity.md) where it allows to restore default sandboxing behaviour for paths whose parents have been configured as Open, WriteOnly, or even Closed.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:

```
   .
   .
   .
   [DefaultBox]
   NormalIpcPath=*BaseNamedObjects*\__ComCatalogCache__
   NormalIpcPath=*BaseNamedObjects*\ComPlusCOMRegTable
   NormalIpcPath=*BaseNamedObjects*\RotHintTable
   NormalIpcPath=*BaseNamedObjects*\{A3BD3259-3E4F-428a-84C8-F0463A9D3EB5}
   NormalIpcPath=*BaseNamedObjects*\{A64C7F33-DA35-459b-96CA-63B51FB0CDB9}
   NormalIpcPath=\RPC Control\actkernel
   NormalIpcPath=\RPC Control\epmapper
   NormalIpcPath=\RPC Control\OLE*
   NormalIpcPath=\RPC Control\LRPC*
```

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Normal
