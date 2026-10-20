# 沙盒别名

**沙盒别名** 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 **v1.14.6** 起可用。它允许为沙盒设置备选显示名称。

## 语法

```ini
BoxAlias=显示名称
```

别名可以包含显示文本，以及在真实沙盒名称中无效的特殊字符。

## 用法

沙盒别名提供了一种方法，为包含特殊字符的沙盒设置自定义显示名称，这些字符对沙盒名称而言本来是无效的。设置沙盒别名时，它覆盖默认的显示行为：

```ini
[MyTestBox]
BoxAlias=Development & Testing

[WebBox]  
BoxAlias=Secure Web Browser v2.0

[WorkSandbox]
BoxAlias=Email Client*
```

## 显示名称与沙盒标识

别名只用于展示。真实沙盒名称仍然是 INI 中的段名，也是沙盒的实际标识。设置别名不会重命名或改变以下内容：

* `Sandboxie.ini` 中的段名；
* 沙盒文件或注册表根的标识；
* IPC 或其他内部沙盒标识；
* API 或命令行工具所使用的名称；
* 强制规则所引用的沙盒名称。

不同的显示界面可能以不同方式呈现名称。SandMan 在呈现真实沙盒名称时通常会把下划线替换为空格，而 Start.exe 和更底层的使用者可能显示原始名称。如果未设置沙盒别名，沙盒名称显示时下划线会被替换为空格。

## BoxAliasDisplayMode

**BoxAliasDisplayMode** 是一项全局显示设置，自 **v1.18.2** 起可用：

```ini
[GlobalSettings]
BoxAliasDisplayMode=0
```

| 值 | 显示行为 |
| --- | --- |
| `0` | 存在生效别名时显示别名，否则显示沙盒名称。 |
| `1` | 显示真实沙盒名称。 |
| `2` | 在常规（非紧凑）显示中，当非空别名与真实名称不同时，显示 `别名 (真实沙盒名)`。紧凑显示可能只显示别名。 |

当前的多个显示路径都会读取该设置，包括 SandMan、Start.exe、沙盒窗口标题、边框、工具提示、恢复日志和消息。它并不保证所有界面的格式完全一致，也不会改变沙盒的实际标识。

!!! note

    当前各组件在缺少 _BoxAliasDisplayMode_ 时使用的回退值并不相同。SandMan 的主要显示路径和边框路径使用模式 `2`，而 Start.exe 和沙盒窗口标题处理使用模式 `0`。若希望所有使用者统一为明确的模式，请直接配置 _BoxAliasDisplayMode_。

    SandMan 的设置界面当前在保存**沙盒别名和名称**时，会通过移除显式的键来实现，而不是写入 `2`。这是当前的界面行为，也意味着各组件特有的缺键回退值仍然生效。

## 全局界面设置

全局控件位于：

**全局设置 > 界面设置 > 用户界面 > 界面选项**

**沙盒名称显示：** 选择器提供以下选项：

| 选项 | 存储的值 |
| --- | --- |
| **沙盒名称** | `1` |
| **沙盒别名** | `0` |
| **沙盒别名和名称** | `2`，通过当前 SandMan 界面保存时以缺键的形式表示 |

该选择器控制全局的显示行为。别名文本本身仍然是每个沙盒单独的设置。

## 隐藏和恢复别名

当前 SandMan 的**重命名沙盒**对话框为真实沙盒名称和别名提供了独立的控件。它可以在不丢弃别名文本的前提下隐藏别名，方式是在 _BoxAlias_ 和 _BoxAliasDisabled_ 之间移动该值：

* 别名生效时，_BoxAlias_ 存储文本，_BoxAliasDisabled_ 不存在。
* 选中**隐藏别名**时，_BoxAlias_ 被移除，_BoxAliasDisabled_ 存储该文本。
* 清空别名会同时移除两个设置。
* 重新启用已保存的别名时，会将其恢复到生效的 _BoxAlias_ 设置中。

例如，被隐藏的别名可以存储为：

```ini
[MyTestBox]
BoxAliasDisabled=Development & Testing
```

_BoxAliasDisabled_ 只是用来保存被隐藏的别名，并不是另一个生效的别名。常规显示路径读取的是 _BoxAlias_；隐藏别名不会改变 _BoxAliasDisplayMode_。

## 用户界面

沙盒别名可以通过 **Sandboxie Plus** 中的**重命名**功能配置。把沙盒重命名为包含特殊字符的名称时，Sandboxie Plus 会自动提示将其设置为别名，而不是重命名沙盒。

## 版本历史

* _BoxAlias_ 元数据记录为 v1.14.6。
* _BoxAliasDisabled_ 元数据记录为 v1.17.2。Sandboxie Plus 1.17.2 / Classic 5.72.2 的发布说明描述了重新设计的 SandMan 重命名对话框及其**隐藏别名**持久化。
* _BoxAliasDisplayMode_ 元数据记录为 v1.18.2。Sandboxie Plus 1.18.2 / Classic 5.73.2 的发布说明描述了它在当前仅用于显示的名称界面中的使用。