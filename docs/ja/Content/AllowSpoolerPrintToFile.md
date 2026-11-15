# Allow Spooler Print To File

`AllowSpoolerPrintToFile` は、Windows Print Spooler サービス `spoolsv.exe` がサンドボックス化されたプロセスに代わって動作するときの、特別なファイル オープン ガードを制御します。有効な値が構成されていない場合、既定で `n` になります。

```
   .
   .
   .
   [DefaultBox]
   AllowSpoolerPrintToFile=n
```

`AllowSpoolerPrintToFile=n` の場合、Sandboxie はホスト `spoolsv.exe` による該当する書き込みアクセスのファイル オープンを、発信元のサンドボックス化されたプロセスの通常のファイル アクセス ポリシーと照合します。このガードには例外 (サンドボックスのスプーラー作業ディレクトリなど) があり、すべての `CreateFile` 呼び出しやすべての印刷ジョブをブロックするわけではありません。通常のファイル アクセス ルールは、宛先が許可されるかどうかに影響することがあります。

`AllowSpoolerPrintToFile=y` の場合、この特別なガードは関連するサンドボックス化されたプロセスに対してスキップされます。これは `spoolsv.exe` にホスト ファイルシステムへの無制限のアクセスを与えるものではありません。Windows のアクセス許可およびその他の制御が引き続き適用されます。

該当する拒否は **SBIE1319** を生成することがあります。まだ実行中のプロセスについて、SandMan はそのプロセスに対してスプーラーがサンドボックス外へ書き込むことを許可するかどうかを尋ねることができます。**Yes** を選択すると、そのプロセス ID および将来の一致するファイル オープンに対して一時的な例外が付与されます。これは Sandboxie.ini を変更したり、`AllowSpoolerPrintToFile=y` を設定したり、すでに失敗したファイル オープンを再試行したりするものではありません。例外はそのプロセスが終了すると終わります。Sandboxie Control Classic では、**SBIE1319** の後に **SBIE1320** が続きます。後者をダブルクリックすると、同じプロセス固有の例外が付与されます。

永続的な設定は、サンドボックス化されたプロセスが IPC 状態を初期化するときに読み込まれます。変更後は影響を受けるサンドボックス化されたプロセスを再起動して、新しい値を使用するようにしてください。SandMan では、コントロールは **Sandbox Options > General Options > Restrictions > Printing restrictions > Allow the print spooler to print to files outside the sandbox** です。**Block access to the printer spooler** または **Disable Security Filtering (not recommended)** がチェックされている場合は無効になりますが、ボックスが Application Compartment を使用しているという理由だけで無効になるわけではありません。`NoSecurityFiltering=y` の Application Compartment では、このガードが使用する通常のファイル ポリシー チェックが通常の拒否を提供しなくなります。チェックボックスは直接のボックス値を反映しますが、実行時には該当するテンプレートまたはグローバル構成も使用される場合があります。

[ClosePrintSpooler](ClosePrintSpooler.md) は代わりに新しいスプーラー エンドポイント解決要求を制御し、[OpenPrintSpooler](OpenPrintSpooler.md) は別個の選択的なメッセージ フィルターを制御します。
