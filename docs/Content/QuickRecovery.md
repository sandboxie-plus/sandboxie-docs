# Quick Recovery

[Sandboxie Control](SandboxieControl.md) > [Sandbox Menu](SandboxMenu.md) > Quick Recovery

[Sandboxie Control](SandboxieControl.md) > [Tray Icon Menu](TrayIconMenu.md) > Quick Recovery

![](../Media/QuickRecoverSandbox.png)

Sandboxed programs create files and folders inside the sandbox. It may be desirable to move some of these created files out of the sandbox. For instance, a document file downloaded by a sandboxed browser is saved into the sandbox, but that file should be extracted and placed in the _Documents_ folder outside the sandbox.

The rudimentary approach is to use the regular, non-sandboxed Windows Explorer to navigate inside the folders that make up the sandbox. By using the [Sandbox Menu > Sandbox > Explore Contents](SandboxMenu.md#sandbox-menu) command, you can open a folder window (unsandboxed) with a view into the sandbox. You can then navigate in the depth of the sandbox folder, and _cut_ sandboxed files in order to _paste_ them somewhere else.

The Quick Recovery feature makes it easier to extract files (and even whole folders) that are created and saved by sandboxed programs. It scans a few sandboxed folders, which have to be selected in advance, and lists the files (and folders) it finds within them. These files (and folders) can be recovered into the corresponding location outside the sandbox, or to any location.

To invoke the Quick Recovery window, use the [Sandbox Menu > Sandbox > Quick Recovery](SandboxMenu.md#sandbox-menu) command (or the corresponding command from the [Tray Icon Menu](TrayIconMenu.md)). Quick Recovery also appear as part of the [Delete Sandbox](DeleteSandbox.md) window.

**The Quick Recovery Window**

The central area which extends to the lower right corner of the window shows the quick-recoverable files and folders in a particular sandbox. Select a file or folder, and then click one of the two _Recover to_ buttons on the left:

*   _Recover to Same Folder_ moves the file (or folder) from the sandbox to a corresponding location outside the sandbox. For example, the picture above shows the file _favicon.ico_ in the sandboxed _Desktop_ folder. Clicking this command on the file will move it to the real desktop folder.
*   _Recover to Any Folder_ first displays a _Browse For Folder_ dialog box, then moves the file (or folder) to the folder selected in the dialog box.

These commands are also available if you invoke the context menu on a file or folder, typically by clicking the right mouse button on it.

**Adding Folders to Quick Recovery**

As noted, Quick Recovery only scans folders which are explicitly selected. By default, it scans the _Desktop_, _Favorites_ and _Documents_ folders. Where applicable, your _Downloads_ folder is also considered a recoverable folder.

*   You can add more folders using the _Add Folder_ button.
*   You can use [Sandbox Settings > Recovery > Quick Recovery](RecoverySettings.md#quick-recovery) to add and remove folders.
*   When [Sandboxie Control](SandboxieControl.md) is in [Files And Folders View](FilesAndFoldersView.md) view, you can right-click a folder and select _Add Folder to Quick Recovery_.

* * *

Go to [Delete Sandbox](DeleteSandbox.md), [Immediate Recovery](ImmediateRecovery.md), [Sandboxie Control](SandboxieControl.md), [Help Topics](HelpTopics.md).
