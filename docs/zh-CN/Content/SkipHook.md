# 跳过钩子

`SkipHook` 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，用于阻止 Sandboxie 为特定模块或钩子标识符安装特定钩子。使用 `Dll_SkipHook` 辅助函数的调用方会查询它。

当以逗号分隔的标识符列表比逐函数列表更方便时，可使用此设置进行模块级或钩子名级排除。

## 语法

```ini
[DefaultBox]

; 跳过特定模块/钩子标识符的钩子（逗号分隔列表）
SkipHook=[<program>,]<entry1>,<entry2>,...
```

注意：

- 条目是以逗号分隔的标记。每个标记可以选择以程序/映像名称加逗号作为前缀（例如：`PotPlayer64.exe,cocreate`），把该标记限定到特定程序。存在程序前缀时，其余标记仅适用于该程序。
- 每个标记（任何可选程序前缀之后的部分）会与请求的钩子名进行不区分大小写的前缀比较。[^1]
- 并非每条钩子安装路径都会查询 `Dll_SkipHook`，因此 `SkipHook` 可能无法阻止每一次钩子尝试。

## 用法

通常用于模板中，以避免为特定应用程序或钩子标识符安装钩子。

示例：

```ini
[DefaultBox]

SkipHook=DragonSaga.exe,enumwin,findwin
SkipHook=PotPlayer64.exe,cocreate
```

## 行为

- 调用时，`Dll_SkipHook` 会为当前映像/模板加载配置的 `SkipHook` 字符串，并扫描以逗号分隔的标记。如果某个标记匹配请求钩子名的开头（不区分大小写），辅助函数返回真，调用方可以跳过安装该钩子。
- 由于此检查并未在每一个钩子安装点普遍使用，即使列在 `SkipHook` 中，某些钩子仍可能被安装。

## 图形界面

`SkipHook` 是高级设置，通常手工编辑 INI。Sandboxie 附带的模板文件可能包含示例 `SkipHook` 条目。

## 相关设置

- [跳过函数钩子](FuncSkipHook.md) — 用于跳过特定 API 函数钩子的函数级设置。

## 脚注

[^1]: `Dll_SkipHook` 用 `SbieDll_GetSettingsForName(..., L"SkipHook", ...)` 初始化内部缓冲区，然后扫描以逗号分隔的标记。匹配使用不区分大小写的前缀比较（`_wcsnicmp`）。
