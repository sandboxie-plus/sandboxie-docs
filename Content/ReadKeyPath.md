# Read Key Path

_ReadKeyPath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni). It specifies a path patterns, for which Sandboxie will not apply sandboxing for registry keys, and will not allow writing.

[Program Name Prefix](ProgramNamePrefix) may be specified.

Example:
```
   .
   .
   .
   [DefaultBox]
   ReadKeyPath=HKEY_LOCAL_MACHINE\SOFTWARE\Policies
```

This example forces the _Policies_ key, and everything below it, to be readable, but not writable (or deletable) by sandboxed programs.

Note: _ReadKeyPath_ is a restricted form of [OpenKeyPath](OpenKeyPath). As with _OpenKeyPath_, any already-existing sandboxed contents for the specified file or folder locations, are ignored.

Related [Sandboxie Control](SandboxieControl) setting: [Sandbox Settings > Resource Access > Registry Access > Read-Only Access](ResourceAccessSettings#key)
