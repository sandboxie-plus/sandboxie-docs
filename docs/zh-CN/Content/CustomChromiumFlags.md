# 自定义 Chromium 启动参数

_CustomChromiumFlags_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.14.2 / 5.69.2 起可用。此设置允许你在基于 Chromium 的浏览器于沙盒内启动时，向其传递额外的命令行标志。Sandboxie 会自动把这些标志注入浏览器的启动命令行，从而在沙盒化环境中对浏览器行为进行精细控制，以实现增强的兼容性和功能。

## 用法

```ini
[DefaultBox]

CustomChromiumFlags=--disable-features=PrintCompositorLPAC --disable-gpu
```

## 语法

```ini
CustomChromiumFlags=--disable-features=PrintCompositorLPAC [<标志 1> <标志 2> ...]
```

## 技术细节

配置了 `CustomChromiumFlags` 时，Sandboxie 会在进程初始化期间修改被识别为基于 Chromium 浏览器的应用程序的命令行：

1. **浏览器检测**：此设置只适用于通过 [`特殊图像分类`](SpecialImage.md) 配置或自动检测分类为 Chrome 的应用程序[^1]。

2. **命令行注入**：在内核初始化期间，Sandboxie 拦截进程参数，通过在可执行路径与现有参数之间插入自定义标志来重建命令行[^7][^2]。

3. **子进程过滤**：标志只添加到主浏览器进程，不添加到包含 `--type=` 参数的子进程，防止重复和潜在冲突[^3]。

## 默认配置

Sandboxie 包含一个默认值以确保浏览器兼容性：

```ini
CustomChromiumFlags=--disable-features=PrintCompositorLPAC
```

此默认标志禁用 Print Compositor LPAC（低权限应用容器）功能，该功能在沙盒化环境中可能导致兼容性问题[^4]。

## 用法示例

- **基本禁用 GPU 加速**：
  ```ini
  CustomChromiumFlags=--disable-features=PrintCompositorLPAC --disable-gpu
  ```

- **多个性能标志**：
  ```ini
  CustomChromiumFlags=--disable-features=PrintCompositorLPAC --no-sandbox --disable-web-security
  ```

- **调试选项**：
  ```ini
  CustomChromiumFlags=--disable-features=PrintCompositorLPAC --enable-logging --log-level=0
  ```

## 安全影响

- **浏览器兼容性**：默认的 `PrintCompositorLPAC` 标志可防止与打印相关的崩溃，确保浏览器在沙盒内稳定运行
- **标志验证**：用户应仔细验证自定义标志，因为某些标志可能损害沙盒安全或浏览器稳定性
- **自动应用**：此设置自动适用于所有定义为 Chrome 浏览器的应用程序，无论手动配置还是自动检测

## 实现说明

此设置在对基于 Chromium 浏览器的 DLL 初始化期间处理。系统：

- 使用 `SbieApi_QueryConfAsIs` 以键 `CustomChromiumFlags` 查询配置[^5]
- 为展开的命令行分配额外内存以容纳自定义标志
- 通过复制可执行路径、插入自定义标志并追加剩余参数来重建命令行[^6]
- 钩住 `GetCommandLineW` 和 `GetCommandLineA` 函数，向应用程序返回修改后的命令行

## 浏览器支持

此设置适用于所有基于 Chromium 的浏览器，包括：
- Google Chrome
- Microsoft Edge（Chromium）
- Brave Browser
- Opera
- Vivaldi
- 任何其他基于 Chromium 引擎构建的浏览器

## 相关设置

- [特殊图像分类](SpecialImage.md) - 用于把应用程序分类为 Chromium 浏览器

相关 Sandboxie Plus 设置：不在界面中直接暴露（自动使用默认值）

[^1]: `dllmain.c` 中的浏览器检测：应用程序通过 `SpecialImage` 配置系统分类为 `DLL_IMAGE_GOOGLE_CHROME`，该配置把浏览器可执行文件映射到 Chrome 映像类型以进行专门处理。

[^2]: `kernel.c` 中的命令行重建：系统调用 `SbieDll_FindArgumentEnd` 定位可执行路径与参数之间的边界，然后分配扩展内存并用注入的标志重建命令行。

[^3]: `kernel.c` 中的子进程过滤：条件 `!wcsstr(ProcessParms->CommandLine.Buffer, L" --type=")` 确保只有主浏览器进程接收自定义标志，排除渲染器和实用工具进程。

[^4]: `Templates.ini` 中的默认配置：默认的 `--disable-features=PrintCompositorLPAC` 标志可防止可能导致沙盒化环境中浏览器不稳定的低权限应用容器打印问题。

[^5]: `kernel.c` 中的配置查询：`SbieApi_QueryConfAsIs(NULL, L"CustomChromiumFlags", 0, CustomChromiumFlags, ARRAYSIZE(CustomChromiumFlags))` 在内核初始化期间检索设置值。

[^6]: `kernel.c` 中的命令行修改：系统复制原始可执行路径，以正确的间距追加自定义标志，并连接剩余参数以创建修改后的命令行。

[^7]: Chromium 命令行开关列表 - `https://peter.sh/experiments/chromium-command-line-switches/`
