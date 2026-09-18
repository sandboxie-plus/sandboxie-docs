# 特殊图像分类

_SpecialImage_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v0.5.3a / 5.45.2 起可用。此设置允许你把特定可执行文件分类为属于预定义的应用程序类别。Sandboxie 使用此分类应用针对每种应用程序类型定制的专门处理、优化和安全措施。该设置把应用程序可执行文件映射到内部映像类型，在整个沙盒化过程中触发类别特定的行为。

## 用法

```ini
[DefaultBox]

SpecialImage=chrome,chrome.exe
SpecialImage=firefox,firefox.exe
SpecialImage=mail,outlook.exe
```

## 语法

```ini
SpecialImage=<类别>,<可执行文件>
```

其中：

- `<类别>` 是预定义应用程序类型之一
- `<可执行文件>` 是应用程序可执行文件的名称（不区分大小写）

## 技术细节

配置了 `SpecialImage` 时，Sandboxie 在 DLL 初始化期间执行应用程序分类：

1. **映像类型检测**：进程启动期间，系统查询所有 `SpecialImage` 配置，并把当前可执行文件与定义的映射匹配[^1]。

2. **内部分类**：匹配的应用程序被分配内部映像类型（如 `DLL_IMAGE_GOOGLE_CHROME` 或 `DLL_IMAGE_MOZILLA_FIREFOX`），这些类型决定专门的行为[^2]。

3. **行为定制**：分配的映像类型影响各个方面，包括图形界面处理、进程限制、文件访问模式和安全令牌管理[^3]。

## 支持的类别

- **chrome**：基于 Chromium 的浏览器和 Electron 应用程序
- **firefox**：Mozilla Firefox 及相关浏览器  
- **thunderbird**：Mozilla Thunderbird 邮件客户端
- **browser**：不基于 Chrome 或 Firefox 的其他网页浏览器
- **mail**：Thunderbird 以外的邮件客户端
- **plugin**：浏览器插件容器和辅助进程

## 默认配置

Sandboxie 在 `Template_SpecialImages` 模板中包含大量默认映射：

```ini
# Chromium 系浏览器
SpecialImage=chrome,chrome.exe
SpecialImage=chrome,msedge.exe  
SpecialImage=chrome,brave.exe
SpecialImage=chrome,vivaldi.exe
SpecialImage=chrome,opera.exe

# Firefox 系列
SpecialImage=firefox,firefox.exe
SpecialImage=firefox,waterfox.exe
SpecialImage=firefox,librewolf.exe

# 邮件客户端
SpecialImage=mail,winmail.exe
SpecialImage=mail,foxmail.exe
SpecialImage=mail,mailbird.exe

# Electron 应用程序
SpecialImage=chrome,slack.exe
SpecialImage=chrome,spotify.exe
SpecialImage=chrome,steam.exe
```

## 类别特定行为

- **Chrome 应用程序**：接收专门的沙盒处理、通过 [自定义 Chromium 启动参数](CustomChromiumFlags.md) 注入自定义命令行标志、对子进程的受限令牌管理，以及优化的图形界面窗口站处理[^4]。

- **Firefox 应用程序**：获得定制的文件访问权限、特定 Windows 版本上的专门 D3D11 处理、沙盒进程令牌修改，以及定制的图形界面枚举行为[^5]。

- **邮件客户端**：接收适当的文件系统访问权限和针对邮件数据库操作的专门处理。

- **插件容器**：其进程令牌被丢弃以防权限提升，并接收专门的受限令牌处理[^6]。

**安全影响**

- **权限管理**：被分类为插件容器或某些浏览器类型的应用程序，其安全令牌会被自动限制或完全丢弃
- **子进程处理**：浏览器应用程序对其沙盒子进程接收专门处理，防止令牌继承问题
- **文件系统访问**：每个类别接收与其功能相称的定制文件系统访问权限
- **图形界面隔离**：浏览器和邮件应用程序通过专门的窗口站处理获得增强的图形界面隔离

## 实现说明

映像类型分类系统：

- 在 DLL 初始化期间使用 `SbieApi_QueryConfAsIs` 以索引访问查询配置，以处理多个映射[^7]
- 在当前可执行文件名称与配置的映射之间执行不区分大小写的字符串匹配
- 如果没有显式映射，则回退到对知名应用程序的自动检测
- 全局存储确定的映像类型，供整个沙盒化过程使用
- 影响众多子系统，包括进程创建、图形界面处理、文件访问和安全令牌管理

## 用法示例

- **Electron 应用程序支持**：
  ```
  SpecialImage=chrome,discord.exe
  SpecialImage=chrome,vscode.exe
  ```

- **替代浏览器分类**：
  ```
  SpecialImage=chrome,thorium.exe
  SpecialImage=firefox,librewolf.exe
  ```

- **自定义邮件客户端支持**：
  ```
  SpecialImage=mail,myclient.exe
  ```

## 相关设置

- [自定义 Chromium 启动参数](CustomChromiumFlags.md) - 自动适用于分类为 `chrome` 的应用程序
- [丢弃子进程令牌](DropChildProcessToken.md) - 影响插件容器和某些浏览器类型的行为

相关 Sandboxie Plus 设置：不在界面中直接暴露（自动使用模板定义的默认值）

[^1]: `dllmain.c` 中的映像类型检测：函数 `Dll_GetImageType` 使用索引查询遍历所有 `SpecialImage` 配置，解析以逗号分隔的类别和可执行文件对，以找到与当前进程可执行文件名称的匹配。

[^2]: `dllmain.c` 中的内部分类映射：字符串比较把类别名称映射到内部常量："chrome" 映射到 `DLL_IMAGE_GOOGLE_CHROME`，"firefox" 到 `DLL_IMAGE_MOZILLA_FIREFOX`，"thunderbird" 到 `DLL_IMAGE_MOZILLA_THUNDERBIRD`，"browser" 到 `DLL_IMAGE_OTHER_WEB_BROWSER`，"mail" 到 `DLL_IMAGE_OTHER_MAIL_CLIENT`，"plugin" 到 `DLL_IMAGE_PLUGIN_CONTAINER`。

[^3]: 整个代码库中的行为定制：分配的映像类型影响多个子系统，包括 `guienum.c` 中的图形界面窗口枚举、`proc.c` 中的进程创建和令牌处理、`file.c` 中的文件访问权限，以及 `kernel.c` 中的专门浏览器处理。

[^4]: `kernel.c` 中的 Chrome 特定处理：分类为 `DLL_IMAGE_GOOGLE_CHROME` 的应用程序通过 `CustomChromiumFlags` 机制接收自定义命令行标志的自动注入，并特殊处理以避免在包含 "--type=" 参数的子进程中重复标志。

[^5]: `guienum.c` 和 `proc.c` 中的 Firefox 特定优化：Firefox 应用程序在 Windows 10+ 上接收专门的 D3D11 图形处理、对 contentproc 子进程的自定义沙盒进程令牌管理，以及为更好兼容性定制的图形界面窗口站行为。

[^6]: `proc.c` 中的插件容器限制：分类为 `DLL_IMAGE_PLUGIN_CONTAINER` 的应用程序在进程创建期间自动完全丢弃其安全令牌以防权限提升，Adobe Reader 和其他沙盒化插件系统也是如此。

[^7]: `dllmain.c` 中的配置查询机制：系统使用递增的索引值调用 `SbieApi_QueryConfAsIs(NULL, L"SpecialImage", index, buf, 90 * sizeof(WCHAR))` 检索所有 SpecialImage 条目，解析每个以逗号分隔的值对，直到不再有条目。
