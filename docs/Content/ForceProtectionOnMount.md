# Force Protection On Mount

_ForceProtectionOnMount_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) (introduced in v1.13.4 / 5.68.4) that forces a file-backed sandbox image to be mounted with root protection enabled. When set, the mount flow and the mount/create dialog enforce the image root protect option so users cannot mount the image without protection.

## Usage

```ini
[DefaultBox]

ForceProtectionOnMount=y
```

## When to use

- You want a sandbox image always mounted in protected mode (prevent unsandboxed processes from accessing the mounted image).

- Useful for encrypted images where you want to guarantee protection at mount time.

## Behavior and UI

- The General / File Options UI exposes a checkbox bound to `ForceProtectionOnMount` (`ui.chkForceProtection` in the code).
    - The checkbox is enabled only when the sandbox is configured as an [encrypted sandbox](UseFileImage.md) (not for RAM disk).

      ![Force Protection On Mount 1](../Media/UseFileImage1.png)

- When the box image mount dialog is shown programmatically with force applied, `CBoxImageWindow::SetForce(true)`:
    - forces `ui.chkProtect` checked,
    - disables the protect checkbox so users cannot uncheck it,

      ![Force Protection On Mount 2](../Media/UseFileImage8.png)

    - forces `ui.chkAutoLock` (auto-unmount on last process stop) checked/disabled in the dialog.  
- On mount the service receives a mount request with the `protect_root` flag set; the mount manager and driver enforce protection.

## Technical notes / code references

- UI reads/writes:
    - Read: `m_pBox->GetBool("ForceProtectionOnMount", false)` (see `COptionsWindow::LoadGeneral`).[^1]
    - Save: `WriteAdvancedCheck(ui.chkForceProtection, "ForceProtectionOnMount", "y", "")` (see `COptionsWindow::SaveGeneral`).[^1]

- Mount wire protocol:
    - `IMBOX_MOUNT_REQ` contains `BOOL protect_root;` (mount wire header in `MountManagerWire.h`).[^2]

- Mount dialog enforcement:
    - `CBoxImageWindow::SetForce(bool force)` sets the protect checkbox enabled/checked state.[^3]

- Mount flow:
    - `MountManager::AcquireBoxRoot` (mount manager) will include the `protect_root` flag in mount requests when appropriate.[^4]

- Start process integration:
    - `Start.cpp` handles the `mount_protected` parameter during sandbox startup and process creation.[^5]

## Compatibility & constraints

- Only meaningful for sandboxes using `UseFileImage` (file-backed `.box` images).
- If the filesystem driver or mount manager cannot honor protected mounts (or encrypted containers), mounts may fail and the sandbox will not start - check logs and mount manager errors.
- Protecting the root is enforced at mount time; unmounting while processes run will terminate those processes.

## Best practices

- Apply per-sandbox (do not set globally unless you intend to force protection for every sandbox).

## Related

- [`UseFileImage`](UseFileImage.md) - enables file-backed sandbox images.
- `CBoxImageWindow::SetForce` - UI enforcement on the mount/create dialog.
- `IMBOX_MOUNT_REQ.protect_root` - mount request flag used by the mount manager.
- [`StartCommandLine`](StartCommandLine.md#mount-box-images) - Command-line operations including `mount_protected` switch for protected mounting.

[^1]: See UI code in `SandMan\Windows\OptionsGeneral.cpp` - `COptionsWindow::LoadGeneral` and `COptionsWindow::SaveGeneral` handle reading and writing the `ForceProtectionOnMount` key via `m_pBox`.
[^2]: Mount protocol definition in `..\Sandboxie\core\svc\MountManagerWire.h` - `tagIMBOX_MOUNT_REQ` includes the `protect_root` field used by the mount manager.
[^3]: Implementation in `SandMan\Windows\BoxImageWindow.cpp` - `CBoxImageWindow::SetForce(bool force)` forces the dialog checkboxes to reflect a forced protected mount.
[^4]: Mount manager code (mount request assembly) will propagate the `protect_root` flag to the service/driver; see the mount manager implementation (e.g., `MountManager::AcquireBoxRoot`) in the service codebase.
[^5]: Start process implementation in `Sandboxie\apps\start\Start.cpp` - handles the `mount_protected` parameter during sandbox startup and process initialization.