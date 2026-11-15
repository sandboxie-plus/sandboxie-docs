# Copy Empty

_CopyEmpty_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 0.6.5 以降で利用できます。ファイル移行中に、ホスト ファイルの内容をコピーする代わりに、Sandboxie が長さゼロのサンドボックス コピーを作成するホスト ファイルのパス パターンを指定します。

使用法:

`CopyEmpty=[program,]pattern`

```ini
[DefaultBox]
CopyEmpty=*\Cache\*.log
CopyEmpty=indexer.exe,*\SearchData\*.db
```

各 _CopyEmpty_ エントリは 1 つのルールであり、この設定は繰り返すことができます。コンマの前の省略可能なプレフィックスはルールをそのプログラムに制限します。[Program Name Prefix](ProgramNamePrefix.md) を参照してください。パスは [OpenFilePath](OpenFilePath.md) と同じパターン形式を使用します。照合は大文字と小文字を区別せず、ホスト (真の) ファイル パスに対して実行されます。`*` はパス区切り文字を含む任意の文字シーケンスに一致し、`?` は 1 文字に一致します。

プログラム プレフィックスを使用する場合、現在の設定メタデータでは、パスのドライブまたはデバイス部分をワイルドカードで表す必要があります (例: `*\Cache\*.log`)。`C:\Cache\*.log` のような固定ドライブ パスを使用したり、プログラム固有のルールで完全なパスになる[展開可能な変数](ExpandableVariables.md)に依存したりしないでください。

一致する既存の通常のファイルを移行する必要がある場合、Sandboxie はホスト ファイルを開いてそのファイル情報を取得し、対応するサンドボックス ファイルを作成し、内容の長さをゼロに設定します。ホスト ファイルは変更されません。その後、サンドボックス化されたプログラムは空のサンドボックス コピーを操作し、それに新しい内容を書き込むことができます。

このルールは [CopyLimitKb](CopyLimitKb.md) より前に選択されるため、ホスト ファイルのサイズに関係なく空のコピーを作成します。[CopyLimitSilent](CopyLimitSilent.md) はこのルールに影響しません。[NotifyNoCopy](NotifyNoCopy.md) が有効な場合、移行の試行は内容が破棄されたことを報告するメッセージ SBIE2113 を生成します。

_CopyEmpty_ が存在しないか、一致するエントリがない場合、Sandboxie は別の一致する移行ルールまたは通常のサイズベースの決定を使用します。ルールが重複する場合、[DontCopy](DontCopy.md) は [CopyAlways](CopyAlways.md) よりも優先され、_CopyAlways_ は _CopyEmpty_ よりも優先されます。[CopyNewer](CopyNewer.md) は既存のサンドボックス コピーに対して別個に評価されます。初期の空のコピーがどのように選択されるかは変更しません。

次の制限に注意してください:

- _CopyEmpty_ は、既存の通常のホスト ファイルの内容が通常移行される場合に参照されます。これには、[CopyNewer](CopyNewer.md) の更新中に試行される移行も含まれます。
- それ自体が既存のサンドボックス コピーの更新をトリガーするものではありません。_CopyNewer_ が更新を開始する場合、一致する _CopyEmpty_ ルールが空の置き換えを選択できます。
- ディレクトリ、サンドボックス内でのみ作成されたファイル、または Sandboxie がホストの内容をコピーしない上書き/削除/作成操作には影響しません。
- Sandboxie は依然としてホスト オブジェクトを開き、そのファイル情報を照会できる必要があります。その段階での失敗は、空のコピーを生成する代わりに移行を失敗させることがあります。

コピー ルールは、SandMan の Sandbox Options > General Options > File Migration で管理できます。このルールの種類には **Copy empty** を選択します。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [CopyAlways](CopyAlways.md)、[DontCopy](DontCopy.md)、[CopyNewer](CopyNewer.md)、[NotifyNoCopy](NotifyNoCopy.md)、[CopyLimitKb](CopyLimitKb.md)。[File Migration Settings](FileMigrationSettings.md) も参照してください。
