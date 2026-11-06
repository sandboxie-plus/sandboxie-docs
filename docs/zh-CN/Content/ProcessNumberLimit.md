# 进程数限制 {#process-number-limit}

_ProcessNumberLimit_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus v1.14.0 起可用。它使用 Windows 作业对象来限制该沙盒和会话对应的作业对象所关联的活动进程数。

语法：

```ini
ProcessNumberLimit=<process_count>
```

示例：

```ini
[DefaultBox]
ProcessNumberLimit=50
```

在此示例中，最多可有 50 个关联进程同时处于活动状态。将要超出限制的进程无法继续执行正常的沙盒化启动。已经关联的进程会继续运行。

_ProcessNumberLimit_ 使用 Windows 作业对象的活动进程数限制。达到限制时，Sandboxie 不会提供专门的通知。如果未配置 _ProcessNumberLimit_，则不应用此特定的作业对象进程数限制。

> [!IMPORTANT]
> 这些限制仅适用于被分配到 Sandboxie 作业对象的进程。当适用 `NoAddProcessToJob=y`、`NoSecurityIsolation=y` 或 `OpenWinClass=*` 时，受影响进程会跳过作业对象分配。`AllowBoxedJobs=y` 不会禁用这些限制。

这些限制在 Sandboxie 创建作业对象时配置。如果该沙盒和会话已有一个活动中的作业对象，其中有正在运行的关联进程，则更改可能要到该作业对象不再使用并创建新作业对象后才会生效。

_ProcessNumberLimit_ 与 [进程数量限制](ProcessLimit.md) 是两项独立的设置。_ProcessLimit_ 由 Sandboxie 的进程初始化逻辑强制执行，而 _ProcessNumberLimit_ 使用 Windows 作业对象的活动进程数限制。

相关 [Sandboxie Ini](SandboxieIni.md) 设置：[总内存限制](TotalMemoryLimit.md)、[进程内存限制](ProcessMemoryLimit.md)
