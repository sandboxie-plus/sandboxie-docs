# 无 UAC 代理 {#no-uac-proxy}

<div id="overview"></div>

## 概述

**NoUACProxy** 控制 Sandboxie 是否拦截发往 Windows 应用程序信息服务（AppInfo）的受支持异步 RPC 请求，并把识别出的提权请求交给它自己的 UAC 代理处理。它默认禁用，因此 Sandboxie 的代理处理通常处于活动状态。

```ini
[DefaultBox]
NoUACProxy=y
```

启用 `NoUACProxy=y` 后，Sandboxie 的 RPC 包装会针对这些调用跳过提权识别与代理逻辑。原始的本地 RPC 调用随后被允许继续执行。

<div id="what-it-does-not-mean"></div>

## 它并不意味着什么

此设置不会禁用 Windows 用户账户控制，也不会单独阻止提权请求。原生 UAC 路径是否成功，取决于 Windows 以及沙盒的 RPC 与资源访问配置。

反过来，`NoUACProxy=n` 也不意味着 Sandboxie 拦截了所有可能的提权机制。当前代理识别的是受支持的、用于进程提权与管理员令牌请求的异步 AppInfo/UAC RPC 请求。

<div id="boolean-setting-and-compatibility-template"></div>

## 布尔设置与兼容性模板

该布尔设置与内置模板的作用范围不同：

```ini
NoUACProxy=y
```

会禁用 Sandboxie 对提权 RPC 的拦截。它不会添加 RPC 访问规则。

```ini
Template=NoUACProxy
```

会启用该布尔设置，同时提供与 UAC 相关的 RPC 端口绑定，目的是让原生路径在该模板的兼容性场景中可用。这些额外绑定来自 `Template_NoUACProxy`，而不是来自该布尔设置本身。

SandMan 没有专门的 **NoUACProxy** 复选框。内置模板位于 **沙盒选项 > 应用模板 > 模板** 的 **杂项** 分类下，名称为 **Open RPC Port Bindings for UAC**。也可以通过 `Template=NoUACProxy` 手动选择它。

<div id="application-compartment-history"></div>

## 应用隔间历史

Sandboxie Plus 1.0.4 / Classic 5.55.4 的更新日志称，应用隔间沙盒会默认启用该模板。当前 SandMan 代码在创建或选择应用隔间预设时不再自动启用它；原先的调用已被注释掉。不要假定现在选择该沙盒类型就会启用 **NoUACProxy** 或其模板。

<div id="relationship-to-other-elevation-settings"></div>

## 与其他提权设置的关系

* [使用 Sandboxie UAC](UseSandboxieUAC.md) 控制 Sandboxie 代理内部的增强提示。当 `NoUACProxy=y` 跳过代理拦截时，该提示不会通过被跳过的路径触发。
* [Apply ElevateCreateProcess Fix](ApplyElevateCreateProcessFix.md) 可以在 `CreateProcess` 报告需要提权后发起 Windows `runas` 请求。**NoUACProxy** 决定 Sandboxie 受支持的 RPC 拦截是否参与由此产生的提权路径。

`UseSandboxieUAC=n` 不能替代 `NoUACProxy=y`：前者只跳过增强提示，后者跳过 Sandboxie 受支持的 RPC 提权拦截。

<div id="applying-changes"></div>

## 应用更改

RPC 钩子会为每个相关请求读取 **NoUACProxy**。配置保存并重新加载后，已在运行的进程中的后续请求会使用新的生效值；通常不需要重启进程、SandMan、SbieSvc 或驱动程序。正在进行的请求不会被追溯更改。

<div id="version-history"></div>

## 版本历史

`NoUACProxy` 及其附带的模板在 Sandboxie Plus 1.0.4 / Classic 5.55.4 中引入。

<div id="related-pages"></div>

## 相关页面

* [Apply ElevateCreateProcess Fix](ApplyElevateCreateProcessFix.md)
* [无安全隔离](NoSecurityIsolation.md)
* [Sandboxie Ini](SandboxieIni.md)
* [使用 Sandboxie UAC](UseSandboxieUAC.md)
