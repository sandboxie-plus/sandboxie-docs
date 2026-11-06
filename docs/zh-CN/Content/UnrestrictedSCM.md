# 不受限的 SCM {#unrestricted-scm}

*UnrestrictedSCM* 是一项高级沙盒设置，它会绕过 Sandboxie 服务启动授权路径中的一项服务控制管理器（SCM）权限检查：

```ini
[DefaultBox]
UnrestrictedSCM=y
```

默认值为 `n`。

> [!WARNING]
> 启用此设置会削弱隔离。仅应在已确定存在服务兼容性需求时才使用它。

## 该设置改变的内容 {#what-the-setting-changes}

当全局路径 `RunServicesAsSystem=y` 为沙盒化服务选择 SYSTEM 源令牌时，SbieSvc 通常会检查调用方对真实 Windows SCM 是否会具有 `SC_MANAGER_ALL_ACCESS` 权限。它会获取 SCM 的安全描述符，并使用适合该沙盒模式的调用方令牌执行 Windows 访问检查。如果该检查失败，Sandboxie 会拒绝此次 SYSTEM 服务启动。

*UnrestrictedSCM* 会绕过该项特定的权限检查。它不会授予每个沙盒化进程不受限的 SCM 访问权限，也不会禁用 Sandboxie 通用的 SCM 拦截与模拟。

## 相关服务控制项 {#related-service-controls}

*UnrestrictedSCM* 不会：

- 启用 `RunServicesAsSystem`；
- 将服务添加到 `RunServiceAsSystem`；
- 将服务归类为沙盒化服务；
- 将已有的宿主服务移入沙盒；
- 使由此产生的服务进程变为非沙盒化。

`RunServicesAsSystem` 和 `RunServiceAsSystem` 通过各自独立的全局路径和按服务路径选择 SYSTEM 源身份。这些设置参见 [Sandboxed Services](SandboxedServices.md)。

Sandboxie 会在 *UnrestrictedSCM* 检查之前求值 [撤销管理员权限](DropAdminRights.md)。如果撤销权限策略已经拒绝了提升权限路径，启用 *UnrestrictedSCM* 也不会覆盖该拒绝结果。

`SandboxieDcomLaunch.exe` 有单独的内置授权例外，不需要 *UnrestrictedSCM*。

## 配置范围 {#configuration-scope}

*UnrestrictedSCM* 是一项沙盒级布尔设置。当沙盒未提供覆盖值时，适用的模板和全局设置回退值可以参与构成其生效值。系统在执行相关服务启动授权时查询此设置，因此重新加载配置可能会影响后续的请求；它不会改变已在运行的服务进程。

## SandMan {#sandman}

打开**沙盒选项 > 安全选项 > 高级安全**，使用：

> 仅允许特权进程访问“服务控制管理器”

该复选框与 *UnrestrictedSCM* 的含义相反：

- 选中：启用常规保护，这也是默认行为；
- 未选中：SandMan 可以写入 `UnrestrictedSCM=y`。

SandMan 会将带有 `UnrestrictedSCM=y` 的沙盒识别为**削弱隔离**。

## 版本历史 {#version-history}

*UnrestrictedSCM* 在 Sandboxie Plus 0.3 / Classic 5.42 中引入，是用于禁用在 Security Issue ID-3 修复中添加的 SCM 访问检查的调试选项。

## 相关页面 {#related-pages}

- [Sandboxed Services](SandboxedServices.md)
- [撤销管理员权限](DropAdminRights.md)
- [Sandboxie Ini](SandboxieIni.md)
