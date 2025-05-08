# 沙箱层级

### 概述

当沙箱化程序创建（或修改）对象（如文件）时，实际上会创建某种数据。沙盘会在不影响系统的地方创建这些对象，以保护系统免受有害更改的影响。但这些对象必须存放在系统的某个位置。本页面描述了各种类型的沙箱化对象的存放位置。

从沙盘 2.80 版本开始，沙箱的布局不再与计算机特定的设备名称和账户名称相关联。有关更多信息，请参阅[可移植沙箱](PortableSandbox.md)。

### 文件

文件根据以下层次结构创建在 _Sandbox_ 文件夹中：
```
  . FileRootPath
  . . drive
  . . . C
  . . . D
  . . . Q
  . . user
  . . . all
  . . . current
```

[文件根路径](FileRootPath.md) 设置指定了特定沙箱的根路径。换句话说，如果 [文件根路径](FileRootPath.md) 指定的文件夹为 _C:\MySandbox_，那么子文件夹 _drive_ 和 _user_ 将分别创建为 _C:\MySandbox\drive_ 和 _C:\MySandbox\user_。

如果省略 [文件根路径](FileRootPath.md) 设置，则会使用 [沙箱根文件夹](BoxRootFolder.md) 设置。[沙箱根文件夹](BoxRootFolder.md) 设置指定了一组沙箱的路径。换句话说，如果 [沙箱根文件夹](BoxRootFolder.md) 指定的文件夹为 _C:\MySandbox_，并且假设沙箱名为 DefaultBox，那么子文件夹 _drive_ 和 _user_ 将分别创建为 _C:\MySandbox\Sandbox\DefaultBox\drive_ 和 _C:\MySandbox\Sandbox\DefaultBox\user_。请注意，[沙箱根文件夹](BoxRootFolder.md) 是一个已弃用的设置。

当沙箱化程序创建新文件或修改现有文件时，沙盘会将这些操作重定向到沙箱内的路径。如果沙箱化程序试图创建文件 _C:\NEW.TXT_，它将被重定向为创建 _([文件根路径](FileRootPath.md))\drive\C\NEW.TXT_。

如果沙箱化程序试图创建文件 _C:\Users\joe\Documents\NEW.TXT_，它将被重定向为创建 _([FileRootPath](FileRootPath.md))\user\current\Documents\NEW.TXT_。

在 _profile_（或 _home_）文件夹（如 Windows Vista 及更高版本中的 _C:\Users\joe_）内或其下创建或修改的文件将被重定向到沙箱化的 _user\current_ 文件夹。

在通用（或 _All Users_）配置文件内或其下创建或修改的文件将被重定向到沙箱化的 _user\all_ 文件夹。

其他不符合上述任一路径的文件将被重定向到沙箱化的 _drive\X_ 文件夹，其中 _X_ 是文件原本应写入的驱动器。

在远程网络共享上创建或修改的文件将被重定向到沙箱化的 _share\\servername\\sharename_ 文件夹。

当程序试图打开一个在沙箱中已有副本的文件时，沙盘会将程序重定向到沙箱中先前存储的文件副本。另一方面，如果文件在沙箱中没有副本，并且程序不试图修改该文件，那么沙盘将允许对沙箱外的原始文件进行只读访问。此行为可通过与文件相关的设置 [打开文件路径](OpenFilePath.md)、[读取文件路径](ReadFilePath.md) 和 [关闭文件路径](ClosedFilePath.md) 进行影响。

请注意，_Sandbox_ 文件夹本身位于某个特定的驱动器上，因此即使沙箱化程序可能在多个驱动器上创建和修改文件，所有这些文件最终都会物理地存放在同一个驱动器上，即 _Sandbox_ 文件夹所在的驱动器。

除了 _drive_ 和 _user_ 这两个子文件夹外，_Sandbox_ 文件夹本身还包含文件 _RegHive_，通常还有 _RegHive.LOG_。这些文件保存着沙箱化的注册表。请参阅下文。

### 注册表

注册表项在沙箱化的注册表配置单元中创建。“注册表配置单元”是 Microsoft Windows 术语，指的是一组相关的注册表项，这些项存储在单个“配置单元文件”中。

沙盘在 _Sandbox_ 文件夹中创建配置单元文件，即 _RegHive_ 和 _RegHive.LOG_ 文件。当沙箱化程序启动时，这个配置单元会被挂载（换句话说，加载到注册表中）。当所有沙箱化程序结束时，该配置单元会被卸载。

沙箱化的配置单元在 Windows 注册表的全局结构中具有以下位置和结构：
```
 . HKEY_USERS
 . . KeyRootPath
 . . . machine
 . . . user
 . . . . current
```

[注册表项根路径](KeyRootPath.md) 设置指定了特定沙箱的根路径。如果省略，它默认设置为 _HKEY_USERS\Sandbox_(用户名)_(沙箱名)_。例如，如果用户 joe 使用的沙箱名为 DefaultBox，则默认的 [注册表项根路径](KeyRootPath.md) 为 _HKEY_USERS\Sandbox_joe_DefaultBox_。

当沙箱化程序创建新的注册表项或修改现有项时，沙盘会将这些操作重定向到沙箱内的路径。如果沙箱化程序试图创建项 _HKEY_LOCAL_MACHINE\Software\NewKey_，它将被重定向为创建 _([注册表项根路径](KeyRootPath.md))\machine\Software\NewKey_。

如果沙箱化程序试图创建项 _HKEY_CURRENT_USER\Software\NewKey_，它将被重定向为创建 _([注册表项根路径](KeyRootPath.md))\user\current\Software\NewKey_。

对于沙箱化的注册表，重定向规则比沙箱化文件的规则更简单：

- 在 HKEY_LOCAL_MACHINE 树以下创建或修改的注册表项将被重定向到沙箱化的 _machine_ 项以下。

- 在 HKEY_CURRENT_USER 树以下创建或修改的注册表项将被重定向到沙箱化的 _user\current_ 项以下。

- 在 HKEY_CLASSES_ROOT 树以下创建或修改的注册表项将被重定向到沙箱化的 _user\current_classes_ 项以下。

请注意，沙箱化的 _user\current\software\classes_ 项是指向 _user\current_classes_ 项的符号链接，这意味着这两个项在沙箱化的 Windows 注册表中实际上是同义词，并且共享相同的内容。

与文件一样，对沙箱化注册表中有副本的项的访问将被重定向到使用沙箱中的副本。对沙箱化注册表中没有副本的项的只读访问将被允许访问沙箱外的项。此行为可通过与注册表相关的设置 [打开注册表项路径](OpenKeyPath.md)、[读取注册表项路径](ReadKeyPath.md) 和 [关闭注册表项路径](ClosedKeyPath.md) 进行影响。

### 进程间对象

这些对象由程序用于共享信息、同步处理和提供服务。这些对象永远不会写入磁盘，并且在系统关闭时会消失。

沙盘会隔离这些对象，以便可以同时运行沙箱化和非沙箱化的同一程序。它还可以防止沙箱化程序干扰非沙箱化程序。

这些对象在 NT 对象命名空间中创建。它们在该命名空间中的位置和结构如下：
```
 . IpcRootPath
 . . BaseNamedObjects
 . . . Global
 . . . Local
 . . . Session
 . . RPC Control
```

[IPC 根路径](IpcRootPath.md) 设置指定了特定沙箱的根路径。如果省略，它默认设置为 _\Sandbox\(用户名)\(沙箱名)\Session_(会话编号)_。例如，如果用户 joe 在会话零中运行，并使用沙箱 DefaultBox，则默认的 [IPC 根路径](IpcRootPath.md) 为 _\Sandbox\joe\DefaultBox\Session_0_。

在 [IPC 根路径](IpcRootPath.md) 以下，有构成 NT 命名空间的“对象目录”，这些目录与沙箱区域外现有对象目录的布局相匹配。这些目录以“持久”属性创建，这意味着它们只会在系统关闭时消失。

沙箱化程序创建的对象在沙箱对象目录中创建。如果程序在沙盘的监管之外运行，它通常会在 \BaseNamedObjects 对象目录中创建此类对象。

请注意，对象可以在没有名称的情况下创建，在这种情况下，该对象实际上被隔离到创建它的特定程序。但是，一个程序可以访问另一个程序的内部以定位和使用此类无名称的对象。为了减轻这种情况，沙盘会防止沙箱内的程序以这种方式访问沙箱外的程序。

Sysinternals（现在是 Microsoft 的一部分）提供的免费实用工具 [WinObj](https://docs.microsoft.com/en-us/sysinternals/downloads/winobj) 可用于显示 NT 对象命名空间。

与文件或注册表项的情况不同，沙箱化程序永远不允许访问沙箱命名空间外的 IPC 对象，即使是只读访问也不行。此行为可通过与注册表相关的设置 [打开 IPC 路径](OpenIpcPath.md) 和 [关闭 IPC 路径](ClosedIpcPath.md) 进行影响。

请注意，沙盘包含许多内置的 [打开 IPC 路径](OpenIpcPath.md) 设置，以允许程序正常运行，并且在典型系统中，更多的 [打开 IPC 路径](OpenIpcPath.md) 设置会通过第三方软件的兼容性设置应用。
