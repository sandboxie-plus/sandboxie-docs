# Block Win Hooks

**BlockWinHooks feature was removed in SBIE version 4.+ and up. It is no longer available.**

_BlockWinHooks_ was a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specified whether Sandboxie should allow sandboxed programs to install system-global hooks.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BlockWinHooks=n
```

One application may attach to other applications in the system by employing a mechanism called windows hooks. This mechanism associates a component of the requesting application (called a DLL file) with all other applications.

By default, Sandboxie denies a request to install a global hook, and will instead convert the hook into an application-specific hook, and install this converted hook only into applications running in the same sandbox as the requesting application.

In effect, this restricts the effect of global hooks to a specific sandbox, and increases the protection provided by Sandboxie while still allowing applications that rely on global hooks to execute correctly.

Specifying _BlockWinHooks=n_ disables this protection, and allows a sandboxed application to install global hooks into all running applications, both inside and outside the sandbox.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Restrictions > Low-Level Access](RestrictionsSettings.md#low-level-access--removed)
