# 跳过钩子

`SkipHook` 是沙盘配置（[Sandboxie Ini](SandboxieIni.md)）中的一个沙箱设置，用于阻止沙盘为特定模块或钩子标识符安装指定钩子。调用者在使用 `Dll_SkipHook` 辅助函数时会参考该设置。

请将此设置用于基于模块或钩子名称的排除场景——当逗号分隔的标识符列表比按函数逐一列出更便捷时。

## 语法

```ini
[DefaultBox]

; 针对特定模块/钩子标识符跳过钩子（逗号分隔列表）
SkipHook=[<program>,]<entry1>,<entry2>,...
```

注意事项：

- 条目由逗号分隔。每个条目可选择性地以程序/镜像名称加逗号作为前缀（例如：`PotPlayer64.exe,cocreate`），以便将该条目限定于某个程序。当存在程序前缀时，后续条目仅适用于该程序。
- 每个条目（即去除任何可选程序前缀之后的部分）会采用不区分大小写的前缀比较方式，与请求的钩子名称进行对比[^1]
- 并非所有钩子安装路径都会参考 `Dll_SkipHook`，因此 `SkipHook` 可能无法阻止每一次钩子的安装尝试

## 使用方法

通常用于模板中，以避免对特定应用程序或钩子标识符进行钩挂操作。

示例：

```ini
[DefaultBox]

SkipHook=DragonSaga.exe,enumwin,findwin
SkipHook=PotPlayer64.exe,cocreate
```

## 行为特性

- 调用时，`Dll_SkipHook` 会加载当前镜像或模板配置的 `SkipHook` 字符串，扫描逗号分隔的条目。如果某一条目与请求的钩子名称的起始部分一致（忽略大小写），辅助函数将返回真，调用者可以跳过该钩子的安装
- 由于这种检查并未在每一个钩子安装点全部应用，所以即使已列在 `SkipHook` 中，部分钩子仍可能被安装

## 图形界面

`SkipHook` 属于高级设置，通常需手动编辑 INI 文件。沙盘自带的模板文件内可能包含 `SkipHook` 示例条目。

## 相关设置

- [FuncSkipHook](FuncSkipHook.md) —— 用于跳过特定 API 函数钩挂的函数级设置

## 注释

[^1]: `Dll_SkipHook` 会通过 `SbieDll_GetSettingsForName(..., L"SkipHook", ...)` 初始化内部缓冲区，然后扫描逗号分隔条目。匹配逻辑采用不区分大小写的前缀比较（`_wcsnicmp`）