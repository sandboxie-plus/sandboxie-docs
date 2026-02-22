# 磁盘序列号

_DiskSerialNumber_ 是 [沙盘配置](SandboxieIni.md) 中的一项沙箱设置，从 v1.15.2 / 5.70.2 版本开始提供。该设置允许为沙箱内的指定磁盘设备分配自定义序列号，并与 [隐藏磁盘序列号](HideDiskSerialNumber.md) 功能配合使用。

## 语法

```ini
DiskSerialNumber=<DeviceName>,<SerialNumber>
```

* **DeviceName**：Windows 设备名称（如 HarddiskVolume1、HarddiskVolume2）
* **SerialNumber**：自定义的十六进制格式序列号（可带或不带连字符）

## 示例用法

```ini
[DefaultBox]

HideDiskSerialNumber=y
DiskSerialNumber=HarddiskVolume1,1234-ABCD
DiskSerialNumber=HarddiskVolume2,5678-EFGH
DiskSerialNumber=HarddiskVolume3,9ABC-DEF0
```

## 前置条件

- 需要在同一个沙箱中启用 `HideDiskSerialNumber=y`[^1]
- 如果未满足该条件，DiskSerialNumber 设置将被忽略

## 序列号格式

### 支持的格式

- **带连字符**：`1234-ABCD`, `AA-BB-CC-DD`
- **不带连字符**：`1234ABCD`, `AABBCCDD`
- **混合**：任意十六进制数字和可选连字符的组合

### 有效示例

```ini
DiskSerialNumber=HarddiskVolume1,1234ABCD
DiskSerialNumber=HarddiskVolume2,12-34-AB-CD
DiskSerialNumber=HarddiskVolume3,12345678
DiskSerialNumber=HarddiskVolume4,DEADBEEF
```

### 无效格式

- 含有非十六进制字符（G-Z）
- 十六进制数字为奇数位
- 空字符串
- 除连字符外的其它特殊字符

## 设备名称获取方法

### 方法一：使用 WMIC 命令

在命令提示符下运行以下命令以列出可用磁盘卷：

```cmd
wmic logicaldisk get caption,volumeserialnumber,deviceid
```

### 方法二：使用磁盘管理

1. 打开 **磁盘管理**（`diskmgmt.msc`）
2. 右键点击卷，查看属性
3. 记录卷标和驱动器号

### 方法三：注册表查看

检查注册表项：`HKEY_LOCAL_MACHINE\SYSTEM\MountedDevices`

### 方法四：随机值测试法

1. 设置测试配置：

```ini
DiskSerialNumber=HarddiskVolume1,11111111
DiskSerialNumber=HarddiskVolume2,22222222
DiskSerialNumber=HarddiskVolume3,33333333
```

2. 在沙箱中运行 `vol C:`、`vol D:` 等，确定各磁盘对应的设备名称

## 技术实现

### 设备路径解析

- 沙盘从 Windows NT 路径中提取带有 `\Device\` 前缀的设备名称[^2]
- 设备名称的解析遇到下一个反斜线或字符串结束符即终止[^3]
- 设备提取失败时，会生成随机序列号[^4]

### 十六进制处理

- 自定义解析器支持带连字符和不带连字符的十六进制格式[^5]
- 非法的十六进制串会触发随机序列号生成[^6]
- 字节序自动进行调整，以符合 Windows 的 DWORD 小端格式[^7]

### 缓存机制

- 每个会话中序列号会被缓存以提升性能[^8]
- 通过临界区保证多线程安全[^9]
- 缓存的键值基于原始硬件序列号[^10]

## 使用场景

### 应用程序测试

- 测试软件对特定磁盘序列号模式的响应
- 模拟不同硬件配置
- 调试依赖序列号的功能

### 隐私增强

- 用已知值替换真实硬件识别码
- 创建一致的沙箱指纹
- 防止基于硬件信息的追踪

## 故障排查

### 常见问题

**设置未生效**

- 请确认已启用 `HideDiskSerialNumber=y`
- 请核对设备名称格式是否正确
- 检查十六进制字符串的合法性

**目标设备有误**

- 通过设备获取方法确认名称是否正确
- 用唯一序列号进行映射测试

**返回为随机值**

- 非法十六进制格式会触发随机生成
- 设备名称不匹配会导致生成随机值
- 缺少 `HideDiskSerialNumber` 前置条件

## 相关设置

- [隐藏磁盘序列号](HideDiskSerialNumber.md) —— 必须的前置设置
- [隐藏固件信息](HideFirmwareInfo.md) —— 隐藏其他硬件识别信息
- [隐藏网卡 MAC](HideNetworkAdapterMAC.md) —— 自定义网卡识别码
- [随机注册表 UID](RandomRegUID.md) —— 随机化基于注册表的唯一识别码

## 配置可用性

- **INI 配置**：可用
- **Plus 界面**：不可用（仅支持 INI 配置）
- **Classic 界面**：不可用


[^1]: **前置条件**：必须启用 `HideDiskSerialNumber` 设置，设备序列号映射才会生效（kernel.c）

[^2]: **设备路径解析**：沙盘会在 NT 路径字符串中搜索 `\Device\` 前缀，以提取设备名称（kernel.c）

[^3]: **名称截断逻辑**：设备名解析至遇到第一个反斜线或字符串结束符自动终止（kernel.c）

[^4]: **回退行为**：如果设备名为空，则通过 `Dll_rand()` 生成随机序列号（kernel.c）

[^5]: **十六进制解析实现**：`hex_string_to_uint8_array()` 支持跳过连字符处理十六进制串（custom.c）

[^6]: **错误处理**：非十六进制字符、位数不对或解析失败均返回 FALSE 并触发随机生成（custom.c）

[^7]: **字节序转换**：当 `swap_bytes=TRUE` 时，自动切换为 Windows 小端 DWORD 格式（custom.c）

[^8]: **会话持久化**：`map_insert()` 根据原始硬件值缓存每次计算的序列号（kernel.c）

[^9]: **线程安全**：临界区 `Kernel_DiskSN_CritSec` 保护对序列号缓存的并发访问（kernel.c5）

[^10]: **缓存键策略**：以原始磁盘序列号为映射键值，确保每会话一致性（kernel.c）