# Start Command Line

The Sandboxie Start program can do any of the following, depending on command line parameters specified to it.

*   [Start](#start-programs) programs under the supervision of Sandboxie
*   [Stop](#stop-programs) sandboxed programs
*   [List](#list-programs) sandboxed programs
*   [Delete](#delete-contents-of-sandbox) the contents of a sandbox
*   [Reload](#reload-configuration) Sandboxie configuration
*   Initiate the [Disable Forced Programs](#disable-forced-programs) mode
*   [Related](#related-reading-material) reading material

* * *
### Start Programs

This is the default behavior. By specifying a full or partial path to a program's executable file, Sandboxie Start will launch that program under the supervision of Sandboxie:
```
  "C:\Program Files\Sandboxie\Start.exe"  c:\windows\system32\notepad.exe
  "C:\Program Files\Sandboxie\Start.exe"  notepad.exe
```

Two special program names are allowed:
```
  "C:\Program Files\Sandboxie\Start.exe"  default_browser
  "C:\Program Files\Sandboxie\Start.exe"  mail_agent
```

Sandboxie Start can also display the Run Any Program dialog window, or the Sandboxie Start Menu, depending on parameters specified:
```
  "C:\Program Files\Sandboxie\Start.exe"  run_dialog
  "C:\Program Files\Sandboxie\Start.exe"  start_menu
```

In all forms, the parameter _/box:SandboxName_ is applicable, and may be specified between Start.exe and the parameter, to indicate a sandbox name other than the default of _DefaultBox_. For example:
```
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  run_dialog
```

A special form of the /box parameter is _/box:\_\_ask\_\__ and causes Start.exe to display the sandbox selection dialog box.

The parameter _/silent_ can be used to eliminate some pop-up error messages. For example:
```
  "C:\Program Files\Sandboxie\Start.exe"  /silent  no_such_program.exe
```

In both silent and normal operation, Start.exe exits with a zero exit code on success, or non-zero on failure. In batch files, the exit code can be examined using the _IF ERRORLEVEL_ condition.

The parameter _/elevate_ can be used to run a program with Administartor privileges on a system where User Account Control (UAC) is enabled. For example:
```
  "C:\Program Files\Sandboxie\Start.exe"  /elevate cmd.exe
```

The parameter _/env_ can be used to pass an environment variable:
```
  "C:\Program Files\Sandboxie\Start.exe"  /env:VariableName=VariableValueWithoutSpace
  "C:\Program Files\Sandboxie\Start.exe"  /env:VariableName="Variable Value With Spaces"
```

The parameter _/hide_window_ can be used to signal that the starting program should not display its window:
```
  "C:\Program Files\Sandboxie\Start.exe"  /hide_window cmd.exe /c automated_script.bat
```

The parameter _/wait_ can be used to run a program, wait for it to finish, and return the exit status from the program:
```
  "C:\Program Files\Sandboxie\Start.exe"  /wait cmd.exe
```

Note that Start.exe is a Win32 application and not a console application, so the system "start" command is useful here to force the system to wait for Start.exe to finish:
```
  start /wait "C:\Program Files\Sandboxie\Start.exe" /wait cmd /c exit 9
  echo %ERRORLEVEL%
  9
```

The system waits for Start.exe to finish, which in turn waits for "cmd /c exit 9" to finish, and then the exit status 9 is returned all the way back.

Parameters can be combined in any order. For example:
```
   "C:\Program Files\Sandboxie\Start.exe"  /box:CustomBox /silent MyProgram.exe
```

### Stop Programs

Terminate all programs running in a particular sandbox. Note that the request is transmitted to the Sandboxie service SbieSvc, which actually carries out the termination.
```
  "C:\Program Files\Sandboxie\Start.exe"  /terminate
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /terminate
  "C:\Program Files\Sandboxie\Start.exe"  /terminate_all
```

If the parameter _/box:SandboxName_ is omitted, programs running in the default sandbox, _DefaultBox_, will be stopped.

The form _/terminate_all_ terminates all programs in all sandboxes.

* * *

### Unmount Box Images

These commands unmount encrypted box images or RAM disks created by Sandboxie Plus. These parameters are available since v1.11.0 / 5.66.0.
```
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /unmount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount_all
```

If the parameter _/box:SandboxName_ is omitted, default sandbox, _DefaultBox_ image, will be unmounted.

The form _/unmount_all_ terminates all programs in all encrypted sandboxes and unmounts all encrypted box images, including RAM disks created by Sandboxie Plus.

### Mount Box Images

These commands mount encrypted box images created by Sandboxie Plus. These parameters are available since v1.11.0 / 5.66.0.
```
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
```
  "C:\Program Files\Sandboxie\Start.exe"  /listpids
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /listpids
```

If the parameter _/box:SandboxName_ is omitted, programs running in the default sandbox, _DefaultBox_, will be listed.

The output is formatted as one number per line. The first line contains the number of programs, followed by one process ID per line. Example output:
```
    "C:\Program Files\Sandboxie\Start.exe"  /listpids | more
    3
    3036
    2136
    384
```

Note that Start.exe is not a console applications, so the output does not appear in a command prompt window unless you pipe the output using a construct such as `| more`.

* * *

### Delete Contents of Sandbox
```
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
```
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase1
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase2
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase1
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase2
```

* * *

### Reload Configuration

This command reloads the Sandboxie configuration in SandboxieIni into the active Sandboxie driver. Typically useful after manually editing the Sandboxie.ini file.
```
  "C:\Program Files\Sandboxie\Start.exe"  /reload
```

Note that reloading the configuration does not take effect on sandboxed programs that are already running when this command is issued.

* * *

### Disable Forced Programs

The following command runs a program outside the sandbox, even if the program is forced. It is similar to using the Run Outside Sandbox option from the sandbox selection window of the Run Sandboxed command.
```
  "C:\Program Files\Sandboxie\Start.exe"  /dfp            c:\path\to\program.exe
  "C:\Program Files\Sandboxie\Start.exe"  /disable_force  c:\path\to\program.exe
```

Note that /dfp and /disable_force are identical. You can also select this option by holding the Ctrl and Shift keys down when you click the Run Sandboxed command.

An older form of this command can temporarily disable the forced programs mode, for all programs. It is similar in function to using the Disable Forced Programs command from the [Tray Icon Menu](TrayIconMenu.md#disable-forced-programs) in Sandboxie Control (and not the [File Menu](FileMenu.md#disable-forced-programs)).
```
  "C:\Program Files\Sandboxie\Start.exe"  disable_force
```

Note the missing slash in this command syntax. Note also that this command is not a toggle. It always puts the Disable Forced Programs mode into effect and always restarts the countdown timer. At this time, Start.exe does not offer a way to request the cancellation of this mode.

* * *

### Related Reading Material

See also: [InjectDll](InjectDll.md) and [SBIE DLL API](SBIEDLLAPI.md)

Go to [Help Topics](HelpTopics.md).
