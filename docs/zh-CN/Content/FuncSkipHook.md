# 跳过函数钩子

`FuncSkipHook` 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，告诉 Sandboxie 不要尝试钩住特定的导出 API 函数。

当对某个函数的钩子尝试导致不稳定、与其他安全产品不兼容或出现不想要的行为时，此设置很有用。

## 语法

```ini
[DefaultBox]

FuncSkipHook=FunctionNameA
FuncSkipHook=FunctionNameB
```

注意：

- 每条 `FuncSkipHook` 条目会与正在考虑钩住的函数名开头进行比较；匹配会导致跳过该钩子。

## 用法

通常用于模板中，以避免为特定应用程序或钩子标识符安装钩子。

示例：

```ini
[DefaultBox]

FuncSkipHook=SomeVendor_BrokenCall
FuncSkipHook=PStoreCreateInstance
```

## 行为

- 辅助函数 `SbieDll_FuncSkipHook` 查询 `FuncSkipHook` 条目的配置。对每条配置条目，它在配置的宽字符字符串与被钩住的 ASCII 函数名之间执行前缀比较。如果配置的字符串在匹配函数名开头字符时耗尽，则认为该函数匹配并跳过钩子。
- 为提高效率，如果首次查询未找到任何 `FuncSkipHook` 条目，后续调用将完全跳过此检查。

## 技术说明

- 代码使用 `SbieApi_QueryConfAsIs` 以循环方式按索引读取条目，直到查询失败（或返回不同错误）。每个返回的 `WCHAR` 缓冲区通过与函数名并行推进两个指针进行比较；当配置的宽字符串结束而 ASCII 函数名仍有字符时，比较停止并报告匹配。
- 这种比较实际上是区分大小写的前缀匹配（它并行比较原始字符）。如果你依赖不区分大小写的匹配，请注意 `FuncSkipHook` 的行为与 `SkipHook` 不同。

## 图形界面

`FuncSkipHook` 是高级设置，通常手工编辑 INI。Sandboxie 附带的模板文件可能包含示例 `FuncSkipHook` 条目。

## 相关设置

- [跳过钩子](SkipHook.md) — 按模块或标识符跳过钩子的模块/钩子名级设置。

## 脚注

[^1]: 实现位于 `SbieDll_FuncSkipHook`（见 `dllhook.c`）。该函数用 `SbieApi_QueryConfAsIs` 查询 `FuncSkipHook` 条目，并逐字符比较配置的宽字符串与函数名；配置的字符串耗尽即表示匹配并触发跳过钩子。如果未找到条目，函数会设置内部标志以禁用进一步检查，提高效率。
