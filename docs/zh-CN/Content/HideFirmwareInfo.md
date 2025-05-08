# 隐藏固件信息

_HideFirmwareInfo_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。

```
   .
   .
   .
   [DefaultBox]
   HideFirmwareInfo=y
```

使用 'HideFirmwareInfo=y' 选项可以在 HKCU\System\SbieCustom 中返回 SMBiosTable 值作为固件信息。启用后，将优先使用沙盒条目（如果存在），然后才是主机系统中的条目。

相关 Sandboxie Plus 设置：沙盒选项 > 高级选项 > 隐私 > 隐藏固件信息 