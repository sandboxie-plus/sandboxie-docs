# Files And Folders View

[Sandboxie Control](SandboxieControl.md) > [View Menu](ViewMenu.md) > [Files and Folders](ViewMenu.md#files-and-folders)

![](../Media/FileViewFavIcon.png)

The _Files and Folders View_ is a secondary view mode in [Sandboxie Control](SandboxieControl.md). It displays the files and folders in each of the sandboxes, organized into a tree of folders, and grouped by sandbox name.

Within each sandbox, there are two top-level folders:

*   _Quick Recover Folders_ shows the folders configured to [Quick Recovery](QuickRecovery.md), and any folders or files contained within these folders.

*   _All Files and Folders_ contains the full contents of the sandbox (as described in [Sandbox Hierarchy](SandboxHierarchy.md#files)) in a friendly way. This folder is itself organized into two folders:
    *   _Drives_ shows the sandboxed contents that were created for drives in the system.
    *   _User Files_ shows the sandboxed contents of user profile folders. A user profile folder contains folders such as _My Documents_, _Desktop_ and _Favorites_.
    *   The _All Files and Folders_ folder typically also contains _RegHive_ files which represent the sandboxed copy of the Windows registry.

Use the small _+_ or _-_ icon, located at the beginning of each sandbox row, to expand or collapse the display of files and folders in the sandbox.

**Context Menus**

The _Files and Folders View_ provides context menus for sandboxes and programs. To display a context menu for the item (sandbox or file or folder) in some row, do one of the following:

*   Click the right mouse button anywhere on the row.

*   Select (highlight) the row using the mouse or keyboard, then press Shift+F10\.

*   Select (highlight) the row using the mouse or keyboard, then use the [View Menu -> Context Menu](ViewMenu.md#context-menu) command.

For a sandbox row, the context menu displayed is the same as [Sandbox Menu -> Sandbox Sub-Menu](SandboxMenu.md#sandbox-sub-menu). See there for a full description.

For a file or folder, the context menu offers these commands:

*   The _Run Sandboxed_ command opens the file or folder under the supervision of Sandboxie:
    *   Executable program files will be invoked directly.
    *   Document files will be opened in a sandboxed instance of the program associated with the document type.
    *   Folders will be opened in a sandboxed instance of Windows Explorer.

*   The _Recover to Same Folder_ and _Recover to Any Folder_ commands move the file or folder out of the sandbox. See [Quick Recovery](QuickRecovery.md) for a full description.

*   The _Add Folder to Quick Recovery_ command is available in folders below the top-level _All Files and Folders_ folder, and adds the folder to the list of [Quick Recovery](QuickRecovery.md) folders.

*   The _Remove Folder from Quick Recovery_ command is available in folders below the top-level _Quick Recovery Folders_ folder, and removes the folder from the list of [Quick Recovery](QuickRecovery.md) folders.

* * *

Go to [Sandboxie Control](SandboxieControl.md), [Programs View](ProgramsView.md), [Help Topics](HelpTopics.md).
