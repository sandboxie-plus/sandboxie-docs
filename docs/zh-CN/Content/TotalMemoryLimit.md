# 总内存限制 {#total-memory-limit}

_TotalMemoryLimit_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus v1.14.0 起可用。它限制该沙盒和会话对应的 Sandboxie Windows 作业对象所关联进程的已提交虚拟内存总量。

该值以字节为单位指定，并直接作为作业对象的已提交内存总限制应用。它不是物理内存或工作集限制。

语法：

```ini
TotalMemoryLimit=<total_limit_in_byte>
```

示例：

```ini
[DefaultBox]
TotalMemoryLimit=1073741824
```

在此示例中，已提交内存总限制为 1073741824 字节，即 1 GiB。

当一次新增的内存提交会超出该限制时，Windows 会使该分配或提交失败。达到限制本身不会自动终止所有沙盒化进程。接下来会发生什么取决于受影响的应用程序如何处理该分配失败。

如果同时配置了 [进程内存限制](ProcessMemoryLimit.md)，每个进程除受此总限制约束外，仍受每进程限制约束。如果未配置 _TotalMemoryLimit_，则不应用此特定的作业对象内存限制。

> [!IMPORTANT]
> 这些限制仅适用于被分配到 Sandboxie 作业对象的进程。当适用 `NoAddProcessToJob=y`、`NoSecurityIsolation=y` 或 `OpenWinClass=*` 时，受影响进程会跳过作业对象分配。`AllowBoxedJobs=y` 不会禁用这些限制。

这些限制在 Sandboxie 创建作业对象时配置。如果该沙盒和会话已有一个活动中的作业对象，其中有正在运行的关联进程，则更改可能要到该作业对象不再使用并创建新作业对象后才会生效。

相关 [Sandboxie Ini](SandboxieIni.md) 设置：[进程内存限制](ProcessMemoryLimit.md)、[进程数限制](ProcessNumberLimit.md)
