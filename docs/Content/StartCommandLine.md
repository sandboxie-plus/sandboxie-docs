# Start Command Line

The Sandboxie Start program can do any of the following, depending on command line parameters specified to it.

*   [Start](#start-programs) programs under the supervision of Sandboxie
*   [Stop](#stop-programs) sandboxed programs
*   [Unmount](#unmount-box-images) box images or RAM disks
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

For a normal launch from outside a sandbox, the parameter _/box:SandboxName_ selects the target sandbox and must precede the program or launch helper. If omitted, Start.exe initially selects the `DefaultBox` value from `[GlobalSettings]`, falling back to the sandbox named `DefaultBox` when that value is unavailable or empty. For example:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  run_dialog
```

A special form of the /box parameter is _/box:\_\_ask\_\__ and causes Start.exe to display the sandbox selection dialog box.

`/box:current` follows the same selection workflow; it is not a general instruction to target the caller's current sandbox. The advanced host-side launch form `/box:-PID` can use an existing sandboxed process as a model, but is not a universal selector for control operations.

An already-sandboxed Start.exe launching a program remains in its actual sandbox; `/box:` does not move that launch to another box. All-box operations enumerate their own targets, `/reload` is not box-scoped, and deletion phase 2 scans pending directories more broadly.

The parameter _/silent_ can be used to eliminate some pop-up error messages. For example:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /silent  no_such_program.exe
```

Exit codes are command-dependent; see [Exit status](#exit-status). The _IF ERRORLEVEL_ condition can examine the launcher result in a batch file, but zero is not a universal acknowledgement that the requested operation succeeded. `/silent` does not turn failures into success and does not suppress every prompt or dialog, including [Alert Before Start](AlertBeforeStart.md) confirmations.

The parameter _/elevate_ requests elevation under the applicable Windows UAC and Sandboxie restrictions; it does not guarantee Administrator privileges. For example:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /elevate cmd.exe
```

The parameter _/env_ sets an environment variable in the launcher before the child workflow:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /env:VariableName=VariableValueWithoutSpace cmd.exe
  "C:\Program Files\Sandboxie\Start.exe"  /env:VariableName="Variable Value With Spaces" cmd.exe
```

The parameter _/hide_window_ signals that the starting program should not display its window; an application can still display UI:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /hide_window cmd.exe /c automated_script.bat
```

The parameter _/wait_ requests waiting for the launched process and can return its exit status when the launch path supplies a process handle and waiting and status retrieval succeed. It does not wait for an entire descendant process tree:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /wait cmd.exe
```

Note that Start.exe is a Win32 application and not a console application, so the system "start" command is useful here to force the system to wait for Start.exe to finish:
```cmd
  start "" /wait "C:\Program Files\Sandboxie\Start.exe" /wait cmd /c exit 9
  echo %ERRORLEVEL%
  9
```

In this ordinary successful launch, CMD's `start /wait` waits for Sandboxie Start.exe, whose `/wait` waits for `cmd /c exit 9` and propagates status 9. The two `/wait` options belong to different launchers.

Shell execution can succeed without returning a process handle. A program can also delegate work to another process and exit first, and some internal launch paths bypass normal waiting. Do not assume child-status propagation in those cases or if waiting or status retrieval fails.

Put applicable modifiers before the operation or program they affect. `/reload`, `/terminate`, `/terminate:*`, `/terminate_all`, `/unmount`, `/unmount_all`, `/mount`, `/mount_protected`, and `/listpids` execute immediately during parsing; later options are not processed. The program token ends normal slash-option parsing, so later arguments belong to that program. For example:
```cmd
   "C:\Program Files\Sandboxie\Start.exe"  /box:CustomBox /silent MyProgram.exe
```

Similarly, `Start.exe /box:ExampleBox /mount` selects the box before mounting; `Start.exe /mount /box:ExampleBox` is not equivalent. The internal `run_sbie_ctrl` and `open_agent` helpers have separate early dispatch; see their section below.

#### Exit status

Automation should verify its intended outcome rather than treating every zero exit code as success.

| Operation | Meaning and limitation |
| --- | --- |
| Normal launch | Usually reports whether launching succeeded, not the program's eventual outcome. |
| `/wait`, `/keep_alive` | Can report the waited or final supervised result when the applicable process-handle path succeeds. |
| `/mount`, `/mount_protected` | Report the mount request result, not complete sandbox readiness, password validation on reuse, or verified protection. |
| Termination and unmount commands | Discard individual operation results; zero does not prove termination or detachment. |
| `/reload`, `/listpids` | Zero does not prove a successful reload or complete successful enumeration. |
| `delete_sandbox` | Initial launcher completion does not prove asynchronous phase-2 deletion completed. |

### Stop Programs

Request termination of programs in a particular sandbox in the caller's session. The request is transmitted to SbieSvc, which attempts termination and re-enumeration; immediate or successful termination is not guaranteed.
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /terminate
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /terminate
  "C:\Program Files\Sandboxie\Start.exe"  /terminate_all
```

If _/box:SandboxName_ is omitted, the request uses the selected default sandbox.

The forms _/terminate_all_ and `/terminate:*` enumerate sandboxes enabled for the caller and request termination in the caller's session. They do not automatically terminate every sandboxed process in every session. Start.exe discards the service's termination results, so zero does not confirm that all targeted processes stopped.

* * *

### Unmount Box Images

These commands request unmounting of box images or RAM disks created by Sandboxie Plus. These parameters are available since v1.11.0 / 5.66.0.
```cmd
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /unmount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount_all
```

`/unmount` first attempts to terminate relevant sandboxed processes in the caller's session, then requests service-side unmounting for the selected box. If _/box:SandboxName_ is omitted, it uses the selected default sandbox. It proceeds without reliably checking termination success.

`/unmount_all` enumerates eligible sandboxes for termination, then enumerates them again for unmounting. The enumeration is not restricted to encrypted boxes, and can include boxes using shared RAM backing. It is not a complete inventory of all mounted devices or all boxes on the machine.

Process termination is scoped to the caller's session, but service-managed storage can involve shared resources; detachment is not guaranteed to be session-local. Start.exe does not aggregate individual unmount failures, so zero does not prove successful detachment. An unsuccessful attempt can still change mounted-root state; do not assume rollback.

### Mount Box Images

> [!WARNING]
> When using `/key:password` with `Start.exe`, the password can be exposed through command line history, process lists, and potentially event logs. Do not store real passwords in batch files or logs; consider [SandMan's interactive image-mount workflow](UseFileImage.md) instead.

These commands request mounting of a box image through the image-management service. These parameters are available since v1.11.0 / 5.66.0.
```cmd
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /key:"example password" /mount_protected
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /key:"example password" /mount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /key:"example password" /mount_protected
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /key:"example password" /mount
```

`/box:` and `/key:` must precede the mount operation. Quoting permits spaces in the password; an unquoted value ends at a space. There is no general embedded-quote escaping mechanism. Explicit empty values are rejected, and omitting `/key:` does not invoke an interactive password prompt.

If _/box:SandboxName_ is omitted, the request uses the selected default sandbox. An already-mounted image can be reused without authenticating the newly supplied password, so a successful result is not always proof that the password was validated.

The explicit image-mount handler attempts its image path without independently requiring `UseFileImage=y`. This does not make every storage configuration a valid target: ImBox/ImDisk availability, feature availability, and actual image/backend conditions still matter. This operation is not complete sandbox startup, Registry hive initialization, or RAM-disk backing acquisition. See [Use File Image](UseFileImage.md).

`/mount_protected` requests mounted-root protection in addition to mounting the image. Successful mounting does not independently verify that the protection was registered. Mounted-root filesystem protection is separate from image encryption and `ConfidentialBox` process protection, and is not a guarantee against every possible host access. See [Force Protection On Mount](ForceProtectionOnMount.md) and [Protect Admin Only](ProtectAdminOnly.md) for the protection boundary.

The Start.exe mount commands do not consume `ForceProtectionOnMount`; that setting controls SandMan's mount-dialog workflow. `/mount_protected` makes an explicit protection request.

* * *

### List Programs

List process ID numbers for programs in a particular sandbox in the caller's session.
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /listpids
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /listpids
```

If _/box:SandboxName_ is omitted, the selected default sandbox is used. Enumeration by an already-sandboxed caller uses its actual sandbox instead of a different `/box` target.

The output is formatted as one number per line. The first line contains the number of programs, followed by one process ID per line. Example output:
```cmd
    "C:\Program Files\Sandboxie\Start.exe"  /listpids | more
    3
    3036
    2136
    384
```

Note that Start.exe is not a console application, so the output does not appear in a command prompt window unless you pipe the output using a construct such as `| more`. Exit code zero does not prove complete successful enumeration or output.

* * *

### Delete Contents of Sandbox
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent
```

The _/box:SandboxName_ parameter may be specified between Start.exe and the delete command.

The `_silent` suffix suppresses deletion error messages; detected errors can still terminate the operation with failure.

These commands delete sandbox filesystem contents, not the box's configuration section in `Sandboxie.ini`. They are the Classic-compatible Start.exe deletion path, not SandMan's separate cleanup or trigger workflow.

The delete operation occurs in two phases:

*   Phase 1 renames the selected sandbox filesystem root to a pending-deletion directory in the format `__Delete_(sandbox name)_(timestamp-derived suffix)`. For example, if the sandbox is DefaultBox, it could be renamed to `__Delete_DefaultBox_01C4012345678912`. The suffix comes from the current FILETIME value, not a random number.

*   Phase 2 enumerates eligible boxes and searches for pending-deletion directories renamed as described above. It prepares their contents before executing the deletion command:
    *   Attempts to remove directory reparse points, such as junctions.
    *   Clears selected read-only, hidden, and system attributes; this does not universally rewrite ACLs or make every file accessible.
    *   Renames problematic names or long paths to facilitate deletion.
    *   More than one box's pending directories may be processed; `/box:` does not limit this phase to only that box.
    *   By default, the standard system command RMDIR is used to delete the renamed sandbox folder.
    *   Alternatively, a third-party utility can be selected through [DeleteCommand](DeleteCommand.md). See [Secure Delete Sandbox](SecureDeleteSandbox.md).

The _delete_sandbox_ command performs phase 1 and launches phase 2 asynchronously. The first Start.exe process does not wait for all physical deletion to complete, so its successful exit is not proof that all contents were deleted. Start.exe also accepts these commands to invoke a specific phase:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase1
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase2
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase1
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase2
```

* * *

### Reload Configuration

This command reloads the shared driver configuration from Sandboxie.ini. It is typically useful after manually editing the file and is not scoped by `/box:`.
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /reload
```

Start.exe returns exit code 0 after dispatching `/reload`, even when the underlying reload operation reports a failure. This is not a successful-reload acknowledgement. The command does not request optional driver-component reconfiguration.

Reload updates the shared configuration, but whether an already-running process observes a changed setting depends on the setting's consumer and cache lifecycle. Process-initialized settings generally require restarting the affected process. Do not assume universal live updates, atomic reload, or retention of the previous configuration on every failure.

* * *

### Disable Forced Programs

For a host-side launch, the following modifiers request running a program outside the sandbox despite force rules. They are similar to using Run Outside Sandbox from the Run Sandboxed selection window; they are not a way for an already-sandboxed process to escape its sandbox.
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /dfp            c:\path\to\program.exe
  "C:\Program Files\Sandboxie\Start.exe"  /disable_force  c:\path\to\program.exe
```

Note that /dfp and /disable_force are identical. You can also select this option by holding the Ctrl and Shift keys down when you click the Run Sandboxed command.

An older bare command requests temporary Disable Forced Programs mode for the caller's session. It is similar in function to using the command from the [Tray Icon Menu](TrayIconMenu.md#disable-forced-programs) in Sandboxie Control (and not the [File Menu](FileMenu.md#disable-forced-programs)).
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  disable_force
```

Note the missing slash. This command requests enabling the mode and restarting its countdown; it is not a toggle. To request cancellation:

```cmd
  "C:\Program Files\Sandboxie\Start.exe"  disable_force_off
```

Both bare commands are subject to the driver's authorization and session rules. Their zero exit status does not prove that the requested change was applied.

* * *

### Advanced / Internal switches

The following switches and bare commands are intended primarily for advanced usage, automation, or internal/debugging scenarios. These options may change across versions and are not typically needed by end users.

#### /keep_alive

The boxed Start.exe instance can supervise a launched process and restart it after a nonzero result, rather than performing only a one-shot wait. This is not a crash detector: a deliberate nonzero exit can also trigger a restart.

> [!Note]
> The restart loop runs in the boxed instance. Normal host-to-box launching does not forward a consumed `/keep_alive` modifier. Some direct host launch paths can still use it to wait, without performing that restart loop.

- When the applicable launch path provides a process handle, Start.exe waits and reads that process's exit code. The single-process waiting limitations described above still apply.
- A zero result stops supervision.
- Consecutive short nonzero attempts permit the initial attempt followed by up to five retries.
- A nonzero attempt lasting at least five seconds resets the counter only while another retry is permitted. An exhausted counter stops supervision even if the final attempt was longer; five retries is not a universal lifetime maximum.
- The five-second measurement includes the launcher's launch-and-wait work, not only isolated child execution time.
- There is no explicit delay or backoff between permitted retries.
- If the program cannot be created, Start disables keep-alive for that invocation instead of retrying creation.

Unlike `/wait`, the boxed supervision path can launch the program again after a nonzero result. It does not guarantee continuous availability or supervise an entire process tree. When supervision ends, it returns the final supervised result; if retries are exhausted, this is the last nonzero result.

Use the first example when the supervising Start.exe already runs inside a sandbox. For a normal host launch, the second example starts an inner Start.exe that can supervise inside the box:
```cmd
"Start.exe" /keep_alive notepad.exe
"Start.exe" Start.exe /keep_alive notepad.exe
```
The inner `Start.exe` must be resolvable. These examples request single-process supervision, not guaranteed recovery from every failure.

#### /fake_admin

For a host-side sandbox-entry launch, request a faked Administrator context inside the sandbox. This can help some installers or legacy programs that detect administrator state and behave differently. It is a compatibility measure, not real UAC elevation; an already-boxed invocation does not necessarily apply the same flag. See [Fake Admin Rights](FakeAdminRights.md).

Example:
```cmd
"Start.exe" /fake_admin setup.exe
```

#### /force_children (or /fcp)

For a host-side direct launch, attempt to register the launched process so its children are forced into the selected sandbox. This does not, by itself, sandbox the initially launched program, and is not a way to move an already-boxed caller outside its sandbox. Registration occurs after launching and is not guaranteed to be race-free or successful, including some combinations with `/wait` or `/keep_alive`. See [Force Child Processes](ForceChildren.md).

Example:
```cmd
"Start.exe" /fcp myinstaller.exe
"Start.exe" /force_children myinstaller.exe
```

#### /env:=Refresh

Refresh the currently boxed Start.exe process's environment before launching a program. The refresh action does not run in the host parsing instance and does not modify arbitrary already-running processes. Use `/env:Name=Value` to set individual values. This modifier alone is not a complete launch command.

Example:
```cmd
"Start.exe" /env:=Refresh cmd.exe
```

#### uac_prompt

This bare internal helper displays Sandboxie's UAC prompt using parameters generated by other components. Use of a secure desktop depends on the applicable Windows and Sandboxie settings. It is not a normal `/uac_prompt` switch or a stable public API for arbitrary callers.

Example:
```cmd
"Start.exe" uac_prompt <internal-pkt-params>
```

#### mount_hive

An internal sandbox-initialization helper. Host execution forwards it into the box; boxed execution briefly keeps the helper process present. Registry hive mounting occurs through sandboxed-process initialization, not a direct mount call in this command's parser. Helper exit does not prove complete Registry readiness.

Example:
```cmd
"Start.exe" mount_hive
```

#### run_sbie_ctrl and open_agent[:param]

These internal commands request control-agent startup through the service. `run_sbie_ctrl` uses the configured/default agent; `open_agent:` can specify agent command text for an eligible host caller. They are not unrestricted arbitrary agent-task execution, and startup depends on service/session conditions, including whether an agent already runs.

They are handled before the normal slash-option parser; do not assume that prefixing `/box:` or `/silent` retains the same helper behavior.

Example:
```cmd
"Start.exe" run_sbie_ctrl
"Start.exe" open_agent:SandMan.exe
"Start.exe" open_agent:"SandMan.exe -autorun"
```

#### auto_run

This startup helper processes supported copied sandbox `Run`/`RunOnce` entries and Startup locations. It is separate from `StartProgram`, `StartService`, and `AutoExec`, and does not promise execution of every host-visible Run key. See [Start System Box](StartSystemBox.md) for the service-start workflow.

```cmd
"Start.exe" /box:ExampleBox auto_run
```

* * *

### Related Reading Material

See also: [InjectDll](InjectDll.md) and [SBIE DLL API](SBIEDLLAPI.md)

Go to [Help Topics](HelpTopics.md).
