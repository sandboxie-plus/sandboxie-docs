# No Rename Win Class

_NoRenameWinClass_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies the window class names that should not be translated by Sandboxie.

Usage:
```
   .
   .
   .
   [DefaultBox]
   NoRenameWinClass=ExampleWinClass
   NoRenameWinClass=program.exe,*
```

The first setting tells Sandboxie to not translate _ExampleWinClass_ window class name by making it accessible to sandboxed programs, and goes a step further to disable a few other windowing-related Sandboxie functions. This may also cause the Sandboxie indicator [#] to not appear in window titles.

The second setting tells Sandboxie to not translate window class names created by _program.exe_ by making them accessible to sandboxed programs, and goes a step further to disable a few other windowing-related Sandboxie functions. This may also cause the Sandboxie indicator [#] to not appear in window titles.

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Wnd > Add Wnd Class > Access column > No Rename
