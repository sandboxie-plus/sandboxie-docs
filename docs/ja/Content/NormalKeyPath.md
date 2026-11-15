# Normal Key Path

_Normal Key Path_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie が既定のサンドボックス化スキームを適用するパス パターンを指定します。この設定は [Rule Specificity](../PlusContent/RuleSpecificity.md) と組み合わせて使用するのが最も有用で、親が Open、WriteOnly、または Closed として構成されているパスの既定のサンドボックス化動作を復元できます。

[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:

```
   .
   .
   .
   [DefaultBox]
   NormalKeyPath=HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize\*
```

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Normal
