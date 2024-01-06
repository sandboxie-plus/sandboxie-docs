# Start Command Line

The Sandboxie Start program can perform various actions based on the command line parameters specified to it. Here are the available options:

## Start Programs

This is the default behavior. By specifying a full or partial path to a program's executable file, Sandboxie Start will launch that program under the supervision of Sandboxie:

```plaintext
"C:\Program Files\Sandboxie\Start.exe"  c:\windows\system32\notepad.exe
"C:\Program Files\Sandboxie\Start.exe"  notepad.exe
```

Two special program names are allowed:

```plaintext
"C:\Program Files\Sandboxie\Start.exe"  default_browser
"C:\Program Files\Sandboxie\Start.exe"  mail_agent
```

Sandboxie Start can also display the Run Any Program dialog window or the Sandboxie Start Menu, depending on parameters specified:

```plaintext
"C:\Program Files\Sandboxie\Start.exe"  run_dialog
"C:\Program Files\Sandboxie\Start.exe"  start_menu
```

In all forms, the parameter `/box:SandboxName` is applicable and may be specified between Start.exe and the parameter to indicate a sandbox name other than the default of `DefaultBox`. For example:

```plaintext
"C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  run_dialog
```

Other parameters include `/silent` to eliminate some pop-up error messages, `/elevate` to run a program with Administrator privileges, `/env` to pass an environment variable, `/hide_window` to signal that the starting program should not display its window, and `/wait` to run a program, wait for it to finish, and return the exit status from the program.

Example with multiple parameters:

```plaintext
"C:\Program Files\Sandboxie\Start.exe"  /box:CustomBox /silent MyProgram.exe
```

## Stop Programs

Terminate all programs running in a particular sandbox. Note that the request is transmitted to the Sandboxie service SbieSvc, which actually carries out the termination.

```plaintext
"C:\Program Files\Sandboxie\Start.exe"  /terminate
"C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /terminate
"C:\Program Files\Sandboxie\Start.exe"  /terminate_all
```

## Unmount Box Images

Unmount encrypted box images or RAM disks created by Sandboxie Plus.

```plaintext
"C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount
"C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /unmount
"C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount_all
```

## Mount Box Images

Mount encrypted box images created by Sandboxie Plus.

```plaintext
"C:\Program Files\Sandboxie-Plus\Start.exe"  /key:[box image password] /mount_protected
"C:\Program Files\Sandboxie-Plus\Start.exe"  /key:[box image password] /mount
"C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /key:[box image password] /mount_protected
"C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /key:[box image password] /mount
```

## List Programs

List the system process ID numbers for all programs running in a particular sandbox.

```plaintext
"C:\Program Files\Sandboxie\Start.exe"  /listpids
"C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /listpids
```

If the parameter `/box:SandboxName` is omitted, programs running in the default sandbox, `DefaultBox`, will be listed.

## Delete Contents of Sandbox

```plaintext
"C:\Program Files\Sandboxie\Start.exe"  delete_sandbox
"C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent
```

The `/box:SandboxName` parameter may be specified between Start.exe and the delete command. The `silent` suffix on the delete command indicates Sandboxie Start should silently ignore any errors and not display any error messages.

The delete operation occurs in two phases: Phase 1 scans the contents of the sandbox and processes files that could pose a problem during the second phase. Phase 2 deletes any sandboxes that were processed in phase 1.

Example commands for specific phases:

```plaintext
"C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase1
"C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase2
"C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase1
"C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase2
```

## Reload Configuration

Reload the Sandboxie configuration in SandboxieIni into the active

 Sandboxie driver. Typically useful after manually editing the Sandboxie.ini file.

```plaintext
"C:\Program Files\Sandboxie\Start.exe"  /reload
```

Note that reloading the configuration does not take effect on sandboxed programs that are already running when this command is issued.

## Disable Forced Programs

Run a program outside the sandbox, even if the program is forced. Similar to using the Run Outside Sandbox option from the sandbox selection window of the Run Sandboxed command.

```plaintext
"C:\Program Files\Sandboxie\Start.exe"  /dfp  c:\path\to\program.exe
"C:\Program Files\Sandboxie\Start.exe"  /disable_force  c:\path\to\program.exe
```

An older form of this command can temporarily disable the forced programs mode, for all programs.

```plaintext
"C:\Program Files\Sandboxie\Start.exe"  disable_force
```

Note that `/dfp` and `/disable_force` are identical. The command `/dfp` can also be selected by holding the Ctrl and Shift keys down when you click the Run Sandboxed command.

## Related Reading Material

See also: [InjectDll](InjectDll.md) and [SBIE DLL API](SBIEDLLAPI.md)

Go to [Help Topics](HelpTopics.md).
