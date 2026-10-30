# 只写文件路径

只写文件路径（`WriteFilePath`）是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，用于仅限沙盒内的文件访问：对于常规文件打开操作，主机侧内容通常被隐藏，而文件和文件夹可在沙盒内的相应位置创建。

可以指定 [个人文件夹](ShellFolders.md)。可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   WriteFilePath=%Cookies%
```

此示例表示：沙盒中的程序通常无法打开沙盒外 Internet Explorer Cookie 文件夹中已有的 Cookie，但可以在沙盒内的相应文件夹中创建文件。对于常规文件打开操作，主机上的 Cookie 被视为不存在；能否在沙盒内创建文件，仍取决于请求的操作和访问检查。

`WriteFilePath` 既适用于匹配的文件路径，也适用于文件夹路径。“只写”并不禁止读取沙盒内的内容：当具体操作和句柄获授的访问权限允许时，已有的沙盒副本仍可读取。

[封闭文件路径](ClosedFilePath.md) 会同时封闭对主机侧内容和沙盒副本的访问，而实际选用的 `WriteFilePath` 规则通常只封闭主机侧的访问，允许访问沙盒副本。

允许访问沙盒副本并不保证操作成功。结果还取决于实际生效的规则、已有沙盒副本的状态、请求的操作和访问权限、文件与文件夹的创建条件、Windows 权限，以及适用的虚拟化和访问限制处理路径。

相关 [Sandboxie Control](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 文件访问 > 只写访问](ResourceAccessSettings.md#文件访问-只写访问)

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 仅限沙盒内（只写）
