# Start Command Line

The Sandboxie Start program can do any of the following, depending on command line parameters specified to it.

*   [Start](#start-programs) programs under the supervision of Sandboxie
*   [Stop](#stop-programs) sandboxed programs
*   [Unmount](#unmount-box-images) encrypted box images
*   [Mount](#mount-box-images) encrypted box images
*   [List](#list-programs) sandboxed programs
*   [Delete](#delete-contents-of-sandbox) the contents of a sandbox
*   [Reload](#reload-configuration) Sandboxie configuration
*   Initiate the [Disable Forced Programs](#disable-forced-programs) mode
*   [Related](#related-reading-material) reading material

* * *
### Start Programs

This is the default behavior. By specifying a full or partial path to a program's executable file, Sandboxie Start will launch that program under the supervision of Sandboxie:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  c:\windows\system32\notepad.exe
  "C:\Program Files\Sandboxie\Start.exe"  notepad.exe
```

Two special program names are allowed:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  default_browser
  "C:\Program Files\Sandboxie\Start.exe"  mail_agent
```

Sandboxie Start can also display the Run Any Program dialog window, or the Sandboxie Start Menu, depending on parameters specified:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  run_dialog
  "C:\Program Files\Sandboxie\Start.exe"  start_menu
```

In all forms, the parameter _/box:SandboxName_ is applicable, and may be specified between Start.exe and the parameter, to indicate a sandbox name other than the default of _DefaultBox_. For example:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  run_dialog
```

A special form of the /box parameter is _/box:\_\_ask\_\__ and causes Start.exe to display the sandbox selection dialog box.

The parameter _/silent_ can be used to eliminate some pop-up error messages. For example:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /silent  no_such_program.exe
```

In both silent and normal operation, Start.exe exits with a zero exit code on success, or non-zero on failure. In batch files, the exit code can be examined using the _IF ERRORLEVEL_ condition.

The parameter _/elevate_ can be used to run a program with Administrator privileges on a system where User Account Control (UAC) is enabled. For example:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /elevate cmd.exe
```

The parameter _/env_ can be used to pass an environment variable:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /env:VariableName=VariableValueWithoutSpace
  "C:\Program Files\Sandboxie\Start.exe"  /env:VariableName="Variable Value With Spaces"
```

The parameter _/hide_window_ can be used to signal that the starting program should not display its window:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /hide_window cmd.exe /c automated_script.bat
```

The parameter _/wait_ can be used to run a program, wait for it to finish, and return the exit status from the program:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /wait cmd.exe
```

Note that Start.exe is a Win32 application and not a console application, so the system "start" command is useful here to force the system to wait for Start.exe to finish:
```cmd
  start /wait "C:\Program Files\Sandboxie\Start.exe" /wait cmd /c exit 9
  echo %ERRORLEVEL%
  9
```

The system waits for Start.exe to finish, which in turn waits for "cmd /c exit 9" to finish, and then the exit status 9 is returned all the way back.

Parameters can be combined in any order. For example:
```cmd
   "C:\Program Files\Sandboxie\Start.exe"  /box:CustomBox /silent MyProgram.exe
```

### Stop Programs

Terminate all programs running in a particular sandbox. Note that the request is transmitted to the Sandboxie service SbieSvc, which actually carries out the termination.
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /terminate
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /terminate
  "C:\Program Files\Sandboxie\Start.exe"  /terminate_all
```

If the parameter _/box:SandboxName_ is omitted, programs running in the default sandbox, _DefaultBox_, will be stopped.

The form _/terminate_all_ terminates all programs in all sandboxes.

* * *

### Unmount Box Images

These commands unmount encrypted box images or RAM disks created by Sandboxie Plus. These parameters are available since v1.11.0 / 5.66.0.
```cmd
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /unmount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount_all
```

If the parameter _/box:SandboxName_ is omitted, default sandbox, _DefaultBox_ image, will be unmounted.

The form _/unmount_all_ terminates all programs in all encrypted sandboxes and unmounts all encrypted box images, including RAM disks created by Sandboxie Plus.

### Mount Box Images

> [!WARNING]
> When using `/key:password` parameter with `Start.exe`, the password will be visible in command line history, process lists, and potentially event logs. Use this parameter only in secure environments or consider interactive password prompts instead.

These commands mount encrypted box images created by Sandboxie Plus. These parameters are available since v1.11.0 / 5.66.0.
```cmd
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /key:[box image password] /mount_protected
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /key:[box image password] /mount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /key:[box image password] /mount_protected
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /key:[box image password] /mount
```

If the parameter _/box:SandboxName_ is omitted, default sandbox, _DefaultBox_ image, will be mounted.

The form _/mount_protected_ mounts encrypted box images with the _Box Root Protection_. _Box Root Protection_ prevents processes running outside the sandbox from accessing the root folder of the encrypted box.

* * *

### List Programs

List the system process ID numbers for all programs running in a particular sandbox.
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /listpids
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /listpids
```

If the parameter _/box:SandboxName_ is omitted, programs running in the default sandbox, _DefaultBox_, will be listed.

The output is formatted as one number per line. The first line contains the number of programs, followed by one process ID per line. Example output:
```cmd
    "C:\Program Files\Sandboxie\Start.exe"  /listpids | more
    3
    3036
    2136
    384
```

Note that Start.exe is not a console applications, so the output does not appear in a command prompt window unless you pipe the output using a construct such as `| more`.

* * *

### Delete Contents of Sandbox
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent
```

The _/box:SandboxName_ parameter may be specified between Start.exe and the delete command.

The __silent_ suffix on the delete command, indicates Sandboxie Start should silently ignore any errors and not display any error messages.

The delete operation occurs in two phases:

*   Phase 1 scans the contents of the sandbox and processes files which could pose a problem during the second phase:
    *   Junctions (also known as reparse points) are removed.
    *   Read-only files and directories are made fully accessible.
    *   Files and directories that have very long names are renamed to shorter names.
    *   Renames the sandbox to the format `__Delete_(sandbox name)_(some random number)`. For example, if the sandbox is DefaultBox, it could be renamed to `__Delete_DefaultBox_01C4012345678912`.

*   Phase 2 deletes any sandboxes that were processed in phase 1\.
    *   Sandboxes that were processed in phase 1 are those that have been renamed as described above.
    *   More than one sandbox may be deleted in phase 2\.
    *   By default, the standard system command RMDIR is used to delete the renamed sandbox folder.
    *   Alternatively, a third-party delete utility may used. See [Secure Delete Sandbox](SecureDeleteSandbox.md).

Issuing the _delete_sandbox_ command causes Start.exe to invoke phase 1 followed by phase 2\. Start.exe also accepts these commands to invoke a specific phase:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase1
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase2
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase1
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase2
```

* * *

### Reload Configuration

This command reloads the Sandboxie configuration in SandboxieIni into the active Sandboxie driver. Typically useful after manually editing the Sandboxie.ini file.
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /reload
```

Note that reloading the configuration does not take effect on sandboxed programs that are already running when this command is issued.

* * *

### Disable Forced Programs

The following command runs a program outside the sandbox, even if the program is forced. It is similar to using the Run Outside Sandbox option from the sandbox selection window of the Run Sandboxed command.
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /dfp            c:\path\to\program.exe
  "C:\Program Files\Sandboxie\Start.exe"  /disable_force  c:\path\to\program.exe
```

Note that /dfp and /disable_force are identical. You can also select this option by holding the Ctrl and Shift keys down when you click the Run Sandboxed command.

An older form of this command can temporarily disable the forced programs mode, for all programs. It is similar in function to using the Disable Forced Programs command from the [Tray Icon Menu](TrayIconMenu.md#disable-forced-programs) in Sandboxie Control (and not the [File Menu](FileMenu.md#disable-forced-programs)).
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  disable_force
```

Note the missing slash in this command syntax. Note also that this command is not a toggle. It always puts the Disable Forced Programs mode into effect and always restarts the countdown timer. At this time, Start.exe does not offer a way to request the cancellation of this mode.

* * *

### Advanced / Internal switches

The following switches are intended primarily for advanced usage, automation, or internal/debugging scenarios. They are implemented in the Start.exe source (`start.cpp`). These options may change across versions and are not typically needed by end users.

#### /keep_alive
Keep Start.exe alive and supervise the started program. This switch implements a restart loop (supervisor) rather than a simple one-shot wait. The behavior implemented in `start.cpp` is:

> [!Note]
> `/keep_alive` is only effective when the supervising `Start.exe` instance runs inside the sandbox (the boxed instance). When run outside a sandbox it has no effect.

- Start.exe captures the launched process handle (it uses ShellExecuteEx/CreateProcess with SEE_MASK_NOCLOSEPROCESS when waiting).
- Start.exe waits for the child process to exit and reads its exit code with GetExitCodeProcess.
- If the child exits with EXIT_SUCCESS (zero), Start.exe finishes and returns that zero exit code.
- If the child exits with a non-zero code, and `/keep_alive` is still in effect, Start.exe will attempt to restart the program and supervise it again. The loop retries a limited number of times:
  - The implementation increments a retry counter and will retry while the counter is less than 5 (i.e., up to 5 retries).
  - Very short runs (the code treats runs shorter than ~5 seconds as initialization failures) contribute to the retry count; longer runs reset the failure counter.
- If the program cannot be started at all, Start disables keep-alive for that invocation (no retries).

In short: use `/keep_alive` when you want Start.exe to remain the supervising parent and to automatically restart the launched program on non-graceful exits (with a small retry/backoff policy). This differs from `/wait`: `/wait` causes Start.exe to wait and then exit when the child exits; `/keep_alive` keeps Start.exe supervising and will restart the child when it crashes or exits non-zero, up to the retry limit.

Final result:
- On a successful (0) exit the final returned exit code is 0.
- If retries are exhausted and the program keeps exiting with non-zero codes, Start.exe will stop retrying and return the last non-zero exit code.

Example:
```cmd
"Start.exe" /keep_alive notepad.exe
"Start.exe" Start.exe /keep_alive notepad.exe
```
This is useful when you want the started program to remain available inside the box (restarted after crashes) and also keep Start.exe as the supervising parent process for the session.

#### /fake_admin

Mark the started program as having a faked Administrator context inside the sandbox. This can help some installers or legacy programs that detect administrator state and behave differently. This is a sandbox-side compatibility measure and is not the same as a real UAC elevation.

Example:
```cmd
"Start.exe" /fake_admin setup.exe
```

#### /force_children (or /fcp)

Mark the started process so that any child processes it creates will be forced into the specified sandbox. It does not, by itself, place the initially started program (e.g. the installer) into the sandbox. Start.exe issues an API call to force children when this option is present.

Example:
```cmd
"Start.exe" /fcp myinstaller.exe
"Start.exe" /force_children myinstaller.exe
```

#### /env:=Refresh

Trigger an environment refresh for the currently boxed process. When invoked from a boxed instance Start.exe calls an internal `Env_Refresh` helper; when run outside a sandbox it has no effect. Use `/env:Name=Value` to set individual environment variables instead.

Example:
```cmd
"Start.exe" /env:=Refresh
```

#### /uac_prompt

Invoke Sandboxie's secure UAC prompt UI (the boxed UAC dialog) with parameters. This is primarily an internal helper used by other Sandboxie components to display a secure UAC prompt. The command accepts internal parameters used to populate the dialog (typically generated by service/agent code).

Example:
```cmd
"Start.exe" uac_prompt <internal-pkt-params>
```

#### mount_hive

Request the sandboxed instance to mount a registry hive copy for access by boxed programs. When invoked outside the sandbox Start.exe forwards the command to the boxed instance so the boxed instance performs the mount; when invoked inside the sandbox the mount is performed directly.

Example:
```cmd
"Start.exe" mount_hive
```

#### run_sbie_ctrl and open_agent[:param]

Internal service control commands used to ask the Sandboxie service/agent to run Sandboxie Agent or perform agent tasks. `run_sbie_ctrl` sends a request to the service to launch the Agent UI. `open_agent:` can pass an argument to the agent/service. These are primarily used by helper tooling and automation.

Example:
```cmd
"Start.exe" run_sbie_ctrl
"Start.exe" open_agent:SandMan.exe
"Start.exe" open_agent:"SandMan.exe -autorun"
```

* * *  

### Related Reading Material

See also: [InjectDll](InjectDll.md) and [SBIE DLL API](SBIEDLLAPI.md)

Go to [Help Topics](HelpTopics.md).
