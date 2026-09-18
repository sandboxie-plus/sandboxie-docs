# 网络适配器 MAC

**网络适配器 MAC** 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 **v1.15.2 / 5.70.2** 起可用。此设置允许在沙盒内为特定网络适配器分配自定义 MAC 地址。

## 语法

```ini
NetworkAdapterMAC=<索引>,<MAC 地址>
```

* **索引**：目标网络适配器的索引值，从 0 开始
* **MAC 地址**：带连字符格式（AA-BB-CC-DD-EE-FF）或纯格式（AABBCCDDEEFF）的自定义 MAC 地址

## 用法示例

```ini
[DefaultBox]
HideNetworkAdapterMAC=y
NetworkAdapterMAC=0,12-34-56-78-9A-BC
NetworkAdapterMAC=1,DE-F0-12-34-56-78
```

## 识别网络适配器索引值

Sandboxie 只把索引值分配给有 MAC 地址的适配器，按系统枚举它们的顺序。没有 MAC 地址的虚拟适配器会被跳过。

要识别哪些适配器获得哪些 Sandboxie 索引值，先获取带 MAC 地址适配器的大致列表（在命令提示符中运行）：
```
wmic path win32_networkadapter where "MACAddress is not null" get netconnectionid,name,macaddress
```

Sandboxie 对此列表中第一个适配器从 0 开始分配索引值，然后是 1、2、3 等。不过，Sandboxie 的内部枚举顺序可能与命令输出顺序不匹配。

要获得准确映射，请使用测试方法：

1. 为每个索引设置唯一的 MAC 地址：
```ini
NetworkAdapterMAC=0,AA-00-00-00-00-00
NetworkAdapterMAC=1,AA-11-11-11-11-11
NetworkAdapterMAC=2,AA-22-22-22-22-22
NetworkAdapterMAC=3,AA-33-33-33-33-33
```
2. 在沙盒内运行 `ipconfig /all`，查看哪个适配器具有哪个测试 MAC

## 重要说明

- 需要在同一沙盒中启用 `HideNetworkAdapterMAC=y`
- 只能通过 INI 配置（没有用户界面选项）
- 无效的 MAC 地址格式会回退为随机生成 MAC
- 每个沙盒可以给相同的物理适配器分配不同的 MAC 地址

## 相关设置

- [隐藏网卡 MAC 地址](HideNetworkAdapterMAC.md) - MAC 地址定制的必要依赖
- [绑定适配器](BindAdapter.md) - 控制程序使用哪个网络适配器
