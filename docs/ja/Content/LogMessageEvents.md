# Log Message Events

_LogMessageEvents_ は [Sandboxie Ini](SandboxieIni.md) のグローバル設定で、v1.15.2 / 5.70.2 以降で使用できます。Sandboxie がすべての Sandboxie メッセージを Windows の [System Event Log](SystemEventLog.md) にログ記録することを示します。

## 使用法

```ini
[GlobalSettings]

LogMessageEvents=y
```

## 概要

有効にすると、この設定はすべての Sandboxie メッセージ (SBIE コード) を、ソース `SbieDrv`[^1] で Windows System Event Log に書き込むようにします。これにより、通常はポップアップ ダイアログまたは Sandboxie メッセージ ログにのみ表示されるエラー、警告、および情報メッセージを含む、すべての Sandboxie アクティビティを表示および監視するための集中化された場所が提供されます。

## 動作

`LogMessageEvents` 設定は、ドライバー レベル[^2] でのメッセージ ログ記録の処理方法に影響します。メッセージが生成されると:

1. メッセージはまず通常の Sandboxie メッセージ システム[^3] を通じて処理されます。
2. `LogMessageEvents` が有効な場合、メッセージは追加で情報イベントとして Windows Event Log に送信されます[^4]。
3. イベントにはフォーマットされたメッセージ テキストが含まれ、適切な SBIE メッセージ コードでタグ付けされます[^5]。

## 使用シナリオ

この設定は特に次の場合に役立ちます:

- **システム管理者**: 集中ログ管理を通じて複数のシステムにわたる Sandboxie アクティビティを監視します。
- **デバッグ**: トラブルシューティングのために Sandboxie 操作の完全な記録を取得します。
- **コンプライアンス**: サンドボックス化されたアプリケーションの動作の監査ログを維持します。
- **自動化**: 監視ツールが標準の Windows Event Log API を通じて特定の Sandboxie イベントを監視できるようにします。

## メッセージのフィルター処理

この設定が有効な場合、すべての Sandboxie メッセージがイベント ログに記録されるわけではありません。次のメッセージの種類は、イベント ログ記録から特に除外されます[^6]:

- **MSG_2199**: 自動復元通知。
- **MSG_2198**: ファイル移行の進行状況通知。
- **MSG_1399**: プロセス開始通知。

これらの除外により、通常の Sandboxie 操作中に頻繁に発生する日常的な操作メッセージでイベント ログが圧倒されるのを防ぎます。

## パフォーマンスに関する考慮事項

`LogMessageEvents` を有効にすると、通常の状況ではパフォーマンスへの影響は最小限です。ただし、サンドボックス アクティビティが多い環境では、追加のイベント ログ書き込みがシステム オーバーヘッドの一因となることがあります。最大パフォーマンスが重要な本番環境では、この設定を慎重に使用する必要があります。

## 実装上の注意

`LogMessageEvents` 機能は、カーネル ドライバー レベルとサービス レベルの両方で実装されています[^7]:

- ドライバー コンポーネント (SbieDrv) は構成の読み込み中に設定をチェックします[^8]
- メッセージはサービス コンポーネントを通じて処理され、フォーマットされてイベント ログに書き込まれます[^9]
- 設定はパフォーマンスのためにキャッシュされ、構成が再読み込みされるときに再読み取りされます[^10]

## トラブルシューティング

`LogMessageEvents` が有効であるにもかかわらずイベントが Windows Event Log に表示されない場合:

1. 設定が `[GlobalSettings]` セクションで適切に構成されていることを確認します。
2. Sandboxie サービスに Event Log への書き込みに適切なアクセス許可があることを確認します。
3. 設定を変更した後、Sandboxie サービスを再起動します。
4. Windows Event Log サービスが実行されていることを確認します。

## 歴史的な背景

この機能は、強化された監視機能の一環として Sandboxie Plus バージョン 1.15.2 / 5.70.2 で導入されました[^11]。この設定の使用時にシステム クラッシュ (BSoD) を引き起こす可能性のある重大なバグは、バージョン 1.15.4 で修正されました[^12]。

[^1]: 出典: `/Sandboxie/core/svc/main.cpp` の `LogMessage_Event` 関数。
[^2]: 出典: `/Sandboxie/core/drv/log.c` の `Log_LogMessageEvents` ブール変数定義。
[^3]: 出典: `/Sandboxie/core/drv/log.c` の `Log_Popup_Msg` 関数呼び出しロジック。
[^4]: 出典: `/Sandboxie/core/svc/main.cpp` の `ReportEvent` 呼び出し。
[^5]: 出典: `/Sandboxie/core/svc/main.cpp` の `SbieDll_FormatMessage2` 呼び出しでのメッセージ フォーマット。
[^6]: 出典: `/Sandboxie/core/svc/DriverAssistLog.cpp` のメッセージ フィルター ロジック。
[^7]: 出典: `/Sandboxie/core/drv/log.c` の `Api_SendServiceMessage` を介したデータ通信。
[^8]: 出典: `/Sandboxie/core/drv/conf.c` の `Conf_Get_Boolean` 呼び出しでの構成の読み込み。
[^9]: 出典: `/Sandboxie/core/svc/DriverAssistLog.cpp` の `LogMessage` 関数。
[^10]: 出典: `/Sandboxie/core/drv/log.h` の `Log_LogMessageEvents` グローバル変数キャッシュ。
[^11]: 出典: バージョン 1.15.2 / 5.70.2 の CHANGELOG.md エントリ
[^12]: 出典: バージョン 1.15.4 / 5.70.4 の BSoD 修正の CHANGELOG.md エントリ
