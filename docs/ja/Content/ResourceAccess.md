# Resource Access

[Resource Access Settings](ResourceAccessSettings.md) は、サンドボックス化されたプログラムがリソースにアクセスする方法を制御します。一部のルールは、要求元プログラムの実行可能ファイルがサンドボックスの外から読み込まれたか内側から読み込まれたかを区別します。

以下の両方の列は、Sandboxie の下で実行されているプログラムについて説明しています。「はい」は、その実行可能ファイルの場所にあるプログラムにルールが適用される資格があることを意味し、アクセスが許可されることを意味しません。プログラム セレクター、[ルールの優先順位](../PlusContent/RuleSpecificity.md)、およびその他のセキュリティ制限が依然として結果に影響します。


| 設定         | サンドボックスの外の実行可能ファイル | サンドボックス内の実行可能ファイル |
|-----------------|---------|--------|
|[ClosedClsid](ClosedClsid.md)        | はい     | はい    |
|[ClosedFilePath](ClosedFilePath.md)   | はい     | はい    |
|[ClosedIpcPath](ClosedIpcPath.md)    | はい     | はい    |
|[ClosedKeyPath](ClosedKeyPath.md)    | はい     | はい    |
|[ClosedRT](ClosedRT.md)   | はい     | はい    |
|[NoRenameWinClass](NoRenameWinClass.md) |  はい    |    はい    |
|[NormalFilePath](NormalFilePath.md)    | はい     | はい      |
|[NormalIpcPath](NormalIpcPath.md)     | はい     | はい      |
|[NormalKeyPath](NormalKeyPath.md)     | はい     | はい      |
|[OpenClsid](OpenClsid.md)        | はい     | はい    |
|[OpenConfPath](OpenConfPath.md)        | はい     | はい    |
|[OpenFilePath](OpenFilePath.md)     | はい     | 既定ではいいえ       |
|[OpenIpcPath](OpenIpcPath.md)      | はい     | はい      |
|[OpenKeyPath](OpenKeyPath.md)      | はい     | 既定ではいいえ       |
|[OpenPipePath](OpenPipePath.md)     | はい     | はい      |
|[OpenWinClass](OpenWinClass.md)     | はい     | はい    |
|[ReadFilePath](ReadFilePath.md)     | はい  | はい   |
|[ReadIpcPath](ReadIpcPath.md)       | はい     | はい   |
|[ReadKeyPath](ReadKeyPath.md)       | はい  | はい   |
|[WriteFilePath](WriteFilePath.md)   | はい      | はい     |
|[WriteKeyPath](WriteKeyPath.md)     | はい      | はい     |


「既定ではいいえ」のエントリは、サンドボックス内から読み込まれた実行可能ファイルに対する通常の `OpenFilePath` および `OpenKeyPath` ルールの除外を説明しています。`DontOpenForBoxed=n` はこの除外を無効にします。[Application Compartment](NoSecurityIsolation.md) モードも同様です。`OpenPipePath` および `OpenConfPath` はこの除外の対象ではありません。

`ReadIpcPath` はここではその `$:...` ターゲット プロセス ルールを指します。これらは別のプロセスへの限定的な読み取りアクセスを許可し、一般的な名前付き IPC オブジェクト一致とは別個のポリシーを使用します。[Read IPC Path](ReadIpcPath.md) を参照してください。

`AlwaysCloseForBoxed` がアクティブな場合 (Application Compartment モード以外の既定)、`ClosedFilePath`、`ClosedKeyPath`、または `ClosedIpcPath` の `!program.exe` などの否定されたプログラム セレクターは、サンドボックス内から読み込まれた実行可能ファイルを免除しません。`AlwaysCloseForBoxed=n` を設定すると、通常のセレクター一致が復元されます。Sandboxie コンポーネントには、否定された `ClosedIpcPath` エントリに対する追加の例外があります。
