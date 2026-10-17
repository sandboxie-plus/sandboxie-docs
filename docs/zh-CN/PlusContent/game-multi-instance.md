# 在 Sandboxie 中运行游戏

本页汇总在 Sandboxie Plus 中运行游戏（尤其是同一游戏的多个实例）的实践指南。它补充 [App Compartment](compartment-mode.md) 文档，提供面向游戏场景的决策路径；隔离模型本身的细节请参考该页。

## 何时需要宽松沙盒

大多数游戏在标准沙盒里都能正常运行。当游戏的启动器或引擎与 Sandboxie 的隔离机制交互不佳时，游戏通常需要更宽松的配置。典型症状包括：

- **启动器起来了，但游戏一直卡在加载阶段**。启动器可能触发自身的看门狗超时（例如弹出“启动器无响应”提示框），而此时引擎仍在初始化；
- **沙盒内的启动速度明显慢于沙盒外**，严重时慢到启动器的超时机制率先放弃；
- **游戏能运行，但每次首次启动都非常漫长**，之后恢复正常（写时复制迁移已经完成）。

这些症状通常指向游戏自身的保护或反作弊层与 Sandboxie 的 API hook 产生冲突：它可能将初始化过程拖慢到超出启动器超时阈值。在部分系统上，Windows 升级之后才会出现这种现象——因为更新的 Windows 构建改变了 hook 所依赖的拦截路径。

!!! tip

    在修改沙盒设置之前，请先确认 Sandboxie Plus 本身版本较新：较新的版本携带了在近期 Windows 构建上所需的内核数据（DynData），过期的驱动在新版 Windows 上本身就可能导致沙盒应用变慢或无法启动。可在 [CHANGELOG](https://github.com/sandboxie-plus/Sandboxie/blob/master/CHANGELOG.md) 中查看带有 "updated DynData" 的条目确认。

## 优先尝试标准沙盒

标准沙盒提供最强隔离，是默认的正确选择。即使游戏启动缓慢，也值得先在标准沙盒里诊断一次——这可能暴露的是一条真正缺失的访问规则，而非 hook 冲突。当程序能在标准沙盒里成功启动时，可以把它的访问跟踪记录（见 [跟踪日志](TraceLog.md)）与宽松沙盒对比，看清究竟需要放行什么。

如果游戏确实无法使用标准沙盒，[App Compartment](compartment-mode.md) 沙盒会绕过大部分隔离 hook，同时保留文件和注册表虚拟化——足以让多个实例互相分离，但它不是安全边界：

```ini
[MyGameBox]
Enabled=y
NoSecurityIsolation=y
```

!!! note

    此功能需要[支持者证书](supporter-certificate.md)。没有有效证书时，Sandboxie 会拒绝在此配置的沙盒中启动进程并显示错误。

## 每个游戏实例一个沙盒

为每个实例分配独立的沙盒。文件和注册表虚拟化会随之让各实例彼此分离，无需额外配置——每个沙盒拥有独立的写时复制文件夹，以及各自的存档、设置和缓存：

```ini
[Game1]
NoSecurityIsolation=y
BoxDataFolder=%UserProfile%\Documents\GameInstance1

[Game2]
NoSecurityIsolation=y
BoxDataFolder=%UserProfile%\Documents\GameInstance2
```

`BoxDataFolder` 是可选的；不设置时使用默认沙盒目录。让每个沙盒指向各自的数据目录，可以让备份、重置（“清空沙盒内容”）以及按实例安装 MOD 都变得简单——因为一个实例的所有内容都集中在一处。

从各自的沙盒分别启动各实例，例如：

```plaintext
"C:\Program Files\Sandboxie-Plus\Start.exe" /box:Game1 "C:\Games\MyGame\launcher.exe"
"C:\Program Files\Sandboxie-Plus\Start.exe" /box:Game2 "C:\Games\MyGame\launcher.exe"
```

## 多实例的资源规划

每个实例运行的是完整的游戏客户端——瓶颈通常在游戏本身而非沙盒。供参考：典型网游的三个实例在 32GB 内存的机器上运行从容，建议每个实例至少分配两个 CPU 核心，以免主机响应迟滞。图形需求高的游戏通常受限于 GPU 而非 Sandboxie；沙盒内降低虚拟图形设置可以减少 CPU 开销，但可能损失画质。

磁盘占用主要来自各沙盒的写时复制文件夹。每个实例首次启动时会把游戏文件复制（迁移）进沙盒，之后的启动复用该副本。请按“游戏体积 × 实例数”规划磁盘空间，并记住：退役某个实例时，“清空沙盒内容”是回收空间的正规方式。

## 游戏仍然无法启动时

- **在 App Compartment 沙盒里依然卡住**：此时 Sandboxie 的隔离大概率不是症结。请检查游戏自身的要求（显卡驱动、运行库、反作弊组件），并尝试在沙盒外启动作为对照。
- **Windows 更新之前能跑**：先更新 Sandboxie Plus（驱动可能缺少新构建的内核数据）；如果已经是最新版本，再重新审视沙盒类型的选择。
- **修改系统虚拟化设置没有帮助**：社区反馈（以及在 Windows 11 上的本地实测）表明，关闭内存完整性（HVCI）或 VBS 通常**不能**解决启动器看门狗超时；冲突发生在游戏保护层而非内核虚拟化检查。请把这类设置视为安全决策，而不是游戏兼容性手段。

## 需要留意的限制

- App Compartment 沙盒会显著降低隔离强度——参见其[安全与兼容模型](compartment-mode.md#security-and-compatibility-model)。只把它用于游戏，而不要作为通用配置。
- 如果支持者证书过期，设置了 `NoSecurityIsolation=y` 的沙盒将拒绝启动进程，直到应用新证书为止。日常依赖此模式时，请留意证书到期时间。
- 模板规则在 App Compartment 沙盒中仍然生效。当游戏需要特定路径或对象时，请把规则添加到它自己的沙盒，而不是进一步弱化沙盒。

## 相关页面

- [App Compartment](compartment-mode.md)
- [禁用安全隔离](../Content/NoSecurityIsolation.md)
- [Start.exe 命令行](../Content/StartCommandLine.md)
- [跟踪日志](TraceLog.md)
