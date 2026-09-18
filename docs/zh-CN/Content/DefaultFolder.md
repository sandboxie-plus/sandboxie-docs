# 默认文件夹

_DefaultFolder_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.15.12 / 5.70.12 起可用。它指定启用 [隐私模式](../PlusContent/privacy-mode.md) 时，应在初始化期间于沙盒中预创建的文件夹。此设置确保在程序尝试访问之前，必要的系统和用户目录已存在于沙盒环境中，防止潜在失败。

## 用法

```ini
[DefaultBox]

DefaultFolder=%SystemRoot%
DefaultFolder=%USERPROFILE%
DefaultFolder=%Desktop%
DefaultFolder=C:\SomeSpecificPath
```

## 概述

当沙盒以隐私模式（`UsePrivacyMode=y`）运行时，系统上的大多数位置被隔离，程序可能期望某些标准目录存在。`DefaultFolder` 设置确保这些目录在沙盒内预创建，保持与依赖这些目录存在的应用程序的兼容性。

## 工作原理

在沙盒初始化期间[^1]，Sandboxie 按以下方式处理每条 `DefaultFolder` 条目：

1. **环境变量展开**：如果路径包含环境变量（如 `%SystemRoot%` 或 `%USERPROFILE%`），它们会被展开为实际值。
2. **路径转换**：DOS 路径被转换为 NT 等价路径供内部处理。
3. **沙盒创建**：在沙盒层次结构中创建相应的目录结构。

## 模板集成

Sandboxie 包含一个名为 `TemplateDefaultFolders`[^2] 的内置模板，提供应用程序通常需要的标准目录的综合集合。此模板包括：

### 系统目录

- `%SystemRoot%`（Windows 目录）
- `%TEMP%`（临时文件）
- `%ProgramFiles%` 和 `%ProgramFiles(x86)%`
- `%CommonProgramFiles%` 和 `%CommonProgramFiles(x86)%`

### 用户配置文件目录

- `%USERPROFILE%`（用户配置文件根目录）
- `%Desktop%`（用户桌面）
- `%Personal%`（文档文件夹）
- `%{374DE290-123F-4565-9164-39C4925E467B}%`（下载文件夹）
- `%Favorites%`（Internet 收藏夹）
- `%{BFB9D5E0-C6A9-404C-B2B2-AE6DB6AF4968}%`（链接文件夹）
- `%My Music%`、`%My Pictures%`、`%My Video%`（媒体文件夹）
- `%{4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}%`（已保存的游戏）

### 公共目录

- `%PUBLIC%` 及其子目录
- `%LOCALAPPDATA%`（本地应用程序数据）

## 使用场景

- **隐私模式**：启用 `UsePrivacyMode=y` 时正常运行所必需
- **应用程序兼容性**：确保检查标准目录是否存在的程序不会失败
- **初始化优化**：预创建否则会在首次访问时创建的目录

## 限制

- 仅在启用隐私模式时激活。
- 目录创建遵循标准沙盒路径规则和限制。
- 环境变量在初始化时必须有效且可展开。

## 示例

### 自定义应用程序目录

```ini
[ApplicationBox]

UsePrivacyMode=y
DefaultFolder=C:\MyApp\Data
DefaultFolder=%APPDATA%\MyApplication
```

## 相关设置

- [使用隐私模式](UsePrivacyMode.md) - 启用隐私模式（`DefaultFolder` 生效所必需）
- [标准文件路径](NormalFilePath.md) - 控制特定路径的读/写访问
- [文件根路径](FileRootPath.md) - 指定沙盒容器位置

[^1]: 文件夹预创建发生在进程初始化期间检测到隐私模式标志时的 `File_CreateBaseFolders()` 函数中。此函数遍历模板默认值和用户指定的 `DefaultFolder` 条目。（来源：`/Sandboxie/core/dll/file_dir.c:3550`）

[^2]: `TemplateDefaultFolders` 模板定义在 `Templates.ini` 文件中，提供应用程序通常期望存在的标准 Windows 目录的综合列表。（来源：`/Sandboxie/install/Templates.ini`）
