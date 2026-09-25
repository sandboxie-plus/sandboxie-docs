# Never Delete

_NeverDelete_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). With _NeverDelete=y_, SandMan does not start [`AutoDelete`](AutoDelete.md) cleanup when the box closes, and ordinary full-cleanup paths reject content deletion. This is not an absolute safeguard against every manual snapshot or image-backed operation, nor a filesystem permission boundary. For example:

```
   .
   .
   .
   [DefaultBox]
   NeverDelete=y
```

`NeverRemove` is separate: it guards the normal manual **Remove Sandbox** action, which removes the box definition. In SandMan, **Sandbox Options > File Options > Box Delete options > Protect this sandbox from deletion or emptying** is a tri-state control: checked saves both protections; partially checked saves `NeverRemove=y` without `NeverDelete`. The current automatic `AutoRemove` transition after cleanup does not consult `NeverRemove`. See [Sandbox Deletion and Removal Lifecycle](SandboxRemoval.md) for the path-specific limits and interaction.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Delete > Invocation](DeleteSettings.md#invocation)
