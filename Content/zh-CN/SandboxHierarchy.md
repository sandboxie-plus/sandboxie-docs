# 沙盒层级结构

### 概述


当沙盒化的程序创建（或修改）某些对象，例如文件时，实际上创建了某些对应的对象。 Sandboxie 将这些对象将这些对象隔离存储以保护系统免受危害，但是这些对象必须存储在系统中的某个位置。本页面介绍了各种类型的沙盒化对象放置的位置。

从 Sandboxie 的 2.80 版本开始，沙盒的布局不再受制于计算机设备名称和帐户名称。有关更多信息，请参见 [Portable Sandbox](PortableSandbox.md) 。

### 文件

文件被按照如下结构在_Sandbox_文件夹中创建：
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

[文件根目录（FileRootPath）](FileRootPath.md)设置指定了特定沙盒的根路径。换句话说，如果 [文件根目录](FileRootPath.md) 指定为文件夹 _C:\MySandbox_，那么子文件夹 _drive_ 和 _user_ 将分别被创建为 _C:\MySandbox\drive_ 和 _C:\MySandbox\user，_

如果没有配置 [文件根目录](FileRootPath.md) ，则会使用 [沙盒根目录](BoxRootFolder.md) 的配置。[沙盒根目录](BoxRootFolder.md) 设置指定了一组沙盒的路径。换句话说，如果 [沙盒根目录](BoxRootFolder.md) 设置为文件夹 _C:\MySandbox_，假设沙盒名为 DefaultBox，那么子文件夹 _drive_ 和 _user_ 将被创建为 _C:\MySandbox\Sandbox\DefaultBox\drive_ 和 _C:\MySandbox\Sandbox\DefaultBox\user_。请注意，[沙盒根目录]( BoxRootFolder .md ) 这个选项已被弃用。

当沙盒程序创建新文件或修改现有文件时，Sandboxie将重定向这些操作到沙盒中的对应路径。如果沙盒化的程序试图创建文件_C:\NEW.TXT_，它将被重定向为创建 _([FileRootPath](FileRootPath.md))\drive\C\NEW.TXT_。

如果沙盒程序试图创建文件 _C:\Users\joe\Documents\NEW.TXT_，它将被重定向以创建 _([FileRootPath](FileRootPath.md))\user\current\Documents\NEW.TXT_。

在 _profile_（或 _home_）文件夹中创建或修改的文件，例如 _C:\Users\joe_ (Windows Vista或更高系统中) 被重定向到沙盒化的 _user\current_ 文件夹。

在通用（或_All Users_）配置文件中创建或修改的文件将被重定向到沙盒化的 _user\all_ 文件夹中。

其他不匹配以上路径的文件将被重定向到沙盒化的 _drive\X_ 文件夹， 其中 _X_ 是文件 _应该_ 被写入的驱动器。

在沙盒中，创建或修改在远程网络共享的文件将被重定向到沙盒化的 _share\\servername\\sharename_ 文件夹。

当程序尝试打开一个已经在沙盒中有副本的文件时，Sandboxie会将操作重定向到之前存储在沙盒中的文件副本。另一方面，如果该文件的副本不存在于沙盒中，并且程序不尝试修改该文件，则Sandboxie将允许对位于沙箱外部的原始文件进行只读访问。这一行为可以通过与文件相关的设置[OpenFilePath](OpenFilePath.md)、[ReadFilePath](ReadFilePath.md)和[ClosedFilePath](ClosedFilePath.md)来配置。

请注意，_沙盒_文件夹本身位于一个特定的驱动器上，因此即使被隔离的程序可能会在多个驱动器中创建和修改文件，所有这些文件最终都将_物理意义上_存储在同一驱动器中 -- 即_Sandbox_ 文件夹所在的驱动器。

除了两个子文件夹_drive_和_user_之外，_Sandbox_ 文件夹本身还包含文件 _RegHive_（通常还有 _RegHive.LOG_）。这些保存着沙盒化的注册表。请参见下文。

### 注册表

注册表键在沙盒化的_Registry Hive_中创建，_Registry Hive_ 是 Windows 中用于存储一组相关注册表键的术语，这些键存储在单个 _hive_ 文件中。

Sandboxie会在_Sandbox_文件夹中创建hive文件，包括_RegHive_和_RegHive.LOG_。当沙盒化程序启动时，该hive被挂载（或者说加载到注册表中）。当所有沙盒化程序结束时，该hive将被卸载。

以下是沙盒化注册表在 Windows 全局注册表中的位置于结构：
```
 . HKEY_USERS
 . . KeyRootPath
 . . . machine
 . . . user
 . . . . current
```

[KeyRootPath](KeyRootPath.md)”配置指定了特定沙盒根目录的路径。如果省略，则默认为 _HKEY_USERS\Sandbox_(user name)_(sandbox name)_。例如，如果用户joe正在使用DefaultBox沙盒，则默认的[KeyRootPath](KeyRootPath.md)是 _HKEY_USERS\Sandbox_joe_DefaultBox_。

当沙盒程序创建新的注册表键或修改现有键时，Sandboxie 会将这些操作重定向到沙盒化的路径上。如果被沙盒化的程序试图创建 _HKEY_LOCAL_MACHINE\Software\NewKey_，它将被重定向为创建 _([KeyRootPath](KeyRootPath.md))\machine\Software\NewKey_。

如果沙盒程序试图创建 _HKEY_CURRENT_USER\Software\NewKey_，它将被重定向为创建 _([KeyRootPath](KeyRootPath.md))\user\current\Software\NewKey_。

沙盒化注册表的重定向规则比沙盒化文件更简单：

- 在 HKEY_LOCAL_MACHINE 下创建或修改的注册表键将被重定向到沙盒化的 _machine_ 下。

- 在 HKEY_CURRENT_USER 下创建或修改的注册表键将被重定向到沙盒化的 _user\current_ 下。

- 在 HKEY_CLASSES_ROOT 下创建或修改的注册表键将被重定向到沙盒化的 _user\current_classes_ 下。

请注意，沙盒化的 _user\current\software\classes_ 是指向 _user\current_classes_ 的符号链接，这意味着这些注册表实际上相同的，并且在沙盒化的 Windows 注册表中共享相同内容。

与文件一样，访问在沙盒注册表中有副本的注册表将被重定向以使用沙盒中的副本。对于没有在沙盒注册表中有副本的注册表的只读访问将被允许。这种行为可以通过与注册表相关的设置[OpenKeyPath](OpenKeyPath.md)，[ReadKeyPath](ReadKeyPath.md)和[ClosedKeyPath](ClosedKeyPath.md)来配置。

### 进程间对象（IPC 对象）

这些对象被程序用于共享信息、同步操作并提供服务。这些对象不会被写入磁盘，当系统关闭时它们会消失。

Sandboxie 将这些对象隔离开来，以便可以同时运行同一程序的沙盒和非沙盒版本，这样还防止沙盒程序干扰非沙盒程序。

这些对象创建于NT对象命名空间。它们在该命名空间内的位置和结构如下：
```
 . IpcRootPath
 . . BaseNamedObjects
 . . . Global
 . . . Local
 . . . Session
 . . RPC Control
```

[IPC根路径（IpcRootPath）](IpcRootPath.md) 配置指定了特定沙盒的根目录路径。如果省略，则默认为 _\Sandbox\(user name)\(sandbox name)\Session_(session number)_。例如，如果用户joe在零号会话中运行，并使用DefaultBox沙盒，则默认的 [IPC根路径](IpcRootPath.md) 为 _\Sandbox\joe\DefaultBox\Session_0_。

在[IpcRootPath](IpcRootPath.md)中，有组成NT命名空间的“对象目录”，并且与沙盒区域外现有的对象目录布局相匹配。这些目录具有“持久性”，这意味着它们只会在系统关闭时消失。

由沙盒程序创建的对象将被创建在沙盒对象目录中。如果该程序不在 Sandboxie 中运行，它通常会在 \BaseNamedObjects 对象目录中创建这些对象。

请注意，对象可以在没有名称的情况下创建，这种情况下该对象实际上只能被创建它的特定程序所隔离。但是，一个程序可以访问另一个程序内部以查找和使用这些无名对象。为了缓解这个问题，Sandboxie 会阻止沙盒中的程序以此方式访问沙盒外部的程序。

由Sysinternals（现在是Microsoft的一部分）提供的免费实用程序[WinObj](https://docs.microsoft.com/zh-cn/sysinternals/downloads/winobj)可用于显示NT对象命名空间。

与文件或注册表键不同，沙盒化程序永远无权访问沙盒命名空间之外的IPC对象，即使是只读访问也不行。这一行为可以通过与注册表相关的设置[OpenIpcPath](OpenIpcPath.md)和[ClosedIpcPath](ClosedIpcPath.md)来配置。

请注意，Sandboxie 包含许多内置的 [OpenIpcPath](OpenIpcPath.md) 设置，以兼容程序正常运行。一般而言，你可以通过第三方软件兼容性设置应用的更多的 [OpenIpcPath](OpenIpcPath.md) 设置。
