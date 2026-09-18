# Sandboxie Ini

Sandboxie 操作的某些方面可以通过一个人类可读的文本配置文件 Sandboxie.ini 来更改或微调。本节描述该文件的结构和内容。

作为一般规则，不建议手动编辑配置文件。建议使用 [沙盒管理器](SandboxieControl.md) 进行配置更改。参见 [沙盒设置](SandboxSettings.md)。

## 位置

Sandboxie 按以下顺序在以下文件夹中查找文件 Sandboxie.ini：

*   在 Windows 文件夹中：大多数 Windows 安装为 `C:\Windows`
*   在 Sandboxie 安装文件夹中：通常为 `C:\Program Files\Sandboxie` 或 `C:\Program Files\Sandboxie-Plus`

对 Sandboxie.ini 的搜索在找到该文件的一个实例时结束，所有其他实例都会被忽略。

当 [沙盒管理器](SandboxieControl.md) 更新配置时，它会在上次读取配置的文件夹中重写 Sandboxie.ini 文件。因此，如果该文件被手动移动，则必须手动 [重新加载](ConfigureMenu.md#重新加载配置) Sandboxie 配置。（重启计算机也会有同样效果。）

**注意：** Sandboxie 不支持 Sandboxie.ini 文件位于任何其他自定义位置。

## 结构

文件中的配置设置被分成组或节。节以指定其名称（括在方括号内）的一行开始，例如：[SomeSectionName]。该节一直延续到文件末尾，或直到另一个节开始。节有三种类型：

*   全局设置节包含对 Sandboxie 而言全局的设置。它们以某种方式适用于所有沙盒和所有用户帐户。全局设置节只能有一个，通常在配置文件顶部。
*   每个 Sandboxie 已知的沙盒对应一个沙盒设置节。有效的沙盒名称是由字母和数字组成的字符串，最大长度为 32 个字符。沙盒设置节应包含设置 [启用](Enabled.md)=y。
*   每个用户帐户对应一个用户设置节。这些设置记录特定用户帐户的 [沙盒管理器](SandboxieControl.md) 状态，并包含诸如窗口大小等信息。这些设置不在此处记录，但请参阅下面的简要讨论。

一个简单的 Sandboxie.ini 文件可能如下所示。

```
   # Sample Sandboxie Configuration File
   [GlobalSettings]
   FileRootPath=C:\Sandbox\%USER%\%SANDBOX%
   # Settings for sandbox DefaultBox
   [DefaultBox]
   Enabled=y
   # Settings for sandbox InstallBox
   [InstallBox]
   Enabled=y
   FileRootPath=D:\Sandbox\Install
   # Sandboxie Control settings for some user
   [UserSettings_054A02CE]
   SbieCtrl_UserName=tzuk
```

此示例显示四个节：全局节（GlobalSettings）、两个沙盒节（DefaultBox 和 InstallBox），以及一个用户帐户节（UserSettings_054A02CE）。

以井号（#）开头的行是注释。这些行会被跳过。

**注意：** 在运行过程中，[沙盒管理器](SandboxieControl.md) 会定期重写 Sandboxie.ini 文件，这种重写会丢失所有注释。然而，未被识别的设置不会在重写时丢失，因此一种变通办法是以 Comment=text 的形式书写注释。

配置文件最多可包含 30,000 行文本。每行最长 1000 个字符。

该文件以 UNICODE 编码，这意味着每个字符由两个字节组成。许多文本文件编辑器（包括系统自带的记事本）都能正确处理这种编码。

## 设置

### 全局设置：

*   列在右侧导航栏的“全局设置”标题下。
*   设置适用于 Sandboxie 的一般操作，而非任何特定沙盒。
*   全局设置必须放在 GlobalSettings 节中，不能通过在沙盒节中也包含它们来覆盖。
*   沙盒设置可以出现在 GlobalSettings 节中，并可通过在沙盒节中也包含它们来覆盖。

### 沙盒设置：

*   列在右侧导航栏的“沙盒设置”标题下。
*   在关联的沙盒节中指定时，设置适用于特定沙盒。
*   在 [GlobalSettings] 节中指定时，设置适用于所有沙盒。
*   沙盒节中的设置会覆盖 [GlobalSettings] 中的相应设置。

在上面的示例中，沙盒设置 [文件根路径](FileRootPath.md) 出现在 [GlobalSettings] 中并适用于所有沙盒，但请注意它在 [InstallBox] 节中被覆盖。

*   沙盒设置可以应用于特定程序。参见 [程序名称前缀](ProgramNamePrefix.md)。
*   某些沙盒设置是 [是或否设置](YesOrNoSettings.md)。
*   沙盒设置可以指定 Sandboxie 可识别的 [可扩展变量](ExpandableVariables.md)。

### 用户设置

*   设置记录 [沙盒管理器](SandboxieControl.md) 的状态，例如窗口的位置。
*   每个用户帐户被定向到不同的 [UserSettings_XXXXXXXX] 节。
*   创建新的 [UserSettings_XXXXXXXX] 时，默认值取自 [UserSettings_Default] 节（如果存在）。
*   如果 [UserSettings_Portable] 节存在，则所有用户帐户都被定向到使用该节。

## 自动化

Sandboxie 包含一个命令行实用程序，用于查询或更新 Sandboxie.ini 配置文件。该实用程序适合直接命令行交互，也可从脚本或程序调用。该实用程序位于 Sandboxie 安装目录中，名为 SbieIni.exe。更多详情，请参阅 [通过命令行创建沙盒](https://github.com/sandboxie-plus/Sandboxie/issues/278#issuecomment-856207910) 和 [SbieIni.exe 用法](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica6bca6bc.html#p126947) 部分。
