# Start Command Line

The Sandboxie Start program can do any of the following, depending on command line parameters specified to it.

*   [Start](#start) programs under the supervision of Sandboxie
*   [Stop](#stop) sandboxed programs
*   [List](#list) sandboxed programs
*   [Delete](#delete) the contents of a sandbox
*   [Reload](#reload) Sandboxie configuration
*   Initiate the [Disable Forced Programs](#disableforce) mode
*   [Related](#related) reading material

* * *
### Start Programs  <a name="start" href="#start">#</a>

This is the default behavior. By specifying a full or partial path to a program executable file, Sandboxie Start will launch that program under the supervision of Sandboxie:
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  c:\windows\system32\calc.exe
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  calc.exe
```

Two special program names are allowed:
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  default_browser
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  mail_agent	
```

Sandboxie Start can also display the Run Any Program dialog window, or the Sandboxie Start Menu, depending on parameters specified:
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  run_dialog
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  start_menu	
```

In all forms, the parameter _/box:SandboxName_ is applicable, and may be specified between Start.exe and the parameter, to indicate a sandbox name other than the default of _DefaultBox_. For example:
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /box:TestBox  run_dialog	
```

A special form of the /box parameter is _/box:_**_ask_**__ and causes Start.exe to display the sandbox selection dialog box.

The parameter _/nosbiectrl_ can be used to make sure Start.exe does not try to run [Sandboxie Control](SandboxieControl.md) before running the sandboxed program.
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /nosbiectrl calc.exe	
```

The parameter _/silent_ can be used to eliminate some pop-up error messages. For example:
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /silent  no_such_program.exe
```

In both silent and normal operation, Start.exe exits with a zero exit code on success, or non-zero on failure. In batch files, the exit code can be examined using the _IF ERRORLEVEL_ condition.

The parameter _/elevate_ can be used to run a program with Administartor privileges on a system where User Account Control (UAC) is enabled. For example:
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /elevate cmd.exe	
```

The parameter _/env_ can be used to pass an environment variable:
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /env:VariableName=VariableValueWithoutSpace
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /env:VariableName=&quot;Variable Value With Spaces&quot;	
```

The parameter _/hide_window_ can be used to signal that the starting program should not display its window:
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /hide_window cmd.exe /c automated_script.bat	
```

The parameter _/wait_ can be used to run a program, wait for it to finish, and return the exit status from the program:
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /wait cmd.exe	
```

Note that Start.exe is a Win32 application and not a console application, so the system "start" command is useful here to force the system to wait for Start.exe to finish:
```
  start /wait &quot;C:\Program Files\Sandboxie\Start.exe&quot; /wait cmd /c exit 9
  echo %ERRORLEVEL%
  9	
```

The system waits for Start.exe to finish, which in turn waits for "cmd /c exit 9" to finish, and then the exit status 9 is returned all the way back.

Parameters can be combined in any order. For example:
```
   &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /box:CustomBox /silent /nosbiectrl MyProgram.exe	
```

### Stop Programs <a name="stop" href="#stop">#</a>

Terminate all programs running in a particular sandbox. Note that the request is transmitted to the Sandboxie service SbieSvc, which actually carries out the termination.
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /terminate
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /box:TestBox  /terminate
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /terminate_all
```

If the parameter _/box:SandboxName_ is omitted, programs running in the default sandbox, _DefaultBox_, will be stopped.

The form _/terminate_all_ terminates all programs in all sandboxes.

* * *

### List Programs <a name="list" href="#list">#</a>

List the system process ID numbers for all programs running in a particular sandbox.
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /listpids
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /box:TestBox  /listpids	
```

If the parameter _/box:SandboxName_ is omitted, programs running in the default sandbox, _DefaultBox_, will be listed.

The output is formatted as one number per line. The first line contains the number of programs, followed by one process ID per line. Example output:
```
    &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /listpids | more
    3
    3036
    2136
    384	
```

Note that Start.exe is not a console applications, so the output does not appear in a command prompt window unless you pipe the output using a construct such as _| more_.

* * *

### Delete Contents of Sandbox <a name="delete" href="#delete">#</a>
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  delete_sandbox
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  delete_sandbox_silent	
```

The _/box:SandboxName_ parameter may be specified between Start.exe and the delete command.

The __silent_ suffix on the delete command, indicates Sandboxie Start should silently ignore any errors and not display any error messages.

The delete operation occurs in two phases:

*   Phase 1 scans the contents of the sandbox and processes files which could pose a problem during the second phase:
    *   Junctions (also known as reparse points) are removed.
    *   Read-only files and directories are made fully accessible.
    *   Files and directories that have very long names are renamed to shorter names.
    *   Renames the sandbox to the format __Delete__(sandbox name)___(some random number)__. For example, if the sandbox is DefaultBox, it could be renamed to __Delete_DefaultBox_01C4012345678912\.

*   Phase 2 deletes any sandboxes that were processed in phase 1\.
    *   Sandboxes that were processed in phase 1 are those that have been renamed as described above.
    *   More than one sandbox may be deleted in phase 2\.
    *   By default, the standard system command RMDIR is used to delete the renamed sandbox folder.
    *   Alternatively, a third-party delete utility may used. See [Secure Delete Sandbox](SecureDeleteSandbox.md).

Issuing the _delete_sandbox_ command causes Start.exe to invoke phase 1 followed by phase 2\. Start.exe also accepts these commands to invoke a specific phase:
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  delete_sandbox_phase1
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  delete_sandbox_phase2
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  delete_sandbox_silent_phase1
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  delete_sandbox_silent_phase2	
```

* * *

### Reload Configuration <a name="reload" href="#reload">#</a>

This command reloads the Sandboxie configuration in SandboxieIni into the active Sandboxie driver. Typically useful after manually editing the Sandboxie.ini file.
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /reload	
```

Note that reloading the configuration does not take effect on sandboxed programs that are already running when this command is issued.

* * *

### Disable Forced Programs <a name="disableforce" href="#disableforce">#</a>

The following command runs a program outside the sandox, even if the program is forced. It is similar to using the Run Outside Sandbox option from the sandbox selection window of the Run Sandboxed command.
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /dfp            c:\path\to\program.exe
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  /disable_force  c:\path\to\program.exe	
```

Note that /dfp and /disable_force are identical.

An older form of this command can temporarily disable the forced programs mode, for all programs. It is similar in function to using the Disable Forced Programs command from the [Tray Icon Menu](TrayIconMenu#disableforce) in Sandboxie Control (and not the [File Menu](FileMenu#disableforce)).
```
  &quot;C:\Program Files\Sandboxie\Start.exe&quot;  disable_force	
```

Note the missing slash in this command syntax. Note also that this command is not a toggle. It always puts the Disable Forced Programs mode into effect and always restarts the countdown timer. At this time, Start.exe does not offer a way to request the cancelation of this mode.

* * *

### Related Reading Material <a name="related" href="#related">#</a>

See also: [InjectDll](InjectDll.md) and [SBIE DLL API](SBIE_DLL_API)

Go to [Help Topics](HelpTopics.md).
