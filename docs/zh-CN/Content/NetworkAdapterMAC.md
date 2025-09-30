# 网络适配器 MAC

**NetworkAdapterMAC** 是 [Sandboxie Ini](SandboxieIni.md)自 **v1.15.2 / 5.70.2** 起可用的沙箱设置。此设置允许为沙箱内的特定网络适配器分配自定义 MAC 地址。

## 语法

```ini
NetworkAdapterMAC=<索引>,<MAC 地址>
```

* **索引**：目标网络适配器的索引值，从 0 开始
* **MAC 地址**：以连字符格式（AA-BB-CC-DD-EE-FF）或纯格式（AABBCCDDEEFF）表示的自定义 MAC 地址

## 示例用法

```ini
[DefaultBox]
HideNetworkAdapterMAC=y
NetworkAdapterMAC=0,12-34-56-78-9A-BC
NetworkAdapterMAC=1,DE-F0-12-34-56-78
```

## 确定网络适配器索引值

Sandboxie 仅为具有 MAC 地址的适配器分配索引值，按照系统枚举它们的顺序。没有 MAC 地址的虚拟适配器会被跳过。

要确定哪些适配器获得了哪些 Sandboxie 索引值，可以获取具有 MAC 地址的适配器的大致列表（在命令提示符下运行）：
```pwsh
wmic path win32_networkadapter where "MACAddress is not null" get netconnectionid,name,macaddress
```

Sandboxie 从此列表中的第一个适配器开始分配索引值，依次为 0、1、2、3 等。然而，Sandboxie 的内部枚举顺序可能与命令输出顺序不匹配。

为了准确映射，请使用测试方法：

1. 为每个索引设置唯一的 MAC 地址：
```ini
NetworkAdapterMAC=0,AA-00-00-00-00-00
NetworkAdapterMAC=1,AA-11-11-11-11-11
NetworkAdapterMAC=2,AA-22-22-22-22-22
NetworkAdapterMAC=3,AA-33-33-33-33-33
```
2. 在沙箱内运行 `ipconfig /all` 以查看哪个适配器具有哪个测试 MAC

## 重要说明

- 需要在同一沙箱中启用 `HideNetworkAdapterMAC=y`
- 配置仅通过 INI 可用（没有用户界面选项）
- 无效的 MAC 地址格式会回落为随机生成的 MAC 地址
- 每个沙箱可以为相同的物理适配器分配不同的 MAC 地址

## 相关设置

- [隐藏网络适配器 MAC](HideNetworkAdapterMAC.md) - MAC 地址自定义的必要依赖项
- [绑定适配器](BindAdapter.md) - 控制程序使用哪个网络适配器