# 沙盘配置文件（Sandboxie.ini）

可以通过一个名为 Sandboxie.ini 的、人类可读的文本配置文件来更改或微调沙盘（Sandboxie）的某些操作方面。本节将介绍该文件的结构和内容。

一般来说，不建议手动编辑此配置文件。建议使用 [沙盘控制（Sandboxie Control）](SandboxieControl.md) 来进行配置更改。请参阅 [沙箱设置（Sandbox Settings）](SandboxSettings.md)。

## 位置

沙盘会按以下顺序在以下文件夹中查找 Sandboxie.ini 文件：

* Windows 文件夹：在大多数 Windows 系统安装中为 `C:\Windows`
* 沙盘安装文件夹：通常为 `C:\Program Files\Sandboxie` 或 `C:\Program Files\Sandboxie-Plus`

当找到该文件的一个实例时，对 Sandboxie.ini 的搜索即结束，所有其他实例将被忽略。

当 [沙盘控制（Sandboxie Control）](SandboxieControl.md) 更新配置时，它会重写上次读取配置的文件夹中的 Sandboxie.ini 文件。因此，如果手动移动了该文件，则必须手动 [重新加载](ConfigureMenu.md#reload-configuration) 沙盘配置。（重启计算机也会有相同的效果。）

**注意：** 沙盘不支持 Sandboxie.ini 文件的任何其他自定义位置。

## 结构

文件中的配置设置被分为组或节。一个节以一行指定其名称并包含在方括号内的内容开始。例如：[SomeSectionName]。该节一直延续到文件末尾，或者直到另一个节开始。有三种类型的节：

* 全局设置节包含适用于沙盘的全局设置。这些设置以某种方式应用于所有沙箱和所有用户账户。只能有一个全局设置节，通常位于配置文件的顶部。
* 沙盘已知的每个沙箱都有一个沙箱设置节。有效的沙箱名称是由字母和数字组成的字符串，最大长度为 32 个字符。沙箱设置节应包含设置 [启用（Enabled）](Enabled.md)=y。
* 每个用户账户都有一个用户设置节。这些设置记录了特定用户账户的 [沙盘控制（Sandboxie Control）](SandboxieControl.md) 的状态，包括窗口大小等信息。这里没有对这些设置进行详细记录，但下面会有简要讨论。

一个简单的 Sandboxie.ini 文件可能如下所示。

```ini
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

该示例显示了四个节：全局节（GlobalSettings）、两个沙箱节（DefaultBox 和 InstallBox）以及一个用户账户节（UserSettings_054A02CE）。

以井号（#）开头的行是注释。这些行将被跳过。

**注意：** 在运行过程中，[沙盘控制（Sandboxie Control）](SandboxieControl.md) 会定期重写 Sandboxie.ini 文件，重写过程会丢失所有注释。但是，在重写过程中未识别的设置不会丢失，因此一种解决方法是以 Comment=text 的形式编写注释。

配置文件最多可包含 30,000 行文本。每行最多可包含 1000 个字符。

该文件采用 UNICODE 编码，这意味着每个字符由两个字节组成。许多文本文件编辑器，包括系统记事本，都能正确处理这种编码。

## 设置

### 全局设置：

* 在右侧导航栏的“全局设置”标题下列出。
* 设置适用于沙盘的一般操作，而不适用于任何特定的沙箱。
* 全局设置必须放在 GlobalSettings 节中，并且不能通过在沙箱节中包含相同设置来覆盖。
* 沙箱设置可能会出现在 GlobalSettings 节中，并且可以通过在沙箱节中包含相同设置来覆盖。

### 沙箱设置：

* 在右侧导航栏的“沙箱设置”标题下列出。
* 当在关联的沙箱节中指定时，设置适用于特定的沙箱。
* 当在 [GlobalSettings] 节中指定时，设置适用于所有沙箱。
* 沙箱节中的设置会覆盖 [GlobalSettings] 节中的相应设置。

在上面的示例中，沙箱设置 [文件根路径（FileRootPath）](FileRootPath.md) 出现在 [GlobalSettings] 中并适用于所有沙箱，但请注意，它在 [InstallBox] 节中被覆盖。

* 沙箱设置可以应用于特定的程序。请参阅 [程序名称前缀（Program Name Prefix）](ProgramNamePrefix.md)。
* 一些沙箱设置是 [是或否设置（Yes Or No Settings）](YesOrNoSettings.md)。
* 沙箱设置可以指定沙盘识别的 [可扩展变量（Expandable Variables）](ExpandableVariables.md)。

### 用户设置

* 设置记录 [沙盘控制（Sandboxie Control）](SandboxieControl.md) 的状态，例如窗口的位置。
* 每个用户账户都指向一个不同的 [UserSettings_XXXXXXXX] 节。
* 当创建一个新的 [UserSettings_XXXXXXXX] 节时，如果 [UserSettings_Default] 节存在，则默认值将取自该节。
* 如果 [UserSettings_Portable] 节存在，则所有用户账户都将指向使用该节。

## 自动化

沙盘包含一个命令行实用程序，用于查询或更新 Sandboxie.ini 配置文件。该实用程序适用于直接的命令行交互，也可从脚本或程序中调用。该实用程序可以在沙盘安装目录中找到，名为 SbieIni.exe。有关更多详细信息，请参阅 [通过命令行创建沙箱](https://github.com/sandboxie-plus/Sandboxie/issues/278#issuecomment-856207910) 和 [SbieIni.exe 使用方法](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica6bca6bc.html#p126947) 部分。
