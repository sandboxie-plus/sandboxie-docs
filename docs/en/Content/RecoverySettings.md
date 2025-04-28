# Recovery Settings

### "Recovery" Settings Group

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Recovery:

![](../Media/RecoverySettings.png)

While you can manually explore the contents of the sandbox and extract the files you need, Sandboxie has a [Quick Recovery](QuickRecovery.md) tool that scans particular folders and informs you if any files are available for recovery out of the sandbox. The Recovery group configures this tool.

* * *

### Quick Recovery

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Recovery > Quick Recovery:

![](../Media/QuickRecoverySettings.png)

Use this settings page to add and remove folders that should be scanned by Sandboxie.

You can also influence this setting indirectly:


*   In [Files And Folders View](FilesAndFoldersView.md), by right-clicking on _folder_ items and invoking the actions _Add Folder to Quick Recovery_ or _Remove Folder from Quick Recovery_.


*   In the [Delete Sandbox](DeleteSandbox.md) or [Quick Recovery](QuickRecovery.md) windows, by clicking the _Add Folder_ button.


Related [Sandboxie Ini](SandboxieIni.md) setting: [RecoverFolder](RecoverFolder.md).

* * *

### Immediate Recovery

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Recovery > Immediate Recovery:

![](../Media/ImmediateRecoverySettings.png)

The Quick Recovery tool scans folders only when invoked, which is either explicitly, or when the sandbox is about to be deleted. [Immediate Recovery](ImmediateRecovery.md) is an extension which notifies you about recoverable files as soon as they are created by a sandboxed program.

This behavior is usually useful and is enabled by default, but it may be disabled if so desired.

It may also be desirable to keep Immediate Recovery enabled, but exclude some file types from Immediate Recovery. For example: You may want to receive Immediate Recovery notifications about document files saved to the (sandboxed) desktop, but not about shortcuts (_.LNK_) files that may be created on the desktop during the installation of sandboxed programs.

Use this settings page to enable or disable the Immediate Recovery extension, and configure exclusions to Immediate Recovery.

Related [Sandboxie Ini](SandboxieIni.md) settings: [AutoRecover](AutoRecover.md), [AutoRecoverIgnore](AutoRecoverIgnore.md).
