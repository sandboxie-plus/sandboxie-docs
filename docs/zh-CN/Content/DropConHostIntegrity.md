# 降低 ConHost 完整性

_DropConHostIntegrity_ 是一个控制台兼容性设置。它让 Sandboxie 尝试降低通过 Sandboxie 控制台代理创建的控制台所关联的外部 `conhost.exe` 的完整性级别。

```ini
[DefaultBox]
DropConHostIntegrity=y
```

默认值为 `n`。这是一个盒级布尔设置；常规的模板与 `GlobalSettings` 继承可以贡献它的生效值。

## 运行时行为

使用 Sandboxie 的控制台代理时，由 SbieSvc 的辅助进程创建控制台，Windows 会在沙盒之外启动关联的 `conhost.exe`。随后沙盒进程附加到该控制台，辅助进程退出。

启用 `DropConHostIntegrity=y` 时，辅助进程会识别与之关联的控制台宿主进程，打开该进程的令牌，并尝试把其强制完整性级别设为 **不受信任**。这改变的是该代理所创建控制台宿主的完整性标签；它不会把 `conhost.exe` 纳入沙盒，也不会改变沙盒应用程序的令牌。

该调整是尽力而为的。如果 Sandboxie 无法识别控制台宿主、无法打开该进程或其令牌，或无法应用新的完整性标签，控制台创建仍会继续，不会把该调整失败当作致命错误。

## 为什么存在

该设置是为那些在更高完整性级别的控制台宿主上附加不受信任的沙盒进程后，无法执行某些控制台缓冲区操作的控制台应用程序引入的。报告的症状包括 PowerShell 报错与 Node.js 交互式控制台失败。把关联的控制台宿主降为不受信任解决了所报告的级别不匹配问题，但并非所有控制台故障都源于此，且不同 Windows 版本上的行为可能不同。原始报告见 [Sandboxie issue #678](https://github.com/sandboxie-plus/Sandboxie/issues/678)。

## 范围与限制

`DropConHostIntegrity` 不是针对每个 `conhost.exe` 进程的全局策略。它只在 Sandboxie 控制台辅助进程成功创建代理控制台时被查询，且只针对该辅助进程所创建控制台关联的那个控制台宿主。

该设置不控制每一种终端架构。特别是其实现并未为 Windows Terminal、伪控制台（ConPTY）或在 Sandboxie 代理路径之外创建的控制台宿主建立通用覆盖。

## 与 NoSandboxieConsole 的关系

[无 Sandboxie 控制台](NoSandboxieConsole.md) 会绕过 Sandboxie 自定义的控制台重定向与代理路径。`DropConHostIntegrity` 在该代理路径内部生效，因此不应指望它能修改通过 `NoSandboxieConsole` 路径创建的控制台宿主。

## SandMan 中的配置

在 SandMan 中打开：

**沙盒选项 > 安全选项 > 高级安全**

复选框标签为 **降低 ConHost.exe 的进程完整级**。勾选会写入 `DropConHostIntegrity=y`；取消勾选会移除该沙盒的显式值。此后该设置回退到任何继承来的模板或 `[GlobalSettings]` 值，若都没有配置则回退到默认值 `n`。

## 应用更改

该值在新建代理控制台时被查询。更改它不会为既有的控制台宿主重新打标签。请重启受影响的沙盒控制台应用程序，以便用新设置创建可用的控制台。通常不需要重启 SandMan、服务或驱动。

## 版本历史

`DropConHostIntegrity` 在 Sandboxie Plus 0.7.3 / Classic 5.49.5 引入。专门的 SandMan 复选框在 Sandboxie Plus 1.14.7 / Classic 5.69.7 添加。

## 相关页面

- [无 Sandboxie 控制台](NoSandboxieConsole.md)
- [Sandboxie Ini](SandboxieIni.md)
