# SandboxieDrv 使用未公开的内核导出函数实现其令牌魔法

Sandboxie 通过让沙盒化进程以高度受限的主令牌运行来实现隔离。由于大多数应用程序无法以这种方式运行，它钩住所有 NTDLL.dll 调用，通过 SbieDrv 中的接口重定向它们。驱动程序随后可以检查调用参数，让调用线程模拟原始的未受限令牌，执行系统调用，并在把控制权返回用户模式前解除模拟。

这样，在 Sandboxie 监管下运行的进程无法使用原始令牌发出系统调用，即使它撤消了 ntdll.dll 的钩子。

为使此机制工作，Sandboxie 利用了几个未公开的操作：

1. 要创建受限令牌，它目前使用未导出的函数 SepFilterToken 以及若干偏移量（RestrictedSidCount、RestrictedSids、UserAndGroups、UserAndGroupCount）。
此机制可以改为调用 CreateToken 或 CreateTokenEx 来替代，但这些函数在内核中也没有导出。

为消除对未导出符号的依赖，这部分过程应导出并使用 ZwCreateTokenEx。

2. 为了能够代表沙盒化进程调用任何系统调用，驱动程序必须知道每个系统调用索引的函数地址和参数数量。
Sandboxie 目前通过分析 KeAddSystemServiceTable 函数来定位未导出的系统调用表地址。

为消除对未导出符号的依赖，需要导出 KeServiceDescriptorTableShadow。

3. 由于 PsImpersonateClient 的限制（从 Windows XP SP2 开始），需要以模拟级别 SecurityIdentification 调用它，然后在不透明的线程对象中把它改为 SecurityImpersonation。

为消除对未导出符号的依赖，需要提供一种有文档记录的机制，让驱动程序达到任何所需的模拟级别。

4. 要替换沙盒化进程的主令牌，需要清除 EPROCESS 结构中的 PrimaryTokenFrozen 位，此操作由向 PsSetLoadImageNotifyRoutine 注册的回调触发。

我没有调查在令牌被正式冻结之前进行令牌替换是否可行。

除上述基本依赖外，Sandboxie 还会从窗口站对象获取剪贴板对象，以调整所存储项目的完整性级别，使沙盒化应用程序可以访问它们。
