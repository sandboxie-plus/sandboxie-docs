# Total Memory Limit

_TotalMemoryLimit_ は Sandboxie Plus v1.14.0 以降で使用可能な [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。サンドボックスおよびセッション用の Sandboxie の Windows Job オブジェクトに関連付けられたプロセスの合計コミット済み仮想メモリを制限します。

値はバイト単位で指定され、Job オブジェクトの合計コミット済みメモリ制限として直接適用されます。物理メモリまたはワーキング セットの制限ではありません。

構文:

```ini
TotalMemoryLimit=<total_limit_in_byte>
```

例:

```ini
[DefaultBox]
TotalMemoryLimit=1073741824
```

この例では、合計コミット済みメモリ制限は 1073741824 バイト、つまり 1 GiB です。

追加のメモリ コミットが制限を超える場合、Windows はその割り当てまたはコミットを失敗させます。制限に達しても、それ自体ですべてのサンドボックス化されたプロセスが自動的に終了するわけではありません。次に何が起こるかは、影響を受けるアプリケーションが割り当て失敗をどのように処理するかによって異なります。

[ProcessMemoryLimit](ProcessMemoryLimit.md) も構成されている場合、各プロセスはこの合計制限と同様にプロセスごとの制限の対象のままです。_TotalMemoryLimit_ が構成されていない場合、この特定の Job オブジェクト メモリ制限は適用されません。

> [!IMPORTANT]
> これらの制限は、Sandboxie の Job オブジェクトに割り当てられたプロセスにのみ適用されます。`NoAddProcessToJob=y`、`NoSecurityIsolation=y`、または `OpenWinClass=*` が適用される場合、影響を受けるプロセスでは Job オブジェクトの割り当てがスキップされます。`AllowBoxedJobs=y` はこれらの制限を無効にしません。

制限は Sandboxie が Job オブジェクトを作成するときに構成されます。サンドボックスとセッションに既に実行中の関連プロセスを持つアクティブな Job オブジェクトがある場合、その Job オブジェクトが使用されなくなり、新しいものが作成されるまで変更が有効にならないことがあります。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [ProcessMemoryLimit](ProcessMemoryLimit.md)、[ProcessNumberLimit](ProcessNumberLimit.md)
