# File Migration Settings

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > File Migration:

![](../Media/FileMigrationSettings.png)

Before a sandboxed program can make changes to a file that already exists in your computer, Sandboxie first must make a copy of this file in the sandbox. However, making copies of very large files would be a long operation. For this reason, Sandboxie will only make copies of files that are below a certain maximum size. Files larger than this size will be considered read-only inside the sandbox, and any attempt to modify them will result in message [SBIE2102](SBIE2102.md).

Use this settings page to set the maximum size threshold, and whether or not you wish to see message [SBIE2102](SBIE2102.md) issued when an attempt is made to modify files larger than that maximum size.

Related [Sandboxie Ini](SandboxieIni.md) settings: [CopyLimitKb](CopyLimitKb.md), [CopyLimitSilent](CopyLimitSilent.md).
