# Write File Path

WriteFilePath is a sandbox setting in [Sandboxie Ini](SandboxieIni). It specifies path patterns for which Sandboxie will hide any files or folders outside the sandbox, while allowing new files and folders to be created in the sandbox.

[Shell Folders](ShellFolders) may be specified. [Program Name Prefix](ProgramNamePrefix) may be specified.

Examples:
```
   .
   .
   .
   [DefaultBox]
   WriteFilePath=%Cookies%
```

This example means that program in the sandbox will not be able to see any files within the Internet Explorer cookies folder outside the sandbox, but may create files in the corresponding folder in the sandbox. In other words, existing cookies outside the sandbox will not be visible, but the program may create new cookies as if the cookie folder was empty.

This setting is not applicable to files. If the path specified in the setting matches a file, the file will be treated as if it matches a ClosedFilePath setting.

Note: WriteFilePath is implemented internally as an enhanced form of [ClosedFilePath](ClosedFilePath).

Related [Sandboxie Control](SandboxieControl) setting: [Sandbox Settings > Resource Access > File Access > Write-Only Access](ResourceAccessSettings#file) 