# Close Print Spooler

_ClosePrintSpooler_ は、Windows Print Spooler エンドポイントを解決するための Sandboxie の仲介パスを制御します。有効な値が構成されていない場合、既定で `n` になります。

```
   .
   .
   .
   [DefaultBox]
   ClosePrintSpooler=n
```

`ClosePrintSpooler=y` の場合、Sandboxie はこのパスを通じた新しいスプーラー エンドポイント解決要求を拒否します。これは通常、そのエンドポイントの取得に依存する印刷を妨げますが、Windows Print Spooler サービスを停止したり、既に取得されたエンドポイント、バインディング、またはハンドルを取り消したりするものではありません。

サービスは、新しいエンドポイント要求ごとに有効な値をチェックします。変更された構成を再読み込みした後、以降のエンドポイント解決要求は新しい値を使用できます。

SandMan では、これは **Sandbox Options > General Options > Restrictions > Printing restrictions > Block access to the printer spooler** です。このチェックボックスは Application Compartment ボックスでは無効です。直接のボックス値を反映しますが、実行時には該当するテンプレートまたはグローバル構成も使用される場合があります。Sandboxie Control Classic は同等のアクティブな設定ページを提供しません。このオプションは `Sandboxie.ini` で構成できます。

0.5.4 / 5.46.0 バージョンの一部として追加されました。

## [OpenPrintSpooler](OpenPrintSpooler.md) との相互作用

```
   .
   .
   .
   [DefaultBox]
   ClosePrintSpooler=n
   OpenPrintSpooler=n
```

両方の設定が `n` の場合、_ClosePrintSpooler_ は新しいエンドポイント解決要求を拒否せず、_OpenPrintSpooler_ は Sandboxie の選択的なスプーラー RPC メッセージ フィルターをアクティブに保ちます。このフィルターはすべてのプリンター構成操作ではなく選択された操作を拒否し、印刷が成功することを保証しません。`OpenPrintSpooler=y` を設定するとその特定のフィルターがスキップされますが、`ClosePrintSpooler=y` は上書きされません。

別個の [AllowSpoolerPrintToFile](AllowSpoolerPrintToFile.md) 設定は、サンドボックス化されたプロセスに代わってホスト スプーラーが行うファイル オープンに関するものです。
