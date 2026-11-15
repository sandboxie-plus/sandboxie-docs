# Normal File Path

_Normal File Path_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie が既定のサンドボックス化スキームを適用するパス パターンを指定します。この設定は [Rule Specificity](../PlusContent/RuleSpecificity.md) と組み合わせて使用するのが最も有用で、親が Open、WriteOnly、または Closed として構成されているパスの既定のサンドボックス化動作を復元できます。

[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:

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

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Files > Add File/Folder > Access column > Normal
