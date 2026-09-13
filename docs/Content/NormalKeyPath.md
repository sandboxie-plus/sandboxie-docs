# Normal Key Path

_Normal Key Path_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for which Sandboxie will apply the default sandboxing scheme. This setting is most useful in combination with [Rule Specificity](../PlusContent/RuleSpecificity.md) where it allows to restore default sandboxing behaviour for paths whose parents have been configured as Open, WriteOnly, or even Closed.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:

```
   .
   .
   .
   [DefaultBox]
   NormalKeyPath=HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize\*
```

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Normal
