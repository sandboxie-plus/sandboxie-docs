# Recover Folder

_RecoverFolder_ は [Sandboxie Ini](SandboxieIni.md) の繰り返し可能なサンドボックス設定です。`AutoRecover=y` の場合、[Quick Recovery](QuickRecovery.md) と自動 [Immediate Recovery](ImmediateRecovery.md) 検出の両方の回復可能な場所を識別します。有効なエントリには有効なテンプレートが含まれることがあります。[Shell Folders](ShellFolders.md) を指定できます。例:
```
   .
   .
   .
   [DefaultBox]
   RecoverFolder=%Personal%
   RecoverFolder=C:\Downloads
   [InstallBox]
   RecoverFolder=D:\Program Files
```

最初の 2 つの設定例は、DefaultBox サンドボックスからの [Quick Recovery](QuickRecovery.md) がドライブ C の _Documents_ および _Downloads_ フォルダーを検索すべきことを指定します。

3 番目の設定例は、InstallBox サンドボックスからの QuickRecovery がドライブ D の _Program Files_ フォルダーを検索すべきことを指定します。

リテラル ディレクトリ エントリの場合、[Quick Recovery](QuickRecovery.md) はそのフォルダーとそのサブフォルダーを再帰的にスキャンします。代わりに自動検出は、対象となるファイル アクティビティを構成されたエントリと照合します。

Sandboxie Plus 1.18.0 以降、エントリは `*`、`?`、および `**` を使用したワイルドカード パターンを含むことができます。ワイルドカード エントリは候補パスをフィルター処理します。それ自体で任意の再帰的 Quick Recovery スキャン ルートを確立するものではありません。一致は翻訳された NT、DOS、およびネットワーク エイリアス パスを考慮することがあります。正確なパターン処理はプロセス側の検出器と SandMan の Quick Recovery リストで異なるため、これらの記号を万能のファイルシステム glob 文法として扱わないでください。

2 つのコンシューマーとそれらの異なるライフサイクルについては [File Recovery Architecture](RecoveryArchitecture.md) を参照してください。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Recovery > Quick Recovery](RecoverySettings.md#quick-recovery)
