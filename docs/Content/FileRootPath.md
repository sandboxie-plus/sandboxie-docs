# File Root Path

_FileRootPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies the file-container root for a particular sandbox. It is a storage-location setting, not a rule granting access to host files.

It can be set for a box or supplied through the effective global or enabled-template configuration. An effective `FileRootPath` takes precedence over the legacy [BoxRootFolder](BoxRootFolder.md), even if `FileRootPath` came from `[GlobalSettings]` and `BoxRootFolder` was set for the box.

See [Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md) and [Sandbox Hierarchy](SandboxHierarchy.md) for the contents beneath this root.

Usage:

```
   .
   .
   .
   [DefaultBox]
   FileRootPath=C:\Sandbox\MySandbox
```

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox menu > Set Container Folder](SandboxMenu.md#set-container-folder)

In SandMan, the global default is at **Global Settings > Advanced Config > Sandboxie Config > Sandbox file system root**. The New Box wizard offers a container location, and a per-box `FileRootPath` can be entered in **Sandbox Options > Advanced Options > Miscellaneous > Add Option**. The Sandboxie Control link above describes the Classic/legacy interface.

**Technical Details**

The following substitution variables may be useful in this path.

*   [Shell Folders](ShellFolders.md) variables such as %Personal% which expands to the user's Documents folder
*   The variable %SBIEHOME% which expands to the root of the Sandboxie installation
*   The variable %SystemDrive% which expands to the Windows system drive letter
*   The variable %SANDBOX% which expands to the name of the sandbox
*   The variable %USER% (or %USERNAME%) which expands to the user name
*   The variable %SID% which expands to the user security ID (SID)
*   The variable %SESSION% which expands to the Terminal Services session number

If no effective _FileRootPath_ is available, Sandboxie checks for the deprecated [BoxRootFolder](BoxRootFolder.md). When present, its value is followed by the old-style suffix:

*   `BoxRootFolder\Sandbox\<box name>`

If neither setting is available, the built-in runtime default is:

*   `\??\%SystemDrive%\Sandbox\%USER%\%SANDBOX%`

For a typical Windows installation this resolves to a location such as `C:\Sandbox\alice\DefaultBox`. `%BOXNAME%` is not a supported root-expansion alias; use `%SANDBOX%`.

Changing `FileRootPath` in configuration does not move an existing container. Stop affected sandboxed processes before changing the path, and do not assume existing content will be relocated automatically; changing the path alone can leave the old content behind.
