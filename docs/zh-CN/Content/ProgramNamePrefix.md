# 程序名称前缀

在 [沙盘配置文件（Sandboxie Ini）](SandboxieIni.md) 的多个设置中，可以指定程序名称。这表示该设置仅对符合程序名称条件的沙箱化进程生效。

前缀指定为可执行文件的名称，需包含扩展名，但**不包含**文件夹路径：

*   _iexplore.exe_ - 正确
*   _C:\Program Files\Internet Explorer\iexplore.exe_ - 错误

前缀可以以感叹号 (!) 开头，表示否定条件。

逗号 (,) 用于将前缀与设置规范的其余部分分隔开。

例如：
```ini
    .
    .
    .
    [DefaultBox]
    OpenFilePath=iexplore.exe,%Favorites%
    ClosedFilePath=!iexplore.exe,%Favorites%
```

这种组合意味着 Internet Explorer（_iexplore.exe_）可以直接访问收藏夹文件夹及其内的快捷方式。

另一方面，任何**其他**程序（非 _iexplore.exe_，注意感叹号）都被拒绝访问该文件夹的**任何**权限。
