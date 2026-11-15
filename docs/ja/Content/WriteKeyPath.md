# Write Key Path

WriteKeyPath は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie がサンドボックス外のレジストリ キーを隠し、サンドボックス内で新しいレジストリ キーとレジストリ値を作成できるようにするパス パターンを指定します。

[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:
```
   .
   .
   .
   [DefaultBox]
   WriteKeyPath=HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths
```


この例は、_TypedPaths_ レジストリ キー内でサンドボックス外に存在するデータを隠し、プログラムがサンドボックス内の対応する _TypedPaths_ レジストリ キー内に新しいキーと値を作成できるようにします。これは、サンドボックス内で実行される Windows Explorer が、サンドボックス外で Windows Explorer に入力されたパスの履歴を表示できないことを意味します。しかし、サンドボックス内で実行される Windows Explorer は、入力された新しいパスを記録して保存できます。

注: このモードは、選択されたスコープの通常のホスト レジストリ データを隠しつつ、サンドボックス側のキーと値を許可します。**Write Only** は、アプリケーションがサンドボックス側ビューに存在するデータを読み取れないという意味ではありません。選択されたスコープはルールの一致によって異なります。[Rule Specificity](../PlusContent/RuleSpecificity.md) を参照してください。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Resource Access > Registry Access > Write-Only Access](ResourceAccessSettings.md#registry-access-write-only-access)

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Box Only (Write Only)
