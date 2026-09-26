# Alert Folder

`AlertFolder` is a global [Sandboxie Ini](SandboxieIni.md) setting introduced in Sandboxie Plus 0.5.0 / Classic 5.45.0. It evaluates the **executable's own path/directory** when a program starts outside a sandbox. It does not inspect the current working directory or a document argument for alert matching, unlike some [Force Folder](ForceFolder.md) checks. It does not watch arbitrary file access.

```ini
[GlobalSettings]
AlertFolder=C:\Example
```

An ordinary folder entry matches executables recursively beneath that folder; entries containing wildcards are processed as patterns. After normal forcing fails to select a sandbox, `AlertFolder` is checked before [Alert Process](AlertProcess.md). A successful earlier force selection does not proceed through this ordinary alert-list check. The alert does not select a destination sandbox.

With the default `StartRunAlertDenied=n`, a match can issue [SBIE1301](SBIE1301.md) without this mechanism itself blocking the start. With global `StartRunAlertDenied=y`, a normal alert-list match is denied instead. `AlertStartRunAccessDenied` defaults to `y` and controls the [SBIE1308](SBIE1308.md) notification for that denial, not the blocking decision.

In SandMan, use **Global Settings > Program Control > Program Alerts > Add Folder**. The **Prevent the listed programs from starting on this system** control enables the blocking mode. See [Program Forcing Controls](ProgramForcingControls.md) for evaluation order, pause behavior, and the distinction from sandbox Start/Run restrictions.
