# Box Root Folder

**This setting is deprecated. Please use [FileRootPath](FileRootPath.md) instead.**

_BoxRootFolder_ is a global setting in [Sandboxie Ini](SandboxieIni.md). It specifies the folder containing all sandboxes. One sub-folder is created within the container folder for each sandbox in active use.

In Sandboxie version 3 and later, the [FileRootPath](FileRootPath.md) setting is the preferred way to specify the location of sandboxes, and takes precedence over BoxRootFolder in case both settings exist. Note that as any other sandbox setting, the [FileRootPath](FileRootPath.md) may appear in the _GlobalSettings_ section, and in that case, it applies to all sandboxes.

See [Sandbox Hierarchy](SandboxHierarchy.md) for more information.

Usage:

```
   .
   .
   .
   [GlobalSettings]
   BoxRootFolder=C:\Sandbox
```

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox menu > Set Container Folder](SandboxMenu.md#set-container-folder)
