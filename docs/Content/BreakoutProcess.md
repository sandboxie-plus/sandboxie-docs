# Breakout Process

_BreakoutProcess_  is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.0.8 / 5.55.8. It specifies which applications shall run unsandboxed when launched within the sandbox. A combination of this and _ForceProcess_ allows for a simple priority system.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BreakoutProcess=ProgramName.exe
   BreakoutProcess=Program*.exe
   BreakoutProcess=Program?.exe
   BreakoutProcess=Pro?ram*.exe
```

- `*` defines any name after Program (Program0Test1.exe, Program5Test92G.exe and etc.).
- `?` defines one character from name (Program1.exe, Programg.exe and etc.).

Also, you can combine several wildcards to match the specified name.

Specifying _ProgramName_ indicates the application that should be launched unsandboxed. Alternatively, the program's path can be specified.

Priority System:
If you set a program to breakout from a sandbox and force it to be sandboxed in another, this acts as a useful priority system.

Example:
Let's say you happen to use your browser as a PDF viewer and have 2 sandboxes "Browser" and "Email". Assume you received a PDF through an email and would rather have the PDF launch a browser tab in the respective "Browser" sandbox rather than the current ("Email") sandbox. You can break out your browser exe in the "Email" sandbox and force it in the "Browser" sandbox.

Check [ForceProcess](ForceProcess.md) for more information.
