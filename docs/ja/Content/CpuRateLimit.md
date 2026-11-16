# CPU Rate Limit

_CpuRateLimit_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 1.17.5 以降で利用できます。Sandboxie Job オブジェクトに対して 1 から 100 までの整数の CPU レート パーセンテージを構成します。

## 使用法

```ini
[DefaultBox]
CpuRateLimit=25
```

## 構文

```ini
CpuRateLimit=1-100
```

この例では、Sandboxie は Job オブジェクトに対して 25% のハード CPU レート上限を構成します。内部的には、Windows がレートをパーセンテージに 100 を掛けたものとして表すため、値は `CpuRate = 2500` として Windows に渡されます。ユーザーはパーセンテージを直接構成する必要があります。`25` は 25% を意味し、`100` は 100% を意味します。

## 集合的な CPU 制限

この制限は、同じ Sandboxie Job オブジェクトに割り当てられたすべてのプロセスに集合的に適用されます。複数のサンドボックス化されたプロセスが同時に CPU を消費する場合、それらは 1 つの CPU レート バジェットを共有します。各プロセスが個別に 25% のクォータを受け取るわけではありません。

Sandboxie Job に CPU レート制御を持つ親 Job がない場合、このパーセンテージはシステム全体のプロセッサ サイクル容量の一部を表します。CPU レート制御も持つ親の下にネストされている場合、Windows はそのレートを直接の親の割り当てを基準に計算します。

Sandboxie は Windows の `JOB_OBJECT_CPU_RATE_CONTROL_HARD_CAP` ポリシーを有効にします。Job がスケジューリング間隔に対して許可されたプロセッサ サイクルを消費すると、Windows は次の間隔までそのスレッドのスケジューリングを停止します。これはプロセスを終了させるのではなくスロットルし、プロセッサ アフィニティ制限ではありません。基になる Windows メカニズムは Windows 8 および Windows Server 2012 以降で利用できます。

## Job オブジェクトの要件

_CpuRateLimit_ は、Sandboxie の Job オブジェクトに割り当てられたプロセスのみに影響します。Sandboxie は、`NoAddProcessToJob=y`、[`NoSecurityIsolation=y`](NoSecurityIsolation.md)、または [`OpenWinClass=*`](OpenWinClass.md) が構成されている場合、影響を受けるプロセスのその割り当てをスキップします。`AllowBoxedJobs=y` 自体は Sandboxie の CPU レート制限を無効にしません。

このレートは、Sandboxie がその Job オブジェクトを作成するときに構成されます。その Job にまだアクティブなプロセスがある場合、Sandboxie はそれを再利用するため、現在の Job が使用されなくなり新しい Job が作成されるまで、構成の変更が有効にならないことがあります。

SandMan では、この設定は **Sandbox Options > Security Options > Job Object** の **Total CPU Rate Limit (%)** で利用できます。このフィールドは 1 から 100 までの値を受け入れ、設定が構成されていない場合は `unlimited` を表示します。

_CpuRateLimit_ は、Job オブジェクトが消費できる集約プロセッサ スケジューリング容量を制御します。サンドボックス化されたプロセスがどこで実行されるかを制限するには、[CPU Affinity Mask](CpuAffinityMask.md) を参照してください。2 つの設定は一緒に使用できます。パーセンテージは、アフィニティ マスクによって選択されたプロセッサのみから再計算されるわけではありません。
