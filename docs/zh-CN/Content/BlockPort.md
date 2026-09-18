# 阻止端口

**此功能已自 v0.9.0 / 5.51.0 起移除。如果你在 [Sandboxie Ini](SandboxieIni.md) 中有自定义阻止端口条目，需要手工把它们更新为新格式，例如 `BlockPort=137,138,139,445` 变成 `NetworkAccess=*,Block;Port=137,138,139,445`（目前包含在 _Templates.ini_ 文件的 `[Template_BlockPorts]` 节中）。**

_BlockPort_ 曾是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定要阻止的出站通信 IP 端口号。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockPort=137-139,445
   BlockPort=*,80,8080
```

上面列出的端口号与 SMB/CIFS 网络文件共享子系统相关联。

此设置的主要目的是阻止 SMB/CIFS 端口上的出站通信，以防止恶意的沙盒化程序通过 SMB/CIFS 子系统访问文件，而不是直接向本地系统发出请求。

该设置可以跨多行重复指定，效果会累积。端口范围可按第一个示例所示指定。第二个示例展示了否定用法：阻止除星号（*）后指定端口之外的所有端口。

此设置不能通过沙盒管理器配置，除非启用或禁用预定义的默认阻止端口列表：

[沙盒设置 > 应用程序 > 其他](ApplicationsSettings.md#其他) > 默认阻止的 TCP/IP 端口列表

注意：此设置会阻止 [smbclient](http://www.samba.org/samba/docs/man/manpages-3/smbclient.1) 之类的程序在 Sandboxie 下正常运行。如果需要，可以关闭此设置。
