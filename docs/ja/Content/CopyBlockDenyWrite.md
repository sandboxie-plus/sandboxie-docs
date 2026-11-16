# Copy Block Deny Write

_CopyBlockDenyWrite_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 0.6.5 以降で利用できます。Sandboxie がホスト ファイルをコピーしないと決定したときに、ファイル移行を必要とするオープンがどうなるかを制御します。

使用法:

```ini
[DefaultBox]
CopyBlockDenyWrite=y
CopyBlockDenyWrite=viewer.exe,n
```

構文は `CopyBlockDenyWrite=[program,]y|n` です。省略可能な [Program Name Prefix](ProgramNamePrefix.md) により、値はその実行可能ファイルにのみ適用されます。複数のエントリで異なるプログラムの値を提供できますが、これはパス リストではなくはい/いいえの設定です。

初期移行では、`y` に設定されている場合、移行の決定が **コピーしない** であるときに、サンドボックス コピーを必要とするオープンがアクセス拒否で失敗します。存在しないか `n` に設定されている場合、Sandboxie は代わりに要求から書き込みおよび削除の権限を削除し、ホスト ファイルに対してオープンを再試行します。したがって、読み取り可能な要求は読み取り専用として成功することがあります。それらの権限を削除した後に満たすことができない要求は、依然として失敗することがあります。

**コピーしない** 決定は、一致する [DontCopy](DontCopy.md) ルール、または [CopyLimitKb](CopyLimitKb.md) によって制御される通常のサイズ決定から生じることがあります。これには、大きなファイルのプロンプトが利用できないか拒否された場合も含まれます。この設定自体はファイルを選択したり、成功する移行を妨げたりするものではありません。

一致する [CopyAlways](CopyAlways.md) および [CopyEmpty](CopyEmpty.md) ルールは代わりにコピー モードを選択するため、_CopyBlockDenyWrite_ はそれらの結果に対して作用しません。[CopyNewer](CopyNewer.md) が更新を開始する場合、この設定は更新移行の結果に影響することがあります。更新が失敗しても、既に存在するサンドボックス コピーの後続のオープンが必ずしも拒否されるわけではありません。

[CopyLimitSilent](CopyLimitSilent.md) はサイズベースの拒否に対するメッセージ SBIE2102 のみを制御し、移行の決定を変更しません。明示的な _DontCopy_ ルールの場合、[NotifyNoCopy](NotifyNoCopy.md) を有効にすると、この設定が `y` のときは SBIE2114 が、`n` のときは SBIE2115 が生成されます。これらのメッセージは、更新試行後に既存のコピーを開いた最終結果ではなく、選択されたモードを説明します。

SandMan では、Sandbox Options > General Options > File Migration を開きます。チェックボックスは逆の方向で表現されています: **When a file cannot be migrated, open it in read-only mode instead**。そのチェックボックスをオフにすると `CopyBlockDenyWrite=y` が有効になります。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [DontCopy](DontCopy.md)、[CopyAlways](CopyAlways.md)、[CopyEmpty](CopyEmpty.md)、[CopyLimitKb](CopyLimitKb.md)、[CopyLimitSilent](CopyLimitSilent.md)、[NotifyNoCopy](NotifyNoCopy.md)。[File Migration Settings](FileMigrationSettings.md) も参照してください。
