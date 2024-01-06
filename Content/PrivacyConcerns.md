# Privacy Concerns

**Overview:**
This advanced topic delves into the privacy implications of running a program under Sandboxie. While Sandboxie's primary goal is isolating and containing program actions for system cleanliness, it doesn't prevent Windows from keeping records of your computer activities. This explanation clarifies the privacy aspects and various mechanisms that may record information about the programs you run.

**Prefetch and SuperFetch:**
- Prefetch and SuperFetch in Windows store copies of program files in the Prefetch folder, even for programs executed under Sandboxie.
- Configurable behavior: [Enable Prefetcher](https://www.ghacks.net/2008/01/13/enableprefetcher-in-prefetchparameters), [Customize SuperFetch](https://www.howtogeek.com/998/change-superfetch-to-only-cache-system-boot-files-in-vista), [Disable SuperFetch](https://www.howtogeek.com/989/how-to-disable-superfetch-on-windows-vista).

**MUI Cache:**
- Windows Explorer records launched programs in the registry (HKEY_CURRENT_USER\Software\Microsoft\Windows\ShellNoRoam\MUICache).
- Information within the sandbox is kept in the sandbox registry.
- Third-party registry clearing tools can erase this information.

**Windows 7 Taskbar:**
- Windows Explorer stores taskbar icon information in specific folders.
- Sandbox Settings > Applications > Miscellaneous includes a setting for taskbar jump lists.

**Windows Page File:**
- Memory contents of sandboxed and normal programs may coexist in the Windows page file.
- Possible configurations: [Clear Page File at Shutdown](https://winaero.com/clear-pagefile-shutdown-windows-10), [Encrypt Page File in Windows Vista](https://www.vistax64.com/threads/virtual-memory-paging-file-clear-at-shutdown.157323).

**Windows Hibernate File:**
- Similar to the page file, the hibernate file may contain memory bits used by sandboxed programs.

**System Restore:**
- System Restore may create backup copies in its folders for sandboxed files/programs.
- Moving the sandbox to C:\TEMP\SANDBOX can make System Restore ignore it.

**System, Audit, and Other Event Logs:**
- Windows Event Viewer records information about running programs.
- Security auditing may log details of actions by a program under Sandboxie.

**Windows System Tray Icons:**
- Programs running under Sandboxie place icons in the real system tray.
- Manual clearing of tray icon history in Windows.

**Disk Defragmentation:**
- Sandboxie's isolation occurs at the file level, unaffected by disk defragmentation.

**IP Privacy:**
- Sandboxie's isolation is local, not visible to remote computers.
- Internet access appears the same, and third-party solutions offer anonymous web browsing.

**Windows DNS Host Cache:**
- Sandboxie doesn't prevent logging and storage of DNS Hosts files on the Windows machine.

Note: While Sandboxie prioritizes isolation, user awareness of additional Windows mechanisms is crucial for a comprehensive understanding of privacy implications.
