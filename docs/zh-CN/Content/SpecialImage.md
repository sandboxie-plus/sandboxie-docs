# 特殊图像分类

_SpecialImage_ 是一个沙箱设置项，位于 [沙盘配置](SandboxieIni.md)，自 v0.5.3a / 5.45.2 起提供。该设置允许你将特定可执行文件归类为预定义的应用程序类别。沙盘利用这些分类，为每种应用类型应用专门的处理、优化和安全策略。该设置通过将应用程序可执行文件与内部图像类型进行映射，在整个沙箱隔离过程中触发特定类别的行为。

## 使用方法

```ini
[DefaultBox]

SpecialImage=chrome,chrome.exe
SpecialImage=firefox,firefox.exe
SpecialImage=mail,outlook.exe
```

## 语法说明

```ini
SpecialImage=<category>,<executable>
```

其中：

- `<category>` 是预定义的应用程序类型之一
- `<executable>` 是应用程序的可执行文件名称（不区分大小写）

## 技术细节

在配置了 `SpecialImage` 后，沙盘会在 DLL 初始化期间执行应用程序分类：

1. **图像类型检测**：进程启动时，系统会查询所有 `SpecialImage` 配置，并将当前可执行文件与已定义的映射进行比对[^1]

2. **内部分类**：匹配到的应用程序会分配内部图像类型（如 `DLL_IMAGE_GOOGLE_CHROME` 或 `DLL_IMAGE_MOZILLA_FIREFOX`），以决定专用的行为方式[^2]

3. **行为定制**：分配的图像类型将影响 GUI 处理、进程限制、文件访问模式以及安全令牌管理等多方面[^3]

## 支持的类别

- **chrome**：基于 Chromium 的浏览器与 Electron 应用程序
- **firefox**：Mozilla Firefox 及相关浏览器
- **thunderbird**：Mozilla Thunderbird 邮件客户端
- **browser**：除 Chrome 或 Firefox 外的其它网页浏览器  
- **mail**：除 Thunderbird 外的邮件客户端
- **plugin**：浏览器插件容器与辅助进程

## 默认配置

沙盘在 `Template_SpecialImages` 模板中包含广泛的默认映射：

```ini
# 基于 Chromium 的浏览器
SpecialImage=chrome,chrome.exe
SpecialImage=chrome,msedge.exe  
SpecialImage=chrome,brave.exe
SpecialImage=chrome,vivaldi.exe
SpecialImage=chrome,opera.exe

# Firefox 系浏览器
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

## 各类别专用行为

- **Chrome 应用程序**：获得专门的沙箱处理，通过 [CustomChromiumFlags](CustomChromiumFlags.md) 自动注入自定义命令行参数，对子进程的安全令牌进行限制，并优化 GUI 窗口站点处理[^4]
- **Firefox 应用程序**：获得定制的文件访问权限、在特定 Windows 版本上专门的 D3D11 处理、沙箱进程令牌的调整，以及定制的 GUI 枚举行为[^5]
- **邮件客户端**：具备适当的文件系统访问权限，并专门处理邮件数据库操作
- **插件容器**：进程令牌会被丢弃，防止权限提升，并进行专用的令牌限制处理[^6]

**安全影响**

- **权限管理**：如插件容器或某些浏览器类型的应用程序，会自动限制或丢弃其安全令牌
- **子进程处理**：浏览器应用程序对其沙箱内子进程做专门处理，防止令牌继承相关问题
- **文件系统访问**：每个类别依据其功能获得定制的文件系统访问权限
- **GUI 隔离**：浏览器与邮件类应用程序，通过专用窗口站点处理实现更好的 GUI 隔离

## 实现说明

图像类型分类系统：

- 在 DLL 初始化期间通过 `SbieApi_QueryConfAsIs` 查询配置，支持索引访问以处理多个映射[^7]
- 对当前可执行文件名称与配置进行不区分大小写的字符串比对
- 若无明确映射，则对知名应用程序自动检测
- 全球性存储已确定的图像类型，供沙箱全过程使用
- 影响诸多子系统，包括进程启动、GUI 处理、文件访问以及安全令牌管理等

## 用法示例

- **支持 Electron 应用程序**：
  ```
  SpecialImage=chrome,discord.exe
  SpecialImage=chrome,vscode.exe
  ```

- **浏览器分类补充**：
  ```
  SpecialImage=chrome,thorium.exe
  SpecialImage=firefox,librewolf.exe
  ```

- **自定义邮件客户端支持**：
  ```
  SpecialImage=mail,myclient.exe
  ```

## 相关设置

- [CustomChromiumFlags](CustomChromiumFlags.md) - 自动应用于被归类为 `chrome` 的应用程序
- [DropChildProcessToken](DropChildProcessToken.md) - 会影响插件容器与特定浏览器类型的行为

相关沙盘 Plus 设置：未直接在 UI 暴露（自动采用模板定义的默认值）

[^1]: `dllmain.c` 中的图像类型检测：函数 `Dll_GetImageType` 通过索引方式遍历所有 `SpecialImage` 配置，解析逗号分隔的类别与可执行文件名，逐一比对当前进程文件名称
[^2]: `dllmain.c` 中的内部分类映射：字符串比较将类别名称映射为内部常量，如 "chrome" 映射为 `DLL_IMAGE_GOOGLE_CHROME`，"firefox" 映射为 `DLL_IMAGE_MOZILLA_FIREFOX`，"thunderbird" 为 `DLL_IMAGE_MOZILLA_THUNDERBIRD`，"browser" 为 `DLL_IMAGE_OTHER_WEB_BROWSER`，"mail" 为 `DLL_IMAGE_OTHER_MAIL_CLIENT`，"plugin" 为 `DLL_IMAGE_PLUGIN_CONTAINER`
[^3]: 行为定制遍布代码库：分配的图像类型影响多个子系统，包括 `guienum.c` 的 GUI 窗口枚举、`proc.c` 的进程启动与令牌处理、`file.c` 的文件访问权限及 `kernel.c` 的专用浏览器处理
[^4]: `kernel.c` 中的 chrome 特定处理：被分类为 `DLL_IMAGE_GOOGLE_CHROME` 的应用程序，通过 `CustomChromiumFlags` 机制自动注入定制命令行参数，并针对包含 "--type=" 参数的子进程避免重复注入
[^5]: Firefox 专用优化在 `guienum.c` 与 `proc.c`：Firefox 应用在 Windows 10+ 获得定制 D3D11 图形处理，对 contentproc 子进程执行专用沙箱令牌管理，并获得针对性 GUI 窗口站点兼容性优化
[^6]: 插件容器限制在 `proc.c`：被分类为 `DLL_IMAGE_PLUGIN_CONTAINER` 的应用程序，在进程创建时会自动丢弃安全令牌，防止权限提升，Adobe Reader 与其它沙箱插件系统同样适用
[^7]: `dllmain.c` 中的配置查询机制：系统通过 `SbieApi_QueryConfAsIs(NULL, L"SpecialImage", index, buf, 90 * sizeof(WCHAR))` 不断递增索引值检索所有 SpecialImage 配置，并解析每个逗号分隔的值，直到不再有条目