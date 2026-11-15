# Don't Copy

_DontCopy_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 0.6.5 以降で利用できます。その内容をサンドボックスに移行してはならないホスト ファイルのパス パターンを指定します。

使用法:

`DontCopy=[program,]pattern`

```ini
[DefaultBox]
DontCopy=*.iso
DontCopy=media-player.exe,*\Media\*.mkv
```

各 _DontCopy_ エントリは 1 つのルールであり、この設定は繰り返すことができます。コンマの前の省略可能なプレフィックスはルールをそのプログラムに制限します。[Program Name Prefix](ProgramNamePrefix.md) を参照してください。パスは [OpenFilePath](OpenFilePath.md) と同じパターン形式を使用します。照合は大文字と小文字を区別せず、ホスト (真の) ファイル パスに対して実行されます。`*` はパス区切り文字を含む任意の文字シーケンスに一致し、`?` は 1 文字に一致します。

プログラム プレフィックスを使用する場合、現在の設定メタデータでは、パスのドライブまたはデバイス部分をワイルドカードで表す必要があります (例: `*\Media\*.mkv`)。`D:\Media\*.mkv` のような固定ドライブ パスを使用したり、プログラム固有のルールで完全なパスになる[展開可能な変数](ExpandableVariables.md)に依存したりしないでください。

ホスト ファイルへの通常の読み取り専用アクセスは移行を必要とせず、ホスト ファイルを引き続き使用します。このルールは、Sandboxie が通常、既存のファイルをサンドボックス内で変更できるように移行する操作をサンドボックス化されたプログラムが要求する場合に重要になります。初期移行中に一致するファイルに対して、Sandboxie はその内容コピーを作成しません:

- [CopyBlockDenyWrite](CopyBlockDenyWrite.md) が存在しないか `n` に設定されている場合、Sandboxie は要求から書き込みおよび削除の権限を削除し、ホスト ファイルに対してオープンを再試行します。したがって、読み取り可能な要求は読み取り専用として成功することがあります。書き込み専用の要求、互換性のない作成 disposition、またはホストのアクセス許可は、依然としてオープンを失敗させることがあります。
- プログラムに対して _CopyBlockDenyWrite=y_ の場合、移行依存のオープンは代わりにアクセス拒否で失敗します。

_DontCopy_ は [OpenFilePath](OpenFilePath.md) のような直接アクセス許可ではありません。サンドボックス化されたプログラムがホスト ファイルに書き込むことを決して許可しません。既存のサンドボックス コピーは通常、初期移行をバイパスしますが、[CopyNewer](CopyNewer.md) が更新を開始する場合、更新移行は _DontCopy_ を評価できます。一致するルールは、既存のサンドボックス コピーが利用可能なままその更新を防ぐことができます。そのコピーを削除または置き換えるものではありません。

_DontCopy_ が存在しないか、一致するエントリがない場合、移行を抑制しません。Sandboxie は別の一致する移行ルールまたは通常のサイズベースの決定を使用します。

_DontCopy_ は [CopyLimitKb](CopyLimitKb.md) より前に評価されるため、ファイル サイズと [CopyLimitSilent](CopyLimitSilent.md) は選択されたルールを変更しません。また、一致する [CopyAlways](CopyAlways.md) および [CopyEmpty](CopyEmpty.md) エントリよりも優先されます。[CopyNewer](CopyNewer.md) は既に存在するサンドボックス コピーに関するものであり、この初期移行の決定の一部ではありません。

このルールは、内容がそうでなければ移行される既存の通常のホスト ファイルに対してのみ参照されることに注意してください。ディレクトリ、新しいファイル、または Sandboxie がホストの内容をコピーする必要のない作成/上書き/削除操作を制御するものではありません。

[NotifyNoCopy](NotifyNoCopy.md) が有効な場合、一致する移行の試行は、アクセス削減モードに対して SBIE2115 を、書き込み拒否モードに対して SBIE2114 を生成します。更新中、これらのメッセージは移行の決定を説明するものであり、必ずしも既存のサンドボックス コピーを開いた結果ではありません。

コピー ルールは、SandMan の Sandbox Options > General Options > File Migration で管理できます。このルールの種類には **Don't copy** を選択します。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [CopyAlways](CopyAlways.md)、[CopyEmpty](CopyEmpty.md)、[CopyNewer](CopyNewer.md)、[CopyBlockDenyWrite](CopyBlockDenyWrite.md)、[NotifyNoCopy](NotifyNoCopy.md)。[File Migration Settings](FileMigrationSettings.md) も参照してください。
