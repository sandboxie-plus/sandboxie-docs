# Normal File Path

_Normal File Path_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for which Sandboxie will apply the default sandboxing scheme. This setting is most useful in combination with [Rule Specificity](../PlusContent/RuleSpecificity.md) where it allows to restore defaul sandboxing behavioure for paths which parents have been configured as Open, WriteOnly, or even Closed.

[Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:

```
   .
   .
   .
   [DefaultBox]
   NormalFilePath=C:\Downloads\
   NormalFilePath=*.eml
   NormalFilePath=iexplore.exe,%Favorites%
   NormalFilePath=msimn.exe,*.eml
```
