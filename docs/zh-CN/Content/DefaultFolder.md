# 默认文件夹

_DefaultFolder_ 是 [沙盘配置](SandboxieIni.md) 中自 v1.15.12 / 5.70.12 起提供的沙箱设置，在启用 [隐私模式](../PlusContent/privacy-mode.md) 时，用于指定初始化期间需要在沙箱内预先创建的文件夹。此设置用于确保关键的系统及用户目录在应用程序尝试访问之前，已经在沙箱环境中存在，以防止可能发生的访问失败现象。

## 用法

```ini
[DefaultBox]

DefaultFolder=%SystemRoot%
DefaultFolder=%USERPROFILE%
DefaultFolder=%Desktop%
DefaultFolder=C:\SomeSpecificPath
```

## 概述

当沙箱以隐私模式（`UsePrivacyMode=y`）运行时，系统上的大多数位置都会被隔离，而许多程序可能会要求某些标准目录必须存在。`DefaultFolder` 设置可以确保这些目录在沙箱内部被预先创建，从而保证依赖这些目录的应用程序能够兼容正常运行。

## 工作原理

在沙箱初始化阶段[^1]，Sandboxie 按如下流程处理每一个 `DefaultFolder` 项：

1. **环境变量展开**：若路径中包含环境变量（如 `%SystemRoot%` 或 `%USERPROFILE%`），系统会将其展开为实际的值。
2. **路径转换**：DOS 路径会被转换为对应的 NT 内部路径，便于内部处理。
3. **沙箱内创建**：相应的目录结构会在沙箱目录层级中被创建。

## 模板集成

Sandboxie 内置了一个名为 `TemplateDefaultFolders` 的模板[^2]，为应用程序提供了一组常用标准目录。该模板包括：

### 系统目录

- `%SystemRoot%`（Windows 目录）
- `%TEMP%`（临时文件夹）
- `%ProgramFiles%` 与 `%ProgramFiles(x86)%`
- `%CommonProgramFiles%` 与 `%CommonProgramFiles(x86)%`

### 用户配置文件目录

- `%USERPROFILE%`（用户配置文件根目录）
- `%Desktop%`（用户桌面）
- `%Personal%`（文档文件夹）
- `%{374DE290-123F-4565-9164-39C4925E467B}%`（下载文件夹）
- `%Favorites%`（Internet 收藏夹）
- `%{BFB9D5E0-C6A9-404C-B2B2-AE6DB6AF4968}%`（链接文件夹）
- `%My Music%`、`%My Pictures%`、`%My Video%`（媒体文件夹）
- `%{4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}%`（保存的游戏）

### 公共目录

- `%PUBLIC%` 及其子目录
- `%LOCALAPPDATA%`（本地应用数据目录）

## 使用场景

- **隐私模式**：在启用 `UsePrivacyMode=y` 时，确保沙箱正确运行
- **应用兼容性**：避免那些检测标准目录是否存在的程序因目录缺失而出错
- **初始化优化**：提前创建本应首次访问时才生成的目录

## 限制

- 仅在启用隐私模式时生效
- 目录创建需遵循沙箱的路径规范及限制
- 环境变量需在初始化时为有效且可展开

## 示例

### 自定义应用程序目录

```ini
[ApplicationBox]

UsePrivacyMode=y
DefaultFolder=C:\MyApp\Data
DefaultFolder=%APPDATA%\MyApplication
```

## 相关设置

- [UsePrivacyMode](UsePrivacyMode.md) — 启用隐私模式（`DefaultFolder` 需此项为前提）
- [NormalFilePath](NormalFilePath.md) — 控制对指定路径的读写访问
- [FileRootPath](FileRootPath.md) — 指定沙箱数据容器的位置

[^1]: 文件夹的预创建过程发生在检测到隐私模式标志的进程初始化期间的 `File_CreateBaseFolders()` 函数中。该函数会遍历模板默认项及用户自定义的 `DefaultFolder` 配置项。（来源：`/Sandboxie/core/dll/file_dir.c:3550`）

[^2]: `TemplateDefaultFolders` 模板定义在 `Templates.ini` 文件中，涵盖了应用程序通常需要存在的标准 Windows 目录。（来源：`/Sandboxie/install/Templates.ini`）