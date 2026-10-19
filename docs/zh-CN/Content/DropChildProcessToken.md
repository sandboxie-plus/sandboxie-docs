# 丢弃子进程令牌

`DropChildProcessToken` 是一项高级调试设置，自 Sandboxie Plus 1.15.6 / Classic 5.70.6 起可用。它可用于排查创建子进程时的兼容性问题，包括历史上所称的“绿盒”兼容性问题，不宜作为放宽令牌限制的常规做法。

当设置匹配时，Sandboxie 会清除调用进程在创建子进程时显式提供的 `hToken` 参数。此操作不会禁用 Sandboxie 的整个令牌处理流程，也不会改写已有的令牌对象。

<div id="_2"></div>
<div id="_3"></div>
<div id="_8"></div>

## 配置与调用进程范围 {#configuration-and-caller-scope}

```ini
[DefaultBox]
DropChildProcessToken=parent.exe,y
```

运行时默认值为 `n`。此设置按调用进程的映像名称匹配：示例中的 `parent.exe` 指定的是**发起子进程创建调用的沙盒内进程**，不是它启动的可执行文件。该规则改变匹配进程创建子进程的方式，不会改变 `parent.exe` 自身的令牌。

<div id="_5"></div>

对于被识别为 Acrobat Reader 或插件容器的调用进程，Sandboxie 也会自动清除其为创建子进程提供的令牌参数，无需配置 `DropChildProcessToken` 规则。历史上的 Flash 专用条件已被注释掉，目前不会触发这种自动处理。

<div id="_4"></div>
<div id="_6"></div>

## 对子进程的影响 {#what-happens-to-the-child}

此设置会从本次创建请求中移除调用进程提供的子进程令牌（`hToken = NULL`）。子进程最终使用何种令牌运行，取决于后续的沙盒模式和令牌处理路径：

- **标准沙盒**：驱动程序通常仍会执行 `Token_ReplacePrimary()`，并为子进程分配 Sandboxie 的受限主令牌。清除调用者传入的令牌参数与随后替换主令牌，是两个独立阶段。
- **[应用隔间](../PlusContent/compartment-mode.md)或 [OriginalToken](OriginalToken.md)**：会绕过正常的受限主令牌替换。因此，清除传入的令牌参数对 Windows 为子进程选择的令牌可能产生不同且更大的影响。

<div id="_9"></div>

此设置不保证子进程继承父进程的完整令牌，也不意味着 Sandboxie 的其他隔离机制已被禁用。应仅用它排查具体的子进程创建兼容性问题，并在决定保留此配置前评估对令牌的影响。

<div id="_7"></div>
<div id="_10"></div>

## 相关页面 {#related-pages}

- [AppContainer 令牌兼容性](AppContainerTokens.md)
- [原始令牌](OriginalToken.md)
- [应用隔间](../PlusContent/compartment-mode.md)
- [Sandboxie Ini](SandboxieIni.md)
