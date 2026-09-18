# 沙盒层级

### 概述

当沙盒化程序创建（或修改）对象（如文件）时，实际上应当创建某种数据。Sandboxie 在不会碍事的地方创建这些对象，以保护系统免受有害更改。但这些对象必须驻留在系统中的某处。本页描述各种类型的沙盒化对象被放置在哪里。

自 Sandboxie 2.80 版起，沙盒的布局不再与特定计算机的设备名称和帐户名称绑定。更多信息参见 [便携式沙盒](PortableSandbox.md)。

### 文件

文件按照以下层级创建在 _Sandbox_ 文件夹中：

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

[文件根路径](FileRootPath.md) 设置指定特定沙盒根目录的路径。换句话说，如果 [文件根路径](FileRootPath.md) 指定文件夹 _C:\MySandbox_，则子文件夹 _drive_ 和 _user_ 将分别创建为 _C:\MySandbox\drive_ 和 _C:\MySandbox\user_。

如果省略 [文件根路径](FileRootPath.md) 设置，则改用 [沙盒根文件夹](BoxRootFolder.md) 设置。[沙盒根文件夹](BoxRootFolder.md) 设置指定一组沙盒的路径。换句话说，如果 [沙盒根文件夹](BoxRootFolder.md) 指定文件夹 _C:\MySandbox_，则子文件夹 _drive_ 和 _user_ 将分别创建为 _C:\MySandbox\Sandbox\DefaultBox\drive_ 和 _C:\MySandbox\Sandbox\DefaultBox\user_（假设沙盒名为 DefaultBox）。请注意，[沙盒根文件夹](BoxRootFolder.md) 是已弃用的设置。

当沙盒化程序创建新文件或修改现有文件时，Sandboxie 会把这些操作重定向到通向沙盒内部的路径。如果沙盒化程序试图创建文件 _C:\NEW.TXT_，它会被重定向为创建 _([文件根路径](FileRootPath.md))\drive\C\NEW.TXT_。

如果沙盒化程序试图创建文件 _C:\Users\joe\Documents\NEW.TXT_，它会被重定向为创建 _([文件根路径](FileRootPath.md))\user\current\Documents\NEW.TXT_。

在 _profile_（或 _home_）文件夹（如 _C:\Users\joe_，Windows Vista 及更高版本）之中或其下创建或修改的文件，会被重定向到沙盒化的 _user\current_ 文件夹。

在通用（或 _All Users_）配置文件之中或其下创建或修改的文件，会被重定向到沙盒化的 _user\all_ 文件夹。

其他不符合上述任何路径的文件，会被重定向到沙盒化的 _drive\X_ 文件夹，其中 _X_ 是这些文件“本应”被写入的驱动器。

在远程网络共享上创建或修改的文件，会被重定向到沙盒化的 _share\servername\sharename_ 文件夹。

当程序试图打开一个在沙盒中已有副本的文件时，Sandboxie 会把程序重定向到先前存储在沙盒中的该文件副本。另一方面，如果沙盒中不存在该文件的副本，且程序不试图修改该文件，则 Sandboxie 会允许对沙盒外的原始文件进行只读访问。此行为可以受与文件相关的设置 [开放文件路径](OpenFilePath.md)、[只读文件路径](ReadFilePath.md) 和 [封闭文件路径](ClosedFilePath.md) 影响。

注意：_Sandbox_ 文件夹本身位于某个特定驱动器上，因此即使沙盒化程序可能在多个驱动器中创建和修改文件，所有这些文件最终都会_物理上_位于同一个驱动器——即 _Sandbox_ 文件夹所在的驱动器。

除了 _drive_ 和 _user_ 这两个子文件夹外，_Sandbox_ 文件夹本身还包含文件 _RegHive_，通常还有 _RegHive.LOG_。它们保存沙盒化的注册表。见下文。

### 注册表

注册表项创建在沙盒化的注册表配置单元中。_注册表配置单元_（registry hive）是 Microsoft Windows 的术语，指存储在单个_配置单元文件_中的一组相关注册表项。

Sandboxie 在 _Sandbox_ 文件夹中创建配置单元文件，即 _RegHive_ 和 _RegHive.LOG_。当沙盒化程序启动时，此配置单元会被挂载（换句话说，加载到注册表中）。当所有沙盒化程序结束时，配置单元会被卸载。

沙盒化的配置单元在 Windows 注册表的全局结构中具有以下位置和结构：

```
 . HKEY_USERS
 . . KeyRootPath
 . . . machine
 . . . user
 . . . . current
```

[注册表根路径](KeyRootPath.md) 设置指定特定沙盒根目录的路径。如果省略，默认值为 _HKEY_USERS\Sandbox_(用户名称)_(沙盒名称)_。例如，如果用户 joe 使用沙盒 DefaultBox，默认的 [注册表根路径](KeyRootPath.md) 是 _HKEY_USERS\Sandbox_joe_DefaultBox_。

当沙盒化程序创建新的注册表项或修改现有项时，Sandboxie 会把这些操作重定向到通向沙盒内部的路径。如果沙盒化程序试图创建项 _HKEY_LOCAL_MACHINE\Software\NewKey_，它会被重定向为创建 _([注册表根路径](KeyRootPath.md))\machine\Software\NewKey_。

如果沙盒化程序试图创建项 _HKEY_CURRENT_USER\Software\NewKey_，它会被重定向为创建 _([注册表根路径](KeyRootPath.md))\user\current\Software\NewKey_。

对于沙盒化的注册表，重定向规则比沙盒化文件更简单：

-   在 HKEY_LOCAL_MACHINE 树之下创建或修改的注册表项，会被重定向到沙盒化的 _machine_ 项之下。

-   在 HKEY_CURRENT_USER 树之下创建或修改的注册表项，会被重定向到沙盒化的 _user\current_ 项之下。

-   在 HKEY_CLASSES_ROOT 树之下创建或修改的注册表项，会被重定向到沙盒化的 _user\current_classes_ 项之下。

注意：沙盒化的 _user\current\software\classes_ 项是到 _user\current_classes_ 项的符号链接，这意味着这些项实际上是同义词，在沙盒化的 Windows 注册表中共享相同内容。

与文件一样，访问在沙盒化注册表中有副本的项时，会被重定向到使用沙盒中的副本。对沙盒化注册表中没有副本的项进行只读访问时，会被允许访问沙盒外的该项。此行为可以受与注册表相关的设置 [开放注册表路径](OpenKeyPath.md)、[读取注册表项路径](ReadKeyPath.md) 和 [封禁注册表项路径](ClosedKeyPath.md) 影响。

### 进程间对象

这些对象被程序用来共享信息、同步处理以及提供服务。这些对象从不写入磁盘，系统关闭时即消失。

Sandboxie 隔离这些对象，以便让同一个程序能够在沙盒中和沙盒外并排运行。它还能防止沙盒化程序干扰非沙盒化程序。

这些对象创建在 NT 对象命名空间中。它们在该命名空间中的位置和结构如下：

```
 . IpcRootPath
 . . BaseNamedObjects
 . . . Global
 . . . Local
 . . . Session
 . . RPC Control
```

[IPC 根目录](IpcRootPath.md) 设置指定特定沙盒根目录的路径。如果省略，默认值为 _\Sandbox\(用户名称)\(沙盒名称)\Session_(会话编号)_。例如，如果用户 joe 在会话 0 中运行并使用沙盒 DefaultBox，默认的 [IPC 根目录](IpcRootPath.md) 是 _\Sandbox\joe\DefaultBox\Session_0_。

在 [IPC 根目录](IpcRootPath.md) 之下，是构成 NT 命名空间的_对象目录_，它们与沙盒区域外现有对象目录的布局一致。这些目录以_持久_属性创建，这意味着它们只在系统关闭时消失。

沙盒化程序创建的对象创建在沙盒对象目录内。如果程序在 Sandboxie 的监管之外运行，它通常会在 \BaseNamedObjects 对象目录中创建此类对象。

注意：对象可以不命名地创建，这种情况下该对象实际上被隔离到创建它的特定程序。然而，程序可以访问另一个程序的内部以定位和使用此类无名对象。为减轻这种风险，Sandboxie 阻止沙盒中的程序以这种方式访问沙盒外的程序。

Sysinternals（现为 Microsoft 的一部分）的免费工具 [WinObj](https://docs.microsoft.com/en-us/sysinternals/downloads/winobj) 可用于显示 NT 对象命名空间。

与文件或注册表项的情况不同，沙盒化程序永远不允许访问沙盒命名空间之外的 IPC 对象，即使是只读访问也不允许。此行为可以受与注册表相关的设置 [开放 IPC 路径](OpenIpcPath.md) 和 [封禁 IPC 路径](ClosedIpcPath.md) 影响。

注意：Sandboxie 包含许多内置的 [开放 IPC 路径](OpenIpcPath.md) 设置以使程序正常运行，在典型系统中，还会通过第三方软件的兼容性设置应用更多 [开放 IPC 路径](OpenIpcPath.md) 设置。
