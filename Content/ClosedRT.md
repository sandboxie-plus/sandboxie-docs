# Closed RT

_ClosedRT_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.5.3a / 5.45.2. It specifies the problematic Windows RT interfaces that should not be accessible by a sandboxed program.

Examples:
```
   .
   .
   .
   [DefaultBox]
   ClosedRT=ExampleRT
```

This example makes the _ExampleRT_ not accessible to sandboxed programs.

Related Sandboxie Plus setting:

Sandbox Options > Resource Access > COM
