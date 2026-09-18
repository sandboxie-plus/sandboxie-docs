# Secure Delete Sandbox

Typical file deletion makes data inaccessible to the operating system and programs, but the data is not physically wiped from the hard drive storage medium, and may be recovered by a data recovery technician. To make this recovery more difficult, third-party software exists that can perform a _secure deletion._ This is typically accomplished by overwriting the data multiple times before deleting it.

For more information, see [Data remanence in Wikipedia](https://en.wikipedia.org/wiki/Data_remanence).

By default, the Sandboxie Control Classic/`Start.exe` deletion path uses the standard Windows _RMDIR_ command to delete folders. This makes sure the contents of the sandbox (including malicious software) are properly removed from the operating system. But as mentioned above, it leaves the data vulnerable to inspection and recovery by forensics experts.

People who are concerned about the privacy of their sensitive data can plug a third-party secure deletion utility into the Classic/`Start.exe` deletion path, to be used instead of the standard command.

For the Classic/`Start.exe` deletion path, you can configure a custom delete command through Sandboxie Control or by manually editing the [Sandboxie Ini](SandboxieIni.md) configuration file.

SandMan instead provides [`OnBoxDelete`](SandManTriggers.md#onboxdelete), a host-side trigger that runs configured automation before SandMan performs its own cleanup. It is not the same mechanism as `DeleteCommand`, and enabling the trigger does not by itself change SandMan's deletion method or guarantee secure erasure.

**In Sandboxie Control**

Use [Sandbox Settings > Delete > Command](DeleteSettings.md#command). A couple of examples for the Delete Command:

*   Invoke [Eraser by Heidi Computers](https://eraser.heidi.ie/) to delete the contents securely:
```
    %SystemRoot%\System32\eraserl.exe -folder "%SANDBOX%" -subfolders -method DoD_E -resultsonerror -queue
```

*   Invoke [SDelete by SysInternals/Microsoft](https://technet.microsoft.com/en-us/sysinternals/bb897443.aspx) to delete the contents securely.
```
    "C:\Program Files\Sysinternals\SDelete\sdelete.exe" -p 3 -s -q "%SANDBOX%"
```

**In the Sandboxie.ini Configuration File**

To configure a custom delete command for a particular sandbox, edit or insert the [DeleteCommand](DeleteCommand.md) setting in the sandbox section of [Sandboxie Ini](SandboxieIni.md).

To configure a global custom delete command, edit or insert the [DeleteCommand](DeleteCommand.md) setting in the [GlobalSettings] section of [Sandboxie Ini](SandboxieIni.md).


When specifying this setting, make sure to include **"%SANDBOX%"** (with quote marks) in the command.

Before launching the delete command, Sandboxie scans the sandbox to make sure all files can be properly deleted, as described in [Delete Contents of Sandbox](StartCommandLine.md#delete-contents-of-sandbox).

* * *

Go to [Help Topics](HelpTopics.md).
