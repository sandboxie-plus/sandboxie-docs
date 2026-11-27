# 沙盒根与卷布局 {#sandbox-roots-and-volume-layout}

Sandboxie 为沙盒的文件容器、已挂载的注册表配置单元和命名对象命名空间分别使用独立的根。这些设置选择位置与布局；它们本身并不授予对宿主文件、注册表项或 IPC 对象的访问权。下面的路径是默认值，而不是对每个已配置沙盒的不变描述。

<div id="the-three-sandbox-roots"></div>

## 三个沙盒根

| 根 | 默认值 | 用途 |
| --- | --- | --- |
| [`FileRootPath`](FileRootPath.md) | `\??\%SystemDrive%\Sandbox\%USER%\%SANDBOX%` | 存放重定向文件和 `RegHive` 文件的文件容器。 |
| [`KeyRootPath`](KeyRootPath.md) | `\REGISTRY\USER\Sandbox_%USER%_%SANDBOX%` | 该配置单元挂载到的注册表位置。 |
| [`IpcRootPath`](IpcRootPath.md) | `\Sandbox\%USER%\%SANDBOX%\Session_%SESSION%` | 沙盒化命名对象的 NT 命名空间根；其默认值包含会话。 |

根字符串会针对沙盒展开并规范化，包括把合适的 DOS 文件路径转换为 NT 路径，以及移除重复或结尾的反斜杠。可用的替换包括 `%SANDBOX%`、`%USER%`（或 `%USERNAME%`）、`%SID%` 与 `%SESSION%`；文件位置还可以使用 `%SystemDrive%`、`%SBIEHOME%` 以及相应的 shell 文件夹变量。在此根展开路径中，`%BOXNAME%` **不是** `%SANDBOX%` 受支持的别名。展开并不会使任意注册表、IPC 或文件根值变为有效。

<div id="file-root-selection-and-legacy-fallback"></div>

## 文件根的选择与旧版回退

Sandboxie 首先查找有效的 `FileRootPath`。只有在没有任何可用值时，它才会去找有效的、已弃用的 [`BoxRootFolder`](BoxRootFolder.md)，追加 `\Sandbox\<box name>`，并将其作为文件根。如果两个设置都不可用，则使用上面的内置默认值。“有效”包括沙盒自身的设置、适用的已启用模板以及 `[GlobalSettings]` 回退：例如全局 `FileRootPath` 会胜过沙盒本地的 `BoxRootFolder`。新配置请使用 `FileRootPath`。

<div id="file-layout"></div>

## 文件布局

在默认布局下，沙盒的文件根可以包含：

```text
FileRootPath\
  drive\C\...                 驱动器 C: 上的本地文件
  user\current\...           当前用户的配置文件
  user\all\...               共享/所有用户的配置文件
  user\public\...            公共配置文件（若可用）
  share\server\share\...     网络共享文件
  RegHive                     沙盒化的注册表配置单元
```

其他驱动器会以各自的驱动器号出现。Windows 还可能维护与 `RegHive` 关联的文件。[沙盒层级](SandboxHierarchy.md) 页面介绍了常规的重定向示例；下面的设置可以更改文件侧的文件夹名，而不改变应用程序使用的宿主路径。

<div id="user-profile-layout"></div>

## 用户配置文件布局

[`SeparateUserFolders`](SeparateUserFolders.md) 默认为 `y`。启用后，Sandboxie 会把可识别的配置文件路径映射到可移植的 `user\current`、`user\all` 以及（若可用）`user\public` 位置。设为 `n` 时，它不初始化这些特殊的配置文件映射，因此普通的本地配置文件路径会遵循驱动器布局，例如 `drive\C\Users\...`。这不会更改 Windows 配置文件或账户权限。

<div id="drive-identity-in-the-sandbox"></div>

## 沙盒中的驱动器标识

`UseVolumeSerialNumbers` 默认为 `n`。设为 `y` 时，只要能够读取，已知的驱动器号后面会跟上 Windows 文件系统的卷序列号：例如 `drive\C` 会变为 `drive\C~1234-ABCD`。驱动器号仍是名称的一部分；如果序列号不可用或为零，则不加后缀。这有助于区分重复使用同一驱动器号的可移动卷，但并不保证避免所有冲突，也不是安全边界。它不使用物理磁盘的固件序列号，不隐藏磁盘标识，也不更改 `share` 布局。

<div id="volumes-without-drive-letters"></div>

## 没有驱动器号的卷

`UseVolumeGuidWhenNoLetter` 默认为 `n`。对于挂载在目录中但未分配驱动器号的卷，默认布局使用第一个挂载目录作为该卷的沙盒位置，并把它的其他挂载点映射到那里。设为 `y` 时，Sandboxie 可以改用形如 `drive\{volume-guid}` 的文件夹，并把已挂载的目录映射到它。正常的驱动器号映射仍然优先；GUID 设置并不是适用于所有驱动器的新布局。其结果取决于 Windows 公开的卷与挂载点。

<div id="changing-roots-or-layout"></div>

## 更改根或布局

更改根或布局设置会改变后续操作查找或放置沙盒数据的位置；它**不会**自动移动既有内容。特别是，在非空沙盒上切换 `SeparateUserFolders` 或 `UseVolumeSerialNumbers`，可能会把文件留在原先的文件夹名之下。沙盒非空时，SandMan 会禁用这两个复选框。请在空沙盒上使用布局选项。如果必须保留既有数据，请单独处理；更改这些设置不会迁移这些数据。仅更改配置中的 `FileRootPath` 不会重新定位旧的文件容器。在旧配置单元仍处于挂载状态时更改 `KeyRootPath`，还可能与正在使用的配置单元冲突。

恢复路径映射使用该沙盒当前识别到的布局；留在较旧布局下的内容不会因更改这些设置而被迁移。清理行为是另一个话题。

<div id="verbose-volume-checks"></div>

## 详细的卷检查

`EnableVerboseChecks` 默认为 `n`。其元数据与历史变更日志描述了一项可选警告（`SBIE2227`），涉及在所属卷上创建短名（8.3）。在当前实现中，配置单元挂载处理程序在卷检查之前传给 DOS 路径转换的是**注册表**根，而不是文件根。正常的 `KeyRootPath` 无法通过该转换，因此即便设置 `EnableVerboseChecks=y`，普通沙盒也不会执行 8.3 测试或触发该警告。请不要把此选项当作对文件容器卷的有效检查。如果通过非常规配置执行到该测试，它查询的是该卷的短名创建状态，而不是特定的 8.3 名称是否已存在。

<div id="applying-changes"></div>

## 应用更改

根路径在 Sandboxie 构造沙盒路径信息时解析。三个 DLL 文件布局选项在沙盒化进程初始化其文件处理时读取。已初始化的进程不会仅因配置更改而重建这些映射；请重启受影响的沙盒化进程，并避免就地更改已挂载或非空的沙盒。设备更改通知可以在进程内刷新驱动器号信息，但不会重新读取选项值。

SandMan 在 **全局设置 > 高级选项 > 沙盒配置** 中提供全局根默认值，并在 **沙盒选项 > 高级选项 > 杂项 > 添加选项** 中提供按沙盒的根条目。新建沙盒向导也会提供文件容器位置。两个主要的文件布局复选框位于 **沙盒选项 > 文件选项** 下。`UseVolumeGuidWhenNoLetter` 与 `EnableVerboseChecks` 没有专用复选框；可以在高级配置中手动输入。

<div id="version-history"></div>

## 版本历史

- `SeparateUserFolders=n` 在 Sandboxie Plus 0.2.2 / Classic 5.41.2 中引入。
- `UseVolumeSerialNumbers=y` 在 Plus 0.8.0 / Classic 5.50.0 中引入，用于帮助避免混用重复使用同一驱动器号的可移动卷中的数据。
- `EnableVerboseChecks=y` 在 Plus 1.7.2 / Classic 5.62.2 中成为历史上 `SBIE2227` 检查的选用形式；上文所述的当前运行时限制优先于该历史描述。
- 在较新的无驱动器号布局被回退后，`UseVolumeGuidWhenNoLetter=y` 在 Plus 1.13.1 / Classic 5.68.1 中成为选用的 GUID 布局。

<div id="related-pages"></div>

## 相关页面

- [文件根路径](FileRootPath.md)、[沙盒根文件夹](BoxRootFolder.md)、[注册表根路径](KeyRootPath.md) 与 [IPC 根目录](IpcRootPath.md) 分别介绍各根设置。
- [分离用户文件夹](SeparateUserFolders.md) 与 [沙盒层级](SandboxHierarchy.md) 更详细地说明普通文件布局。
- [Sandboxie Ini](SandboxieIni.md) 说明沙盒与全局配置。
