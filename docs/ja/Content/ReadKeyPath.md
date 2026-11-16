# Read Key Path

_ReadKeyPath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。勝ち抜いたルールはホスト レジストリへの直接アクセスを選択します。レジストリ フィルターがアクティブな標準サンドボックスでは、ホストへの書き込み/削除アクセスは通常ドライバーによって拒否されます。ネイティブ Windows のアクセス許可も依然として適用されます。

[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:
```
   .
   .
   .
   [DefaultBox]
   ReadKeyPath=HKEY_LOCAL_MACHINE\SOFTWARE\Policies
```

標準のレジストリ フィルターがアクティブで、このルールが選択されている場合、例では _Policies_ キーとその子孫に対してホスト読み取りを使用し、通常はホストへの書き込み/削除アクセスを拒否します。

注: _ReadKeyPath_ は [OpenKeyPath](OpenKeyPath.md) と同じ直接ホスト データ パスを使用します。通常のサンドボックス コピーはその選択されたビューにマージされません。これは通常のアクセス パスを説明するもので、すべてのメタデータ/クエリ API ではありません。関連するレジストリ フィルター処理を無効にすると読み取り専用の強制の前提が変わり、構成の変更は既に開かれているハンドルを普遍的に取り消すものではありません。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Resource Access > Registry Access > Read-Only Access](ResourceAccessSettings.md#registry-access-read-only-access)

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Read Only
