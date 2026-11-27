# 规则特异性

Sandboxie 评估相互冲突的文件、注册表和 IPC 资源规则时有两种模式。**经典评估**为访问模式赋予固定优先级；**基于特异性的评估**先比较进程选择器和资源模式匹配，再决定应用哪个访问模式。

这是决策中彼此独立的部分：

* **进程选择器**决定规则的哪种程序专用形式匹配；
* **资源模式**决定配置的路径或对象名如何匹配所请求的资源；
* **访问模式**决定胜出规则所代表的动作，例如封闭（Closed）、只读（Read）、只写（Write）、常规（Normal）或打开（Open）。

规则特异性不会把这些部分简化为“最长规则获胜”的计算。

## 何时启用基于特异性的评估

生效状态为：

```text
RestrictDevices OR UsePrivacyMode OR UseRuleSpecificity
```

`UseSecurityMode=y` 会启用设备限制行为，因此也会启用规则特异性。所以在隐私模式或设备限制处于活动状态时，显式设置 `UseRuleSpecificity=n` 并不会关闭特异性。

在上述选项都未启用该功能的普通沙盒中，使用经典评估。配置和 SandMan 行为参见 [Use Rule Specificity](../Content/UseRuleSpecificity.md)。

## 经典评估

规则特异性关闭时，文件和注册表规则使用固定的经典优先级：

```text
封闭 > 写入 > 读取 > 打开 > 常规 > 默认
```

匹配的封闭、写入或读取规则会在其优先级层级终止比较。常规匹配可以被选中，但匹配的打开规则可以替代它。因此在这一模型下，即使打开模式看起来范围更窄，封闭匹配仍优先于冲突的打开匹配。

## 基于特异性的评估

启用规则特异性时，Sandboxie 从相关访问列表中比较候选项。当进程选择器不更差且资源模式匹配改进了匹配器所考虑的某项特征时，靠后的访问列表可以替代靠前的候选。

这意味着程序专用规则或看起来更长的路径都不会自动获胜。进程选择器和实际模式匹配都起作用。

### 进程选择器

当前的进程匹配层级为：

| 选择器 | 内部层级 |
| --- | ---: |
| 匹配的正向进程名、通配名或 ProcessGroup | 0 |
| 匹配的否定选择器 | 1 |
| 显式 `*` 选择器 | 2 |
| 无进程选择器 | 3 |

例如：

```ini
OpenFilePath=firefox.exe,C:\Path
OpenFilePath=fire*.exe,C:\Path
OpenFilePath=<Browsers>,C:\Path
OpenFilePath=!firefox.exe,C:\Path
OpenFilePath=*,C:\Path
OpenFilePath=C:\Path
```

前三种形式在匹配时都可以获得最佳层级。因此把层级 0 称为**匹配的正向进程选择器**比称为“精确进程名匹配”更准确。

更好的进程层级在跨列表比较中起门控作用；它不是绝对优先级。新候选的进程层级不能更差，并且必须改进某项相关的资源匹配特征。例如：

```ini
OpenFilePath=firefox.exe,C:\*
ClosedFilePath=C:\Sensitive\Records\*
```

正向的 Firefox 选择器本身并不保证范围更宽的打开规则会替代更具体的封闭候选项。

### 资源模式匹配

Sandboxie 内部的“精确/非精确”之分并不等同于“不含通配符”。它主要基于模式是否以 `*` 结尾：

```text
C:\Foo\*   非精确
*foo*      非精确
*.tmp      精确
foo?       可以是精确
```

匹配长度描述模式在测试资源上成功匹配到的范围。对于通配模式，它不一定是配置规则中的字面字符数。

因此，`*.tmp` 可以是强候选：它可以被归类为精确，且其匹配可以延伸到所请求路径的末尾。但它并不普遍优先于其他所有规则——进程层级、访问列表比较、其他匹配属性和平局仍然参与判定。

匹配器还区分直接匹配与用尾部分隔符重试路径所产生的某些兼容匹配。在其他候选项相互竞争时，直接匹配可以优先。

当来自不同访问列表的候选项具有相同的正向匹配长度时，内部通配段更少的候选项可能被优先。这不是“通配符少者永远获胜”的通用规则；特别地，它不是同一列表内条目之间的通用平局判定依据。

在一个访问列表内部，更长的合格匹配可以替代靠前的候选。仅因通配符更少，等长候选通常不会替代已有候选。因此在完全平局时，配置顺序仍然可能有影响；但沙盒、模板、回退和内部规则的详细加载顺序不应被视为稳定的公开优先级契约。

### 访问列表比较

对于基于特异性的文件和注册表评估，当前遍历顺序为：

```text
封闭, 写入, 读取, 常规, 打开
```

当靠后列表的实际匹配被认为更优时，它可以替代靠前候选。如果所有比较特征均平局，则保留靠前的候选。因此完全平局时的偏好为：

```text
封闭 > 写入 > 读取 > 常规 > 打开
```

**这只是平局行为**——并不意味着规则特异性激活时封闭总是获胜。

## 文件和注册表规则

文件和注册表匹配使用五个访问列表：

| 访问模式 | 一般含义 |
| --- | --- |
| 常规 | 应用 Sandboxie 的常规虚拟化策略 |
| 打开 | 直接访问主机资源 |
| 封闭 | 拒绝访问 |
| 读取 | 允许读取真实资源，同时拒绝修改 |
| 写入 / 仅沙盒 | 隐藏主机资源，同时保留沙盒副本可用 |

这些是概念性描述；具体的文件和注册表操作在 Windows API 层面不一定完全对应。

例如，启用特异性时：

```ini
UseRuleSpecificity=y
ClosedFilePath=C:\Data\*
OpenFilePath=C:\Data\App\*
```

更具体的打开规则可以在 `C:\Data\App\` 下的资源上胜出。特异性关闭时，经典评估下匹配的封闭规则获胜。

## IPC 的差异

通用命名 IPC 对象匹配不使用同样的五列表比较。它使用：

```text
NormalIpcPath
OpenIpcPath
ClosedIpcPath
```

特异性激活时，在相同比较原则下，更具体的常规或打开 IPC 候选项可以替代范围更宽的封闭候选项。参见 [Normal IPC Path](../Content/NormalIpcPath.md)。

`ReadIpcPath` 则不同。它有文档的 `$:` 形式主要属于独立的进程/线程访问策略：

```ini
ClosedIpcPath=$:target.exe
OpenIpcPath=$:target.exe
ReadIpcPath=$:target.exe
```

这些目标进程规则使用它们自己的匹配器以及封闭、打开、再读取的相关顺序。它们不使用上述资源路径特异性层级。参见 [Read IPC Path](../Content/ReadIpcPath.md)。

## 配置模式细节

配置的文件和注册表规则在模式不含 `*` 时通常会获得隐式后缀星号处理。例如这样一条配置规则：

```ini
NormalFilePath=C:\Foo
```

加载时可能等价于 `C:\Foo*`。这会改变规则的范围及其精确/非精确分类。前置的 `|` 会抑制该自动后缀，并在文件/注册表匹配前被移除。

IPC 路径列表不会获得同样的隐式尾部 `*`。需要更广泛匹配时，请显式书写 IPC 通配符。

## 版本历史

| 变更 | 版本 |
| --- | --- |
| 引入可选的规则特异性和常规规则 | Sandboxie Plus 1.0.0 / Classic 5.55.0 |
| 改进精确与尾部通配符的优先级 | Sandboxie Plus 1.3.0 / Classic 5.58.0 |
| 改进通配符和平局处理 | Sandboxie Plus 1.3.1 / Classic 5.58.1 |
| 主要匹配优先于辅助匹配 | Sandboxie Plus 1.8.0 / Classic 5.63.0 |

## 相关页面

- [Use Rule Specificity](../Content/UseRuleSpecificity.md)
- [Normal File Path](../Content/NormalFilePath.md)
- [Normal Key Path](../Content/NormalKeyPath.md)
- [Normal IPC Path](../Content/NormalIpcPath.md)
- [Resource Access Settings](../Content/ResourceAccessSettings.md)
