# Alert Process

`AlertProcess` is a global [Sandboxie Ini](SandboxieIni.md) setting for programs starting outside sandboxes. It matches executable/image identity, not arbitrary program activity, and does not select a destination sandbox.

```ini
[GlobalSettings]
AlertProcess=example.exe
```

Ordinary entries match executable image names. An entry containing `*` is handled as a case-insensitive pattern against the normalized executable path. Do not assume that other selector syntaxes apply to this alert path.

After configured forcing fails to select a box, Sandboxie checks [Alert Folder](AlertFolder.md) and then `AlertProcess`. A successful earlier normal force selection does not receive the ordinary alert-list decision through this branch.

With the default `StartRunAlertDenied=n`, a match can issue [SBIE1301](SBIE1301.md) without this mechanism itself denying the start. With global `StartRunAlertDenied=y`, a normal alert-list match blocks the start. `AlertStartRunAccessDenied` defaults to `y` and controls whether the denied start reports [SBIE1308](SBIE1308.md); it does not control the denial.

In SandMan, use **Global Settings > Program Control > Program Alerts > Add Program**. **Prevent the listed programs from starting on this system** controls blocking. See [Program Forcing Controls](ProgramForcingControls.md) for the broader force, alert, and pause architecture.

For Sandboxie Control Classic, see [Configure Menu > Program Alerts](ConfigureMenu.md#program-alerts) and the [Program Settings alert option](ProgramSettings.md#alert).
