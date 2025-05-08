# 阻止 Windows 钩子

**BlockWinHooks 功能已在 SBIE 版本 4.+ 及更高版本中移除。它不再可用。**

_BlockWinHooks_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定 Sandboxie 是否应该允许沙盒化程序安装系统全局钩子。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockWinHooks=n
```

一个应用程序可以通过使用称为 Windows 钩子的机制来附加到系统中的其他应用程序。这种机制将请求应用程序的一个组件（称为 DLL 文件）与所有其他应用程序关联。

默认情况下，Sandboxie 会拒绝安装全局钩子的请求，而是将钩子转换为应用程序特定的钩子，并且只将这个转换后的钩子安装到与请求应用程序在同一沙盒中运行的应用程序中。

实际上，这将全局钩子的效果限制在特定的沙盒中，并在仍然允许依赖全局钩子的应用程序正确执行的同时增加了 Sandboxie 提供的保护。

指定 _BlockWinHooks=n_ 会禁用此保护，并允许沙盒化应用程序将全局钩子安装到所有正在运行的应用程序中，无论是在沙盒内还是沙盒外。

相关 [Sandboxie 控制器](SandboxieControl.md) 设置：[沙盒设置 > 限制 > 低级访问](RestrictionsSettings.md#low-level-access--removed) 