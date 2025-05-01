Sandboxie Plus 用户界面提供了许多全新的功能，以提升安全性、兼容性以及整体沙箱体验。

然而，其中部分功能（*）仅对拥有[支持证书](../PlusContent/supporter-certificate.md)的用户开放。您可以通过[为 Sandboxie 项目做贡献](https://github.com/sandboxie-plus/Sandboxie/blob/master/CONTRIBUTING.md)或在我们的[在线商城](https://xanasoft.com/shop/)购买支持证书。
<!-- https://github.com/sandboxie-plus/Sandboxie/blob/master/CONTRIBUTING.md 贡献者证书文档没有翻译，故没有修改md文件指向。等待后续翻译后，重新指定 -->


另外，还有部分功能（**）向 [Sandboxie-Insider](../PlusContent/Sandboxie-Insider.md) 计划的参与者开放。


#### [规则特异性](../PlusContent/RuleSpecificity.md) *
 - 启用此选项后，规则会根据其特异性优先排序（详细内容请参考更新日志/文档）。这样可以允许子路径具有可读写权限，而父路径依然受到保护


#### [安全增强沙箱](../PlusContent/security-mode.md) *
 - 将系统调用权限提升限制为已批准的安全或经过筛选的系统调用
 - 将设备端点访问权限限制为已知安全或经过筛选的端点


#### [隐私增强沙箱](../PlusContent/privacy-mode.md) *
- 启用此功能后，通过应用预设规则集，可以保护所有可能包含个人数据的位置。在启用个人数据保护的沙箱中运行的应用程序将只能看到一台没有任何用户数据的空白电脑


#### [隔离模式](../PlusContent/compartment-mode.md) *
- 此模式旨在以牺牲安全性为代价优化兼容性，在该模式下，Sandboxie 的基于令牌的隔离方案不会被使用。隔离仅限于文件系统迷你过滤器，以及注册表和对象回调机制。该方式有可能显著提升与各种应用程序的兼容性


#### 虚拟磁盘集成 **
- [RamDisk 支持](../PlusContent/RamDiskSupport.md)自最新 Insider 版本起可用，允许你通过 ImDisk 驱动在系统内存中创建虚拟磁盘，这样可以加快文件访问速度，并增加机密性，因为所有沙箱内容将在磁盘卸载时（无论是手动还是重启时自动）被清除
- [加密沙箱镜像支持](../PlusContent/BoxEncryption.md)目前仍在开发中，可让你为机密数据创建加密的沙箱环境，进一步提升保护。这项功能会将沙箱文件根目录从 AES-XTS 加密的盒镜像挂载，此外也支持其他加密算法。即将推出的功能还包括安全的盒口令处理，以及驱动扩展功能，防止未在加密沙箱内运行的应用程序访问沙箱文件


#### 增强的网络过滤与重定向 **
 - [代理注入](../PlusContent/ProxySupport.md) 是在内部版本中新增的一项功能，它允许强制任何应用程序使用 Socks5 代理，而非直接连接
 - [DNS 查询日志记录、过滤与重定向](../PlusContent/DNSFilter.md) 功能允许你针对选定域名，阻止或重定向由沙箱程序发起的 DNS 查询


#### [WFP (Windows Filtering Platform) 支持](../PlusContent/WFPSupport.md)
 - 通过此功能，Sandboxie 可以像一个应用防火墙一样，在每个沙箱级别应用规则，从而允许相同的应用程序在某个沙箱中访问互联网，同时在另一个沙箱中阻止其访问


#### 集成 Windows 11 右键菜单


#### 进程/线程句柄过滤（obCallbacks）
- 利用此机制能够大幅提升进程的隔离性，并提供更高级别的安全防护


#### Win32 系统调用钩子
- 启用此特性后，Win32 系统调用能够与 NT 系统调用同样进行处理，有助于图形和硬件加速


#### 新 UI 及暗黑模式等更多功能
- Sandboxie-Plus 带来了全新的基于 Qt 的界面 sandman.exe
- 每个沙箱可自定义运行菜单
- 全局热键可终止所有沙箱
- INI 分区编辑器便于高级选项配置
- 沙箱事件触发器/脚本
- 能够全局阻止选定应用运行，无论沙箱预设如何


#### [快照功能](../PlusContent/BoxSnapshots.md)
- Sandboxie-Plus 可以创建沙箱快照，使用户能够轻松将沙箱恢复到指定的先前状态
- 设置为自动删除的沙箱，在可用时会自动还原到最近一次快照，从而每次都可获得全新干净但带有部分预设配置的沙箱


#### [增强的调试/追踪监控器](../PlusContent/TraceLog.md)


#### 虚拟管理员权限
 - 允许沙箱中的所有进程认为自己拥有管理员权限并据此运行，但不会带来实际授予管理员权限的潜在风险


#### 沙箱空间占用监视
 - 在独立列中监控并列出沙箱的空间占用情况


#### 开始菜单集成
 - 将来自沙箱的开始菜单条目集成到主机的开始菜单中


#### 沙箱 SID 隔离
 - 不再使用匿名登录 SID，而是为每个沙箱（如 Sandboxie/DefaultBox）分配自定义 SID，这样，来自不同沙箱的进程将无法访问彼此的资源


#### [分离进程](../Content/BreakoutProcess.md)
- 允许指定哪些应用程序在沙箱内启动时可以以非沙箱模式运行。将此功能与 强制进程 结合使用，可以实现一个简单的优先级系统
- [分离文档](../Content/BreakoutDocument.md) 是对已有的分离机制的扩展，允许在沙箱内将已保存到开放文件路径的特定文件类型，通过与其相关联的应用程序，以非沙箱实例打开


#### [USB 驱动器沙箱化](../PlusContent/USBSandboxing.md)
- 此功能允许您在将任何 USB 驱动器插入计算机时，自动对其进行沙箱化，从而为您的系统增加一层额外的保护


#### EFS 支持 **
 - 支持受 EFS（加密文件系统）保护的文件


#### Windows 11 的 ARM64 支持 *
 - 原生支持 ARM64
 - 支持 x86 仿真
 - 支持 x64 仿真（ARM64EC）
