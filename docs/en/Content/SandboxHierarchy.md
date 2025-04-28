# Sandbox Hierarchy

### Overview

When sandboxed programs create (or modify) objects, such as files, in fact, some kind of data should be created. Sandboxie creates these objects out of the way, to protect the system from harmful changes. But these objects must reside somewhere in the system. This page describes where various types of sandboxed objects are placed.

Beginning with version 2.80 of Sandboxie, the layout of the sandbox is not tied to computer-specific device names and account names. See [Portable Sandbox](PortableSandbox.md) for more information.

### Files

Files are created in the _Sandbox_ folder according to the following hierarchy:
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

The [FileRootPath](FileRootPath.md) setting specifies a path to the root of a particular sandbox. In other words, if [FileRootPath](FileRootPath.md) specifies the folder _C:\MySandbox_, then the sub-folders _drive_ and _user_ are created as _C:\MySandbox\drive_ and _C:\MySandbox\user,_ respectively.

If the [FileRootPath](FileRootPath.md) setting is omitted, the [BoxRootFolder](BoxRootFolder.md) setting is used instead. The [Box Root Folder](BoxRootFolder.md) setting specifies a path to a group of sandboxes. In other words, if [Box Root Folder](BoxRootFolder.md) specifies the folder _C:\MySandbox_, then the sub-folders _drive_ and _user_ are created as _C:\MySandbox\Sandbox\DefaultBox\drive_ and _C:\MySandbox\Sandbox\DefaultBox\user,_ respectively, and assuming the sandbox is called DefaultBox. Please note that [BoxRootFolder](BoxRootFolder.md) is a deprecated setting.

As sandboxed programs create new files or modify existing files, Sandboxie redirects these operations to act on paths that lead into the sandbox. If the sandboxed program was trying to create the file _C:\NEW.TXT_, it will be redirected to create instead _([FileRootPath](FileRootPath.md))\drive\C\NEW.TXT_.

If the sandboxed program was trying to create the file _C:\Users\joe\Documents\NEW.TXT_, it will be redirected to create _([FileRootPath](FileRootPath.md))\user\current\Documents\NEW.TXT_.

Files that are created or modified in or below _profile_ (or _home_) folders, such as _C:\Users\joe_ (on Windows Vista and later) are redirected into the sandboxed _user\current_ folder.

Files that are created or modified in or below the generic (or _All Users_) profile, are redirected into the sandboxed _user\all_ folder.

Other files that don't match either of the above paths are redirected to the sandboxed _drive\X_ folder, where _X_ would be the drive in which the files were _supposed_ to have been written.

Files that are created or modified on a remote network share are redirected into the sandboxed _share\\servername\\sharename_ folder.

When a program tries to open a file for which a copy already exists in the sandbox, Sandboxie will redirect the program to the copy of the file that was previously stored in the sandbox. On the other hand, if a copy for the file does not exist in the sandbox, and if the program does not try to modify the file, then Sandboxie will permit read-only access on the original file outside the sandbox. This behavior can be affected with the file-related settings [OpenFilePath](OpenFilePath.md), [ReadFilePath](ReadFilePath.md), and [ClosedFilePath](ClosedFilePath.md).

Note that the _Sandbox_ folder itself resides on one particular drive, so even as sandboxed programs may create and modify files in multiple drives, all these files will end up residing _physically_ in the same drive -- the drive where the _Sandbox_ folder resides.

Apart from the two sub-folders, _drive_ and _user_, the _Sandbox_ folder itself contains the file _RegHive_, and typically also _RegHive.LOG_. These hold the sandboxed registry. See below.

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
