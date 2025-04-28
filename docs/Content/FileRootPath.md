# File Root Path

_FileRootPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies the root folder for a particular sandbox.

As with all sandbox settings, it may also be specified in the global section, and in that case will apply for all sandboxes where the setting is not also specified in the sandbox section.

See [Sandbox Hierarchy](SandboxHierarchy.md) for more information.

Usage:

```
   .
   .
   .
   [DefaultBox]
   FileRootPath=C:\Sandbox\MySandbox
```

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox menu > Set Container Folder](SandboxMenu.md#set-container-folder)

Related Sandboxie Plus setting: Options menu > Global Settings > Advanced Config > Sandboxie Config > Sandbox file system root

**Technical Details**

The following substitution variables may be useful in this path.

*   [Shell Folders](ShellFolders.md) variables such as %Personal% which expands to the user's Documents folder
*   The variable %SBIEHOME% which expands to the root of the Sandboxie installation
*   The variable %SANDBOX% which expands to the name of the sandbox
*   The variable %USER% which expands to the user name
*   The variable %SID% which expands to the user security ID (SID)
*   The variable %SESSION% which expands to the Terminal Services session number

If _FileRootPath_ is not specified, its default value is constructed using the _deprecated_ [BoxRootFolder](BoxRootFolder.md) setting, thus:

*   `BoxRootFolder\Sandbox\%SANDBOX%`

If _BoxRootFolder_ is also not specified, then the default setting is:

*   `C:\Sandbox\%USER%\%SANDBOX%`
