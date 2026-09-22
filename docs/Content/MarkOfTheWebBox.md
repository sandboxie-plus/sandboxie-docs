# Mark Of The Web Box

_MarkOfTheWebBox_ is a global [Sandboxie Ini](SandboxieIni.md) setting that names the destination sandbox for [Force Mark of The Web](ForceMarkOfTheWeb.md) process-start evaluation.

```ini
[GlobalSettings]
ForceMarkOfTheWeb=y
MarkOfTheWebBox=Web_Box
```

If `MarkOfTheWebBox` is absent or empty, the driver's runtime fallback is `DefaultBox`. The destination name is matched case-insensitively against sandboxes eligible for forcing. The sandbox must be enabled for the current user and session; [DisableForceRules](DisableForceRules.md) excludes it from the eligible list.

If the Mark-of-the-Web check matches but the destination cannot be selected, Sandboxie marks the new process for termination instead of allowing this path to continue unsandboxed. See [Force Mark of The Web](ForceMarkOfTheWeb.md) for what is checked and the limits of this process-start rule.
