# Copy Newer

_CopyNewer_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 1.18.1 以降で利用できます。ホスト上の一致するファイルがより最近変更されたときに、ファイルの既存のサンドボックス コピーが更新されるファイル パス パターンのリストを指定します。

使用法:

```
   .
   .
   .
   [DefaultBox]
   CopyNewer=C:\Data\*.txt
```

通常、ファイルがサンドボックスにコピーされると ([File Migration Settings](FileMigrationSettings.md) を参照)、ホスト上の元のファイルが後で変更されても、サンドボックス化されたプログラムはそのコピーを使用し続けます。ファイル パスが _CopyNewer_ パターンに一致する場合、Sandboxie は該当するオープンでホスト ファイルとサンドボックス コピーの最終書き込み時刻を比較します。ホスト ファイルが新しい場合、オープンが完了する前に更新が試行されます。

更新移行は、初期の内容移行と同じ移行ルール、サイズ制限、プロンプト動作、および通知を使用します。一致する [DontCopy](DontCopy.md) ルールは更新を防ぐことができ、[CopyAlways](CopyAlways.md) はサイズ制限とプロンプトの前に完全な内容の移行を選択でき、[CopyEmpty](CopyEmpty.md) は空の置き換えを選択できます。これらのルール自体は更新をトリガーしません。[CopyBlockDenyWrite](CopyBlockDenyWrite.md) は更新移行の結果に影響することがありますが、更新が失敗しても、既存のサンドボックス コピーの後続のオープンが必ずしも拒否されるわけではありません。

次の制限に注意してください:

- サンドボックス内に既にコピーがある通常のファイルにのみ適用され、それらが通常どおり開かれる場合に限られます。
- ファイルの初期移行、ディレクトリ、削除されたファイル、または作成/上書き操作には適用されません。更新は、[WriteFilePath](WriteFilePath.md) などの書き込み専用のリソース パス モードでもスキップされます。これは単にアプリケーションが要求したアクセスのテストではありません。
- パターン マッチングは大文字と小文字を区別せず、ホスト (真の) ファイル パスに適用されます。
- 更新が既に進行中であるか失敗した場合、既存のサンドボックス コピーは引き続きプログラムが利用できます。
- 成功した更新は必ずしも完全な内容の置き換えではありません。移行ルールまたはソース アクセスのフォールバックにより、内容が空になることがあります。

"Copy newer" タイプのルールを含むコピー ルールは、SandMan の Sandbox Options > General Options > File Migration で管理できます。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [CopyLimitKb](CopyLimitKb.md)、[CopyLimitSilent](CopyLimitSilent.md)。[File Migration Settings](FileMigrationSettings.md) も参照してください。
