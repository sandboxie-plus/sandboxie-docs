# Open Device Configuration Manager API

`OpenDevCMApi` は [Sandboxie Ini](SandboxieIni.md) のボックス全体のブール設定です。特定の変更を伴う Windows Device Configuration Manager 操作に対する Sandboxie の選択的フィルターを無効にします。既定は `n` です。

```ini
[DefaultBox]
OpenDevCMApi=y
```

!!! warning
    この設定を有効にすると、昇格されたサンドボックス化されたプロセスが、サンドボックス削除後も保持されるホストのハードウェア構成変更を行うことができるようになる場合があります。すべてのハードウェアへの無制限のアクセスを付与したり、Windows のアクセス チェックをバイパスしたり、他の Sandboxie リソース制限を無効にしたりするものではありません。

## 何がフィルター処理されるか

既定の `OpenDevCMApi=n` では、Sandboxie ドライバーは Configuration Manager API エンドポイントに向けられたデバイス制御要求を検査します:

```text
\Device\DeviceApi\CMApi
```

選択された変更操作は、アクセス拒否ステータスで拒否されます。現在のフィルターは次のカテゴリをカバーします:

- ソフトウェア デバイスのプロパティまたは有効期間の変更。
- ソフトウェア デバイス インターフェイスの登録とその状態またはプロパティの変更。
- デバイス ノード、デバイス インターフェイス、またはデバイス クラスのプロパティの設定。
- デバイス クラスまたはデバイス ノードのレジストリ プロパティの設定。
- デバイス ノードの問題状態の設定。
- デバイス ノードの無効化またはデバイス サブツリーの削除要求。
- デバイス インターフェイスの登録または登録解除。
- デバイス ノードの作成またはアンインストール。
- デバイス インターフェイス、デバイス ノード、またはデバイス クラスのキーの削除。

これは選択的な拒否リストであり、Configuration Manager API の完全なブロックではありません。現在のクエリおよび読み取り操作は一般に通過させられます。これには、デバイスまたはクラスの列挙、プロパティの読み取り、デバイス ノードの状態または深さのクエリ、インターフェイス エイリアスの解決、デバイス インスタンスの検証、および関連するレジストリ キーを開くための代表的な操作が含まれます。フィルターによって選択されていない他の操作も、基になる Windows デバイス制御パスに続行されます。

`OpenDevCMApi=y` はこの CMApi 固有の変更フィルターをスキップします。基になる操作は依然として Windows のアクセス許可および独立した Sandboxie コントロールの対象であるため、この設定は要求されたハードウェア管理操作が成功することを保証しません。また、それ自体で CMApi デバイス オブジェクトを開けるかどうかを変更するものでもありません。

## フィルターが存在する理由

このフィルターは、[issue #552](https://github.com/sandboxie-plus/Sandboxie/issues/552) が、昇格されたプロセスがサンドボックス内からデバイス マネージャーを使用してホスト デバイスを削除できることを実証した後、Security Issue ID-14 のために導入されました。それらの変更はホストに影響を与え、サンドボックスの削除とは独立して保持されました。

`OpenDevCMApi=y` は、フィルター処理されたデバイス管理操作の 1 つを真に必要とするソフトウェアの互換性例外としてのみ使用してください。

## 互換性

Sandboxie Plus 0.7.1 / Classic 5.48.5 は、選択された変更制限を維持しながら Web カメラ アクセスの問題を修正するためにフィルターを改良しました。したがって、通常の Web カメラ アクセスが `OpenDevCMApi=y` を必要とすると想定すべきではありません。

## 変更の適用

この設定はサンドボックスに対して指定することも、通常のテンプレートおよびグローバル構成の解決を通じて継承することもできます。文書化された実行可能ファイル修飾構文はありません。

ドライバーは、各サンドボックス化されたプロセスを初期化するときに有効な値をキャッシュします。設定を変更した後は、影響を受けるサンドボックス化されたアプリケーションを再起動するか、サンドボックス化されたプロセス ツリーを再作成してください。新しく開始されたプロセスのために SandMan、サービス、またはドライバーを再起動する必要は通常ありません。

## SandMan の構成

コントロールは次の場所にあります:

**Sandbox Options > General Options > Isolation > Allow sandboxed programs to manage Hardware/Devices**

このチェックボックスは既定でクリアです。これを選択すると `OpenDevCMApi=y` が書き込まれ、これはより制限の少ない互換性状態です。SandMan は **No Security Isolation** が選択されているときにこのコントロールを無効にします。

## 他のデバイス機能との関係

[`BlockRegisterDeviceNotification`](BlockRegisterDeviceNotification.md) は、デバイス通知登録用の別個のユーザー モード フックを制御します。CMApi 変更フィルターを有効または無効にしません。

[USB Drive Sandboxing](../PlusContent/USBSandboxing.md) も独立しています。その機能は、対象となる USB バッキング ボリュームの強制フォルダー ルールを維持する SandMan 自動化であり、USB デバイスを仮想化または制御するために `OpenDevCMApi` を使用しません。

## バージョン履歴

| 変更 | バージョン |
| --- | --- |
| CMApi 変更フィルターと `OpenDevCMApi` 互換性設定を導入 | Sandboxie Plus 0.7.0 / Classic 5.48.0 |
| フィルターを有効にした状態での Web カメラ互換性を改善 | Sandboxie Plus 0.7.1 / Classic 5.48.5 |

## 関連ページ

- [Block Register Device Notification](BlockRegisterDeviceNotification.md)
- [USB Drive Sandboxing](../PlusContent/USBSandboxing.md)
- [Sandboxie Ini](SandboxieIni.md)
