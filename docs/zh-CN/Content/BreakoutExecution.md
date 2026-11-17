# 分离执行 {#breakout-execution}

分离（breakout）是针对选定的后续操作、有意对沙盒封闭性做出的例外。[分离沙盒进程](BreakoutProcess.md) 与 [分离文件夹](BreakoutFolder.md) 可以影响从沙盒内部发起的新进程创建尝试。[分离文档](BreakoutDocument.md) 则适用于受支持的、用于打开匹配路径的 Shell 请求。这些设置都不会把已在运行的进程移出其沙盒、授予权限提升，或让任意文件访问脱离沙盒。

<div id="process-breakout"></div>

## 进程分离

当沙盒化程序尝试启动新进程时，Sandboxie 会先检查目标是否为分离候选对象。随后，沙盒化进程请求 Sandboxie 服务在源沙盒之外创建该进程。服务在创建进程之前会独立检查分离规则；仅凭最初的候选检查并不构成对这次逃逸的授权。

如果服务以 `ERROR_NOT_SUPPORTED` 拒绝该分离请求，Sandboxie 会继续走常规的沙盒化进程创建路径。其他创建错误不一定具有这种回退处理。对于 `BreakoutProcess`，服务还要求目标可执行文件解析到源沙盒文件根之外的宿主文件。这项特定的宿主文件检查不适用于 `BreakoutFolder`。

成功分离并不一定让进程脱离沙盒。服务会检查已启用的沙盒中是否存在匹配的 [强制进程](ForceProcess.md) 或 [强制文件夹](ForceFolder.md) 规则，因此另一个沙盒可以捕获这次启动。例如，若从 Email 沙盒中查看 PDF 时启动了 `browser.exe`，Email 中的 `BreakoutProcess=browser.exe` 与 Browser 沙盒中的 `ForceProcess=browser.exe` 可以把这次浏览器启动路由到 Browser。这不是可配置的沙盒间优先级：当多个沙盒匹配时，不要依赖会选中某个特定目标。`ForceChildren` 不参与这项显式的目标检查。

如果该强制检查最终指回源沙盒，服务会以 `ERROR_NOT_SUPPORTED` 拒绝分离请求，并恢复常规的沙盒化创建。对于宿主分离，服务会使用与请求相符的令牌创建进程，并向沙盒化调用方返回受限访问的进程与线程句柄，而不是完全控制句柄。分离不是一种权限提升机制。

<div id="document-breakout"></div>

## 文档分离

`BreakoutDocument` 是独立的 Shell 打开机制，而不是基于文件夹的进程规则。在被拦截的 `ShellExecuteExW` 路径上，Sandboxie 会把提供的文件/路径文本与配置的模式进行比较。一旦匹配，该请求会经由用户会话代理发送，由代理验证沙盒化调用方与会话，并再次检查规则。随后它请求宿主 Shell 用 `open` 谓词打开匹配的路径。

宿主请求包含的是路径，而不是原始 Shell 请求的未经更改的副本：原始谓词、参数与工作目录都不会被转发。这并不覆盖应用程序打开文档的所有方式。宿主侧打开可能会启动某个应用程序，或在原始沙盒的文件与注册表虚拟化之外执行内容。

> **安全警告：** 请使用较窄的路径和预期的文档类型。像 `BreakoutDocument=C:\path\*` 这样的宽泛规则可能允许可执行文件或脚本内容在源沙盒之外运行。SandMan 会对宽泛或有风险的文档模式发出警告，但其扩展名检查属于界面层防护，并非运行时允许列表。手动编辑的配置可能包含更宽泛的模式。

<div id="explorer-compatibility-bridge"></div>

## Explorer 兼容性桥接

`BreakoutDocumentProcess` 是一项可识别映像的布尔兼容性设置，默认禁用。Windows Explorer 模板会设置 `BreakoutDocumentProcess=explorer.exe,y`，因为 Explorer 可能通过进程创建而非通常被拦截的 `ShellExecuteExW` 路径来发起相关的文档启动。对于该映像，Sandboxie 会在后续的进程创建尝试中按 `BreakoutDocument` 规则检查命令行的剩余部分。这是一个 Explorer 兼容性桥接，而不是另一份通用分离列表；通常不需要手动配置。它在 Sandboxie Plus 1.15.1 / Classic 5.70.1 中加入。

<div id="configuration-and-applying-changes"></div>

## 配置与应用更改

生效的分离条目可以来自沙盒配置或适用的模板。在 SandMan 中，打开 **沙盒选项 > 程序控制 > 分离程序**，即可使用**分离程序**、**分离目录**、**分离文档**、**显示模板** 与 **移除**。未选中的条目仍会以相应的 `BreakoutProcessDisabled`、`BreakoutFolderDisabled` 或 `BreakoutDocumentDisabled` 设置保留在界面中；这些已保存的条目并不是生效的分离规则。此界面中不存在单一的全局分离开关。

进程规则会针对后续相关的进程创建尝试进行评估，文档规则则针对后续受支持的 Shell 打开请求进行评估。更改不会迁移已有进程，也不会改变已完成的文档打开。在有效配置更新后，后续被评估的操作可以使用新规则，而无需仅为分离功能重启 Windows、服务或已在运行的沙盒化应用程序。

<div id="version-history"></div>

## 版本历史

`BreakoutProcess` 与 `BreakoutFolder` 出现于 Sandboxie Plus 1.0.8 / Classic 5.55.8。在 1.0.9 / 5.55.9 中，进程分离改为围绕服务创建进程来重做。`BreakoutDocument` 于 1.15.0 / 5.70.0 引入，随后在 1.15.1 / 5.70.1 加入了与 Explorer 相关的 `BreakoutDocumentProcess` 桥接。

<div id="related-pages"></div>

## 相关页面

- [分离沙盒进程](BreakoutProcess.md)
- [分离文件夹](BreakoutFolder.md)
- [分离文档](BreakoutDocument.md)
- [强制进程](ForceProcess.md)
- [强制文件夹](ForceFolder.md)
