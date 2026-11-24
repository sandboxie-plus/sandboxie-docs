# 启动系统沙盒 {#start-system-box}

_StartSystemBox_ 是一项可重复的全局设置，用于在 SbieSvc 启动且 Sandboxie 驱动程序就绪时，在会话 0 中启动指定的沙盒。

```ini
[GlobalSettings]
StartSystemBox=SystemBox
```

每个值都是沙盒名称，而不是布尔值。多个条目会启动多个沙盒：

```ini
[GlobalSettings]
StartSystemBox=BoxOne
StartSystemBox=BoxTwo
```

<div id="startup-behavior"></div>

## 启动行为

对每个配置的名称，SbieSvc 会发起等价于以下内容的操作：

```text
Start.exe /box:<BoxName> auto_run
```

启动流程为：

```text
SbieSvc 启动，驱动程序就绪
    -> 为配置的沙盒启动 Start.exe
    -> Start.exe 在该沙盒内重新启动
    -> auto_run 处理该沙盒支持的自动启动位置
```

由于该流程源自 SbieSvc，它在会话 0 中以 SYSTEM 身份运行。生成的进程仍与指定的沙盒关联；SYSTEM 身份并不会使它们成为非沙盒化的进程。

<div id="what-auto_run-starts"></div>

## `auto_run` 会启动什么

当前的 `auto_run` 实现会处理机器与当前用户下沙盒可见的 `Run`、`RunOnce` 注册表项（包括它们的 32 位位置），以及公共启动文件夹与用户启动文件夹。

该命令当前不会直接启动沙盒内的服务。`StartService`、`StartProgram` 和 `AutoExec` 是彼此独立的沙盒启动机制，不应被视为 _StartSystemBox_ 的同义词。

<div id="security-considerations"></div>

## 安全考量

对于以这种方式启动的沙盒，项目建议启用 [撤销管理员权限](DropAdminRights.md)：

```ini
[SystemBox]
DropAdminRights=y
```

会话 0 的 SYSTEM 身份使令牌加固尤为重要，但 `DropAdminRights` 并不能使任意的 SYSTEM 软件变得安全。[剥离 SYSTEM 权限](StripSystemPrivileges.md) 是一项独立的控制，供特定的服务与 RpcSs 令牌创建路径使用；它不会仅仅因为 _StartSystemBox_ 在会话 0 中启动了沙盒就自动应用。

<div id="applying-changes"></div>

## 应用更改

SbieSvc 会在驱动程序就绪后的启动序列中读取 _StartSystemBox_ 条目。常规的配置重载不会执行新增的条目。更改会在下一次 Sandboxie 服务启动或系统启动时生效。移除条目不会终止已经启动的进程。

## SandMan

SandMan 没有专门的 _StartSystemBox_ 控件。请在 Sandboxie.ini 的 `[GlobalSettings]` 下手动配置它。

<div id="version-history"></div>

## 版本历史

_StartSystemBox_ 于 Sandboxie Plus 0.9.5 / Classic 5.51.5 随会话 0 沙盒启动和 `auto_run` 命令一同引入。

<div id="related-pages"></div>

## 相关页面

- [撤销管理员权限](DropAdminRights.md)
- [剥离 SYSTEM 权限](StripSystemPrivileges.md)
- [启动服务](StartService.md)
- [启动程序](StartProgram.md)
- [自动执行](AutoExec.md)
- [沙盒化服务](SandboxedServices.md)
- [Sandboxie Ini](SandboxieIni.md)
