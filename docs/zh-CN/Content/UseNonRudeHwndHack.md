# 使用非恶意 HWND 修补方案

_UseNonRudeHwndHack_ 是沙盘配置（[沙盘配置](SandboxieIni.md)）中的一个沙箱设置，从 v1.16.0 / 5.71.0 开始可用。启用该设置后，可以针对 NonRudeHWND 属性进行兼容性修补，从而提升沙箱内应用程序的全屏支持能力。

用法如下：

```ini
[DefaultBox]

UseNonRudeHwndHack=y
```

## 目的

NonRudeHWND 属性是 Windows 的一个窗口属性，应用程序可设置此属性以通知系统其全屏行为及与任务栏的交互方式。一些应用程序，尤其是游戏和媒体播放器，会设置该属性以保证全屏显示时不被任务栏干扰。

当沙箱内的应用程序尝试通过 `SetProp()` 设置 NonRudeHWND 属性时，沙盘的安全模型通常会阻止或过滤这些属性修改，以维护隔离性。但对于依赖这一属性的应用程序，这样做可能会导致全屏功能失效。

## 技术细节

该设置控制了沙盘 GUI 属性处理代码中的 `Gui_NonRudeHWND_Hack` 变量[^1]。启用后，沙盘会拦截对 `SetPropW()` 和 `SetPropA()` 函数的调用，并专门允许 NonRudeHWND 属性被成功设置，返回 `TRUE`，但实际上并不会真正执行该操作[^2]。

修补方案的工作原理如下：

1. 拦截以 "NonRudeHWND" 为属性名的 `SetProp` 调用[^3]
2. 检测到此属性时，立即返回成功[^4]
3. 让应用程序认为属性已经正确设置
4. 在不影响沙箱安全性的前提下，允许正常的全屏行为

## 默认行为

默认情况下，该设置：
- **在未启用应用程序隔离模式时**，为 **启用**（`y`）
- **在启用应用程序隔离模式时**，为 **禁用**（`n`）

其逻辑为：`!Dll_CompartmentMode`[^5] ——即，除非启用隔离模式，否则此功能处于启用状态。

## 重要说明

- 此设置仅影响沙盘如何处理 NonRudeHWND 属性，并不会修改 Windows 的实际任务栏行为
- 修补方案能够在保持沙箱安全性的同时，让应用程序在全屏模式下正常运行

## 相关问题

该设置是为解决全屏兼容性问题而引入的，详见 GitHub 问题 [#4761](https://github.com/sandboxie-plus/Sandboxie/issues/4761)[^6]

[^1]: **源码**：guiprop.c: `static BOOLEAN Gui_NonRudeHWND_Hack = FALSE;`

[^2]: **源码**：guiprop.c: `Gui_SetPropW()` 和 `Gui_SetPropA()` 函数会检查 NonRudeHWND 属性，且在修补方案启用时立即返回 `TRUE`

[^3]: **源码**：guiprop.c: `if (_wcsicmp(lpString, L"NonRudeHWND") == 0)` 以及第 537 行：`if (strcmp(lpString, "NonRudeHWND") == 0)`

[^4]: **源码**：guiprop.c: `return TRUE;` ——函数会返回成功，但并不会真正设置属性

[^5]: **源码**：guiprop.c: `Gui_NonRudeHWND_Hack = SbieApi_QueryConfBool(NULL, L"UseNonRudeHwndHack", !Dll_CompartmentMode);`

[^6]: GitHub issue [#4761](https://github.com/sandboxie-plus/Sandboxie/issues/4761)