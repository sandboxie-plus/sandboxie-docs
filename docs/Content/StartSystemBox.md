# Start System Box

_StartSystemBox_ is a repeated global setting that starts named sandboxes in Session 0 when SbieSvc starts and the Sandboxie driver becomes ready.

```ini
[GlobalSettings]
StartSystemBox=SystemBox
```

Each value is a sandbox name, not a Boolean. Multiple entries start multiple boxes:

```ini
[GlobalSettings]
StartSystemBox=BoxOne
StartSystemBox=BoxTwo
```

## Startup behavior

For each configured name, SbieSvc initiates the equivalent of:

```text
Start.exe /box:<BoxName> auto_run
```

The startup flow is:

```text
SbieSvc starts and the driver becomes ready
    -> Start.exe is launched for the configured box
    -> Start.exe restarts inside that sandbox
    -> auto_run processes the sandbox's supported autostart locations
```

Because this flow originates from SbieSvc, it runs in Session 0 with SYSTEM identity. The resulting processes are still associated with the named sandbox; SYSTEM identity does not make them unsandboxed.

## What `auto_run` starts

The current `auto_run` implementation processes sandbox-visible `Run` and `RunOnce` registry entries for the machine and current user, including their 32-bit locations, and the common and user Startup folders.

The command does not currently start boxed services directly. `StartService`, `StartProgram`, and `AutoExec` are separate box-start mechanisms and should not be treated as synonyms for _StartSystemBox_.

## Security considerations

The project recommends enabling [Drop Admin Rights](DropAdminRights.md) for boxes started this way:

```ini
[SystemBox]
DropAdminRights=y
```

Session 0 SYSTEM identity makes token hardening especially important, but `DropAdminRights` does not make arbitrary SYSTEM software safe. [Strip System Privileges](StripSystemPrivileges.md) is a separate control used by specific service and RpcSs token-creation paths; it is not automatically applied merely because _StartSystemBox_ started a box in Session 0.

## Applying changes

SbieSvc reads _StartSystemBox_ entries during its startup sequence after the driver becomes ready. A normal configuration reload does not execute newly added entries. Changes take effect at the next Sandboxie service startup or system boot. Removing an entry does not terminate processes that have already started.

## SandMan

SandMan has no dedicated _StartSystemBox_ control. Configure it manually under `[GlobalSettings]` in Sandboxie.ini.

## Version history

_StartSystemBox_ was introduced in Sandboxie Plus 0.9.5 / Classic 5.51.5 together with Session 0 sandbox startup and the `auto_run` command.

## Related pages

- [Drop Admin Rights](DropAdminRights.md)
- [Strip System Privileges](StripSystemPrivileges.md)
- [Start Service](StartService.md)
- [Start Program](StartProgram.md)
- [Auto Exec](AutoExec.md)
- [Sandboxed Services](SandboxedServices.md)
- [Sandboxie Ini](SandboxieIni.md)
