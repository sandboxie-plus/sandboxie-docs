# 开放文件路径

_OpenFilePath_ 是 [沙箱配置文件（Sandboxie Ini）](SandboxieIni.md) 中的一个沙箱设置项。它用于指定一系列路径模式，使得对于这些模式所匹配的文件（夹），沙箱软件（Sandboxie）不会对其执行沙箱化隔离（也就是允许沙箱访问的意思）。通过这个功能，被沙箱化的程序可以直接访问并更新**沙箱之外**的文件和文件夹。该设置本质上是在特定的文件夹位置为沙箱“打了一个洞”。

可以指定 [Shell 文件夹](ShellFolders.md)；也可以指定 [程序名称前缀](ProgramNamePrefix.md)。

示例：
```ini
.
.
.
[DefaultBox]
OpenFilePath=C:\Downloads\
OpenFilePath=*.eml
OpenFilePath=iexplore.exe,%Favorites%
OpenFilePath=msimn.exe,*.eml
```

在查看上述示例时，请注意：除非值中已经出现星号，否则沙箱会在该值末尾自动追加一个通配星号。因此，例如 _C:\Downloads\\_ 将变为 _C:\Downloads\\*_，而 _*.eml_ 则保持不变。

通配星号用于指定具有可变或未知部分的路径模式。例如，_a.eml_ 只匹配该单一文件，而 _*.eml_ 则匹配 _a.eml_、_test.eml_、_important message.eml_ 等。需要注意的是，这两种形式都不会匹配 _a.txt_。

第一个示例设置指定，在文件夹 _C:\Downloads_（以及其下的所有子文件夹）中新建的任意文件或文件夹都不会被沙箱化。请注意，末尾的反斜杠非常重要，因为系统会在字符串末尾自动追加星号。

第二个示例展示了如何通过使用通配符，来使得 _*.eml_ 文件无论在何处创建，都不会被沙箱化。_.eml_ 文件通常由 Outlook 和 Outlook Express 创建，例如当邮件被直接保存到磁盘时。

第三个示例设置指定了当前用户帐户的收藏夹文件夹应当免于沙箱化隔离。这意味着新添加的收藏夹快捷方式将会保存在沙箱之外。该示例中使用了程序名称前缀，因此该设置仅适用于 Internet Explorer 程序（ _iexplore.exe_ ）。

第四个示例结合了前两个示例，展示了仅对指定程序应用包含通配符的路径设置。

**注意：** 出于安全考虑，当程序可执行文件本身位于沙箱内时，此设置不生效。这意味着下载到计算机并在沙箱中执行的（潜在恶意）软件无法利用该设置。

一个与 _OpenFilePath_ 类似、但**始终**生效的设置是 [OpenPipePath](OpenPipePath.md)。

相关的 [Sandboxie 经典版控制面板（Sandboxie Control）](SandboxieControl.md) 设置：[沙箱设置 > 资源访问 > 文件访问 > 直接访问](ResourceAccessSettings.md#file-access--direct-access)

相关的 Sandboxie Plus 设置：沙箱选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 开放