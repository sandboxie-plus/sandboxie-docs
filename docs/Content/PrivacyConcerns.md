# Privacy Concerns

This is an advanced topic, which explains that even after running a program under Sandboxie, your computer may still record _which_ programs were executed or what they did. It is important to emphasize that this is not a security breach as it will never allow sandboxed programs to infect or otherwise abuse your computer. However, this may be interesting reading for those concerned with the privacy aspects of using Sandboxie.

**Overview**

The guiding principle of Sandboxie is to isolate and contain any actions taken by programs that Sandboxie supervises, for the purpose of keeping your computer and operating system in a clean and healthy state.

Most of the side effects of running a program under Sandboxie are in fact caused by the very program that is running under Sandboxie, and are gone when the sandbox is deleted. For example, a Web browser running under Sandboxie will record your browsing history in the sandbox, and this history will be completely erased when you delete the sandbox.

Thus it is easy to make a small leap of logic from the guiding principle above, and assume that a principle of Sandboxie is to protect your privacy and clean any all traces caused directly or indirectly by any program running under its supervision. However, this assumption would not be correct.

Sandboxie puts a great deal of effort into containing the actions taken by the program it supervises, however Sandboxie makes no effect at all to prevent your own Windows operating system from keeping records of what you do in your computer.

One who makes the incorrect assumption of extreme concern for privacy on the part of Sandboxie might be surprised to find several kinds of traces and logs in Windows that record which programs have been running, even inside the sandbox.

This page will explain the various known mechanisms that record information about the programs you run, either inside or outside the supervision of Sandboxie.

**Prefetch and SuperFetch**

Prefetch, introduced in Windows XP, and SuperFetch, introduced in Windows Vista, make up the [prefetcher](https://en.wikipedia.org/wiki/Prefetcher) component in Windows.

This component is designed to improve application start up time by keeping copies of program files in a location that can be quickly accessed. The copies are kept in a folder called _Prefetch_ that resides within the main Windows folder; typically that is _C:\Windows\Prefetch_.

Windows may store copies of programs files in this Prefetch folder even when the programs were executed under Sandboxie.

Prefetch behavior can be reduced to caching only programs using during the boot sequence, or to not cache anything at all. Follow these links for more information:

* [https://www.ghacks.net/2008/01/13/enableprefetcher-in-prefetchparameters](https://www.ghacks.net/2008/01/13/enableprefetcher-in-prefetchparameters)
* [https://www.howtogeek.com/998/change-superfetch-to-only-cache-system-boot-files-in-vista](https://www.howtogeek.com/998/change-superfetch-to-only-cache-system-boot-files-in-vista)
* [https://www.howtogeek.com/989/how-to-disable-superfetch-on-windows-vista](https://www.howtogeek.com/989/how-to-disable-superfetch-on-windows-vista)

**MUI Cache**

Windows Explorer records in the registry the names of programs that are launched directly through it. This includes launching programs through the Start menu, the desktop, the quick launch area, or any folder views. It is true even if the right-click "Run Sandboxed" action is used to launch the program under Sandboxie.

The recorded information is kept in this registry key:
```
   HKEY_CURRENT_USER\Software\Microsoft\Windows\ShellNoRoam\MUICache
```

If launch a program through a Sandboxie facility (such as the Sandboxie Start menu) or through a program which is already running under Sandboxie, then this information is kept in the registry inside the sandbox.

There are various third-party registry cleaning tools that can erase this information.

**Windows Taskbar**

On Windows 7 and later, Windows Explorer stores information associated with icons on the taskbar. This information includes the icon for the program and the command used to launch it. The information is stored in files in the following folder, within the user profile folder:
```
   %Appdata%\Microsoft\Internet Explorer\Quick Launch\User Pinned\ImplicitAppShortcuts
```

The [Sandbox Settings > Applications > Miscellaneous](ApplicationsSettings.md#miscellaneous) settings page includes the setting "Permit programs to update jump lists in the Windows 7 taskbar". If this setting is enabled, additional files are created in the following folders, within the user profile folder:
```
   %Appdata%\Microsoft\Windows\Recent\CustomDestinations
   %Appdata%\Microsoft\Windows\Recent\AutomaticDestinations
```

**Windows Page File**

During its normal course of operation, Windows sometimes needs to put away the contents of memory used by one program in order to make room for another program. The memory contents are stored in the Windows [page file](https://www.howtogeek.com/126430/what-is-the-windows-page-file).

Programs that run under Sandboxie are still running in the same Windows operating system as any other program in the computer, so portions of sandboxed and normal programs may end up sitting side by side in the same page file.

It is possible to configure Windows to clear the contents of the page file at shutdown. More information [here](https://winaero.com/clear-pagefile-shutdown-windows-10) and [here](https://www.vistax64.com/threads/virtual-memory-paging-file-clear-at-shutdown.157323).

It is possible to configure Windows to encrypt the contents of the page file:

* Run _secpol.msc_ to open the _Local Security Policy_ editor
* Expand the group labeled _Public Key Policies_
* Right-click _Properties_ on the item labeled _Encrypting File System_
* Select _Allow_ to enable Encrypting File System (EFS)
* Click _Apply_ and then _OK_
* Reboot to put the new setting into effect

**Windows Hibernate File**

Similar to the Windows Page File, the hibernate file stores a copy of the memory and state of the system before the computer is turned off as part of the hibernate process. Thus the hibernate file may contain bits of memory that were used by a sandboxed program.

**System Restore**

Restore points are snapshots of the state of the operating system at some points in time. The System Restore component in Windows XP and later versions records and restores these snapshots.

Snapshots are recorded in the (typically inaccessible) folder called _System Volume Information_ and may include [many types of files](https://docs.microsoft.com/en-us/windows/win32/sr/monitored-file-extensions) found throughout the system, including within the folders of the sandbox.

Thus it is possible that System Restore will create backup copies in its folders for files or programs that exist only in the sandbox.

The System Restore component can be set to ignore files and folders in temporary folders, so [moving the sandbox](FileRootPath.md) to _%TEMP%\SANDBOX_ (instead of the default _C:\SANDBOX_) and adding the path within the registry key [FilesNotToSnapshot](https://learn.microsoft.com/en-us/windows/win32/vss/excluding-files-from-shadow-copies#using-the-filesnottosnapshot-registry-key), System Restore should ignore the sandbox when creating a Shadow Copy snapshot. More information [here](https://learn.microsoft.com/en-us/windows/win32/backup/registry-keys-for-backup-and-restore).

**System, Audit and Other Event Logs**

Windows sometimes records bits of information about running programs in its various [event logs](https://en.wikipedia.org/wiki/Event_Viewer). Typically, very little if any information is logged about a program. However, if security auditing has been enabled for some aspects of the system, Windows will have no trouble logging the details of any actions taken by a program running under Sandboxie.

Windows has an Event Viewer program which can be used to view and delete the event logs. More information [here](https://www.howtogeek.com/123646/htg-explains-what-the-windows-event-viewer-is-and-how-you-can-use-it).

**Windows System Tray Icons**

When a programs which is running under Sandboxie asks to place an icon in the [system tray area](https://www.computerhope.com/issues/chsys.htm), Sandboxie lets the program place the icon in the real system tray, which is typically located at the bottom right corner of the display.

This has the advantage that interaction with the tray icon of the sandboxed program is as easy as interacting with any other tray icon. However, it also means that Windows will record this icon and its description in the history of all tray icons it has ever displayed.

It is possible to manually clear this history in [Windows](https://www.howtogeek.com/739/clean-up-past-notification-icons-in-windows-vista). There may also be third-party registry cleaning tools that can erase this information.

**Disk Defragmentation**

Disk defragmenter software can be used to organize the contents of the hard disk at the level of data blocks, so that files may be accessed faster by the operating system.

Although this is not a privacy concern, the issue of sandboxed programs being able to defragment the disk has been raised and should be addressed.

Sandboxie isolation occurs at the higher file level rather than the lower level of data blocks. Moving data blocks around on the disk has no impact on the isolation of the sandbox, and cannot be used by a malicious program to somehow "move" its data out of the sandbox.

**IP Privacy**

Sandboxie isolation and protection occurs entirely within the local computer and is not visible to any other remote computer. Thus accessing the Internet using a sandboxed program looks the same as accessing the Internet using a program that is not running under Sandboxie. In both cases the remote computer identifies the accessing computer by its IP address.

There are various third-party solutions for anonymous Web access. More information [here](https://en.wikipedia.org/wiki/Anonymous_web_browsing).

**Windows DNS Host Cache**

Sandboxie does not prevent the logging and storage of the _hosts_ file (DNS cache) on your Windows machine. This is written to _C:\Windows\System32\drivers\etc_.
