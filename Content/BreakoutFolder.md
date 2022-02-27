# BreakoutFolder

_BreakoutFolder_  is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available only for certified project supporters since v1.0.8 / 5.55.8. It forces a folder's content to run unsandboxed even if started from inside the sandbox.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BreakoutFolder=C:\Downloads
   BreakoutFolder=E:\
```

The first example specifies that any content inside the folder "C:\Downloads" will be launched unsandboxed.

Entire drives can also be specified as shown in the second example.

NOTE:
 * Shortcuts that link to a program outside the specified folders will be launched sandboxed. For example: if you place a shortcut inside a broken out folder and it links to some program in a non broken out folder, then the shortcut will launch sandboxed.
 
Check [BreakoutProcess](BreakoutProcess.md) for information on breaking out programs.

Also check [ForceFolder](ForceFolder.md), the counterpart of this setting, which forces a folder's content to launch sandboxed.
