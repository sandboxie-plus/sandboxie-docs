# Copy Always

_CopyAlways_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 0.6.5 以降で利用できます。サンドボックス化されたプログラムがサンドボックス コピーを必要とするときに、その内容とともに移行する必要があるホスト ファイルのパス パターンを指定します。

使用法:

`CopyAlways=[program,]pattern`

```ini
[DefaultBox]
CopyAlways=C:\Data\Reference\*.db
CopyAlways=reporter.exe,*\Reports\*.csv
```

各 _CopyAlways_ エントリは 1 つのルールであり、この設定は繰り返すことができます。コンマの前の省略可能なプレフィックスはルールをそのプログラムに制限します。[Program Name Prefix](ProgramNamePrefix.md) を参照してください。パスは [OpenFilePath](OpenFilePath.md) と同じパターン形式を使用します。照合は大文字と小文字を区別せず、ホスト (真の) ファイル パスに対して実行されます。`*` はパス区切り文字を含む任意の文字シーケンスに一致し、`?` は 1 文字に一致します。

プログラム プレフィックスを使用する場合、現在の設定メタデータでは、パスのドライブまたはデバイス部分をワイルドカードで表す必要があります (例: `*\Reports\*.csv`)。`C:\Reports\*.csv` のような固定ドライブ パスを使用したり、プログラム固有のルールで完全なパスになる[展開可能な変数](ExpandableVariables.md)に依存したりしないでください。

通常、Sandboxie は、サンドボックス化されたプログラムがサンドボックス コピーを必要とする操作を要求した場合にのみ、既存のホスト ファイルを移行します。ファイルが _CopyAlways_ に一致する場合、Sandboxie は [CopyLimitKb](CopyLimitKb.md) を検討する前に完全な内容の移行を選択します。したがって、構成されたサイズしきい値と大きなファイルのプロンプトは、その一致する移行ではバイパスされます。[CopyLimitSilent](CopyLimitSilent.md) はそれに影響しません。

_CopyAlways_ が存在しないか、一致するエントリがない場合、Sandboxie は別の一致する移行ルールまたは通常のサイズベースの決定を使用します。ルールが重複する場合、[DontCopy](DontCopy.md) は _CopyAlways_ よりも優先され、_CopyAlways_ は [CopyEmpty](CopyEmpty.md) よりも優先されます。[CopyNewer](CopyNewer.md) は別個です。これは既存のサンドボックス コピーの更新をトリガーします。_CopyAlways_ 自体はその更新をトリガーしませんが、一致するルールは、通常のサイズ制限とプロンプトの前に、その内部で完全な内容の移行を選択できます。

次の制限に注意してください:

- このルールは、内容がそうでなければ移行される既存の通常のホスト ファイルに対してのみ参照されます。それ自体が既存のサンドボックス コピーの更新をトリガーするものではなく、ホストの内容をコピーしない新しいファイル、ディレクトリ、または作成/上書き操作を制御するものでもありません。
- このルールは移行サイズの決定を上書きしますが、アクセスできないホストの内容を読み取れることを保証することはできません。このルールはホスト ファイルのアクセス制限をバイパスしません。Sandboxie が移行に必要なソース ファイルにアクセスできない場合、移行は失敗するか、その内容をコピーせずに進むことがあります。
- ホスト ファイルは変更されません。後続の書き込みはサンドボックス コピーに対して行われます。

コピー ルールは、SandMan の Sandbox Options > General Options > File Migration で管理できます。このルールの種類には **Always copy** を選択します。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [DontCopy](DontCopy.md)、[CopyEmpty](CopyEmpty.md)、[CopyNewer](CopyNewer.md)、[CopyLimitKb](CopyLimitKb.md)、[CopyLimitSilent](CopyLimitSilent.md)。[File Migration Settings](FileMigrationSettings.md) も参照してください。
