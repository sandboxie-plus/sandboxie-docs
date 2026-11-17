# CPU 速率限制 {#cpu-rate-limit}

_CpuRateLimit_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus 1.17.5 起可用。它为 Sandboxie 作业对象配置一个 1 到 100 的整数 CPU 速率百分比。

## 用法 {#usage}

```ini
[DefaultBox]
CpuRateLimit=25
```

## 语法 {#syntax}

```ini
CpuRateLimit=1-100
```

在此示例中，Sandboxie 为作业对象配置 25% 的强制 CPU 速率上限。在内部，该值会以 `CpuRate = 2500` 的形式传给 Windows，因为 Windows 用百分比乘以 100 表示速率。用户应直接配置百分比；`25` 表示 25%，`100` 表示 100%。

## 集体 CPU 限制 {#collective-cpu-limit}

该限制集体适用于分配到同一个 Sandboxie 作业对象的所有进程。如果多个沙盒化进程同时占用 CPU，它们共享一份 CPU 速率预算；每个进程并不会各自获得 25% 的独立配额。

当 Sandboxie 作业没有带 CPU 速率控制的父作业时，该百分比表示整个系统处理器周期容量的一部分。如果它嵌套在同样具有 CPU 速率控制的父作业之下，Windows 会相对于直接父作业的分配量来计算其速率。

Sandboxie 启用 Windows 的 `JOB_OBJECT_CPU_RATE_CONTROL_HARD_CAP` 策略。当作业在一个调度间隔内用完其允许的处理器周期后，Windows 会停止调度其线程，直到下一个间隔。这样会限制这些进程的速度，而不是终止它们，并且它不属于处理器亲和性限制。底层的 Windows 机制从 Windows 8 与 Windows Server 2012 起可用。

## 作业对象要求 {#job-object-requirements}

_CpuRateLimit_ 只影响分配到 Sandboxie 作业对象的进程。当配置了 `NoAddProcessToJob=y`、[`NoSecurityIsolation=y`](NoSecurityIsolation.md) 或 [`OpenWinClass=*`](OpenWinClass.md) 时，Sandboxie 会为受影响的进程跳过该分配。`AllowBoxedJobs=y` 本身不会禁用 Sandboxie 的 CPU 速率限制。

该速率在 Sandboxie 创建其作业对象时配置。如果该作业仍有活动进程，Sandboxie 会复用它，因此配置更改可能要等到当前作业不再使用并创建新作业之后才会生效。

在 SandMan 中，该设置位于 **沙盒选项 > 安全选项 > 作业对象** 之下，名称为 **总 CPU 使用率限制 (%)**。该字段接受 1 到 100 的数值，未配置该设置时显示 `unlimited`。

_CpuRateLimit_ 控制作业对象可以占用多少总处理器调度能力。若要限制沙盒化进程可以在何处执行，参见 [CPU 亲和性掩码](CpuAffinityMask.md)。两项设置可以一起使用；该百分比不会仅根据亲和性掩码所选择的处理器重新计算。
