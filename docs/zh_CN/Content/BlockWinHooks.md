# 阻止 Win Hooks

**BlockWinHooks 功能自 SBIE 4.+ 版本起已被移除，现已不再可用**

_BlockWinHooks_ 曾是 [Sandboxie Ini](SandboxieIni.md) 中的沙箱设置项。该选项用于指定 Sandboxie 是否允许沙箱中的程序安装系统全局钩子。

用法示例：

```
   .
   .
   .
   [DefaultBox]
   BlockWinHooks=n
```

某些应用程序可以通过名为 Windows 钩子的机制，附着到系统中的其他应用程序上。该机制会将发起请求的应用程序的某个组件（即 DLL 文件）关联到所有其他应用程序中。

默认情况下，Sandboxie 会拒绝安装全局钩子的请求，并将其转换为仅适用于应用程序自身的钩子，仅安装到与请求应用程序处于同一沙箱中的其他程序里。

实际上，这种方式将全局钩子的影响范围限制在特定沙箱内，提升了 Sandboxie 提供的保护能力，同时允许依赖全局钩子的程序能够正常运行。

指定 _BlockWinHooks=n_ 时，将禁用上述保护机制，并允许沙箱内的应用程序向所有正在运行的程序（无论是否处于沙箱内）安装全局钩子。

相关 [沙箱](SandboxieControl.md) 设置项见：[沙箱设置 > 限制 > 低级访问](RestrictionsSettings.md#low-level-access--removed)
