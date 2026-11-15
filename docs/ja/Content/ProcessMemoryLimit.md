# Process Memory Limit

_ProcessMemoryLimit_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus v1.14.0 以降で使用できます。Sandboxie の Windows Job オブジェクトに関連付けられた各プロセスのコミット済み仮想メモリを制限します。

値はバイト単位で指定され、関連付けられたすべてのプロセスに個別に適用されます。物理メモリまたはワーキング セットの制限ではありません。

構文:

```ini
ProcessMemoryLimit=<per_process_limit_in_byte>
```

例:

```ini
[DefaultBox]
ProcessMemoryLimit=536870912
```

この例では、関連付けられた各プロセスのコミット済みメモリ制限は 536870912 バイト、つまり 512 MiB です。

追加のメモリ コミットがプロセスごとの制限を超える場合、Windows はその割り当てまたはコミットを失敗させます。Job オブジェクトのメモリ制限に達したという理由だけでプロセスが自動的に終了されることはありません。次に何が起こるかは、アプリケーションが割り当て失敗をどのように処理するかに依存します。

この設定は [TotalMemoryLimit](TotalMemoryLimit.md) と組み合わせて使用できます。両方が構成されている場合、各プロセスはその個別の制限の対象となり、関連付けられたすべてのプロセスは合計制限の対象にもなります。_ProcessMemoryLimit_ が構成されていない場合、この特定の Job オブジェクト メモリ制限は適用されません。

> [!IMPORTANT]
> これらの制限は、Sandboxie の Job オブジェクトに割り当てられたプロセスにのみ適用されます。`NoAddProcessToJob=y`、`NoSecurityIsolation=y`、または `OpenWinClass=*` が適用される場合、影響を受けるプロセスでは Job オブジェクトの割り当てがスキップされます。`AllowBoxedJobs=y` はこれらの制限を無効にしません。

制限は、Sandboxie が Job オブジェクトを作成するときに構成されます。サンドボックスとセッションに既に実行中の関連プロセスを持つアクティブな Job オブジェクトがある場合、変更はその Job オブジェクトが使用されなくなり、新しいものが作成されるまで有効にならないことがあります。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [TotalMemoryLimit](TotalMemoryLimit.md)、[ProcessNumberLimit](ProcessNumberLimit.md)
