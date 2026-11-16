# Start System Box

_StartSystemBox_ は繰り返し可能なグローバル設定で、SbieSvc が起動し Sandboxie ドライバーが準備完了になったときに、名前付きサンドボックスをセッション 0 で開始します。

```ini
[GlobalSettings]
StartSystemBox=SystemBox
```

各値はサンドボックス名であり、ブール値ではありません。複数のエントリで複数のボックスを開始します:

```ini
[GlobalSettings]
StartSystemBox=BoxOne
StartSystemBox=BoxTwo
```

## 起動時の動作

構成された各名前に対して、SbieSvc は次と同等のものを開始します:

```text
Start.exe /box:<BoxName> auto_run
```

起動フローは次のとおりです:

```text
SbieSvc starts and the driver becomes ready
    -> Start.exe is launched for the configured box
    -> Start.exe restarts inside that sandbox
    -> auto_run processes the sandbox's supported autostart locations
```

このフローは SbieSvc から発生するため、SYSTEM ID でセッション 0 で実行されます。結果として得られるプロセスは依然として名前付きサンドボックスに関連付けられています。SYSTEM ID はそれらをサンドボックス外にするものではありません。

## `auto_run` が開始するもの

現在の `auto_run` 実装は、マシンおよび現在のユーザー用のサンドボックス可視の `Run` および `RunOnce` レジストリ エントリ (32 ビットの場所を含む)、および共通およびユーザーのスタートアップ フォルダーを処理します。

このコマンドは現在、ボックス化されたサービスを直接開始しません。`StartService`、`StartProgram`、および `AutoExec` は別個のボックス起動メカニズムであり、_StartSystemBox_ の同義語として扱うべきではありません。

## セキュリティに関する考慮事項

プロジェクトは、この方法で開始されるボックスに対して [Drop Admin Rights](DropAdminRights.md) を有効にすることを推奨しています:

```ini
[SystemBox]
DropAdminRights=y
```

セッション 0 の SYSTEM ID はトークンの強化を特に重要にしますが、`DropAdminRights` が任意の SYSTEM ソフトウェアを安全にするわけではありません。[Strip System Privileges](StripSystemPrivileges.md) は特定のサービスおよび RpcSs トークン作成パスによって使用される別個のコントロールです。_StartSystemBox_ がセッション 0 でボックスを開始したというだけでは自動的に適用されません。

## 変更の適用

SbieSvc はドライバーが準備完了になった後、その起動シーケンス中に _StartSystemBox_ エントリを読み取ります。通常の構成の再読み込みは新しく追加されたエントリを実行しません。変更は次回の Sandboxie サービス起動またはシステム起動時に有効になります。エントリを削除しても、既に開始されたプロセスは終了しません。

## SandMan

SandMan には専用の _StartSystemBox_ コントロールはありません。Sandboxie.ini の `[GlobalSettings]` の下で手動で構成してください。

## バージョン履歴

_StartSystemBox_ は、セッション 0 のサンドボックス起動および `auto_run` コマンドとともに Sandboxie Plus 0.9.5 / Classic 5.51.5 で導入されました。

## 関連ページ

- [Drop Admin Rights](DropAdminRights.md)
- [Strip System Privileges](StripSystemPrivileges.md)
- [Start Service](StartService.md)
- [Start Program](StartProgram.md)
- [Auto Exec](AutoExec.md)
- [Sandboxed Services](SandboxedServices.md)
- [Sandboxie Ini](SandboxieIni.md)
