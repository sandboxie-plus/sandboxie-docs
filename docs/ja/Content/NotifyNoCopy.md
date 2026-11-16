# Notify No Copy

_NotifyNoCopy_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 1.7.0 以降で使用できます。ホスト ファイルの内容の一部または全部を意図的に省略する移行ルールに対するメッセージを有効にします。

使用法:

`NotifyNoCopy=y|n`

```ini
[DefaultBox]
NotifyNoCopy=y
```

これは [Yes Or No Setting](YesOrNoSettings.md) であり、パス リストではありません。構成されているサンドボックス (`[GlobalSettings]` から継承するサンドボックス) に適用され、プログラム名のプレフィックスを受け入れません。設定が存在しないか `n` に設定されている場合、これらの通知は無効になります。

有効にすると、Sandboxie は明示的なファイル移行ルールが一致した後にメッセージを発行します:

- [CopyEmpty](CopyEmpty.md) がホスト ファイルの内容なしのコピーを選択した場合の SBIE2113。
- [DontCopy](DontCopy.md) が [CopyBlockDenyWrite](CopyBlockDenyWrite.md) を有効にして非コピーを選択した場合の SBIE2114 (初期移行の deny-write モード)。
- _DontCopy_ が deny-write を無効にして非コピーを選択した場合の SBIE2115 (初期移行の低減されたアクセスの再試行モード)。

メッセージにはファイル名、サンドボックス名、およびホスト ファイル サイズが含まれます。サンドボックス化されたプログラムがファイルを読み取ったときだけでなく、移行コードが一致する _CopyEmpty_ または _DontCopy_ ルールを選択したときに生成されます。

[CopyNewer](CopyNewer.md) 専用の _NotifyNoCopy_ メッセージはありません。ただし、その更新移行は _CopyEmpty_ または _DontCopy_ を選択し、対応する通知を発行することがあります。これらのメッセージは選択された移行モードを表すものであり、コピーの完了または最終的な開く結果の証明ではありません。更新中、非コピー結果は、その開くことを拒否したりホストに対して再試行したりするのではなく、既存のサンドボックス コピーを利用可能なままにすることがあります。

_NotifyNoCopy_ は、成功した [CopyAlways](CopyAlways.md) の移行、そのような更新なしでの既存のサンドボックス コピーへの通常のアクセス、または一般的な低レベルのコピー失敗を報告しません。また、[CopyLimitKb](CopyLimitKb.md) のサイズ決定のみによって拒否されたファイルも報告しません。サイズ制限メッセージ SBIE2102 は [CopyLimitSilent](CopyLimitSilent.md) によって別個に制御されます。

SandMan では、Sandbox Options > General Options > File Migration を開き、**Issue message 2113/2114/2115 when a file is not fully migrated** を選択します。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [CopyEmpty](CopyEmpty.md)、[DontCopy](DontCopy.md)、[CopyBlockDenyWrite](CopyBlockDenyWrite.md)、[CopyLimitKb](CopyLimitKb.md)、[CopyLimitSilent](CopyLimitSilent.md)。[File Migration Settings](FileMigrationSettings.md) も参照してください。
