# Auto Delete

AutoDelete is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). With AutoDelete=y, SandMan starts automatic content cleanup when it observes the box close after its active process count reaches zero. The setting is off when absent. It cleans or resets stored contents; it does not remove the sandbox definition. For example:
```
   .
   .
   .
   [DefaultBox]
   AutoDelete=y
```

SandMan offers [Quick Recovery](QuickRecovery.md) where applicable before automatic cleanup. [`NeverDelete`](NeverDelete.md) blocks this automatic path. When snapshots are retained, cleanup may restore a saved state rather than leave the box empty; see [AutoDeleteSnapshotTarget](AutoDeleteSnapshotTarget.md). For the distinction between content cleanup and definition removal, see [Sandbox Deletion and Removal Lifecycle](SandboxRemoval.md).

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Delete > Invocation](DeleteSettings.md#invocation)

Related Sandboxie Plus setting: Sandbox Options > File Options > Box Delete options > Auto delete content changes when last sandboxed process terminates
