# Auto Exec

_AutoExec_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies a list of commands that are executed every time the sandbox is initially populated.

Examples:

```
   .
   .
   .
   [DefaultBox]
   AutoExec=regedit /s c:\defaultbox.reg
   AutoExec=cmd /c del /f "%windir%\system32\someExploitableDLL.dll"
```

The first example shows using _AutoExec_ to populate the sandboxed registry in some way. The second example shows using _AutoExec_ to delete an undesirable DLL file. In both cases the customization takes place only within the sandbox.

Multiple _AutoExec_ settings may be specified for a single sandbox. The commands listed are executed one by one. The commands (whether one or any number of them) are executed _once_ in the life-time of a particular sandbox. To get Sandboxie to execute these commands again, the sandbox must be deleted.

This is true even if the command execution fails -- it will not be executed again, unless the sandbox is deleted.

At this time, there is no corresponding [Sandboxie Control](SandboxieControl.md) configuration for this setting.

**Technical Details**

Each _AutoExec_ command, as it is executed by Sandboxie, is recorded in the registry of that sandbox, in the key _HKEY_CURRENT_USER\Software\SandboxieAutoExec_.

The command will not be executed if it was already recorded in the sandboxed registry. Thus, deleting the sandbox clears all recorded _AutoExec_ commands, so they are executed again the next time any sandboxed program starts in that sandbox. But it is also possible to get them to execute again, by manually deleting the command from that sandboxed registry key.
