# Break Out

_BreakOut_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies which apps shall run unsandboxed when launched within the sandbox. A combination of this and _ForceProcess_ allows for a simple priority system.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BreakoutProcess=ProgramName.exe
```

Specifying _ProgramName_ indicates the application that should be launched unsandboxed. Alternatively, the program's path can be specified. This statement can be repeated for all the applications that the user wishes to launch unsandboxed.

Priority System:
If you set a program to breakout from a sandbox and force it to be sandboxed in another, this acts as a useful priority system.

Example:
Say you happen to use your browser as a PDF viewer and have 2 sandboxes "Browser" and "Email". Assume you received a PDF through an email and would rather have the PDF launch a browser tab in the respective "Browser" sandbox rather than the current ("Email") sandbox. You can break out your browser exe in the "Email" sandbox and force it in the "Browser" sandbox.

Check [ForceProcess](ForceProcess.md) for more information.
