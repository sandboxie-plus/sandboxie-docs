# Process Number Limit

_ProcessNumberLimit_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus v1.14.0 以降で使用できます。Windows Job オブジェクトを使用して、サンドボックスとセッションの Job オブジェクトに関連付けられたアクティブ プロセスの数を制限します。

構文:

```ini
ProcessNumberLimit=<process_count>
```

例:

```ini
[DefaultBox]
ProcessNumberLimit=50
```

この例では、最大 50 個の関連付けられたプロセスが同時にアクティブになることができます。制限を超えるプロセスは通常のサンドボックス化された起動を続行できません。既に関連付けられているプロセスは実行されたままです。

_ProcessNumberLimit_ は Windows Job オブジェクトのアクティブ プロセス制限を使用します。制限に達したときに専用の Sandboxie 通知を提供しません。_ProcessNumberLimit_ が構成されていない場合、この特定の Job オブジェクト プロセス数制限は適用されません。

> [!IMPORTANT]
> これらの制限は、Sandboxie の Job オブジェクトに割り当てられたプロセスにのみ適用されます。`NoAddProcessToJob=y`、`NoSecurityIsolation=y`、または `OpenWinClass=*` が適用される場合、影響を受けるプロセスでは Job オブジェクトの割り当てがスキップされます。`AllowBoxedJobs=y` はこれらの制限を無効にしません。

制限は、Sandboxie が Job オブジェクトを作成するときに構成されます。サンドボックスとセッションに既に実行中の関連プロセスを持つアクティブな Job オブジェクトがある場合、変更はその Job オブジェクトが使用されなくなり、新しいものが作成されるまで有効にならないことがあります。

_ProcessNumberLimit_ は [ProcessLimit](ProcessLimit.md) とは別個です。_ProcessLimit_ は Sandboxie のプロセス初期化ロジックによって強制されますが、_ProcessNumberLimit_ は Windows Job オブジェクトのアクティブ プロセス制限を使用します。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [TotalMemoryLimit](TotalMemoryLimit.md)、[ProcessMemoryLimit](ProcessMemoryLimit.md)
