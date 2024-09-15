# Block Network Files

BlockNetworkFiles is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies whether Sandboxie will block sandboxed programs from accessing network files and folders without specifically opened.
```
   .
   .
   .
   [DefaultBox]
   BlockNetworkFiles=n
```

Specifying _n_ indicates that a sandboxed program may access network files without specifically opened, in this case "Net Share" will appear in sandbox status.

Related Sandboxie Plus setting: Sandbox Options > Network Options > Other Options > Block network files and folders, unless specifically opened

Related Sandboxie Plus setting when creating a new sandbox with "Configure advanced options" selected: Sandbox Isolation options > Network Access > Allow access to network files and folders
