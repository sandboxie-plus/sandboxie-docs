# 应用程序设置

### "应用程序"设置组

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 应用程序。

![](../Media/ApplicationsSettings.png)

这组设置页面提供了 Sandboxie 与其他应用程序一起使用的快速配置，特别是各种知名的 Web 浏览器和电子邮件程序，还包括一些已知需要在 Sandboxie 中进行特殊配置的第三方应用程序。

* * *

### Web 浏览器

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 应用程序 > Web 浏览器

此设置子组本身分为三个子组：

#### Internet Explorer
![](../Media/WebBrowserSettings1.png)

另请参阅：[Internet Explorer 提示](InternetExplorerTips.md)

#### Firefox
![](../Media/WebBrowserSettings2.png)

另请参阅：[Firefox 提示](FirefoxTips.md)

#### 其他浏览器
![](../Media/WebBrowserSettings3.png)

此设置页面为以下浏览器提供快速配置：Internet Explorer、Mozilla Firefox 和 SeaMonkey、Opera Web 浏览器、Maxthon 2 和 Google Chrome。

选择（高亮）所需的配置，然后单击"添加"按钮以在此沙盒中启用它。如果您为 Web 浏览器使用的数据（配置文件）文件夹使用非默认位置，请确保也访问[应用程序 > 文件夹](ApplicationsSettings.md#folders)设置页面以指定替代位置。

Internet Explorer 设置页面上的两个特殊设置：

* 在沙盒外保存：搜索字符串和已调用命令的历史记录。<br>
有关详细信息，请参阅 [Sandboxie Ini](SandboxieIni.md) 设置：[OpenProtectedStorage](OpenProtectedStorage.md)。

* ~~在沙盒外保存：Hotmail 和 Messenger 的账户信息。~~（自 Sandboxie v0.8.0 / 5.50.0 起不再可用）。<br>
有关详细信息，请参阅 [Sandboxie Ini](SandboxieIni.md) 设置：[OpenCredentials](OpenCredentials.md)。
* 另请参阅 [Internet Explorer 提示中的在沙盒外保存](InternetExplorerTips.md#save-outside-sandbox) 获取更多信息和建议。

* * *

#### 电子邮件阅读器

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 应用程序 > 电子邮件阅读器

![](../Media/EmailReaderSettings.png)

此设置页面为以下电子邮件程序提供快速配置：

* Outlook Express
* Office Outlook
* Windows Vista Mail
* Windows Live Mail
* Mozilla Thunderbird
* Mozilla SeaMonkey
* Opera Mail
* IncrediMail
* Eudora
* The Bat!

选择（高亮）所需的配置，然后单击"添加"按钮以在此沙盒中启用它。

在以下情况下，您可能还需要告诉 Sandboxie 您的邮箱数据文件所在的位置：

* 如果您的邮箱位于非默认或非标准位置。
* 如果您使用 Eudora 或 The-Bat! 电子邮件软件。

为此，请打开[沙盒设置 > 应用程序 > 文件夹](ApplicationsSettings.md#folders)，从下拉列表中选择您的电子邮件软件，然后选择要与之关联的文件夹位置。

完成电子邮件配置后，您可能想要测试它，以确保即使在 Sandboxie 下运行时，删除沙盒时也不会丢失新邮件。为此，请按照[测试电子邮件配置](TestEmailConfiguration.md)中概述的步骤操作。

如果 Sandboxie 不知道您的电子邮件程序，您可以使用[沙盒设置 > 资源访问 > 文件访问 > 直接访问](ResourceAccessSettings.md#file-access--direct-access)来明确添加对包含邮箱数据文件的文件夹的直接访问。

另请参阅消息 [SBIE2212](SBIE2212.md)、[电子邮件保护](EmailProtection.md)和[电子邮件常见问题](FAQEmail.md)。

* * *

### <a name="misc" id="misc"></a>其他

以下设置页面用于启用按主题分类的第三方软件配置。有 PDF 和打印软件、密码和安全软件、桌面实用程序和其他杂项程序和设置的设置页面。

选择（高亮）所需的配置，然后单击"打开网站"按钮访问 Sandboxie 识别的特定程序的供应商网站。

选择（高亮）所需的配置，然后单击"添加"按钮以在此沙盒中启用它。在某些情况下，您还需要指定第三方软件使用的数据文件的位置。使用[应用程序 > 文件夹](ApplicationsSettings.md#folders)设置页面指定替代位置。

* * *

#### 本地

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 应用程序 > 本地

![](../Media/LocalApplicationsSettings.png)

使用此设置页面输入您自己的自定义设置作为应用程序配置包，可以轻松地为特定沙盒启用或禁用。

有关设计自己的应用程序配置包或模板的更多信息，请参阅 Sandboxie 安装文件夹中的 _Templates.ini_ 文件。

* * *

#### 文件夹

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 应用程序 > 文件夹

![](../Media/FolderApplicationsSettings.png)

使用此设置页面为已在沙盒中启用（或添加到）的应用程序使用的数据文件指定任何替代（非默认）文件夹位置。

首先，选择（高亮）所需的应用程序，然后单击"添加"按钮指定替代位置。

* * *

#### 辅助功能设置

[Sandboxie Control](SandboxieControl.md) > [沙盒设置](SandboxSettings.md) > 应用程序 > 辅助功能

![](../Media/AccessibilitySettings.png)

此设置页面为以下屏幕阅读程序提供快速配置：

* JAWS
* NVDA
* Windows-Eyes
* System Access

Windows 中的辅助功能支持允许任何程序提供有关其显示内容的提示和信息。屏幕阅读软件通常使用这些提示来提供有关屏幕内容的更多详细信息。

通常，Sandboxie 的隔离会阻止屏幕阅读器访问沙盒程序提供的辅助功能提示。

启用此设置将减弱 Sandboxie 的保护，以允许屏幕阅读程序和沙盒程序之间的双向通信。

您可能希望启用[沙盒设置 > 限制 > 降低权限](RestrictionsSettings.md#drop-rights)来补偿失去的保护。 