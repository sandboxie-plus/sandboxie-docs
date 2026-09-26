# Sandbox Hierarchy

### Overview

When sandboxed programs create (or modify) objects, such as files, in fact, some kind of data should be created. Sandboxie creates these objects out of the way, to protect the system from harmful changes. But these objects must reside somewhere in the system. This page describes where various types of sandboxed objects are placed.

Beginning with version 2.80 of Sandboxie, the layout of the sandbox is not tied to computer-specific device names and account names. See [Portable Sandbox](PortableSandbox.md) for more information.

### Files

With the default file-layout options, redirected files are organized beneath [FileRootPath](FileRootPath.md) approximately as follows:
```
  . FileRootPath
  . . drive
  . . . C
  . . . D
  . . . Q
  . . user
  . . . all
  . . . current
  . . . public
  . . share
  . . . server
  . . . . share
  . RegHive
```

The `user\public` branch applies where a Public profile is available. [SeparateUserFolders](SeparateUserFolders.md) and the volume-layout options can change these folder names; see [Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md).

The [FileRootPath](FileRootPath.md) setting specifies a path to the root of a particular sandbox. In other words, if [FileRootPath](FileRootPath.md) specifies the folder _C:\MySandbox_, then the sub-folders _drive_ and _user_ are created as _C:\MySandbox\drive_ and _C:\MySandbox\user,_ respectively.

If no effective [FileRootPath](FileRootPath.md) is available, the deprecated [BoxRootFolder](BoxRootFolder.md) is used if present. It supplies a base folder: for a box named DefaultBox and `BoxRootFolder=C:\MySandbox`, the derived file root is `C:\MySandbox\Sandbox\DefaultBox`, with `drive` and, under the default profile layout, `user` beneath it. If neither setting is available, Sandboxie uses its built-in file-root default.

As sandboxed programs create new files or modify existing files, Sandboxie redirects these operations to act on paths that lead into the sandbox. If the sandboxed program was trying to create the file _C:\NEW.TXT_, it will be redirected to create instead _([FileRootPath](FileRootPath.md))\drive\C\NEW.TXT_.

If the sandboxed program was trying to create the file _C:\Users\joe\Documents\NEW.TXT_, it will be redirected to create _([FileRootPath](FileRootPath.md))\user\current\Documents\NEW.TXT_.

With `SeparateUserFolders=y` (the default), files created or modified in or below the current user's _profile_ (or _home_) folder, such as _C:\Users\joe_ (on Windows Vista and later), are redirected into the sandboxed _user\current_ folder.

Under that same option, files in the generic (or _All Users_) profile use _user\all_; a recognized Public profile can use _user\public_. With `SeparateUserFolders=n`, ordinary local profile paths instead follow the drive layout, such as _drive\C\Users\joe_. Existing content is not moved between these layouts automatically.

Other local files normally use the sandboxed _drive\X_ folder, where _X_ is the drive letter for their host volume. With `UseVolumeSerialNumbers=y` and a readable filesystem volume serial, the component becomes, for example, _drive\C~1234-ABCD_. For volumes mounted without a drive letter, the default mapping follows a mounted directory; `UseVolumeGuidWhenNoLetter=y` can instead use _drive\{volume-guid}_.

Files that are created or modified on a remote network share are redirected into the sandboxed _share\\servername\\sharename_ folder.

When a program tries to open a file for which a copy already exists in the sandbox, Sandboxie will redirect the program to the copy of the file that was previously stored in the sandbox. On the other hand, if a copy for the file does not exist in the sandbox, and if the program does not try to modify the file, then Sandboxie will permit read-only access on the original file outside the sandbox. This behavior can be affected with the file-related settings [OpenFilePath](OpenFilePath.md), [ReadFilePath](ReadFilePath.md), and [ClosedFilePath](ClosedFilePath.md).

For an ordinary directory-backed box, the file root resides on one storage volume. Sandboxed programs may create or modify files that appear to be on several host drives, while their redirected copies are stored beneath that box's file root.

Alongside the file-layout folders, the sandbox root contains _RegHive_ and may contain associated registry-hive log files. These hold the sandboxed registry. See below.

### Registry

Registry keys are created in a sandboxed registry hive. A _registry hive_ is the Microsoft Windows term for a group of related registry keys that are stored in a single _hive file_.

Sandboxie creates the hive file in the _Sandbox_ folder, as the files _RegHive_ and _RegHive.LOG_. This hive is mounted (or in other words, loaded into the registry) when a sandboxed program starts. The hive is unmounted when all sandboxed programs end.

The sandboxed hive has the following position and structure within the global structure of the Windows registry.
```
 . HKEY_USERS
 . . KeyRootPath
 . . . machine
 . . . user
 . . . . current
```

The [KeyRootPath](KeyRootPath.md) setting specifies a path to the root of a particular sandbox. If omitted, it defaults to _HKEY_USERS\Sandbox_(user name)_(sandbox name)_. For example, if the user joe is using the sandbox DefaultBox, the default [KeyRootPath](KeyRootPath.md) is _HKEY_USERS\Sandbox_joe_DefaultBox_.

As sandboxed programs create new registry keys or modify existing keys, Sandboxie redirects these operations to act on paths that lead into the sandbox. If the sandboxed program was trying to create the key _HKEY_LOCAL_MACHINE\Software\NewKey_, it will be redirected to create instead _([KeyRootPath](KeyRootPath.md))\machine\Software\NewKey_.

If the sandboxed program was trying to create the key _HKEY_CURRENT_USER\Software\NewKey_, it will be redirected to create _([KeyRootPath](KeyRootPath.md))\user\current\Software\NewKey_.

With the sandboxed registry, the rules for redirection are simpler than for sandboxed files:

- A registry key created or modified below the HKEY_LOCAL_MACHINE tree will be redirected below the sandboxed _machine_ key.

- A registry key created or modified below the HKEY_CURRENT_USER tree will be redirected below the sandboxed _user\current_ key.

- A registry key created or modified below the HKEY_CLASSES_ROOT tree will be redirected below the sandboxed _user\current_classes_ key.

Note that the sandboxed _user\current\software\classes_ key is a symbolic link to the _user\current_classes_ key which means and the keys are effectively synonyms and share the same content in the sandboxed Windows registry.

As with files, access to a key which has a copy in the sandboxed registry will be redirected to use the copy in the sandbox. Read-only access to a key which does not have a copy in the sandboxed registry will be permitted to access the key outside the sandbox. This behavior can be affected with the registry-related settings [OpenKeyPath](OpenKeyPath.md), [ReadKeyPath](ReadKeyPath.md), and [ClosedKeyPath](ClosedKeyPath.md).

### Inter-Process Objects

These objects are used by programs to share information, synchronize processing, and provide services. These objects are never written to disk and they disappear when the system shuts down.

Sandboxie isolates these objects in order to make it possible to run the same program sandboxed and un-sandboxed side-by-side. It also keeps sandboxed programs from interfering with un-sandboxed ones.

These objects are created in the NT object namespace. Their position and structure within that namespace are as follows.
```
 . IpcRootPath
 . . BaseNamedObjects
 . . . Global
 . . . Local
 . . . Session
 . . RPC Control
```

The [IpcRootPath](IpcRootPath.md) setting specifies a path to the root of a particular sandbox. If omitted, it defaults to _\Sandbox\(user name)\(sandbox name)\Session_(session number)_. For example, if the user joe is running in session zero, and using the sandbox DefaultBox, the default [IpcRootPath](IpcRootPath.md) is _\Sandbox\joe\DefaultBox\Session_0_.

Below the [IpcRootPath](IpcRootPath.md), there are _object directories_ which comprise the NT namespace, and match the layout of existing object directories outside the sandbox area. The directories are created with a _persistent_ attribute, which means they will only disappear at system shutdown.

Objects created by sandboxed programs are created within the sandbox object directories. If the program is running outside the supervision of Sandboxie, it would typically create such objects in the \BaseNamedObjects object directory.

Note that objects may be created without a name, in which case the object is effectively isolated to the particular program which created it. However, a program can access the internals of another program in order to locate and use such nameless objects. To mitigate this, Sandboxie prevents a program in the sandbox from accessing a program outside the sandbox in this way.

The free utility [WinObj](https://docs.microsoft.com/en-us/sysinternals/downloads/winobj) by Sysinternals (now a part of Microsoft) can be used to display the NT object namespace.

Unlike the case with files or registry keys, sandboxed programs are never permitted to access IPC objects outside the sandbox namespace, not even for read-only access. This behavior can be affected with the registry-related settings [OpenIpcPath](OpenIpcPath.md) and [ClosedIpcPath](ClosedIpcPath.md).

Note that Sandboxie includes a number of built-in [OpenIpcPath](OpenIpcPath.md) settings to allow programs to function correctly, and in a typical system, more [OpenIpcPath](OpenIpcPath.md) settings are applied through compatibility settings for third-party software.
