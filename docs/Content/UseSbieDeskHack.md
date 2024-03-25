# Use SbieDesk Hack

_UseSbieDeskHack_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md).

```
   .
   .
   .
   [DefaultBox]
   UseSbieDeskHack=y
```

A desktop object solution that is now enabled by default for all processes.

**Technical Details**

This is a desktop object solution that is used for all processes.

It was initially implemented to address the issue of infinite callback problems caused by delayed loading (the infinite recursion problem has been resolved in version 0.4.0 / 5.43).

It is now enabled by default. This allows Electron applications to run without the need to set the 'SpecialImage=chrome,program.exe' option.

Related Sandboxie Plus setting: Sandbox Options > Various Options > Compatibility > Use desktop object workaround for all processes
