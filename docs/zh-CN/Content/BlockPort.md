# 阻止端口

**此功能自 v0.9.0 / 5.51.0 版本起已被移除。如果你在你的 [Sandboxie Ini](SandboxieIni.md) 文件中有自定义的 BlockPort 条目，需要手动更新为新的格式。例如，`BlockPort=137,138,139,445` 需改为 `NetworkAccess=*,Block;Port=137,138,139,445`（当前已包含在 _Templates.ini_ 文件中的 `[Template_BlockPorts]` 部分）。**

_BlockPort_ 曾是 [Sandboxie Ini](SandboxieIni.md) 文件中的沙箱设置项。它用于指定要阻止对外通信的 IP 端口号。

用法：

```
   .
   .
   .
   [DefaultBox]
   BlockPort=137-139,445
   BlockPort=*,80,8080
```

上述端口号与 SMB/CIFS 网络文件共享子系统相关联。

此设置的主要目的是阻止 SMB/CIFS 端口上的外发通信，以防止恶意的沙箱程序通过 SMB/CIFS 子系统访问文件，而不是直接发起对本地系统的请求。

此设置可以多次指定于多行，效果将叠加。如第一个示例所示，可以指定端口范围。第二个示例展示了取反用法：阻止所有端口，除了星号（*）后指定的端口。

此设置无法通过沙箱控制进行配置，只能启用或禁用预定义的默认阻止端口列表：

[沙箱设置 > 应用程序 > 其他](ApplicationsSettings.md#misc) > 默认阻止的 TCP/IP 端口列表

请注意，此设置会阻止如 [smbclient](http://www.samba.org/samba/docs/man/manpages-3/smbclient.1) 等程序在 Sandboxie 下正常运行。如确有需要可将其关闭。
