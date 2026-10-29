# 宿主注入 {#host-injection}

## 概述 {#overview}

宿主注入使 Sandboxie 能够将受信任的兼容性 DLL 加载到选定的宿主进程中，而不会把该进程变成普通的沙盒化进程。

普通的 Sandboxie 注入会把 SbieDll 加载到即将被沙盒化的进程中，然后执行文件、注册表、IPC、网络、GUI 及其他沙盒控制所需的初始化。对于由 `HostInjectProcess` 选中的进程，Sandboxie 会复用 SbieDll 的底层引导过程，但进入一条仅负责加载的宿主注入路径。目标进程保留其原有的进程身份和令牌，仍处于普通沙盒进程隔离之外，并加载所配置的 `HostInjectDll*` 条目。

相关的几种注入机制，其目标和用途各不相同：

| 机制 | 目标 | 运行时上下文 | 用途 |
| --- | --- | --- | --- |
| 普通 SbieDll 注入 | 正在被沙盒化的进程 | 普通 Sandboxie 初始化 | 安装 Sandboxie 运行时及其隔离钩子 |
| `InjectDll*` | 普通沙盒化进程 | 沙盒化进程的令牌和限制 | 加载额外配置的 DLL |
| `HostInjectProcess` 配合 `HostInjectDll*` | 选定的外部宿主进程 | 宿主进程原有的身份 | 加载受信任的兼容性 DLL，不执行普通沙盒初始化 |
| `SboxHostDll.dll` | Office 即点即用（Click-to-Run）宿主目标 | 宿主注入上下文 | 提供当前的 Office 令牌兼容性行为 |

共用加载器的一部分，并不意味着这些机制彼此等价。

## 宿主注入进程 {#host-injected-processes}

被宿主注入的进程仍然是外部宿主进程。这条路径不会将其加入常规的 Sandboxie 作业对象，不会将其呈现为普通沙盒化进程，也不会初始化沙盒化程序所使用的文件、注册表、IPC、网络、GUI 和线程处理。它的主令牌不会被替换为降权后的沙盒令牌（reduced sandbox token）。

Sandboxie 会把该进程关联到一份有效配置，以便选出相应的宿主注入 DLL 条目。这种内部关联并不是普通的沙盒身份。如果某个进程已被普通沙盒规则或强制规则选中，它会被当作沙盒化进程处理；只有当进程尚未被分配到普通沙盒执行路径时，宿主注入匹配才会生效。

## `HostInjectProcess` {#hostinjectprocess}

此设置接受一个可执行文件名模式，以及一个可选的 Windows 服务名：

```ini
HostInjectProcess=program.exe
HostInjectProcess=program.exe|ServiceName
```

可执行文件部分与映像的基本名称（而不是完整路径）进行不区分大小写的匹配。可以使用 Sandboxie 的常规通配符，也可以配置多个条目。

`|` 之后的可选值是用于服务生命周期和重启处理的服务名。它不是另一种进程选择方式，也不参与驱动程序对可执行文件的匹配。因此，只写服务名而不带可执行文件模式的配置不会起作用。

宿主注入设置可以通过常规配置和模板继承纳入某个沙盒的有效配置。如果多个已启用的沙盒都提供了匹配的规则，该进程只会关联到其中一份匹配的配置；Sandboxie 不会合并多个沙盒的宿主 DLL 列表。请避免在多个沙盒中出现相互竞争的匹配。`GlobalSettings` 可以通过常规的配置回退参与进来，但它本身不会成为该进程所属的沙盒。

## 宿主注入流程 {#host-injection-flow}

```text
宿主进程启动
        |
        v
评估普通沙盒规则和强制规则
        |
        v
HostInjectProcess 匹配可执行文件
        |
        v
Sandboxie 将该进程标记为待进行宿主注入
        |
        v
SbieSvc 执行 SbieDll 的底层引导
        |
        v
SbieDll 进入宿主注入加载器模式
        |
        v
加载匹配的 HostInjectDll* 条目
        |
        v
宿主兼容性 DLL 完成初始化
```

驱动程序评估进程启动时的配置，并协调宿主注入的决策。SbieSvc 执行进程注入请求。随后 SbieDll 运行的是精简的宿主加载器，而非完整的沙盒初始化，再由所加载的宿主 DLL 提供针对具体应用程序的兼容性行为。

## `HostInjectDll` 的架构变体 {#hostinjectdll-architecture-variants}

请使用与目标进程架构相匹配的设置：

| 目标进程架构 | 设置 |
| --- | --- |
| x86 | `HostInjectDll` |
| x64 | `HostInjectDll64` |
| 原生 ARM64 | `HostInjectDllARM64` |

决定使用哪个列表的是目标进程的架构以及与之对应的 SbieDll 架构；单凭操作系统架构并不能决定。这些条目可以重复配置，按配置顺序加载，且不会被统一去重。此对应关系不应被理解为对 ARM64EC 或 CHPE 的完全兼容保证。

加载某个已配置的 DLL 后，Sandboxie 会检查是否存在可选的 `InjectDllMain` 导出（或相应的修饰名形式）。如果存在，该回调可以访问注入机制所使用的 SbieDll 实例或上下文。对已配置的 DLL 来说，这个导出是可选的；`SboxHostDll.dll` 使用它来完成初始化。现有的公开回调说明请参阅 [SBIE DLL API](SBIEDLLAPI.md)。

## DLL 路径要求 {#dll-path-requirements}

当前的宿主注入条目以反斜杠开头，表示 DLL 路径相对于 Sandboxie 安装目录解析：

```ini
HostInjectDll=\SboxHostDll.dll
```

其他特定架构的设置也使用相同的形式。当前的宿主加载器会拒绝任意绝对路径、包含 `..` 的条目，以及不指向 `.dll` 文件的条目。不应将普通相对路径当作公开的 `HostInjectDll*` 语法使用。

## 与 `InjectDll` 的关系 {#relationship-to-injectdll}

[`InjectDll`](InjectDll.md) 和 [`InjectDll64`](InjectDll64.md) 会把额外的 DLL 加载到普通沙盒化进程中。这些 DLL 在进程的有效沙盒令牌和 Sandboxie 限制下运行，其可接受的路径形式也与宿主注入不同。

`HostInjectDll*` 则是把 DLL 加载到由 `HostInjectProcess` 选中的外部进程中。该进程保留其原有身份，不会进入普通沙盒路径。当前的宿主加载器只接受上文所述的、相对于 Sandboxie 安装目录的路径形式。

SandMan 没有专门用于编辑 `HostInjectProcess` 或 `HostInjectDll*` 的界面；它们通常由兼容性模板或手动 INI 配置提供。**沙盒选项 > 高级选项 > Dll && 扩展** 管理的是受支持的 `InjectDll*` 附加组件条目，而不是宿主注入设置。

## Microsoft Office 即点即用 {#microsoft-office-click-to-run}

当前随附的配置使用宿主注入来实现 Microsoft Office 即点即用（Click-to-Run）的兼容性：

```ini
HostInjectDll=\SboxHostDll.dll
HostInjectDll64=\SboxHostDll.dll
HostInjectDllARM64=\SboxHostDll.dll
HostInjectProcess=OfficeClicktoRun.exe|ClickToRunSvc
```

其中，`OfficeClicktoRun.exe` 用于选中进程，`ClickToRunSvc` 指明用于生命周期处理的 Windows 服务，而与目标架构对应的设置负责加载 `SboxHostDll.dll`。Office 兼容性模板还提供了即点即用与 App-V 通信所需的相关 IPC 规则。

兼容性模板是否适用，是通过检测 `ClickToRunSvc` 服务是否存在来单独判断的。模板检测或启用负责提供配置；运行时的匹配仍然使用 `OfficeClicktoRun.exe` 可执行文件模式。

在当前随附的配置中，Microsoft Office 即点即用是仓库里唯一一项内置的、在生产中实际使用 `HostInjectProcess` 和 `SboxHostDll.dll` 的用途。这些设置提供的基础设施可以支持其他受信任的兼容性组件，但 `SboxHostDll.dll` 本身并不是通用的宿主重定向或虚拟化子系统。

### `SboxHostDll.dll` {#sboxhostdlldll}

`SboxHostDll.dll` 会验证自己是否运行在预期的 Office 即点即用可执行文件上下文中，通过 `InjectDllMain` 完成初始化，并安装其 Office 兼容性钩子。它不提供 Sandboxie 的文件、注册表、环境、进程、COM、RPC 或 App-V 虚拟化。

### 令牌兼容性 {#token-compatibility}

当前的 DLL 挂钩了 `OpenProcessToken`，用于处理 Office 即点即用与沙盒化 Office 进程之间的一种身份兼容性情形。

当 Office 即点即用为某个有效的沙盒化进程请求令牌，而该进程的令牌使用的是 Sandboxie 的匿名登录（Anonymous Logon）身份或 Sandboxie 专用身份时，该 DLL 会查找具有相同登录 SID 的对应宿主侧进程。如果找到，就可以改为返回该宿主令牌。如果找不到合适的替代令牌，则保留原始 API 调用的结果。

## 服务与进程生命周期 {#service-and-process-lifecycle}

对于以 Windows 服务形式运行的目标，Sandboxie 内置了同步逻辑：当宿主注入开始生效、或该服务的进程选择发生变化时，可以重启所配置的服务。`|` 之后的服务名正是为这种 SCM 生命周期处理而存在的。

只有 Windows 服务会参与这种自动同步。已经在运行的普通宿主进程不会被追溯注入。如果只修改了 `HostInjectDll*` 列表，也可能需要手动重启，因为服务同步主要检测的是 SbieDll 是否存在。

修改 `HostInjectProcess` 或 `HostInjectDll*` 后，请重启受影响的目标进程。Sandboxie 可以同步已配置的 Windows 服务，但要确保修改后的宿主 DLL 列表生效，最可靠的方法是手动重启受影响的服务。通常不需要重启系统。

## 安全注意事项 {#security-considerations}

只应配置随 Sandboxie 提供、或由管理员有意安装的受信任 DLL。被宿主注入的 DLL 会在目标进程内部、以该进程原有的身份和权限执行；通过这条路径，目标进程不会被施加常规的降权后沙盒令牌。

宿主注入不会授予 `SYSTEM` 权限，不会自行提升目标进程的权限，也不会绕过 Windows 服务安全机制，更不构成沙盒逃逸。它是一种有意为之的兼容性机制，用于把受信任的代码加载到选定的外部进程中。受保护进程（Protected Process）和 PPL 的限制不会被绕过，因此 Sandboxie 通常无法打开或操作的目标，可能也无法被注入。

`ProtectHostImages` 是一项独立的映像保护功能。它可以阻止沙盒内的 DLL 或映像被映射进某些沙盒化进程，这类进程的可执行映像来自宿主；该功能并不控制 `HostInjectDll*`。`NotifyImageLoadDenied` 同样属于该映像保护机制。

## 失败时的行为 {#failure-behavior}

服务侧（SbieSvc）的进程注入失败时，可能会产生 Sandboxie 注入错误，例如 `SBIE2335`。无效的宿主 DLL 条目可能会被跳过，缺失的 DLL 或架构不匹配的 DLL 可能加载失败。并不存在适用于所有目标和所有注入阶段的统一恢复结果：目标进程可能继续运行，也可能失败，取决于错误发生的位置。

对于 Office 令牌钩子，如果找不到合适的宿主侧替代令牌，会保留原始的 `OpenProcessToken` 结果。

## Sandboxie Plus 与 Classic {#sandboxie-plus-and-classic}

驱动程序、SbieSvc、SbieDll 和 SboxHostDll 是共享的运行时组件。SandMan 目前的 Plus 界面可用于管理兼容性模板和受支持的 `InjectDll*` 附加组件条目，但没有专门的宿主注入编辑界面。Sandboxie Control（Classic）也可以通过共享的运行时使用兼容的模板和手动 INI 配置；两者的用户界面并不完全相同。

## 应用配置更改 {#applying-configuration-changes}

宿主注入的选择发生在目标进程启动时，所选的 DLL 也在这一启动过程中加载。修改设置后，请重启受影响的进程。对于服务类目标，在条件允许时请手动重启该服务，以确保进程选择和 DLL 列表的更改都能生效。仅仅修改配置，通常不需要重启 SandMan、SbieSvc、驱动程序或 Windows。

## 版本历史 {#version-history}

- 宿主注入、`HostInjectProcess`、`HostInjectDll*` 以及 Office 的 `SboxHostDll.dll` 实现，在最初公开的 5.40 版源代码中就已存在。它们具体是在更早的哪个闭源版本中引入的，目前尚无定论。
- Sandboxie Plus 0.7.2 / Classic 5.49.0 收紧了 `HostInjectDll` 的路径限制，不再接受任意的宿主绝对路径，宿主 DLL 必须位于 Sandboxie 安装目录下。
- Sandboxie Plus 1.2.0 / Classic 5.57.0 将 SboxHostDll 的令牌兼容性行为扩展到 Sandboxie 专用 SID。
- Sandboxie Plus 1.5.0 增加了 ARM64 的 `InjectDll` 和 `HostInjectDll` 支持。
- Sandboxie Plus 1.15.9 / Classic 5.70.9 进一步加强了对使用 `..` 的路径遍历的防护。
- Sandboxie Plus 1.15.10 / Classic 5.70.10 更改了注入 DLL 条目的验证方式。
- Sandboxie Plus 1.15.11 / Classic 5.70.11 修复了 SboxHostDll 注入 `OfficeClickToRun.exe` 的问题。
- Sandboxie Plus 1.16.9 / Classic 5.71.9 提升了 Office 即点即用和重复挂钩的可靠性。

## 相关页面 {#related-pages}

- [代码注入](CodeInjection.md)
- [注入 Dll](InjectDll.md)
- [注入 Dll64](InjectDll64.md)
- [SBIE DLL API](SBIEDLLAPI.md)
- [Sandboxie Ini](SandboxieIni.md)
