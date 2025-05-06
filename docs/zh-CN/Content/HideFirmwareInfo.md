# 隐藏固件信息

“隐藏固件信息”（HideFirmwareInfo）是[沙盘配置文件（Sandboxie Ini）](SandboxieIni.md)中的一项设置。

```
   .
   .
   .
   [DefaultBox]
   HideFirmwareInfo=y
```

使用 `HideFirmwareInfo=y` 选项可将 `HKCU\System\SbieCustom` 中的 `SMBiosTable` 值作为固件信息返回。启用此选项后，沙箱条目（如果存在）将具有更高优先级，其次才是主机系统中的条目。

相关的沙盘增强版（Sandboxie Plus）设置：沙箱选项 > 高级选项 > 隐私 > 隐藏固件信息