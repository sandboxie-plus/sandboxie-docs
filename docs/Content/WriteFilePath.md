# Write File Path

WriteFilePath is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for box-only file access: host-side contents are normally hidden from ordinary file opens, while files and folders may be created in the corresponding sandbox location.

[Shell Folders](ShellFolders.md) may be specified. [Program Name Prefix](ProgramNamePrefix.md) may be specified.

Examples:
```
   .
   .
   .
   [DefaultBox]
   WriteFilePath=%Cookies%
```

This example means that a program in the sandbox normally cannot open existing cookies in the Internet Explorer cookies folder outside the sandbox, but may create files in the corresponding folder in the sandbox. The host cookies are treated as absent for ordinary file opens; sandbox-side creation still depends on the requested operation and access checks.

WriteFilePath applies to matching file paths as well as folder paths. "Write Only" does not prohibit reading sandboxed contents: an existing sandbox copy can remain readable when the operation and granted handle rights permit it.

Unlike [ClosedFilePath](ClosedFilePath.md), which closes both host and sandbox-copy access, a selected WriteFilePath rule normally closes the host side while permitting the sandbox-copy side.

Permitting sandbox-copy access does not guarantee that an operation succeeds. The result depends on the effective rule, existing sandbox-copy state, requested operation and access rights, file and folder creation conditions, Windows permissions, and applicable virtualization and enforcement paths.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Resource Access > File Access > Write-Only Access](ResourceAccessSettings.md#file-access-write-only-access)

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Files > Add File/Folder > Access column > Box Only (Write Only)
