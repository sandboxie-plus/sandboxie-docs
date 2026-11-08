# 剥离 SYSTEM 权限 {#strip-system-privileges}

*StripSystemPrivileges* 控制从通过特定 SbieSvc 服务路径和 RpcSs 路径创建的 SYSTEM 源令牌中移除权限的行为：

```ini
[DefaultBox]
StripSystemPrivileges=y
```

默认值为 `y`，即具有保护作用的行为。

> [!WARNING]
> `StripSystemPrivileges=n` 会为受影响的 SYSTEM 令牌路径恢复较早的、限制较少的行为，不建议这样做。

## 移除的权限 {#privileges-removed}

在受影响的路径上启用时，Sandboxie 会从新复制的令牌中移除以下权限：

- `SeTcbPrivilege`
- `SeCreateTokenPrivilege`

Sandboxie 使用 Windows 的 `SE_PRIVILEGE_REMOVED` 操作。这些权限会从该令牌中移除，而不只是被禁用，因此无法简单地在同一令牌上重新启用它们。当前的辅助实现不会移除 `SeAssignPrimaryTokenPrivilege`。

## 运行时范围 {#runtime-scope}

当前的实现在 SbieSvc 创建以下令牌时应用此设置：

- 为选定以 SYSTEM 身份运行的沙盒化服务创建的 SYSTEM 源令牌；
- 为相关的沙盒化 RpcSs 进程服务器路径创建的 SYSTEM 源令牌。

它不适用于普通的用户令牌服务启动，也不应被描述为对每个沙盒化进程或每个 SYSTEM 进程都生效的全局权限过滤器。

如果令牌复制、调整或所需的权限移除操作失败，受影响的启动或令牌请求会失败，而不会故意以未经剥离的 SYSTEM 令牌继续执行。

## 配置范围 {#configuration-scope}

*StripSystemPrivileges* 是一项沙盒级布尔设置。当沙盒未提供覆盖值时，适用的模板和全局设置回退值可以参与构成其生效值。系统会在创建受影响的令牌时查询此设置，因此更改它不会修改已分配给运行中进程的令牌。更改后请重启受影响的沙盒化服务或进程。

## SandMan {#sandman}

打开**沙盒选项 > 安全选项 > 高级安全**，使用：

> 撤销以系统令牌运行中的程序的关键特权

该复选框直接表示此项保护性设置：

- 选中：已启用权限移除，这也是默认行为；
- 未选中：SandMan 会写入 `StripSystemPrivileges=n`。

## 与会话 0 启动的关系 {#relationship-to-session-0-startup}

[Start System Box](StartSystemBox.md) 使用不同的启动路径。在会话 0 中以 SYSTEM 身份启动的沙盒，本身并不会使该令牌经过本文档介绍的 *StripSystemPrivileges* 辅助函数。

## 版本历史 {#version-history}

*StripSystemPrivileges* 在 Sandboxie Plus 0.5.4 / Classic 5.46.0 中引入，是 Security Issue ID-4 修复的一部分。

## 相关页面 {#related-pages}

- [Sandboxed Services](SandboxedServices.md)
- [Start System Box](StartSystemBox.md)
- [撤销管理员权限](DropAdminRights.md)
- [Sandboxie Ini](SandboxieIni.md)
