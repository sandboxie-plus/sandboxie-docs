# Allow Raw Disk Read

_AllowRawDiskRead_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v0.7.0 / 5.48.0. This setting can be used to disable protection which prevents elevated sandboxed processes from accessing volumes/disks for reading.

```
   .
   .
   .
   [DefaultBox]
   AllowRawDiskRead=y
```

Related Sandboxie Plus setting: Sandbox Options > File Options > Allow elevated sandboxed applications to read the harddrive
