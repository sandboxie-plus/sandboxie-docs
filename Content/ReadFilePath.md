# Read File Path

_ReadFilePath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni). It specifies path patterns for which Sandboxie will not apply sandboxing for files, and will not allow writing.

[Shell Folders](ShellFolders) may be specified. [Program Name Prefix](ProgramNamePrefix) may be specified.

Examples:
```
   .
   .
   .
   [DefaultBox]
   ReadFilePath=C:\WINDOWS
```

This example forces the C:\WINDOWS folder, and everything below it, to be readable, but not writable (or deletable) by sandboxed programs.

Note: _ReadFilePath_ is a restricted form of [OpenFilePath](OpenFilePath). As with _OpenFilePath_, any already-existing sandboxed contents for the specified file or folder locations, are ignored.

Related [Sandboxie Control](SandboxieControl) setting: [Sandbox Settings > Resource Access > File Access > Read-Only Access](ResourceAccessSettings#file)
