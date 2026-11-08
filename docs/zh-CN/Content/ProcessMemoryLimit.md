# 进程内存限制 {#process-memory-limit}

_ProcessMemoryLimit_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus v1.14.0 起可用。它限制与 Sandboxie 的 Windows 作业对象关联的每个进程的已提交虚拟内存。

该值以字节为单位指定，并独立应用于每个关联进程。它不是物理内存或工作集限制。

语法：

```ini
ProcessMemoryLimit=<per_process_limit_in_byte>
```

示例：

```ini
[DefaultBox]
ProcessMemoryLimit=536870912
```

在此示例中，每个关联进程的已提交内存限制为 536870912 字节，即 512 MiB。

当一次新增的内存提交会超出每进程限制时，Windows 会使该分配或提交失败。进程不会仅因达到作业对象的内存限制而被自动终止。接下来会发生什么取决于应用程序如何处理该分配失败。

此设置可以与 [总内存限制](TotalMemoryLimit.md) 一起使用。两者同时配置时，每个进程受其单独限制约束，所有关联进程同时也受总限制约束。如果未配置 _ProcessMemoryLimit_，则不应用此特定的作业对象内存限制。

> [!IMPORTANT]
> 这些限制仅适用于被分配到 Sandboxie 作业对象的进程。当适用 `NoAddProcessToJob=y`、`NoSecurityIsolation=y` 或 `OpenWinClass=*` 时，受影响进程会跳过作业对象分配。`AllowBoxedJobs=y` 不会禁用这些限制。

这些限制在 Sandboxie 创建作业对象时配置。如果该沙盒和会话已有一个活动中的作业对象，其中有正在运行的关联进程，则更改可能要到该作业对象不再使用并创建新作业对象后才会生效。

相关 [Sandboxie Ini](SandboxieIni.md) 设置：[总内存限制](TotalMemoryLimit.md)、[进程数限制](ProcessNumberLimit.md)
