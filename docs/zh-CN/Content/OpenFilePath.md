# 开放文件路径

_OpenFilePath_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定路径模式，Sandboxie 对这些路径的文件不应用沙盒化。这让沙盒化程序可以直接访问并更新_沙盒外_的文件和文件夹。本质上，此设置是在沙盒的某个特定文件夹位置_凿了一个洞_。

可以指定 [个人文件夹](ShellFolders.md)。可以指定 [程序名称前缀](ProgramNamePrefix.md)。

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

查看这些示例时请记住：Sandboxie 会在值的末尾添加一个_星号通配符_，_除非值中任何位置已出现星号_。例如，_C:\Downloads\_ 变成 _C:\Downloads\*_，而 _*.eml_ 保持不变。

_星号通配符_用于指定带有可变、未知部分的模式。例如，_a.eml_ 只匹配这一个文件，而 _*.eml_ 匹配 _a.eml_、_test.eml_、_important message.eml_ 等等。但请注意，两种形式都不匹配 _a.txt_。

第一个示例设置指定：在 _C:\Downloads_ 文件夹（及其下任何文件夹）中创建的任何文件（或文件夹）都不会被沙盒化。注意末尾的反斜杠很重要，因为会在字符串末尾放置一个星号。

第二个示例展示如何使用通配符免除 _*.eml_ 文件的沙盒化，无论它们在哪里创建。_.eml_ 文件通常由 Outlook 和 Outlook Express 在消息被显式保存到磁盘时创建。

第三个示例设置指定：当前用户帐户的收藏夹文件夹应被免除。这意味着新的收藏夹快捷方式将被添加到沙盒外。此示例使用了程序名称前缀，因此该设置只适用于 Internet Explorer 程序 _iexplore.exe_。

第四个示例结合了前两个示例，展示一条包含通配符的路径，且仅应用于特定程序。

**注意：** 出于安全原因，当程序可执行文件位于沙盒内时，此设置不适用。这意味着下载到计算机中并执行的（可能恶意的）软件，无法利用此设置。

与 _OpenFilePath_ 类似但_始终_生效的设置是 [开放管道路径](OpenPipePath.md)。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 资源访问 > 文件访问 > 直接访问](ResourceAccessSettings.md#文件访问-直接访问)

相关 Sandboxie Plus 设置：沙盒选项 > 资源访问 > 文件 > 添加文件/文件夹 > 访问列 > 开放
