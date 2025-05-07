# 隐藏网卡 MAC 地址

隐藏网卡 MAC 地址 是 [沙盘配置文件](SandboxieIni.md) 中的一个设置。

```
   .
   .
   .
   [DefaultBox]
   HideNetworkAdapterMAC=y
```

使用 `HideNetworkAdapterMAC=y` 选项，当应用程序尝试获取网卡 MAC 地址时返回一个随机值。

相关的沙盘增强版设置：沙箱选项 > 高级选项 > 隐私 > 隐藏网卡 MAC 地址
