# Getting Started Part Four

### Part Four: Quick Recovery

You may have noticed that when you saved the file _favicon.ico_ to your desktop folder, earlier, Sandboxie offered [Immediate Recovery](ImmediateRecovery) for that file. However, no such offer was made when you saved _test1.txt_ to the root folder of drive C.

This is because the desktop folder is (by default) configured as a _recoverable_ folder location, from which you will typically want to recover files. The root folder of drive C is not considered a recoverable location.

The [Quick Recovery](QuickRecovery) command scans the recoverable folders and displays a summary of all recoverable files:

![](https://xanasoft.com/wp-content/uploads/2020/10/QuickRecoverSandbox.png)

You can invoke the **Quick Recovery** command:

*   From the [Sandbox Menu](SandboxMenu) in the main window of Sandboxie Control.

*   By right-clicking the [Tray Icon Menu](TrayIconMenu) at the corner of the screen.

* * *

The picture above shows _favicon.ico_ as the only recoverable file, because it was the only file saved to a recoverable location -- the desktop folder in this case.

Other folder locations that are set as recoverable folders by default are your _My Documents_ folder, the Windows _Favorites_ folder. Where applicable, your _Downloads_ folder is also considered a recoverable folder. Since these folders don't contain any files eligible for recovery, they are not listed at all in the picture above.

You can use the _Add Folder_ button to add more folders to Quick Recovery.

*   You can switch [Sandboxie Control](SandboxieControl) to the [Files And Folders View](FilesAndFoldersView) to view and recover any file that resides anywhere in the sandbox.

* * *

When recovering a file (or a folder), you can choose to recover the file to the corresponding location outside the sandbox -- for example, from the sandboxed desktop folder, to the real desktop. The _Recover to Same Folder_ command (shown as a button in the picture above) does that.

Alternatively, you can use the _Recover to Any Folder_ command, which can move the sandboxed file to any folder location in your computer system.

* * *

### Immediate Recovery

The [Immediate Recovery](ImmediateRecovery) feature, which was mentioned briefly in the previous part of this guide, is an extension of [Quick Recovery](QuickRecovery). Immediate Recovery keeps scanning the same set of recoverable folders, and will enable you to recover files as soon as they are created:

![](https://xanasoft.com/wp-content/uploads/2020/10/ImmediateRecoverFavIcon.png)

As with Quick Recovery, you can _Recover to Same Folder_ or _Recover to Any Folder_.

* * *

Summary:

*   Files must be created in recoverable folders if they are to be noticed by [Quick Recovery](QuickRecovery) and [Immediate Recovery](ImmediateRecovery).

*   You can customize the set of recoverable folders.

*   You can use [Files And Folders View](FilesAndFoldersView) to recover files that do not reside in any recoverable folder.

* * *

The tutorial continues in [Getting Started Part Five](GettingStartedPartFive).
