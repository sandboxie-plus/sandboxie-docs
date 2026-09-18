# 开放配置路径

_OpenConfPath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.0.0 / 5.55.0 起可用。它指定路径模式，Sandboxie 对这些路径的注册表项不应用沙盒化。这让沙盒化程序可以直接访问并更新_沙盒外_的系统设置。本质上，此设置是在沙盒的某个特定注册表项位置_凿了一个洞_。

它与 [开放注册表路径](OpenKeyPath.md) 设置相同，区别在于此设置始终生效，而 _OpenKeyPath_ 只在应用程序从位于沙盒外的文件或文件夹运行时才生效。

可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   OpenConfPath=firefox.exe,HKEY_LOCAL_MACHINE\Software\Mozilla
   OpenConfPath=firefox.exe,HKEY_CURRENT_USER\Software\Mozilla
```

这些示例让 Firefox 程序 _firefox.exe_ 可以直接访问 Mozilla 注册表项树（系统级和用户级注册表树都包括）。

_OpenConfPath_ 指定的值可以包含通配符，不过对注册表项而言，很少需要使用通配符。更多信息（包括展示通配符用法的示例）参见 [开放文件路径](OpenFilePath.md)。（_OpenFilePath_ 处理的是文件而非注册表项，但使用通配符的原理相同。）

**注意：** 即使程序可执行文件位于沙盒内，此设置也生效。这意味着下载到计算机中并执行的（可能恶意的）软件，可以利用此设置。

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 注册表 > 添加注册表项 > 访问列 > 全部开放
