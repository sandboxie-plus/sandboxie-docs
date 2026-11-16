# 阻止 WinRM {#block-winrm}

*BlockWinRM* 是 Sandboxie 针对 Windows 远程管理（WinRM）及其远程命令组件 WinRS 的一项缓解措施。它不会禁用宿主的 WinRM 服务，也不会阻断所有网络通信。当前 Sandboxie 施加的是一项文件组件限制，以及在沙盒化注册表视图中写入的一项独立策略值。

## 当前的强制执行层 {#current-enforcement-layers}

`[DefaultTemplates]` 中强制的 `Template_BlockWinRM` 为 WinRM/WinRS 组件 `wsmsvc.dll`、`wsmauto.dll` 与 `winrs.exe` 提供 `ClosedFilePath` 规则，作用于相关的 Windows 系统目录。这些是面向沙盒化进程的文件访问限制，并不保证所有可能的远程管理途径都被阻断。

另外，在沙盒首次进行自定义时，启用的 `BlockWinRM` 选项会让 Sandboxie 尝试在以下位置写入 DWORD 值 `AllowNegotiate=0`：

```text
HKLM\Software\Policies\Microsoft\Windows\WinRM\Client
```

该值被放在沙盒化的注册表视图中；Sandboxie 不会通过此操作更改宿主真实的 WinRM 策略。

## 配置与 `n` 的含义 {#configuration-and-the-meaning-of-n}

```ini
[DefaultBox]
BlockWinRM=y
```

在没有任何有效值时，该设置默认为 `y`。沙盒自身的取值优先于 `[GlobalSettings]`。该选项在 SandMan 或 Sandboxie Control（Classic）中都没有专用复选框。在 SandMan 中，请使用 **沙盒选项 > 配置文本 > 编辑配置** 手动配置该布尔值。

在当前实现中，当那项由布尔值控制的自定义尚未执行时，`BlockWinRM=n` 会阻止 `AllowNegotiate=0` 自定义。它本身**不会**移除强制模板 `Template_BlockWinRM` 提供的文件限制。其他适用的文件访问规则仍决定对这些组件的实际访问权限。因此，`n` 并不是一个能在沙盒内完全启用 WinRM 的通用开关。

历史上 Sandboxie Plus 0.7.1 / Classic 5.48.5 的更新日志曾说 `BlockWinRM=n` 会禁用 WinRM 文件封锁。那描述的是更早的直接驱动程序路径；当前构建改用默认模板提供那些文件规则。

## 应用更改 {#applying-changes}

这些文件组件规则会在进程启动时载入其文件策略。更改相关文件规则后，请重启受影响的沙盒化进程。

注册表自定义则不同：它在沙盒首次自定义时执行，并把状态留在沙盒内容中。之后更改 `BlockWinRM` 不会自动清除既有的 `AllowNegotiate=0` 值，也不一定会为既有沙盒重新执行自定义。如果某项更改必须影响初始的沙盒策略状态，请使用空沙盒或新建沙盒，并重启其中的进程。清空沙盒会移除其既有沙盒内容，因此请先保留需要的东西。

## 作用范围与相关页面 {#scope-and-related-pages}

该设置与 [阻止网络文件访问](BlockNetworkFiles.md) 不同，后者控制对网络共享文件与文件夹的访问。两项设置都不能替代互联网访问策略或防火墙策略。手动配置方法参见 [Sandboxie Ini](SandboxieIni.md)。

## 版本历史 {#version-history}

`BlockWinRM` 被列为在 Sandboxie Plus 0.7.1 / Classic 5.48.5 中加入。强制的 `[DefaultTemplates]` 出现于 0.9.8 / 5.53.0。在 1.7.3 / 5.62.3 中，WinRM 文件组件规则被移入 `Template_BlockWinRM` 并纳入 `[DefaultTemplates]`；早先由布尔值控制的驱动程序文件列表不再是活动路径。
