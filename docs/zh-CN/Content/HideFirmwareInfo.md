# 隐藏固件信息

隐藏固件信息是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。

```
   .
   .
   .
   [DefaultBox]
   HideFirmwareInfo=y
```

使用 'HideFirmwareInfo=y' 选项，可以将 HKCU\System\SbieCustom 中的 SMBiosTable 值作为固件信息返回。启用该选项后，将优先使用沙箱内的条目（如果存在），否则使用宿主系统中的条目。

相关的 Sandboxie Plus 设置：沙箱选项 > 高级选项 > 隐私 > 隐藏固件信息