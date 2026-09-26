# Box Root Folder

**This setting is deprecated. Please use [FileRootPath](FileRootPath.md) instead.**

_BoxRootFolder_ is a legacy setting in [Sandboxie Ini](SandboxieIni.md). It specifies a base folder from which Sandboxie derives a box's file root by appending `\Sandbox\<box name>`. It remains an active compatibility fallback, not a removed setting.

In Sandboxie version 3 and later, [FileRootPath](FileRootPath.md) is preferred. The runtime first looks up the effective `FileRootPath` for a box and consults `BoxRootFolder` only if none is available. An effective global `FileRootPath` therefore takes precedence over a box-local `BoxRootFolder`.

Although the historical example below uses `[GlobalSettings]`, the current fallback lookup uses the effective configuration for the box. A box section or applicable enabled template can also supply `BoxRootFolder`; it is not enforced as global-only. Do not use it for new configurations.

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

The Classic/legacy dialog changes configuration and warns when boxes already contain files; it does not itself move those files. Changing this fallback on a populated box can leave existing content under the previous root. See [Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md).
