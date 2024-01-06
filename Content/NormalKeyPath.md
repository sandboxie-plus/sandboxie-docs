# Normal Key Path

The _Normal Key Path_ setting in [Sandboxie Ini](SandboxieIni.md) defines path patterns for which Sandboxie will apply the default sandboxing scheme. This setting is particularly useful when combined with [Rule Specificity](../PlusContent/RuleSpecificity.md), allowing the restoration of default sandboxing behavior for paths whose parents have been configured as Open, WriteOnly, or even Closed.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

### Example:

```ini
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

In this example, the _NormalIpcPath_ setting defines specific inter-process communication (IPC) paths that adhere to the default sandboxing scheme. This helps maintain the default behavior for these paths even if their parent paths have custom sandboxing configurations.
