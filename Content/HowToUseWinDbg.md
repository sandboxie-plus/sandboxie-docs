# How To Use Win Dbg

In some rare cases, programs running under the supervision of Sandboxie might not work correctly, without providing any hint to the cause of the malfunction. In these cases, Microsoft's free [Debugging Tools for Windows](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/debugger-download-tools) can help to shed more light on the problem or even to identify the cause of the problem.

* * *

Download and install the latest release of [_Windows SDK_](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk) (both 32-bit and 64-bit).

If you just need the _Debugging Tools for Windows_, you can install the debugging tools as a standalone component.

The package installs into _C:\Program Files (x86)\Windows Kits\10\Debuggers_ by default.

The package creates an application group called _Windows Kits_ in the Windows Start menu. The application group contains the program _WinDbg_.

You probably should use the 32-bit debugger, even on 64-bit Windows. You only need to use the 64-bit debugger to debug 64-bit programs. For more information, see [Choosing the 32-Bit or 64-Bit Debugging Tools](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/choosing-a-32-bit-or-64-bit-debugger-package).

* * *

**Scenario 1: Start a program from the debugger**

Start the debugger under Sandboxie by using the Sandboxie Start menu.

* [Sandboxie Control](SandboxieControl.md) > [Sandbox Menu](SandboxMenu.md) > Run From Start Menu

* Sandboxie Plus window > right click on your sandbox > Run > Run From Start Menu

Then navigate the Sandboxie Start menu to locate and invoke the _WinDbg_ program within the _Windows Kits_ group.

The WinDbg debugger should start and open its main window.

In the debugger, invoke the File menu > Open Executable command. Then navigate to and select the EXE file for the program that you want to run in the debugger.

For example, navigate to and select _C:\Windows\System32\notepad.exe_

The debugger will open a command window, to control (or to debug) the new program.

Use the Debug menu > Go command to begin the execution of the program. (You can also press F5.) At this time the debugger status line will change to say *BUSY*. Proceed to read the section below titled **Final Step**.

* * *

**Scenario 2: Attach the debugger to a running program**

In this scenario, you already used Sandboxie to start the program, and the program is already running.

Start the debugger normally from the Windows Start menu: Locate and invoke the _WinDbg_ program within the _Windows Kits_ group.

The WinDbg debugger should start and open its main window.

In the debugger, invoke the File menu > Attach to a Process command. (You can also press F6.) Then identify the EXE file for the program to which you want to attach the debugger.

The debugger will open a command window, to control (or to debug) the attached program.

If you attached to the a program after it was already exhibiting the problem, then proceed to read the section below titled **Final Step**.

Otherwise use the Debug menu > Go command to continue the execution of the program. (You can also press F5.) At this time the debugger status line will change to say *BUSY*. Proceed to read the section below titled **Final Step**.

* * *

**Final Step**

This section assumes the program in question has already exhibited the problem:

*   If the program gets stuck in a loop, then it should already be stuck.
*   If the program crashes, then it should already have crashed.

If the problem condition has not yet occurred, you should now cause the program to malfunction.

Once the program exhibits the problem, switch back to the WinDbg debugger command window. If the debugger status line still says *BUSY*, use the Debug menu > Break command to stop the program. (You can also press Ctrl+Break.)

When the debugger status line no longer says *BUSY*, enter the following commands. Enter one command at a time, then press Enter.

```
    .sympath srv*C:\Symbols*https://msdl.microsoft.com/download/symbols
    .reload
    ~* k 99
```

The third command will cause the debugger to produce some output. When the command completes, please copy the entire debug log. Use the Edit menu > _Copy Window Text to Clipboard_ command to copy the entire debug log to your clipboard, then go back to the Sandboxie support and paste this debug log into your comment.

Thank you in advance.
