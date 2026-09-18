# 阻止 Win Hooks

**阻止 Win Hooks 功能已在 SBIE 4.0 及更高版本中移除，不再可用。**

_BlockWinHooks_ 曾是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定 Sandboxie 是否应允许沙盒化程序安装系统级钩子。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockWinHooks=n
```

一个应用程序可以通过一种称为窗口钩子（windows hooks）的机制附加到系统中的其他应用程序。该机制把请求应用程序的一个组件（称为 DLL 文件）与所有其他应用程序关联起来。

默认情况下，Sandboxie 拒绝安装全局钩子的请求，而会把该钩子转换为特定于应用程序的钩子，并且只把这个转换后的钩子安装到与请求应用程序处于同一沙盒中运行的应用程序中。

实际上，这把全局钩子的影响限制到特定沙盒内，在提高 Sandboxie 提供的保护的同时，仍允许依赖全局钩子的应用程序正常运行。

指定 _BlockWinHooks=n_ 会禁用此保护，允许沙盒化应用程序把全局钩子安装到所有正在运行的应用程序中，无论它们在沙盒内还是沙盒外。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 低级访问](RestrictionsSettings.md#低级访问-已移除)
