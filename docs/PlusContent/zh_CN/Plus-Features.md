Sandboxie Plus用户界面提供了众多新功能，这些功能提升了安全性、兼容性和整体沙箱化体验。

然而，其中一些功能（*）仅对拥有[支持证书](../PlusContent/zh_CN/supporter-certificate.md)的用户可用，该证书可通过[为Sandboxie项目做出贡献](https://github.com/sandboxie-plus/Sandboxie/blob/master/CONTRIBUTING.md)获得，也可在我们的[在线商店](https://xanasoft.com/shop/)购买。

还有一些功能（**）对[Sandboxie-Insider](../PlusContent/zh_CN/Sandboxie-Insider.md)计划的参与者可用。

#### [规则特异性](../PlusContent/zh_CN/RuleSpecificity.md) *
 - 使用此选项，规则将根据其特异性进行优先级排序（详情请参阅更新日志/文档），这样子路径可以可读/可写，而父路径仍受保护。

#### [安全增强型沙箱](../PlusContent/zh_CN/security-mode.md) *
 - 将系统调用提升限制为经批准的已知安全/过滤后的系统调用
 - 将对设备端点的访问限制为已知安全/过滤后的端点

#### [隐私增强型沙箱](../PlusContent/zh_CN/privacy-mode.md) *
 - 通过此功能，应用预设规则集后，所有可能包含个人数据的位置都可以得到保护。在启用个人数据保护的沙箱中运行的应用程序将看到一台没有用户数据的空PC。

#### [隔离模式](../PlusContent/zh_CN/compartment-mode.md) *
 - 此模式旨在以牺牲安全性为代价来优化兼容性，这里不使用Sandboxie基于令牌的隔离方案。隔离仅限于文件系统微型过滤器以及注册表和对象回调。这有可能极大地提高与各种应用程序的兼容性。

#### 虚拟磁盘集成 **
 - [内存盘支持](../PlusContent/zh_CN/RamDiskSupport.md)，自最新的内部版本起可用，允许您使用ImDisk驱动程序在系统内存中创建虚拟磁盘，这可以加快文件访问速度并提高保密性，因为当磁盘卸载（手动或在重启时自动卸载）时，所有沙箱内容都将被丢弃。
 - [加密沙箱镜像支持](../PlusContent/zh_CN/BoxEncryption.md)目前正在开发中，允许您创建加密的沙箱环境，以进一步保护您的机密数据。使用此功能时，沙箱文件根目录将从AES - XTS加密的沙箱镜像中挂载，也支持其他加密算法。此核心功能即将增加的功能包括安全的沙箱密码处理以及驱动程序扩展，以防止未在加密沙箱中运行的应用程序访问沙箱文件。

#### 增强的网络过滤和重定向 **
 - [代理注入](../PlusContent/zh_CN/ProxySupport.md)是内部版本中新增的另一项功能，它允许强制任何应用程序使用Socks 5代理而不是直接连接。
 - [DNS查询日志记录、过滤和重定向](../PlusContent/zh_CN/DNSFilter.md)功能允许您阻止或重定向沙箱程序针对选定域名发出的DNS查询。

#### [WFP（Windows过滤平台）支持](../PlusContent/zh_CN/WFPSupport.md)
 - 有了这个功能，Sandboxie可以像一个应用程序防火墙一样，按每个沙箱应用规则，允许同一个应用程序在一个沙箱中访问互联网，而在另一个沙箱中阻止访问。

#### Windows 11上下文菜单集成

#### 进程/线程句柄过滤（obCallbacks）
 - 使用此机制可大大改善进程的隔离性，并提供增强的安全性。

#### Win32系统调用挂钩
 - 有了这个功能，Win32系统调用可以得到与NT系统调用相同的处理，这有助于图形和硬件加速。

#### 带有黑暗模式等更多功能的新用户界面
 - Sandboxie - Plus带来了一个全新的基于Qt的用户界面sandman.exe
 - 每个沙箱可定制的运行菜单
 - 终止所有沙箱的全局热键
 - 用于轻松配置高级选项的INI部分编辑器
 - 沙箱事件触发器/脚本
 - 无论沙箱预设如何，都能阻止选定的应用程序全局运行

#### [快照](../PlusContent/zh_CN/BoxSnapshots.md)
 - Sandboxie - Plus可以创建沙箱快照，使用这些快照可以轻松将沙箱恢复到定义的先前状态。
 - 设置为自动删除的沙箱在可用时将自动恢复到最后一个快照，这样每次都能受益于一个全新干净的沙箱，但带有一些预设配置

#### [增强的调试/跟踪监视器](../PlusContent/zh_CN/TraceLog.md)

#### 虚假管理员权限
 - 允许使沙箱中的所有进程认为它们具有管理员权限并相应地运行，而不会有授予它们管理员权限的潜在弊端

#### 沙箱大小监视器
 - 在单独的列中监视和列出沙箱大小

#### 开始菜单集成
 - 将沙箱中的开始菜单条目集成到主机开始菜单中

#### 沙箱SID隔离
 - 不使用匿名登录SID，而是为每个沙箱使用自定义SID，如Sandboxie/DefaultBox。这样，来自不同沙箱的进程将无法访问彼此的资源。

#### [突破进程](../Content/zh_CN/BreakoutProcess.md)
 - 允许指定在沙箱内启动时哪些应用程序应在沙箱外运行。将此功能与ForceProcess结合使用可实现一个简单的优先级系统。
 - [文档突破](../Content/zh_CN/BreakoutDocument.md)是对已广为人知的突破机制的扩展，允许在沙箱内将选定的文件类型保存到开放文件路径后，在关联应用程序的非沙箱实例中打开这些文件。  **

#### [USB驱动器沙箱化](../PlusContent/zh_CN/USBSandboxing.md) **
 - 此功能允许您自动对插入计算机的任何USB驱动器进行沙箱化，这为您的系统增加了一层额外的保护。

#### EFS支持 **
 - 支持EFS（加密文件系统）保护的文件。

#### Windows 11的ARM64支持 *
 - 原生支持ARM64
 - 支持模拟的x86
 - 支持模拟的x64（ARM64EC）