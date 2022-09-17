# Breakout Folder

_BreakoutFolder_  is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.0.8 / 5.55.8. It forces a folder's content to run unsandboxed even if started from inside the sandbox.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BreakoutFolder=C:\Downloads
   BreakoutFolder=E:\
   BreakoutFolder=C:\App\*
   BreakoutFolder=C:\App?
   BreakoutFolder=C:\?pp\*
```

The first example specifies that any content inside the folder "C:\Downloads" will be launched unsandboxed.

Entire drives can also be specified as shown in the second example.

The third and fourth lines show basic characters from wildcards.

- `*` defines any subfolder beyond App folder (App\1, App\1\1 and etc.).
- `?` defines a single character from folder (Appa, App8 and etc.) but not subfolders.

Also, you can combine several wildcards to match the specified folder name and subfolders.

NOTE:
 * Shortcuts that link to a program outside the specified folders will be launched sandboxed. For example: if you place a shortcut inside a broken out folder and it links to some program in a non broken out folder, then the shortcut will launch sandboxed.

Check [BreakoutProcess](BreakoutProcess.md) for information on breaking out programs.

Also check [ForceFolder](ForceFolder.md), the counterpart of this setting, which forces a folder's content to launch sandboxed.
