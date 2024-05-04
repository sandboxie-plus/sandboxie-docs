# Auto Delete

AutoDelete is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It is typically specified as AutoDelete=y, and indicates that the contents of the sandbox should be automatically deleted as soon as the last sandboxed process is terminated. For example:
```
   .
   .
   .
   [DefaultBox]
   AutoDelete=y
```

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Delete > Invocation](DeleteSettings.md#invocation)

Related Sandboxie Plus setting: Sandbox Options > File Options > Box Delete options > Auto delete content when last sandboxed process terminates
