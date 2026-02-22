# Drop Child Process Token

_DropChildProcessToken_ 是一个沙箱设置，自 v1.15.6 / 5.70.6 起在 [沙盘配置](SandboxieIni.md) 中可用。此设置强制指定应用程序的子进程在运行时不使用受修改的安全令牌，从而绕过沙盘通常的受限令牌机制。该功能主要作为调试工具，用于排查“绿框”（应用程序隔离）兼容性问题，即应用程序因令牌限制而无法正常启动或运行。

## 使用方法

```ini
[DefaultBox]

DropChildProcessToken=chrome.exe,y
DropChildProcessToken=firefox.exe,y
DropChildProcessToken=acroread.exe,y
```

## 语法

```ini
DropChildProcessToken=<executable>,y
```

说明：

- `<executable>` 指应用程序的可执行文件名称（不区分大小写）
- 值必须为 `y`，表示启用该设置

## 技术细节

启用 `DropChildProcessToken` 后，沙盘会在子进程初始化阶段修改进程创建行为：

1. **令牌置空**：在 `CreateProcessInternalW` 中，系统检查目标应用是否匹配已配置的 `DropChildProcessToken` 项目，并将进程令牌设置为 `NULL`[^1]

2. **自动应用**：该设置会自动应用于特定应用类型——Adobe Acrobat Reader 以及插件容器默认会这样处理，通过硬编码的镜像类型检测实现[^2]

3. **绿框兼容性**：此机制帮助那些无法与沙盘受限安全令牌兼容的应用程序，在隔离模式下正常运行，即优先保证兼容性，而不是严格隔离[^3]

## 默认行为

沙盘会自动对某些应用类型应用令牌置空，无需显式配置：

- **Adobe Acrobat Reader**：所有版本的子进程会自动置空令牌，防止权限提升
- **插件容器**：通过 [SpecialImage](SpecialImage.md) 检测为 `DLL_IMAGE_PLUGIN_CONTAINER` 类型的应用会自动处理
- **Flash Player 沙箱**：历史版本支持 Adobe Flash Player 沙箱架构（在当前版本中被注释掉）

**使用场景**

- **绿框调试**：用于排查应用程序隔离沙箱内因令牌限制无法启动的应用
- **旧版应用兼容**：让老应用程序能够在现代安全令牌限制下正常运行
- **插件兼容性**：确保浏览器插件及辅助进程不受令牌相关限制影响
- **开发测试**：测试应用在无沙盘令牌隔离情况下的行为

**安全影响**

- **安全性降低**：子进程将以与父进程相同的令牌运行，隔离效果下降
- **权限管理**：沙盘的权限限制失效，进程将继承父进程的全部权限
- **兼容性权衡**：提升应用兼容性，但牺牲部分安全隔离
- **调试用途**：主要用于故障排查，而非生产环境使用

**绿框集成**

此设置非常适用于绿框（应用程序隔离）配置：

- **隔离模式**：绿框使用 `NoSecurityIsolation=y` 禁用令牌安全隔离，同时保持文件和注册表虚拟化
- **令牌冲突**：部分应用即使在隔离模式下仍因令牌问题出错，需彻底置空令牌
- **兼容性优先**：绿框以兼容性为主，令此设置成为问题应用的解决方案

## 实现说明

令牌置空机制：

- 在 DLL 注入层的 `Proc_CreateProcessInternalW` 函数中执行
- 通过 `Config_GetSettingsForImageName_bool` 查询每应用设置，默认值为 `FALSE`[^4]
- 与镜像类型识别系统集成，自动处理已知问题应用
- 设置 `hToken = NULL`，跳过标准令牌创建与限制流程[^5]
- 影响原本会应用受限令牌的 `CreateProcessInternalW` 调用链

## 相关兼容性设置

- **OriginalToken**：启用后跳过大多数基于令牌的修改，包括 `DropChildProcessToken`
- **DeprecatedTokenHacks**：重新启用已在隔离模式下停用的旧令牌兼容逻辑
- **NoSecurityIsolation**：应用程序隔离模式中关闭令牌安全隔离的核心设置
- **FakeAppContainerToken**：控制特定应用的 AppContainer 令牌模拟

## 实际举例

- **浏览器子进程问题**:
  ```ini
  DropChildProcessToken=chrome.exe,y
  DropChildProcessToken=msedge.exe,y
  ```

- **插件容器兼容问题**:
  ```ini
  DropChildProcessToken=plugin-container.exe,y
  DropChildProcessToken=flashplayer.exe,y
  ```

- **自定义应用调试**:
  ```ini
  DropChildProcessToken=myapp.exe,y
  ```

## 绿框故障排查

当应用在绿框模式下失败时：

1. 针对有问题的可执行文件启用 `DropChildProcessToken`
2. 测试应用能否正常启动和运行
3. 若成功，则说明问题与令牌限制有关，可保持该设置开启
4. 若失败，需进一步排查其他兼容性设置或文件/注册表访问问题

## 相关设置

- [SpecialImage](SpecialImage.md) - 自动对插件容器及 Adobe Reader 应用令牌置空
- [NoSecurityIsolation](NoSecurityIsolation.md) - 应用程序隔离模式的核心绿框设置

沙盘 Plus 相关设置：在高级调试选项中可用（标准界面未展示）

[^1]: `proc.c` 中的令牌置空：函数 `Proc_CreateProcessInternalW` 检查 `Config_GetSettingsForImageName_bool(L"DropChildProcessToken", FALSE)` 若条件成立则设置 `hToken = NULL`，跳过标准受限令牌创建流程
[^2]: `proc.c` 的自动应用逻辑：条件 `Dll_ImageType == DLL_IMAGE_ACROBAT_READER || Dll_ImageType == DLL_IMAGE_PLUGIN_CONTAINER` 会自动对 Adobe Reader 和插件容器应用令牌置空，无需显式配置
[^3]: 绿框兼容机制：该设置回应沙盘安全模型与应用兼容之间的基本矛盾，允许有选择地绕过令牌限制，同时保持文件系统和注册表虚拟化
[^4]: `proc.c` 的配置查询：系统使用 `Config_GetSettingsForImageName_bool(L"DropChildProcessToken", FALSE)` 检索每应用设置，默认 `FALSE` 保证仅按需启用
[^5]: `proc.c` 的令牌置空实现：在 `CreateProcessInternalW` 函数内设置 `hToken = NULL`，彻底关闭受限令牌创建流程，使子进程继承父进程的完整安全上下文