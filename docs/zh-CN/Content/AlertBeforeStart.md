# 启动前警报 {#alertbeforestart}

*AlertBeforeStart* 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 Sandboxie Plus 1.14.1 与 Sandboxie Classic 5.69.1 起提供。它默认禁用。

```ini
[DefaultBox]
AlertBeforeStart=y
```

启用后，*AlertBeforeStart* 会在非沙盒化的 `Start.exe` 实例于所选沙盒内重新启动自身之前请求确认。它为符合条件的宿主侧 `Start.exe` 启动增加了一个用户同意步骤；它不是针对每个沙盒化进程的确认提示，也不是安全边界。

<div id="covered-launch-paths"></div>

## 涵盖的启动路径

确认适用于宿主侧的 `Start.exe` 沙盒入口路径。涵盖的示例包括：

- `Start.exe /box:<box> program.exe`，以及使用所选或默认沙盒的常规宿主侧 `Start.exe` 启动；
- 通过 `Start.exe` 启动的 SandMan 操作，包括 **运行程序(Run)**、**默认浏览器**、**默认电子邮件客户端** 与 **开始菜单**；
- 当前 Sandboxie Plus 的 **在沙盒中运行** shell 集成，它最终通过 SandMan 与 `Start.exe` 启动；
- 由 SandMan 生成的快捷方式，以及直接调用 `Start.exe` 的快捷方式。

这并不意味着每一个 SandMan 操作都被涵盖。该操作必须使用符合条件的 `Start.exe` 沙盒入口路径。仅涉及控制、且在该路径之前就已完成的操作（例如终止、重新加载与删除操作）不在此设置的范围内。更完整的命令参考参见 [启动命令行](StartCommandLine.md)。

那些有意在沙盒之外启动初始程序的启动路径（例如当前的禁用强制与强制子进程绕过路径）不会让该初始进程触发这项确认。

<div id="in-sandbox-and-forced-launches"></div>

## 沙盒内启动与强制启动

已经在沙盒内的 `Start.exe` 实例不会为常规的沙盒内启动重复这项确认。因此，该设置不涵盖本来就发生在沙盒内的普通进程创建，包括：

- `CreateProcess` 子进程；
- 常规的 `ShellExecute` 子进程启动；
- 浏览器渲染进程或 GPU 进程；
- 启动游戏的游戏启动器；
- 沙盒化应用程序的其他普通后代进程。

直接的 [强制进程](ForceProcess.md) 与 [强制文件夹](ForceFolder.md) 启动同样不走这条 `Start.exe` 确认路径。启用 *AlertBeforeStart* 并不意味着所有强制程序都需要确认。强制程序与强制文件夹各自独立的行为参见 [程序启动设置](ProgramStartSettings.md)。

<div id="confirmation-prompts"></div>

## 确认提示

启用该设置后：

1. `Start.exe` 首先询问是否在所选沙盒中启动新程序。
2. 当表面父进程的可执行文件路径（位于 Sandboxie 安装目录下）使其看起来不像是 Sandboxie 组件时，可能会显示第二条警告。

第一个提示会标明目标沙盒。它不会显示正在启动的可执行文件、完整命令行、调用方可执行文件或调用方进程 ID。两个提示都提供 **是** 与 **否** 选项，且没有“记住”选项。

- **是** 会继续到第二条警告（若适用），或继续执行沙盒启动。
- **否** 会取消启动。`Start.exe` 以失败状态终止，而不会启动所请求的沙盒化进程，因此调用它的脚本可以观察到失败的进程结果。

不会仅因为用户选择了 **否** 就生成专门的 SBIE 拒绝消息。

第二条警告使用的是表面父进程路径检查。它不是签名验证、受信任发布者验证、Sandboxie 二进制文件身份验证，也不是调用方沙盒状态校验。

<div id="silent-and-non-interactive-use"></div>

## 静默与非交互使用

`/silent` 开关不会抑制 *AlertBeforeStart* 的确认对话框，`/hide_window` 同样不会。这些开关会影响 `Start.exe` 的其他界面行为，但不会绕过这些确认提示。

该功能期待一个交互式确认对话框，并且没有超时。不应把它当作针对非交互式或服务式启动的确定性拒绝机制；当对话框无法得到回答时，Sandboxie 也不提供单独的日志记录或拒绝回退。

<div id="elevation"></div>

## 提升权限

确认发生在沙盒化的 `Start.exe` 实例创建之前，也发生在最终目标程序的 UAC 或提升权限请求之前。*AlertBeforeStart* 不控制提升权限，也不是 UAC 或权限边界。

<div id="security-and-policy-limitations"></div>

## 安全与策略限制

该选项要求符合条件的沙盒启动先获得用户确认，从而减少宿主侧对 `Start.exe` 的不被察觉的使用。它不会：

- 防止沙盒逃逸；
- 验证 Sandboxie 组件的身份；
- 涵盖沙盒化进程能够启动的每一种方式；
- 取代 `StartRunAccess` 或其他启动限制。

确认警报不会覆盖常规沙盒策略。如果另一项策略拒绝了所请求的启动，选择 **是** 也不会授予权限。[分离沙盒进程](BreakoutProcess.md) 与 [分离文件夹](BreakoutFolder.md) 同样是彼此独立的机制。

<div id="sandbox-options"></div>

## 沙盒选项

在 Sandboxie Plus 中，打开 **沙盒选项 > 程序控制 > 启动限制** 并使用：

**在从外部源启动沙盒中的进程之前显示弹出警告**

该复选框默认未勾选。其工具提示为：

> 该设置可用于防止程序在未经用户知情或同意的情况下在沙盒中运行。

这里的“外部源”描述的是符合条件的宿主侧 `Start.exe` 启动路径。它不是一个经过正式认证的调用方类别。

<div id="scope-and-applying-changes"></div>

## 作用范围与应用更改

该设置可以逐沙盒配置、通过常规模板继承，或通过 `GlobalSettings` 回退值提供。没有文档化的按程序或按映像语法。

`Start.exe` 在每次符合条件的沙盒入口尝试时读取该设置。更改保存后，它会应用于下一次符合条件的调用；这个短时存在的启动器不会在两次启动之间缓存它。SandMan、SbieSvc 与已有的沙盒化程序不必仅因该选项发生变化而重启。如果你手动编辑 `Sandboxie.ini`，常规的配置重新加载要求仍然适用。

<div id="sandboxie-plus-and-classic"></div>

## Sandboxie Plus 与 Classic

启动行为实现在共享的 `Start.exe` 中。Sandboxie Plus 在 SandMan 中提供该复选框，而 Sandboxie Classic 的 `Start.exe` 可以在不提供 SandMan 界面的情况下遵循该 INI 设置。

不要把这个设置与 [警报进程](AlertProcess.md) 混淆。*AlertBeforeStart* 在符合条件的 `Start.exe` 沙盒入口之前请求确认，而 *AlertProcess* 是另一项警报功能，方向与范围都不同。

<div id="version-history"></div>

## 版本历史

*AlertBeforeStart* 在 Sandboxie Plus 1.14.1 与 Sandboxie Classic 5.69.1 中引入，默认禁用。SandMan 复选框在同一发布开发周期内加入。当前行为仍然沿用宿主侧 `Start.exe` 确认模型。

<div id="related-configuration"></div>

## 相关配置

- [Sandboxie Ini](SandboxieIni.md)
- [启动命令行](StartCommandLine.md)
- [程序启动设置](ProgramStartSettings.md)
- [警报进程](AlertProcess.md)
- [强制进程](ForceProcess.md)
- [强制文件夹](ForceFolder.md)
