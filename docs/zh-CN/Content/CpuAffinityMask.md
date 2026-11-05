# CPU 亲和性掩码

_CpuAffinityMask_ 是 [Sandboxie Ini](SandboxieIni.md) 中的沙盒设置，自 Sandboxie Plus 1.13.5 起提供。它通过在进程初始化时应用处理器亲和性掩码，把沙盒进程限制在选定的逻辑处理器上运行。

## 用法

```ini
[DefaultBox]
CpuAffinityMask=0x00000003
```

该值必须是十六进制且以 `0x` 或 `0X` 开头。每个置位的比特允许对应的逻辑处理器。上例中第 0、1 位被置位，因此沙盒进程只能在逻辑处理器 0 与 1 上运行。逻辑处理器与物理 CPU 核心不一定一一对应。

## 当前限制

当前 Sandboxie 实现只支持逻辑处理器索引 0 到 31。逻辑处理器 32 及以上的位无法通过该设置配置，即使在 64 位 Windows 上也是如此。

Sandboxie 只暴露一个亲和性掩码，没有处理器组选择器、`GROUP_AFFINITY` 设置或 CPU Sets 设置。因此在采用多个 Windows 处理器组的系统上，该掩码受 Windows 单组亲和性语义约束，无法显式选择其他组中的处理器。

如果 Windows 拒绝所请求的亲和性掩码，Sandboxie 目前不会因该失败而终止进程。若未配置 _CpuAffinityMask_，Sandboxie 不会施加该设置的处理器亲和性限制。

_CpuAffinityMask_ 控制沙盒进程可以在哪里执行。若要限制它们的总体处理器调度能力，参见 [CPU 速率限制](CpuRateLimit.md)。两个设置可以一起使用。
