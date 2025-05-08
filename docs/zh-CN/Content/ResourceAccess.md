# 资源访问

在沙盘中，各种[资源访问设置](ResourceAccessSettings.md)仅适用于安装在沙盘外部的程序，以防止沙箱内的程序通过更改其可执行文件名称来绕过这些设置。

下表显示了哪些设置适用于哪些安装位置。

|                 | 外部 | 内部 |
|-----------------|---------|--------|
|[关闭文件路径](ClosedFilePath.md)   | 是     | 是    |
|[关闭 IPC 路径](ClosedIpcPath.md)    | 是     | 是    |
|[关闭注册表项路径](ClosedKeyPath.md)    | 是     | 是    |
|[关闭 RT](ClosedRT.md)   | 是     | 是    |
|[打开 CLSID](OpenClsid.md)        | 是     | 是    |
|[关闭 CLSID](ClosedClsid.md)        | 是     | 是    |
|[打开配置路径](OpenConfPath.md)        | 是     | 是    |
|[打开文件路径](OpenFilePath.md)     | 是     | 否       |
|[打开 IPC 路径](OpenIpcPath.md)      | 是     | 是      |
|[打开注册表项路径](OpenKeyPath.md)      | 是     | 否       |
|[打开管道路径](OpenPipePath.md)     | 是     | 是    |
|[打开窗口类](OpenWinClass.md)     | 是     | 是    |
|[不重命名窗口类](NoRenameWinClass.md) |  是    |    是    |
|[普通文件路径](NormalFilePath.md)    | 只读     | 是      |
|[普通 IPC 路径](NormalIpcPath.md)     | 只读     | 是      |
|[普通注册表项路径](NormalKeyPath.md)     | 只读     | 是      |
|[读取文件路径](ReadFilePath.md)     | 只读  | 否   |
|[读取 IPC 路径](ReadIpcPath.md)       | 只读     | 否   |
|[读取注册表项路径](ReadKeyPath.md)       | 只读  | 否   |
|[写文件路径](WriteFilePath.md)   | 否      | 是     |
|[写注册表项路径](WriteKeyPath.md)     | 否      | 是     |

~~请注意，所有 `Close...=!<程序>,...` 仅排除沙盘外部的程序。~~
