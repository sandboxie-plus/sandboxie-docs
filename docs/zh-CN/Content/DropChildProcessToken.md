# 丢弃子进程令牌

_DropChildProcessToken_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.15.6 / 5.70.6 起可用。此设置强制指定应用程序的子进程在无修改安全令牌的情况下运行，绕过 Sandboxie 正常的受限令牌机制。它主要设计为调试工具，用于排查“绿盒”（应用程序隔离）兼容性问题——即应用程序因令牌限制而无法启动或正常运行时。

## 用法

```ini
[DefaultBox]

DropChildProcessToken=chrome.exe,y
DropChildProcessToken=firefox.exe,y
DropChildProcessToken=acroread.exe,y
```

## 语法

```ini
DropChildProcessToken=<可执行文件>,y
```

其中：

- `<可执行文件>` 是应用程序可执行文件的名称（不区分大小写）。
- 值必须为 `y` 才能启用此设置。

## 技术细节

启用 `DropChildProcessToken` 时，Sandboxie 会在子进程初始化期间修改其进程创建行为：

1. **令牌置空**：在 `CreateProcessInternalW` 期间，系统检查目标应用程序是否匹配任何配置的 `DropChildProcessToken` 条目，并把进程令牌设为 `NULL`[^1]。

2. **自动应用**：此设置自动适用于特定应用程序类型——Adobe Acrobat Reader 和插件容器通过硬编码的映像类型检测默认获得此处理[^2]。

3. **绿盒兼容性**：此机制帮助那些难以适配 Sandboxie 受限安全令牌的应用程序在隔离模式中运行，该模式优先考虑兼容性而非严格隔离[^3]。

## 默认行为

无需显式配置，Sandboxie 会自动对某些应用程序类别应用令牌丢弃：

- **Adobe Acrobat Reader**：所有版本都自动丢弃子进程令牌，以防权限提升。
- **插件容器**：通过 [特殊图像分类](SpecialImage.md) 分类为 `DLL_IMAGE_PLUGIN_CONTAINER` 的应用程序自动获得此处理。
- **Flash Player 沙盒**：对 Adobe Flash Player 沙盒架构的历史支持（当前版本中已注释掉）。

**使用场景**

- **绿盒调试**：排查因令牌限制而无法启动的应用程序隔离沙盒。
- **旧应用程序支持**：启用与较新的安全令牌限制配合不佳的旧应用程序。
- **插件兼容性**：确保浏览器插件和辅助进程能在无令牌相关冲突的情况下运行。
- **开发测试**：在无 Sandboxie 基于令牌的安全隔离的情况下测试应用程序行为。

**安全影响**

- **安全性降低**：子进程与父进程使用相同令牌运行，可能降低隔离效果。
- **权限管理**：移除 Sandboxie 正常的权限限制，允许进程继承父进程的完整权限。
- **兼容性权衡**：以牺牲部分安全隔离为代价提高应用程序兼容性。
- **调试场景**：主要用于故障排除，而非生产环境。

**绿盒集成**

此设置与绿盒（应用程序隔离）配置尤其相关：

- **隔离模式**：绿盒使用 `NoSecurityIsolation=y` 禁用基于令牌的安全，同时保持文件/注册表虚拟化。
- **令牌冲突**：某些应用程序即使在隔离模式下仍会遇到问题，需要完全丢弃令牌。
- **兼容性优先**：绿盒把兼容性置于安全之上，使此设置成为问题应用程序的自然选择。

## 实现说明

令牌丢弃机制：

- 在 DLL 注入层的 `Proc_CreateProcessInternalW` 函数期间运行。
- 使用 `Config_GetSettingsForImageName_bool` 查询各应用程序设置，默认值为 `FALSE`[^4]。
- 与映像类型分类系统集成，自动处理已知的问题应用程序类型。
- 设置 `hToken = NULL` 以绕过正常的令牌创建和限制过程[^5]。
- 影响本应应用受限令牌的 `CreateProcessInternalW` 调用链。

## 相关兼容性设置

- **OriginalToken**：启用时，绕过大多数与令牌相关的修改，包括 `DropChildProcessToken`。
- **DeprecatedTokenHacks**：重新启用隔离模式中已禁用的旧式基于令牌的变通方案。
- **无安全隔离**：禁用基于令牌安全隔离的核心绿盒设置。
- **FakeAppContainerToken**：控制特定应用程序的 AppContainer 令牌模拟。

## 用法示例

- **浏览器子进程问题**：
  ```ini
  DropChildProcessToken=chrome.exe,y
  DropChildProcessToken=msedge.exe,y
  ```

- **插件容器问题**：
  ```ini
  DropChildProcessToken=plugin-container.exe,y
  DropChildProcessToken=flashplayer.exe,y
  ```

- **自定义应用程序调试**：
  ```ini
  DropChildProcessToken=myapp.exe,y
  ```

## 绿盒故障排除

当应用程序在绿盒模式下失败时：

1. 为出问题的可执行文件启用 `DropChildProcessToken`。
2. 测试应用程序能否正常启动和运行。
3. 如果成功，说明问题与令牌相关，可保持此设置启用。
4. 如果仍失败，请排查其他兼容性设置或文件/注册表访问问题。

## 相关设置

- [特殊图像分类](SpecialImage.md) - 自动对插件容器和 Adobe Reader 应用令牌丢弃。
- [无安全隔离](NoSecurityIsolation.md) - 应用程序隔离模式的核心绿盒设置。

相关 Sandboxie Plus 设置：可在高级调试选项中使用（标准界面中不暴露）。

[^1]: `proc.c` 中的令牌置空：函数 `Proc_CreateProcessInternalW` 检查 `Config_GetSettingsForImageName_bool(L"DropChildProcessToken", FALSE)`，条件满足时设置 `hToken = NULL`，绕过正常的受限令牌创建过程。

[^2]: `proc.c` 中的自动应用：条件 `Dll_ImageType == DLL_IMAGE_ACROBAT_READER || Dll_ImageType == DLL_IMAGE_PLUGIN_CONTAINER` 会自动对 Adobe Reader 和插件容器应用令牌丢弃，无论是否有显式配置。

[^3]: 绿盒兼容性机制：此设置解决了 Sandboxie 安全模型与应用程序兼容性之间的根本矛盾，允许选择性地绕过令牌限制，同时保持文件系统和注册表虚拟化。

[^4]: `proc.c` 中的配置查询：系统使用 `Config_GetSettingsForImageName_bool(L"DropChildProcessToken", FALSE)` 检索各应用程序设置，`FALSE` 默认值确保该功能仅在显式启用时生效。

[^5]: `proc.c` 中的令牌绕过实现：在 `CreateProcessInternalW` 函数中设置 `hToken = NULL` 有效禁用整个受限令牌创建管道，允许子进程继承父进程的完整安全上下文。
