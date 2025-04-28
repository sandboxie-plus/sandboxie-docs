# Open Win Class

_OpenWinClass_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies the class names for unsandboxed windows that should be accessible by a sandboxed program.

Examples:
```
   .
   .
   .
   [DefaultBox]
   OpenWinClass=ConsoleWindowClass
   OpenWinClass=$:program.exe/IgnoreUIPI
   OpenWinClass=#
   OpenWinClass=*
```

The first example makes console windows created by the _cmd.exe_ process accessible to sandboxed programs.

Normally, Sandboxie will not permit a sandboxed program to access, communicate, close or destroy a window outside the sandbox. The _OpenWinClass_ settings makes an exception to this rule, and allows specific unsandboxed windows to be accessible.

**Special Forms**
```
   OpenWinClass=$:program.exe/IgnoreUIPI
```

This permits a program running inside the sandbox to use the PostThreadMessage API to send a message directly to a thread in a target process running outside the sandbox. This form of the _OpenWinClass_ setting does not support wildcards, so the process name of the target process must match the name specified in the setting.
```
   OpenWinClass=#
```

This setting tells Sandboxie to not alter window class names created by sandboxed programs. Normally, Sandboxie translates class names such as _IEFrame_ to _Sandbox:DefaultBox::IEFrame_ in order to better separate windows that belong to sandboxed programs from the rest of the windows in the system.

However, in some cases, a program outside the sandbox might expect window class names to have a specific name, and therefore might not recognize the windows created by a sandboxed program. Specifying OpenWinClass=# resolves this problem, at the cost of a lesser degree of separation.

Note that OpenWinClass=# does not allow communication with any windows outside the sandbox, and may interfere with some drag-and-drop operations.
```
   OpenWinClass=*
```

This setting tells Sandboxie to not translate window class names as described above, and also makes all windows in the system accessible to sandboxed programs, and goes a step further to disable a few other windowing-related Sandboxie functions. This may also cause the Sandboxie indicator [#] to not appear in window titles.

Note that OpenWinClass=* allows full communication with all windows outside the sandbox, but may interfere with some drag-and-drop operations.

**Identifying Window Class Names**

The unsandboxed windows are identified by their _window class name_, which is an internal name given to the window by the application that created it. You can use a tool like [WinSpy](https://www.catch22.net/software/winspy) to identify window class names. The [Resource Access Monitor](ResourceAccessMonitor.md) tool in Sandboxie Classic and the [Trace Logging](../PlusContent/TraceLog.md) tool in Sandboxie Plus also display window class names.

Related Sandboxie Plus settings:

Sandbox Options > Resource Access > Wnd > Add Wnd Class > Access column > Open

Sandbox Options > Resource Access > Wnd > Add Wnd Class > Access column > Ignore UIPI

Sandbox Options > Resource Access > Wnd > Don't alter window class names created by sandboxed programs

See also: [No Rename Win Class](NoRenameWinClass.md).
