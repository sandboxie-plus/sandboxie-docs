# Recover Folder

_RecoverFolder_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies the sandboxed folders that [Quick Recovery](QuickRecovery.md) should examine. [Shell Folders](ShellFolders.md) may be specified. For example:
```
   .
   .
   .
   [DefaultBox]
   RecoverFolder=%Personal%
   RecoverFolder=C:\Downloads
   [InstallBox]
   RecoverFolder=D:\Program Files
```

The first two example settings specify that [Quick Recovery](QuickRecovery.md) from the DefaultBox sandbox should look in the _Documents_ and the _Downloads_ folders in drive C.

The third example setting specifies that QuickRecovery from the InstallBox sandbox should look in the _Program Files_ folder in drive D.

Note that when [Quick Recovery](QuickRecovery.md) looks in the specified folder, it also looks in any folders within that folder, and any folders within those folders, for as many levels of depth as are needed.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Recovery > Quick Recovery](RecoverySettings.md#quick-recovery)
