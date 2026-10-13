# 开放受保护的存储

当前，若要开放宿主的旧版 Windows [受保护存储](ProtectedStorage.md)（PStore）端点，应为沙盒选择 Sandboxie 的 **Open Protected Storage** 模板：

```ini
[DefaultBox]
Template=OpenProtectedStorage
```

旧的 `OpenProtectedStorage=y` 布尔设置仍保留在设置元数据中，也可能出现在旧配置里，但它**不是**当前的配置方法。Sandboxie Plus 1.8.0 / Classic 5.63.0 已用此模板替代该设置。旧配置迁移可以将此布尔设置转换为模板选择；当前源码中的旧驱动端读取逻辑已被注释掉。无需修改随附模板来启用此选项。

<div id="what-the-template-does"></div>

## 模板的作用

随附模板包含以下系统路径开放规则：

```ini
OpenFilePath=|\Device\NamedPipe\protected_storage
OpenIpcPath=*\BaseNamedObjects*\PS_SERVICE_STARTED
OpenIpcPath=\RPC Control\protected_storage
```

在普通沙盒中，Sandboxie 通常会挂钩 `PStoreCreateInstance`，提供自己的 `IPStoreImpl` 兼容实现。当有效 IPC 策略开放了 `\RPC Control\protected_storage` 时，PStore 初始化会跳过此钩子。模板中的开放规则生效后，就可通过此机制使用原生 PStore，而非 Sandboxie 的替代实现。随附模板中历史遗留的 `FuncSkipHook=PStoreCreateInstance` 行已被注释掉，不是生效的规则。

同一端点检查会在读取 [开放凭据](OpenCredentials.md) 设置之前执行。当该端点实际处于开放状态时，Sandboxie 也会跳过用户模式下的 WinCred 钩子，相关凭据 API 调用可直接使用原生实现。单独设置 `OpenCredentials=y` 则会保留独立的 PStore 钩子。PStore 和 Windows 凭据 API 在此处有关联，但它们并不是同一种机制。

<div id="sandman-and-scope"></div>

## SandMan 设置与适用范围

SandMan 通过 **沙盒选项 > 常规选项 > 限制选项 > 其它限制 > 开放“系统保护的存储”权限** 提供此模板选项。选中后，独立的 **开放 Windows 凭据存储访问权限（用户模式）** 复选框会显示为已勾选且禁用。SandMan 保存的是模板选择，而不是 `OpenProtectedStorage=y`，也不会自动保存 `OpenCredentials=y`。

在[应用隔间](../PlusContent/compartment-mode.md)模式中，Sandboxie 已经会跳过其替代 PStore 钩子。但仅凭这一点，无法判断独立的 WinCred 钩子是否安装；WinCred 自身的端点检查和 `OpenCredentials` 检查仍然有效。

钩子是否安装取决于沙盒化进程中相关模块初始化时的配置。更改模板后，应重启受影响的沙盒化应用程序及其子进程。通常无需仅为这些用户模式钩子重启 Windows、驱动程序或服务。
