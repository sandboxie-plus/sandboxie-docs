# 资源访问

在 Sandboxie 中，各种 [资源访问设置](ResourceAccessSettings.md) 只适用于在 Sandboxie 之外安装的程序，以免被沙盒化程序更改其 exe 名称而绕过。

下表显示哪些设置适用于哪些安装位置。

|                 | 外部 | 内部 |
|-----------------|---------|--------|
|[关闭 Clsid](ClosedClsid.md)        | 是     | 是    |
|[封闭文件路径](ClosedFilePath.md)   | 是     | 是    |
|[封禁 IPC 路径](ClosedIpcPath.md)    | 是     | 是    |
|[封禁注册表项路径](ClosedKeyPath.md)    | 是     | 是    |
|[封禁 RT](ClosedRT.md)   | 是     | 是    |
|[不重命名窗口类](NoRenameWinClass.md) |  是    |    是    |
|[标准文件路径](NormalFilePath.md)    | 只读     | 是      |
|[标准 IPC 路径](NormalIpcPath.md)     | 只读     | 是      |
|[标准注册表路径](NormalKeyPath.md)     | 只读     | 是      |
|[开放 Clsid](OpenClsid.md)        | 是     | 是    |
|[开放配置路径](OpenConfPath.md)        | 是     | 是    |
|[开放文件路径](OpenFilePath.md)     | 是     | 否       |
|[开放 IPC 路径](OpenIpcPath.md)      | 是     | 是      |
|[开放注册表路径](OpenKeyPath.md)      | 是     | 否       |
|[开放管道路径](OpenPipePath.md)     | 是     | 是    |
|[开放窗口类](OpenWinClass.md)     | 是     | 是    |
|[只读文件路径](ReadFilePath.md)     | 只读  | 否   |
|[读取 IPC 路径](ReadIpcPath.md)       | 只读     | 否   |
|[读取注册表项路径](ReadKeyPath.md)       | 只读  | 否   |
|[只写文件路径](WriteFilePath.md)   | 否      | 是     |
|[写入注册表项路径](WriteKeyPath.md)     | 否      | 是     |

~~注意：所有 `Close...=!<program>,...` 都只排除沙盒外的程序。~~
