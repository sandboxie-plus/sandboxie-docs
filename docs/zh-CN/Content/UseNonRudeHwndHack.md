# 使用非恶意 HWND 修补方案

_UseNonRudeHwndHack_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.16.0 / 5.71.0 起可用。此设置为 NonRudeHWND 属性启用兼容性修补，以改善沙盒化应用程序的全屏支持。

用法：

```ini
[DefaultBox]

UseNonRudeHwndHack=y
```

## 目的

NonRudeHWND 属性是一个 Windows 窗口属性，应用程序可以设置它来告知系统其全屏行为以及与任务栏的交互。某些应用程序（尤其是游戏和媒体播放器）设置此属性，以确保正确的全屏显示而不受不必要的任务栏干扰。

当沙盒化应用程序尝试通过 `SetProp()` 设置 NonRudeHWND 属性时，Sandboxie 的安全模型通常会阻止或过滤这些属性修改以保持隔离。然而，这会破坏依赖此属性的应用程序的全屏功能。

## 技术细节

此设置控制 Sandboxie 图形界面属性处理代码中的 `Gui_NonRudeHWND_Hack` 变量[^1]。启用时，Sandboxie 会拦截对 `SetPropW()` 和 `SetPropA()` 函数的调用，专门允许 NonRudeHWND 属性成功设置，在不实际执行操作的情况下返回 `TRUE`[^2]。

此修补的工作原理：

1. 拦截属性名称为"NonRudeHWND"的 `SetProp` 调用[^3]
2. 检测到此特定属性时，立即返回成功[^4]
3. 让应用程序相信属性已正确设置
4. 这在不损害沙盒安全的情况下启用正确的全屏行为

## 默认行为

默认情况下，此设置：

- 未运行在应用程序隔离模式时为**启用**（`y`）
- 运行在应用程序隔离模式时为**禁用**（`n`）

其逻辑是：`!Dll_CompartmentMode`[^5]——即除非隔离模式处于活动状态，否则启用。

## 重要说明

- 此设置只影响 Sandboxie 如何处理 NonRudeHWND 属性——它不修改 Windows 实际的任务栏行为
- 此修补在保持沙盒安全的同时允许应用程序在全屏模式下正常运行

## 相关问题

引入此设置是为了解决全屏兼容性问题，特别是 GitHub 问题 [#4761](https://github.com/sandboxie-plus/Sandboxie/issues/4761)[^6]。

[^1]: **来源**：guiprop.c：`static BOOLEAN Gui_NonRudeHWND_Hack = FALSE;`

[^2]: **来源**：guiprop.c：`Gui_SetPropW()` 和 `Gui_SetPropA()` 函数检查 NonRudeHWND 属性，启用修补时立即返回 `TRUE`。

[^3]: **来源**：guiprop.c：`if (_wcsicmp(lpString, L"NonRudeHWND") == 0)` 以及第 537 行：`if (strcmp(lpString, "NonRudeHWND") == 0)`

[^4]: **来源**：guiprop.c：`return TRUE;` - 函数在不实际设置属性的情况下返回成功。

[^5]: **来源**：guiprop.c：`Gui_NonRudeHWND_Hack = SbieApi_QueryConfBool(NULL, L"UseNonRudeHwndHack", !Dll_CompartmentMode);`
