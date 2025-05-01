# 使用 SbieDesk Hack

_UseSbieDeskHack_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。

```
   .
   .
   .
   [DefaultBox]
   UseSbieDeskHack=y
```

这是一种桌面对象解决方案，现在默认对所有进程启用。

**技术细节**

这是一种用于所有进程的桌面对象解决方案。

它最初是为了解决延迟加载导致的无限回调问题而实现的（无限递归问题在 0.4.0 / 5.43 版本中已得到解决）。

现在默认启用此设置。这使得 Electron 应用程序无需设置 'SpecialImage=chrome,program.exe' 选项即可运行。

相关的 Sandboxie Plus 设置：沙箱选项 > 各种选项 > 兼容性 > 对所有进程使用桌面对象解决方法
