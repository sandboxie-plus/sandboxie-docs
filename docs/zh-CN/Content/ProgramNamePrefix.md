# 程序名称前缀

在 [Sandboxie Ini](SandboxieIni.md) 配置文件的若干设置中，可以指定程序名称。这表示该设置只对匹配程序名称条件的沙盒化进程生效。

前缀指定为带扩展名的可执行文件名称，但_不_含文件夹路径：

*   _iexplore.exe_ - 正确
*   _C:\Program Files\Internet Explorer\iexplore.exe_ - 错误

前缀可以感叹号（!）开头，表示否定条件。

逗号（,）把前缀与设置的其余部分分隔开。

例如：
```
    .
    .
    .
    [DefaultBox]
    OpenFilePath=iexplore.exe,%Favorites%
    ClosedFilePath=!iexplore.exe,%Favorites%
```

这种组合表示 Internet Explorer（_iexplore.exe_）可以直接访问收藏夹文件夹及其中的快捷方式。

另一方面，任何_其他_程序（_不是_ _iexplore.exe_，注意感叹号）都被拒绝访问同一文件夹的_任何_类型访问。
