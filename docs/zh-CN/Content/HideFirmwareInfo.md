# 隐藏固件信息

隐藏固件信息是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。

```
   .
   .
   .
   [DefaultBox]
   HideFirmwareInfo=y
```

使用“HideFirmwareInfo=y”选项可把 HKCU\System\SbieCustom 中的 SMBiosTable 值作为固件信息返回。启用时，沙盒条目（如果存在）优先，然后是宿主系统中的条目。

相关 Sandboxie Plus 设置：沙盒选项 > 高级选项 > 隐私 > 隐藏固件信息
