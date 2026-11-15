# Auto Recover Ignore

_AutoRecoverIgnore_ は [Sandboxie Ini](SandboxieIni.md) の繰り返し可能なサンドボックス設定です。自動 [Immediate Recovery](ImmediateRecovery.md) 検出は [RecoverFolder](RecoverFolder.md) の照合後にこのリストをチェックするため、無視された候補は自動復元のために報告されません。SandMan は、[UseAutoRecoverIgnoreForQuick](UseAutoRecoverIgnoreForQuick.md) が有効な場合、一致する [Quick Recovery](QuickRecovery.md) エントリを非表示にするためにもこれを使用できます。例:

```
   .
   .
   .
   [DefaultBox]
   AutoRecoverIgnore=.part
   AutoRecoverIgnore=%Desktop%
   AutoRecoverIgnore=C:\Folder
```

最初の例は、_.part_ で終わるファイルを自動復元から除外します。このようなファイルは不完全なダウンロードを表すことがあります。拡張子を削除すると、完成したファイルが対象になることがあります。付属の AutoRecoverIgnore テンプレートには _.part_ が含まれています。リテラル エントリは、該当する場合、パス プレフィックスまたはパス末尾のサフィックス パターンとして大文字と小文字を区別せずに照合されます。

2 番目と 3 番目の例は、指定されたフォルダーを自動復元から除外します。有効な無視エントリは、有効化されたテンプレートから取得することもできます。

Sandboxie Plus 1.18.0 以降、エントリには `*`、`?`、および `**` を使用したワイルドカード パターンを含めることができます。照合では、変換された NT、DOS、およびネットワーク エイリアスのパスを考慮することができます。プロセス側の検出器と SandMan の Quick Recovery リストは異なるパターン マッチャーを使用するため、これらの記号を普遍的なファイルシステム glob 文法として読むべきではありません。

Sandboxie Plus 1.18.0 以降、除外リストは [Quick Recovery](QuickRecovery.md) ウィンドウにも適用できます。[UseAutoRecoverIgnoreForQuick](UseAutoRecoverIgnoreForQuick.md) を参照してください。ウィンドウの **Show All Files** または **Show Ignored** ビューは、Quick リスト フィルタリングによって非表示にされたエントリを表示できますが、どちらも自動検出自体の無視チェックを変更しません。

自動検出と Quick リスト フィルタリングの区別については [File Recovery Architecture](RecoveryArchitecture.md) を参照してください。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Recovery > Immediate Recovery](RecoverySettings.md#immediate-recovery)
