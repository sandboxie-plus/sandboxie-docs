# Delete Command

DeleteCommand is a legacy sandbox setting in [Sandboxie Ini](SandboxieIni.md) that remains functional in Sandboxie Control Classic and `Start.exe`. It specifies the command used by that deletion path to physically remove the contents of the sandbox. Its primary purpose is to make it possible to plug a third-party secure deletion utility into Sandboxie. See [Secure Delete Sandbox](SecureDeleteSandbox.md).

SandMan uses the separate [`OnBoxDelete`](SandManTriggers.md#onboxdelete) trigger for configured host-side automation before it cleans sandbox contents. `OnBoxDelete` is not a renamed `DeleteCommand`: the trigger runs before SandMan cleanup, while `DeleteCommand` selects the command that performs directory deletion in the legacy Classic/`Start.exe` path.

Usage:
```
   .
   .
   .
   [DefaultBox]
   DeleteCommand=%SystemRoot%\System32\cmd.exe /c RMDIR /s /q "%SANDBOX%"
```

The example is the default setting used when DeleteCommand is not explicitly specified, and invokes the Windows RMDIR command to remove the sandbox folder.

For more examples, see [Secure Delete Sandbox](SecureDeleteSandbox.md).

***

When specifying this setting, make sure to include **"%SANDBOX%"** (with quote marks) in the command.

***

Note: Secure deletion is a privacy measure, not a security measure. Both regular deletion and secure deletion effectively remove undesired software that was collected into the sandbox. See [Secure Delete Sandbox](SecureDeleteSandbox.md).

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Delete > Command](DeleteSettings.md#command)

Related SandMan documentation: [SandMan Triggers](SandManTriggers.md)
