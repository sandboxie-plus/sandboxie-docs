# 阻止端口

**此功能自 v0.9.0 / 5.51.0 版本起已移除。如果您在 [Sandboxie Ini](SandboxieIni.md) 中有自定义的 BlockPort 条目，需要手动更新为新格式，例如 `BlockPort=137,138,139,445` 变为 `NetworkAccess=*,Block;Port=137,138,139,445`（目前包含在 _Templates.ini_ 文件的 `[Template_BlockPorts]` 部分下）。**

_BlockPort_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定要阻止的出站通信的 IP 端口号。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockPort=137-139,445
   BlockPort=*,80,8080
```

上面列出的端口号与 SMB/CIFS 网络文件共享子系统相关。

此设置的主要目的是阻止在 SMB/CIFS 端口上的出站通信，以防止恶意沙盒化程序通过 SMB/CIFS 子系统访问文件，而不是通过向本地系统发出直接请求。

该设置可以在多行中重复指定，效果将累积。如第一个示例所示，可以指定端口范围。第二个示例显示了否定用法：阻止除星号（*）字符后指定的端口之外的所有端口。

除了启用或禁用预定义的默认阻止端口列表外，此设置无法通过 Sandboxie 控制器进行配置：

[沙盒设置 > 应用程序 > 杂项](ApplicationsSettings.md#misc) > 默认阻止的 TCP/IP 端口列表

请注意，此设置将阻止 [smbclient](http://www.samba.org/samba/docs/man/manpages-3/smbclient.1) 等程序在 Sandboxie 下正常运行。如果需要这些程序，可以关闭此设置。 