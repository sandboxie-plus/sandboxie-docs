# 开放文件路径

_OpenFilePath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定 Sandboxie 不会对其应用沙盒化的文件路径模式。这允许沙盒化程序直接访问更新_沙盒外_的文件和文件夹。此设置本质上在特定文件夹位置_打了一个洞_。

可以指定[Shell 文件夹](ShellFolders.md)。可以指定[程序名称前缀](ProgramNamePrefix.md)。

示例：
```
   .
   .
   .
   [DefaultBox]
   OpenFilePath=C:\Downloads\
   OpenFilePath=*.eml
   OpenFilePath=iexplore.exe,%Favorites%
   OpenFilePath=msimn.exe,*.eml
```

在查看这些示例时，请记住 Sandboxie 会在值的末尾放置一个_通配符星号_，_除非值中已经出现星号_。例如，_C:\Downloads\_ 变成 _C:\Downloads\*_，而 _*.eml_ 保持不变。

_通配符星号_用于指定具有可变、未知部分的模式。例如，_a.eml_ 只匹配该文件，而 _*.eml_ 匹配 _a.eml_、_test.eml_、_important message.eml_ 等。但请注意，这两种形式都不匹配 _a.txt_。

第一个示例设置指定在文件夹 _C:\Downloads_（及其下的任何文件夹）中创建的任何文件（或文件夹）都不会被沙盒化。请注意，最后的反斜杠字符很重要，因为星号将放在字符串的末尾。

第二个示例显示了如何使用通配符来豁免 _*.eml_ 文件的沙盒化，无论它们在何处创建。_.eml_ 文件通常由 Outlook 和 Outlook Express 在消息显式保存到磁盘时创建。

第三个示例设置指定应豁免活动用户账户的收藏夹文件夹。这意味着新的收藏夹快捷方式将在沙盒外添加。在此示例中，使用了 ProgramNamePrefix，因此该设置仅适用于 Internet Explorer 程序 _iexplore.exe_。

第四个示例通过显示仅应用于特定程序的包含通配符的路径，结合了前两个示例。

**注意：** 出于安全原因，当程序可执行文件位于沙盒内时，此设置不适用。这意味着下载到您的计算机并执行的（潜在恶意）软件无法利用此设置。

与 _OpenFilePath_ 类似但_始终_应用的设置是 [OpenPipePath](OpenPipePath.md)。

相关的 [Sandboxie Control](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 文件访问 > 直接访问](ResourceAccessSettings.md#file-access--direct-access)

相关的 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 开放 