# 高级加载器与 SxS 兼容性

这些高级设置针对特定的进程创建、并行（Side-by-Side，SxS）激活上下文、早期 DLL 加载与 Windows 版本兼容问题。它们是故障排查控件，不是通用的安全改进手段，也不能用来复现另一套 Windows 安装。

| 设置 | 当前作用范围 |
| --- | --- |
| `PreferExternalManifest` | 依据**被创建的子进程可执行文件**选择 Sandboxie 的虚拟清单变通方案。 |
| `ExternalManifestHack` | 依据**创建子进程的沙盒父进程**选择同一变通方案。 |
| `DisableBoxedWinSxS` | 对匹配的进程改用另一条激活上下文路径，而不使用 Sandboxie 的沙盒内 SxS 服务。 |
| `DelayLoadDll` | 使指定 DLL 在进程早期初始化期间表现为不可用，并记录其路径。 |
| `OverrideOsBuild` | 改变沙盒进程内选定的版本查询 API 的返回结果。 |

## 进程创建期间的清单兼容性

`PreferExternalManifest` 默认禁用。尽管名字如此，它并不是简单地告诉 Windows 优先使用应用程序自带的 `.manifest` 文件。当针对某个子可执行文件启用时，Sandboxie 可以在进程创建期间拦截对该子进程清单或配置文件的打开，并替换为 Sandboxie 随附的文件。它还可以把相关的 SxS 注册表访问重定向到 Sandboxie 服务侧的兼容项。应用程序实际的清单文件不会被修改。

当 Sandboxie 的进程创建路径把子进程标记为 `asInvoker` 时，例如应用清单明确要求 `asInvoker`，替换掉的文件是一个小巧的 `asInvoker` 清单和一个最小配置文件。否则 Sandboxie 会替换成一个空文件，以便 Windows 仍能应用其 UAC 提升启发式判断。这些替换只属于进程创建兼容路径，不是对所有应用清单的通用替换。

例如：

```ini
[DefaultBox]
PreferExternalManifest=legacyapp.exe,y
```

可选的可执行文件选择器指向的是**被创建的子进程**。盒级的 `PreferExternalManifest=y` 会普遍启用该变通方案；更具体的 `legacyapp.exe,n` 可以为该子进程关闭它。常规的盒、全局与已启用模板配置查找依然适用。

`ExternalManifestHack` 是选择同一条兼容路径的另一条途径，同样默认禁用：

```ini
[DefaultBox]
ExternalManifestHack=parent.exe,y
```

这里的选择器指向**已经在运行的、创建子进程的沙盒父进程**，而不是子进程。若父进程匹配某条已启用的 `ExternalManifestHack` 规则，该变通方案会在面向子进程的 `PreferExternalManifest` 检查之前被选定。因此这两个带可执行文件限定的设置不可互换。面向父进程的选项是为 Windows 11 KB5014019 之后的一个 Edge 兼容案例添加的；旧的 Edge 模板条目目前已注释掉，不应视为生效的默认值。

当前的映像感知查找还接受通配符模式与已配置的进程组。仅对确实需要该变通方案的应用程序使用可执行文件限定的规则；更具体的匹配值可以优先于通用值。

## `DisableBoxedWinSxS`

Sandboxie 常规的 `CreateActCtxW` 处理可以要求其沙盒内 RpcSs SxS 服务生成激活上下文数据。`DisableBoxedWinSxS=y` 是该路线的一条兼容替代路径，**不是**关闭 WinSxS 程序集的开关。对于匹配的进程，SbieDll 改为调用系统的 `CreateActCtxW` 路径，并在需要时转换沙盒内的源文件路径。

```ini
[DefaultBox]
DisableBoxedWinSxS=explorer.exe,y
```

SbieDll 的选择是映像感知的，尽管设置元数据只描述了一个盒级布尔值。随附的 ARM64 兼容模板使用带可执行文件限定的值。在 SandboxieRpcSs 自身内部，以及对于带 AppContainer 令牌的进程，该替代路径也会被自动选用。

沙盒内 RpcSs 中还有第二个读取方。它在启动时读取 `DisableBoxedWinSxS` 的常规生效布尔值；盒级的 `y` 会阻止其 `RPCSS_SXS` 服务线程初始化。该查找并**不**执行与 SbieDll 相同的可执行文件名称匹配。因此，带进程限定的条目应当理解为：对匹配的进程选择替代路径，而不是可靠地为整个盒禁用沙盒内 SxS 服务。

## `DelayLoadDll`

`DelayLoadDll` 接受 DLL 的**基名**，精确匹配且不区分大小写；当前的驱动检查不实现路径或通配符匹配：

```ini
[DefaultBox]
DelayLoadDll=guard64.dll
```

在新启动的进程中，SbieDll 完成初始化之前，对匹配 DLL 的打开会被表现为文件不存在。驱动会把该 DLL 的完整路径记录到每进程队列中，并且存在一个用于取回队列路径的 API。但是，当前代码树中既没有找到调用该 API 的调用方，也没有找到其他能完成后续预期 DLL 加载的路径。不要把 `DelayLoadDll` 当作“该 DLL 随后一定会被加载”的保证。现有兼容模板中仍有 Comodo、ThreatFire、Logitech Process Monitor 等产品的条目；它们的存在并不能证明后续加载路径仍然有效。

## `OverrideOsBuild`

`OverrideOsBuild` 接受十进制的 Windows **内部版本号**，可选地由被启动的可执行文件加以限定：

```ini
[DefaultBox]
OverrideOsBuild=legacyapp.exe,7601
```

盒级取值写成 `OverrideOsBuild=7601`。当前解析器使用 `_wtoi()`；像 `10.0.19045.6216` 这样的完整版本串**不是**合法的内部版本号语法——它会被解析成开头的数字 `10`。当解析出的版本号非零时，SbieDll 会为该进程挂钩 `RtlGetVersion`、`GetVersionExW` 与 `GetVersionExA`。

Sandboxie 通过上述挂钩报告配置的版本号，并推导出对应的主/次版本号与服务包级别。例如版本号 `7601` 映射为 Windows 7 SP1（`6.1`），`9200` 映射为 Windows 8（`6.2`），`9600` 映射为 Windows 8.1（`6.3`），高于 `9600` 的映射为主/次版本 `10.0`。这不会改变实际的操作系统、可用 API、产品版本或内部修订号。它也不覆盖所有版本检测手段；`VerifyVersionInfoW` 不在该机制的挂钩范围内。

可执行文件选择器会与版本查询 API 被挂钩的那个沙盒进程匹配。常规的盒、全局与已启用模板查找适用，映像特定的匹配值优先于通用值。

## SandMan 中的配置

盒级的 `PreferExternalManifest` 复选框位于 **沙盒选项 > 其它选项 > 兼容性**，标签为 **强制使用自定义虚拟 Manifest 文件 (传统行为)**。默认未勾选。

带可执行文件限定的 `PreferExternalManifest` 条目，以及通用或带可执行文件限定的 `ExternalManifestHack` 条目，可通过 **沙盒选项 > 高级选项 > 杂项** 中的高级 **添加选项** 编辑器配置。`ExternalManifestHack` 没有专门的复选框。该编辑器可以单独显示从模板继承来的条目。

当前 SandMan 的特殊选项列表没有针对 `DisableBoxedWinSxS`、`DelayLoadDll` 或 `OverrideOsBuild` 的专门控件；请在 [Sandboxie Ini](SandboxieIni.md) 中或通过适用的兼容模板配置它们。模板存在并不意味着设置生效，除非该模板已启用。

## 应用更改

清单变通方案在子进程创建期间查询。配置重载后，正在运行的沙盒父进程可以对后续子进程使用更改过的 `PreferExternalManifest` 或 `ExternalManifestHack` 规则；已经创建的子进程不受影响。

`DisableBoxedWinSxS` 的替代路径决策在 SbieDll 初始化期间做出。更改后请重启受影响的沙盒进程。对于控制沙盒内 RpcSs SxS 线程的盒级更改，请重建沙盒进程树，使 RpcSs 以新值启动。

`DelayLoadDll` 只由驱动在 SbieDll 初始化之前对符合条件的 DLL 打开进行检查，因此更改主要影响新启动的进程。`OverrideOsBuild` 在进程初始化期间安装其挂钩；更改后请重启受影响的进程。这两个设置都不会追溯性地改变已加载的 DLL 或已初始化的进程。

## 版本历史

- Sandboxie Plus 0.4.5 / Classic 5.44.1 默认禁用了较早的应用清单变通方案；`PreferExternalManifest=y` 保留了该传统行为。
- Plus 0.7.2 / Classic 5.49.0 添加了 `OverrideOsBuild=7601`；Plus 0.7.5 / Classic 5.49.8 添加了逐进程的 `PreferExternalManifest` 配置。
- Plus 1.0.3 / Classic 5.55.3 修复了一个影响 `OverrideOsBuild` 的 `GetVersionExW` 问题。
- Plus 1.1.1 / Classic 5.56.1 改进了 `PreferExternalManifest`，并修复了 KB5014019 之后的 Edge 问题。当前元数据把 `ExternalManifestHack` 记为 1.1.2 添加。

当前元数据无法确定 `DisableBoxedWinSxS` 与 `DelayLoadDll` 的引入版本。特别是 `PreferExternalManifest` 与 `DisableBoxedWinSxS` 的元数据描述，比它们当前的可执行行为更宽泛。

## 相关页面

- [Sandboxie Ini](SandboxieIni.md)
- [RPC 兼容性](RpcCompatibility.md)
- [代码注入](CodeInjection.md)
