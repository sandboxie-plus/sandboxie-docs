# 内存虚拟磁盘盘符

_RamDiskLetter_ 是 [Sandboxie.ini](SandboxieIni.md) 中的一个全局设置项（在 v1.11.1 / 5.66.1 版本中引入），用于指定分配给内存虚拟磁盘的盘符。该内存虚拟磁盘专为启用了 [UseRamDisk](UseRamDisk.md) 设置的沙盒创建。此设置允许用户为内存虚拟磁盘定义一个特定的盘符，以便更轻松地访问。

## 用法

要设置 `RamDiskLetter`，请在 Sandboxie 配置文件的 `[GlobalSettings]` 部分下添加以下行：

```ini
[GlobalSettings]

# 将驱动器号 R 分配给内存虚拟磁盘的示例
RamDiskLetter=R:\
```

## SandMan 界面

可以通过以下步骤选择内存虚拟磁盘盘符设置：

1. 在 SandMan 界面中打开 `全局设置` 窗口。
2. 导航到 `附加组件管理器` > `附加组件配置` 选项卡。
3. 启用 `为内存虚拟磁盘分配盘符` 设置，并为内存虚拟磁盘选择一个盘符。

    ![Ram Disk Letter](../Media/UseRamDisk3.png)

## 重要说明

- **单一盘符**: 只能为内存虚拟磁盘分配一个盘符，该盘符将用于所有使用内存虚拟磁盘功能的沙盒。

- **可用盘符**: 确保指定的盘符未被系统上的其他驱动器或分区占用。如果该盘符已被分配，内存虚拟磁盘可能无法挂载，并且会记录错误。

- **配置要求**: 应在为单个沙盒启用 `UseRamDisk` 之前配置 `RamDiskLetter` 设置，以确保正确分配。

## 性能考量

- **访问便利性**: 为内存虚拟磁盘分配一个特定的盘符可以简化应用程序和用户的访问，使其在文件路径中引用内存虚拟磁盘变得更加容易。

## 相关设置

- [RamDiskSizeKb](RamDiskSizeKb.md) - 指定内存虚拟磁盘的大小。
- [UseRamDisk](UseRamDisk.md) - 为单个沙盒启用内存虚拟磁盘。

通过配置 `RamDiskLetter` 设置，用户可以为内存虚拟磁盘提供一个一致且易于访问的盘符，从而增强其 Sandboxie 使用体验。
