# Recover Folder

_RecoverFolder_ is a sandbox setting in [Sandboxie Ini](SandboxieIni). It specifies the sandboxed folders that [Quick Recovery](QuickRecovery) should examine. [Shell Folders](ShellFolders) may be specified. For example:
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

The first two example settings specify that [Quick Recovery](QuickRecovery) from the DefaultBox sandbox should look in the _My Documents_, and the _Downloads_ folders in drive C.

The third example setting specifies that QuickRecovery from the InstallBox sandbox should look in the _Program Files_ folder in drive D.

Note that when [Quick Recovery](QuickRecovery) looks in the specified folder, it also looks in any folders within that folder, and any folders within those folders, for as many levels of depth as are needed.

Related [Sandboxie Control](SandboxieControl) setting: [Sandbox Settings > Recovery > Quick Recovery](RecoverySettings#quick)
