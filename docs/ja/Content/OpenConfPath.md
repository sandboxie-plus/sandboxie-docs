# Open Conf Path

_OpenConfPath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、v1.0.0 / 5.55.0 以降で使用できます。Sandboxie がレジストリ キーに対してサンドボックス化を適用しないパス パターンを指定します。これにより、サンドボックス化されたプログラムが_サンドボックスの外_のシステム設定を更新するために直接アクセスできます。この設定は本質的に、特定のレジストリ キーの場所でサンドボックスに_穴を開けます_。

一度選択されると、_OpenConfPath_ は [OpenKeyPath](OpenKeyPath.md) と同じ直接ホスト レジストリ アクセス モデルを使用します。その重要な違いは適格性です。通常のボックス化された実行可能ファイルの Open ルール ゲートによって除外されません。**Open for All** はボックス化された実行可能ファイルに適格であることを意味し、優先順位が保証されるわけではありません。プロセス セレクターと [Rule Specificity](../PlusContent/RuleSpecificity.md) は依然として適用されます。

[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:
```
   .
   .
   .
   [DefaultBox]
   OpenConfPath=firefox.exe,HKEY_LOCAL_MACHINE\Software\Mozilla
   OpenConfPath=firefox.exe,HKEY_CURRENT_USER\Software\Mozilla
```

これらの例では、Firefox プログラム _firefox.exe_ が Mozilla レジストリ キー ツリー (システム全体とユーザーごとの両方のレジストリ ツリー) に直接アクセスできます。

_OpenConfPath_ に指定する値にはワイルドカードを含めることができますが、レジストリ キーの場合、ワイルドカードの使用が必要になることはほとんどありません。ワイルドカードの使用を示す例を含む詳細については、[OpenFilePath](OpenFilePath.md) を参照してください。(_OpenFilePath_ はファイルを扱い、レジストリ キーではありませんが、ワイルドカードを使用する原則は同じままです。)

**注:** この設定は、プログラムの実行可能ファイルがサンドボックス内に存在する場合でも適用されることがあります。これは、コンピューターにダウンロードされて実行された (潜在的に悪意のある) ソフトウェアが、このルールが優先されネイティブのアクセス許可が許す場合に、直接のホスト アクセスを利用できることを意味します。

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Open for All
