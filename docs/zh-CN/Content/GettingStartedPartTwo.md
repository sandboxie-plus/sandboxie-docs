# 入门指南第二部分

### 第二部分：运行网络浏览器

要启动您的网络浏览器，找到桌面上的"沙盒化网络浏览器"快捷方式图标并点击它：

![](../Media/SandboxedWebBrowserIcon.png)

或者，右键点击 [Sandboxie 控制器](SandboxieControl.md) 托盘图标，在弹出的[托盘图标菜单](TrayIconMenu.md)中选择"运行网络浏览器"操作。

![](../Media/TrayPopupMenu.png)

第三种方式是通过 Sandboxie 控制器主窗口中的[沙盒菜单](SandboxMenu.md)：

![](../Media/SandboxMenu.png)

* * *

您的网络浏览器应该会以"沙盒化"的方式启动。您可以通过窗口标题栏中包含额外的 Sandboxie **[#]** 指示器来判断程序是否在沙盒中运行：（注意：较新的浏览器可能不会在标题栏中显示 #，但如果您将鼠标悬停在窗口边缘，它会变成黄色。）

![](../Media/SandboxedTitle.png)

（注意：在某些计算机系统中，当您选择"运行网络浏览器"时，Sandboxie 可能会启动错误的程序。如果您遇到这种情况，请参阅[常见问题](FrequentlyAskedQuestions.md#why-does-the-wrong-program-start-when-i-run-my-default-web-browser-sandboxed)来解决此问题。）

沙盒化的程序应该会出现在 [Sandboxie 控制器](SandboxieControl.md)的主窗口中：

![](../Media/MainWindow.png)

该窗口显示当前在 Sandboxie 监督下运行的"沙盒化"程序列表。最初只有一个沙盒，即"DefaultBox"，但可以创建更多沙盒；请参阅[沙盒菜单](SandboxMenu.md)中的[创建新沙盒](SandboxMenu.md#create-new-sandbox)命令。

上图显示 Sandboxie 正在运行三个程序。第一个，_iexplore.exe_，代表 Internet Explorer，因为本教程假设使用的是 Internet Explorer 作为网络浏览器。如果您系统中的默认网络浏览器是 Firefox 或 Opera，那么您会看到 _firefox.exe_ 或 _opera.exe_ 作为沙盒中运行的第一个程序。

截图显示还有两个程序在运行，**SandboxieRpcss.exe** 和 **SandboxieDcomLaunch.exe**。这些支持程序是 Sandboxie 的一部分。如果需要，它们会自动启动，无需您的明确操作。请参阅[服务程序](ServicePrograms.md)。

当 Sandboxie 在任何沙盒中活跃运行程序时，Sandboxie 托盘图标（在屏幕角落）会显示红点：![](../Media/TrayIconFull.png)

* * *

教程继续在[入门指南第三部分](GettingStartedPartThree.md)。 