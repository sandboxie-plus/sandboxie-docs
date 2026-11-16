# Open Key Path

_OpenKeyPath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie がレジストリ キーに対してサンドボックス化を適用しないパス パターンを指定します。これにより、サンドボックス化されたプログラムが_サンドボックスの外_のシステム設定を更新するために直接アクセスできます。この設定は本質的に、特定のレジストリ キーの場所でサンドボックスに_穴を開けます_。

[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:
```
   .
   .
   .
   [DefaultBox]
   OpenKeyPath=firefox.exe,HKEY_LOCAL_MACHINE\Software\Mozilla
   OpenKeyPath=firefox.exe,HKEY_CURRENT_USER\Software\Mozilla
```

これらの例では、Firefox プログラム _firefox.exe_ が Mozilla レジストリ キー ツリー (システム全体とユーザーごとの両方のレジストリ ツリー) に直接アクセスできます。

_OpenKeyPath_ に指定する値にはワイルドカードを含めることができますが、レジストリ キーの場合、ワイルドカードの使用が必要になることはほとんどありません。ワイルドカードの使用を示す例を含む詳細については、[OpenFilePath](OpenFilePath.md) を参照してください。(_OpenFilePath_ はファイルを扱い、レジストリ キーではありませんが、ワイルドカードを使用する原則は同じままです。)

**注:** 通常の _OpenKeyPath_ エントリは、Sandboxie のボックス化されたイメージの Open 制限がアクティブな間に要求側の実行可能ファイル自体がサンドボックス内に存在する場合、通常は除外されます。これは適格性ルールであり、構文の無条件のプロパティではありません。[Application Compartment](NoSecurityIsolation.md) などの構成はそのポリシーを変更できます。[OpenConfPath](OpenConfPath.md) はその通常のゲートによって除外されません。適格性はルールが優先されることを保証しません。[Rule Specificity](../PlusContent/RuleSpecificity.md) を参照してください。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Resource Access > Registry Access > Direct Access](ResourceAccessSettings.md#registry-access-direct-access)

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Open
