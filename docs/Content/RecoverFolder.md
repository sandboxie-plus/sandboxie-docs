# Recover Folder

_RecoverFolder_ is a repeatable sandbox setting in [Sandboxie Ini](SandboxieIni.md). It identifies recoverable locations for both [Quick Recovery](QuickRecovery.md) and automatic [Immediate Recovery](ImmediateRecovery.md) detection when `AutoRecover=y`. Effective entries can include enabled templates. [Shell Folders](ShellFolders.md) may be specified. For example:
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

For a literal directory entry, [Quick Recovery](QuickRecovery.md) scans that folder and its subfolders recursively. Automatic detection instead checks eligible file activity against the configured entries.

Since Sandboxie Plus 1.18.0, entries may contain wildcard patterns using `*`, `?`, and `**`. A wildcard entry filters candidate paths; it does not itself establish an arbitrary recursive Quick Recovery scan root. Matching can consider translated NT, DOS, and network-alias paths. The precise pattern handling differs between the process-side detector and SandMan's Quick Recovery list, so do not treat these symbols as a universal filesystem glob grammar.

See [File Recovery Architecture](RecoveryArchitecture.md) for the two consumers and their different lifecycles.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Recovery > Quick Recovery](RecoverySettings.md#quick-recovery)
