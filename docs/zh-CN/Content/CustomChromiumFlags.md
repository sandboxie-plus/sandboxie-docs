# 自定义 Chromium 启动参数

_CustomChromiumFlags_ 是自 v1.14.2 / 5.69.2 起在 [沙盘配置](SandboxieIni.md) 提供的一个沙箱设置。该设置允许在 Chromium 内核的浏览器被沙箱启动时，向其传递额外的命令行参数。Sandboxie 会自动将这些参数注入到浏览器的启动命令行，实现对浏览器行为的精细控制，以增强在沙箱环境下的兼容性和功能性。

## 用法

```ini
[DefaultBox]

CustomChromiumFlags=--disable-features=PrintCompositorLPAC --disable-gpu
```

## 语法

```ini
CustomChromiumFlags=--disable-features=PrintCompositorLPAC [<flag 1> <flag 2> ...]
```

## 技术细节

当配置了 `CustomChromiumFlags` 后，Sandboxie 会在进程初始化期间，针对检测为 Chromium 内核浏览器的应用程序，对其命令行进行修改：

1. **浏览器识别**：此设置仅适用于通过 [`SpecialImage`](SpecialImage.md) 配置或自动检测为 Chrome 分类的应用程序[^1]

2. **命令行注入**：内核初始化期间，Sandboxie 会拦截进程参数，通过在可执行路径和现有参数之间插入自定义参数，对启动命令行进行重构[^7][^2]

3. **子进程过滤**：参数仅注入到主浏览器进程中，不会对包含 `--type=` 参数的子进程生效，从而避免重复注入及潜在冲突[^3]

## 默认配置

Sandboxie 内置默认值以确保浏览器兼容性：

```ini
CustomChromiumFlags=--disable-features=PrintCompositorLPAC
```

默认参数用于禁用 Print Compositor LPAC（低权限应用容器）功能，以防在沙箱环境中产生兼容性问题[^4]

## 使用示例

- **基础 GPU 加速禁用**：
  ```ini
  CustomChromiumFlags=--disable-features=PrintCompositorLPAC --disable-gpu
  ```

- **多性能参数设置**：
  ```ini
  CustomChromiumFlags=--disable-features=PrintCompositorLPAC --no-sandbox --disable-web-security
  ```

- **调试选项**：
  ```ini
  CustomChromiumFlags=--disable-features=PrintCompositorLPAC --enable-logging --log-level=0
  ```

## 安全性注意事项

- **浏览器兼容性**：默认的 `PrintCompositorLPAC` 参数可避免与打印相关的崩溃，确保浏览器在沙箱中的稳定运行
- **参数校验**：用户应谨慎验证自定义参数，部分参数可能会影响沙箱安全性或浏览器稳定性
- **自动应用**：此设置会自动应用于所有被识别为 Chrome 浏览器的应用程序，无论是手动配置还是自动检测

## 实现说明

在 Sandboxie 检测到 Chromium 内核浏览器时，该设置会在 DLL 初始化阶段被处理。系统会：

- 使用 `SbieApi_QueryConfAsIs` 以 `CustomChromiumFlags` 键查询配置[^5]
- 分配额外内存以容纳注入自定义参数的扩展命令行
- 拷贝原始可执行路径、插入自定义参数，并附加剩余参数，重构命令行[^6]
- 钩取 `GetCommandLineW` 与 `GetCommandLineA` 函数，将修改后的命令行返回给应用

## 浏览器支持

该设置兼容所有基于 Chromium 内核的浏览器，包括：
- Google Chrome
- Microsoft Edge (Chromium)
- Brave 浏览器
- Opera
- Vivaldi
- 任何其他使用 Chromium 引擎构建的浏览器

## 相关设置

- [SpecialImage](SpecialImage.md) - 用于将应用程序归类为 Chromium 浏览器

相关 Sandboxie Plus 设置：界面未直接开放（自动使用默认值）

[^1]: 浏览器识别于 `dllmain.c`：应用通过 `SpecialImage` 配置系统归类为 `DLL_IMAGE_GOOGLE_CHROME`，以便进行专用处理

[^2]: 命令行重构于 `kernel.c`：系统调用 `SbieDll_FindArgumentEnd` 以识别可执行路径与参数的边界，分配扩展内存并插入自定义参数

[^3]: 子进程过滤于 `kernel.c`：通过 `!wcsstr(ProcessParms->CommandLine.Buffer, L" --type=")` 判断，仅主浏览器进程注入自定义参数，排除渲染和工具进程

[^4]: 默认配置于 `Templates.ini`：默认参数 `--disable-features=PrintCompositorLPAC` 避免低权限应用容器打印问题，防止浏览器在沙箱中出现不稳定

[^5]: 配置查询于 `kernel.c`：`SbieApi_QueryConfAsIs(NULL, L"CustomChromiumFlags", 0, CustomChromiumFlags, ARRAYSIZE(CustomChromiumFlags))` 在内核初始化时获取设置值

[^6]: 命令行修改于 `kernel.c`：系统拷贝原始可执行路径，适当加空格插入自定义参数，并拼接剩余参数，生成最终命令行

[^7]: Chromium 命令行参数列表 - `https://peter.sh/experiments/chromium-command-line-switches/`