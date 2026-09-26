# Separate User Folders

_SeparateUserFolders_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 0.2.2 / Classic 5.41.2. It selects how redirected user-profile files are organized beneath [FileRootPath](FileRootPath.md). The runtime default is `y`.

```ini
   [DefaultBox]
   SeparateUserFolders=n
```

With `y`, Sandboxie maps recognized profile locations to portable folders such as `user\current`, `user\all`, and, where available, `user\public`. With `n`, it does not set up those special mappings. An ordinary local profile path then uses the drive layout, for example `drive\C\Users\...`. The setting does not alter Windows user profiles or account permissions.

The SandMan checkbox is **Sandbox Options > File Options > Separate user folders**. It is unavailable when the box is not empty. Changing the setting does not migrate files between `user\...` and `drive\...`; use it on an empty box. If existing data must be preserved, handle it separately rather than assuming the setting will migrate it.

Sandboxie reads this option while initializing file handling in each sandboxed process. Restart affected processes after changing it; existing processes do not rebuild their profile mapping automatically. See [Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md) and [Sandbox Hierarchy](SandboxHierarchy.md).
