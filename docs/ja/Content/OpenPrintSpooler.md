# Open Print Spooler

_OpenPrintSpooler_ は、Windows Print Spooler に送信されるメッセージに対する Sandboxie の選択的フィルターを制御します。有効な値が構成されていない場合は `n` に既定設定されます。

```
   .
   .
   .
   [DefaultBox]
   OpenPrintSpooler=n
```

`OpenPrintSpooler=n` の場合、フィルターはアクティブなままで、一部のプリンター管理操作を含む選択されたスプーラー RPC メッセージ操作を拒否します。すべてのプリンター構成またはインストール操作をブロックするわけではなく、通常の印刷が成功することをそれ自体で保証するものでもありません。

`OpenPrintSpooler=y` を設定すると、この特定のメッセージ フィルターがスキップされます。新しいエンドポイント解決要求を制御する [ClosePrintSpooler](ClosePrintSpooler.md) を上書きしたり、他の IPC 制限、Windows のアクセス許可、または別個の [print-to-file file-open guard](AllowSpoolerPrintToFile.md) をバイパスしたりしません。

有効な値は、サンドボックス化されたプロセスがその IPC 状態を初期化するときに読み込まれます。新しい値を使用することを確実にするために、設定を変更した後は影響を受けるサンドボックス化されたプロセスを再起動してください。

SandMan では、コントロールは **Sandbox Options > General Options > Restrictions > Printing restrictions > Remove spooler restriction, printers can be installed outside the sandbox** です。**Block access to the printer spooler** がチェックされている場合、または Application Compartment では無効になります。チェックボックスはボックスの直接の値を反映しますが、ランタイムは該当するテンプレートまたはグローバル構成も使用できます。Sandboxie Control Classic は同等のアクティブな設定ページを提供していません。オプションは `Sandboxie.ini` で構成できます。

0.5.4 / 5.46.0 バージョンの一部として追加されました。

_[ClosePrintSpooler](ClosePrintSpooler.md) も参照してください。_
