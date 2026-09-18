# 隐藏网卡 MAC 地址

隐藏网卡 MAC 地址是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。

```
   .
   .
   .
   [DefaultBox]
   HideNetworkAdapterMAC=y
```

使用“HideNetworkAdapterMAC=y”选项可在应用程序尝试获取网络适配器 MAC 地址时返回随机值。

相关 Sandboxie Plus 设置：沙盒选项 > 高级选项 > 隐私 > 隐藏网卡 MAC 地址

## 相关设置

- [网络适配器 MAC](NetworkAdapterMAC.md) - 为特定适配器设置自定义 MAC 地址
