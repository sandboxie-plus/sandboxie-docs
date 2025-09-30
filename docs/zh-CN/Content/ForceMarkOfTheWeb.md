# 强制网络标记

_ForceMarkOfTheWeb_ 是 [Sandboxie Ini](SandboxieIni.md) 中的全局设置。当启用时，它会强制所有带有网络标记（MOTW）的文件自动在指定的沙箱中进行沙箱化。这提供了增强的安全性，确保从互联网下载或通过电子邮件接收的文件自动被隔离。

## 设置

该功能使用两个全局设置：

### ForceMarkOfTheWeb

```ini
[GlobalSettings]
ForceMarkOfTheWeb=y
```

启用带有网络标记属性的文件的自动沙箱化。

### MarkOfTheWebBox

```ini
[GlobalSettings]
MarkOfTheWebBox=Web_Box
```

指定用来隔离 MOTW 文件的沙箱。如果未指定，默认值为 `DefaultBox`。

## 什么是网络标记？

网络标记（MOTW）是 Windows 中的一个安全功能，用于标记文件为来自互联网或其他不受信任的位置。Windows 会自动将此标记应用于：

- 从网页浏览器下载的文件
- 电子邮件附件
- 从下载的 ZIP 压缩文件中提取的文件
- 通过即时消息应用程序接收的文件
- 从标记为互联网区域的网络共享中复制的文件

## 重要说明

- 这是一个影响系统上的所有沙箱的 **全局设置**
- 指定的沙箱必须已经存在并在您的 Sandboxie 配置中启用
- 沙箱名称区分大小写，必须完全匹配
- 已在任何沙箱中运行的文件不受此设置的影响

## 故障排除

如果 MOTW 文件未被沙箱化：

1. **验证两个设置是否已配置：**
   - 在 `[GlobalSettings]` 中设置 `ForceMarkOfTheWeb=y`
   - `MarkOfTheWebBox=SandboxName` 指向一个现有的沙箱
2. **检查沙箱名称：** 确保沙箱名称完全匹配（区分大小写）
3. **确认沙箱存在并已启用**
4. **验证文件具有 MOTW 属性：** 使用 `dir /r filename` 检查 `Zone.Identifier` 流

## 相似设置

- [ForceProcess](ForceProcess.md): 强制特定程序进入沙箱
- [ForceFolder](ForceFolder.md): 强制来自特定文件夹的文件进入沙箱

## 用户界面

此设置可以通过 Sandboxie Plus 中的以下路径进行配置：
**全局设置 > 程序控制 > 强制进程选项**

![强制网络标记设置](../Media/ForceMarkOfTheWeb.png)