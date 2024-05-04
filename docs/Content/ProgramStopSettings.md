# Program Stop Settings

### "Program Stop" Settings Group

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Program Stop:

![](../Media/ProgramStopSettings.png)

Settings in this section control when Sandboxie automatically ends programs that run in the sandbox.

* * *

### Lingering Programs

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Program Stop > Lingering Programs

![](../Media/LingeringProgramsSettings.png)

When one sandboxed program starts another program, that other program will be started in the same sandbox. However, the end of first program does not necessarily mean that the second program ends as well. This means that the sandbox can still be active after the primary program in the sandbox has been stopped.

For example, viewing a PDF file in Internet Explorer may cause the Adobe Acrobat Reader program (acrord32.exe) to start in the sandbox. The Reader program will linger in the sandbox even after the Internet Explorer program has ended. This behavior is usually not desired.

Use this settings page to identify the programs that Sandboxie should automatically stop, if they are lingering in the sandbox after all other (non-lingering) programs have ended.


You can also configure this setting in the [Program Settings](ProgramSettings.md) window.


(Note that acrord32.exe is already a default setting.)

Note: When no program is running in the sandbox, and you explicitly start one of the lingering programs, then that program will not be considered a lingering program, and will not be stopped automatically. For example, if nothing is running in the sandbox, and you explicitly start Adobe Acrobat Reader sandboxed, then Sandboxie will not immediately stop this program.

Related [Sandboxie Ini](SandboxieIni.md) setting: [LingerProcess](LingerProcess.md).

* * *

### Leader Programs

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Program Stop > Leader Programs

![](../Media/LeaderProgramsSettings.png)

When this sandboxed program ends, Sandboxie will stop all other programs in the sandbox.

Use this settings page to identify those programs that should be considered primary programs in the sandbox, such that whenever they finish and stop, all other programs in the sandbox are stopped as well.

For example, if you have a sandbox dedicated for Web browsing, then rather than listing all possible lingering programs (see [Lingering Programs](ProgramStopSettings.md#lingering-programs) above for a discussion of a lingering program),you can list just the Web browser program as the leader program.

You can also configure this setting in the [Program Settings](ProgramSettings.md) window.

Related [Sandboxie Ini](SandboxieIni.md) setting: [LeaderProcess](LeaderProcess.md).
