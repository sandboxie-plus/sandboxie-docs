# 阻止 IE 嵌入 {#block-ie-embedding}

_BlockIEEmbedding_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项全局设置。它为某些宿主侧访问 Internet Explorer CLSID 注册表路径的请求启用一种范围很窄的兼容性变通处理；它不是通用的浏览器或 COM 阻止控件。

```ini
[GlobalSettings]
BlockIEEmbedding=y
```

没有有效的全局值时，该变通处理处于关闭状态。仅写在单个沙盒节中的值不会控制它；经全局合并后适用的模板也可以提供有效值。

<div id="scope"></div>

## 范围

启用后，如果传给回调的键名包含 `CLSID\{0002DF01-0000-0000-C000-000000000046}`，且调用方未被该驱动程序路径跟踪为沙盒化进程，Sandboxie 的驱动程序会拒绝注册表键的打开/创建请求。该比较不区分大小写且按子串匹配，因此传入的子键路径也可能匹配。它不保证覆盖访问该注册表键的所有等效方式。在 Windows 10 创意者更新及更高版本上，源自内核模式的请求不受此检查约束。

仅当调用方的可执行文件基本名与下列名称之一完全匹配（不区分大小写）时，才会进行拒绝：

- `winword.exe`
- `powerpnt.exe`
- `excel.exe`
- `explorer.exe`
- `svchost.exe`

匹配的打开/创建请求会在常规的沙盒注册表过滤之前以 `STATUS_ACCESS_DENIED` 被拒绝。`OpenKeyPath` 这类注册表访问规则无法覆盖该项特定拒绝。具有被跟踪的 Sandboxie 进程记录的调用方不会被 `BlockIEEmbedding` 拒绝；后续的注册表处理会走适用于该调用方的常规路径。该设置不会直接拦截值查询、值写入、键枚举或删除。

如果该设置关闭、键名或可执行文件不匹配，或无法获取进程名，则不会发生这种特殊拒绝。该请求仍可能因其他 Sandboxie 规则或 Windows 权限而失败。

<div id="compatibility-context"></div>

## 兼容性背景

该选项起源于 Sandboxie 5.19.1 beta / 5.20 时期，作为针对 Office 超链接场景的变通处理——该场景涉及嵌入的 Internet Explorer 与单独强制沙盒化的浏览器。在当前的 Windows 或 Office 版本上，不保证出现该历史结果。_BlockIEEmbedding_ 本身既不启动 Internet Explorer，也不启用 [强制进程](ForceProcess.md)。

<div id="configuration-availability"></div>

## 配置可用性

这是一项手动 INI 设置；SandMan 与 Sandboxie Control Classic 都没有专门的控件。驱动程序在每次相关的注册表请求时检查有效的全局值。Sandboxie 配置成功重载后，之后的请求可以使用更改后的值，而无需重启应用程序；已获得的注册表句柄不会被撤销。
