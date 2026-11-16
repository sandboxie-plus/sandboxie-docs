# Block Register Device Notification

`BlockRegisterDeviceNotification` は [Sandboxie Ini](SandboxieIni.md) のボックス全体のブール設定です。有効な場合、選択された USER32 API を通じて行われるデバイス通知の登録を抑制します。既定は `n` です。

```ini
[DefaultBox]
BlockRegisterDeviceNotification=y
```

## ランタイムの動作

この設定が有効な場合、Sandboxie は次に対するユーザー モード フックをインストールします:

- `RegisterDeviceNotificationA`
- `RegisterDeviceNotificationW`
- `UnregisterDeviceNotification`

傍受された ANSI および Unicode の登録呼び出しは、基になる Windows の登録関数を呼び出しません。Sandboxie は最後のエラー値をクリアし、成功したように見えるプレースホルダー ハンドルを返すため、その呼び出しを通じて登録が行われなかったにもかかわらず、アプリケーションは登録が成功したと信じることがあります。傍受された登録解除関数も同様に、実際の登録解除操作を実行せずに最後のエラー値をクリアし、成功を報告します。

プレースホルダー ハンドルは実装の詳細であり、アプリケーションが依存すべきではありません。

## スコープと制限事項

この設定は `RegisterDeviceNotificationA/W` を通じて行われる登録を抑制します。すべてのデバイス変更またはプラグ アンド プレイ通知メカニズムに対する普遍的なブロックではありません。現在の実装は、サンドボックス化されたアプリケーションが他のパスを通じて `WM_DEVICECHANGE`、ブロードキャスト通知、Configuration Manager 通知、サービス通知、またはカーネル レベルの通知をまったく受け取れないことを確立しません。

特に、ドライバーの別個の Configuration Manager フィルターは現在、`CMP_Register_Notification` に関連する関数を拒否しません。そのパスは、この設定によって傍受される USER32 登録関数とは異なります。

## 変更の適用

この設定はサンドボックスに対して指定するか、通常のテンプレートおよびグローバル構成の解決を通じて継承できます。文書化された実行可能ファイル修飾構文はありません。

Sandboxie はサンドボックス化されたプロセスで GUI フックを初期化するときに有効な値を読み取ります。設定を変更しても、既に初期化されたプロセスでそれらのフックが動的にインストールまたは削除されることはありません。変更後は、影響を受けるサンドボックス化されたアプリケーションを再起動するか、サンドボックス化されたプロセス ツリーを再作成してください。SandMan、サービス、またはドライバーの再起動は通常必要ありません。

## SandMan 構成

SandMan は現在 `BlockRegisterDeviceNotification` 用の専用チェックボックスを提供していません。サンドボックスの INI セクションで手動で構成してください。

## 他のデバイス機能との関係

[`OpenDevCMApi`](OpenDevCMApi.md) は、選択された変更を伴う Device Configuration Manager 操作のための別個のドライバー フィルターを制御します。2 つの設定は独立して動作します。

[USB Drive Sandboxing](../PlusContent/USBSandboxing.md) は、該当する USB バッキング ボリュームを検出し、強制フォルダー ルールを維持する SandMan のホスト側自動化です。`BlockRegisterDeviceNotification` はその自動化を制御せず、SandMan 自体がデバイス変更を監視することを妨げません。

## バージョン履歴

現在の設定メタデータは `BlockRegisterDeviceNotification` を Sandboxie Plus 1.9.5 / Classic 5.64.5 で導入されたものとして記載しています。対応するランタイム変更により、通知登録フックがこの設定に条件付けられました。同じリリースの変更履歴は、`DBT_DEVTYP_DEVICEINTERFACE` を使用する `RegisterDeviceNotificationW` 登録に関する修正を記録しています。

## 関連ページ

- [Open Device Configuration Manager API](OpenDevCMApi.md)
- [USB Drive Sandboxing](../PlusContent/USBSandboxing.md)
- [Sandboxie Ini](SandboxieIni.md)
