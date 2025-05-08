# 入门指南第三部分

### 第三部分：沙盒

现在您应该已经有一个"沙盒化"运行的网络浏览器了。它可以是 Internet Explorer 或任何其他浏览器。

浏览器程序可能会对您的计算机进行更改。这些更改都会被限制在沙盒中。

现在试试看。右键点击以下链接，并将文件保存到您的桌面。如果您使用的是 Internet Explorer，这是右键菜单中的"将目标另存为"命令。如果您使用的是 Firefox，这是右键菜单中的"将链接另存为"命令：

[favicon.ico](https://github.com/sandboxie-plus/sandboxie-docs/raw/main/Media/favicon.ico)

在默认和推荐的配置下，Sandboxie 会识别出文件被保存到了一个重要位置——在这种情况下是您的桌面——并会提供[即时恢复](ImmediateRecovery.md)选项：

![](../Media/ImmediateRecoverFavIcon.png)

因为这个练习的目的是为了展示文件在未恢复之前会保留在沙盒中，所以点击上面窗口的"关闭"按钮，告诉 Sandboxie 将文件保留在沙盒中。

您保存的文件 _favicon.ico_ 应该会在您的桌面上显示为这个图标：![](../Media/TrayIconEmpty.png)

如果您最小化所有窗口并查看桌面，您应该看不到这个新图标，因为文件实际上是保存在"沙盒中"，尚未恢复。

[Sandboxie 控制器](SandboxieControl.md)最初以[程序视图](ProgramsView.md)运行，显示在沙盒中运行的程序列表，但您可以使用[视图菜单](ViewMenu.md)将视图模式切换到[文件和文件夹视图](FilesAndFoldersView.md)，以显示沙盒的内容。点击"视图"菜单中的"文件和文件夹"。

![](../Media/FileViewFavIcon.png)

展开分支（通过点击 **_+_** 号）以显示按文件夹排列的沙盒内容。如上图所示，您之前保存的文件 _favicon.ico_ 已被放置在"沙盒化"的桌面文件夹中。

* * *

同样地，任何由沙盒化程序创建的文件都会被放置在对应于它"本应"被放置的真实文件夹的沙盒文件夹中。

让我们再试一次，这次使用沙盒化的记事本。要做到这一点，使用"运行任意程序"命令：

![](../Media/TrayPopupRunAny.png)

Sandboxie 显示其"运行..."对话框。输入 **notepad**：

![](../Media/RunAnyNotepad.png)

记事本应该以沙盒化的方式启动：

![](../Media/NotepadSandboxed.png)

在新的记事本文档中输入一些字母，并将其保存为 C 盘根目录下的 _test1.txt_ 文件。然后，在 C 盘根目录下查找这个文件。您应该找不到它。这是因为文件被保存在沙盒中：

![](../Media/FileViewNotepad.png)

* * *

总结：

* 由沙盒化程序创建或修改的文件最初会被放置在沙盒中。

* 沙盒中的文件对沙盒外的程序不可见。

* * *

教程继续在[入门指南第四部分](GettingStartedPartFour.md)。 