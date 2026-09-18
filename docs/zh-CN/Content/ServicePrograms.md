# 服务程序

### 概览

Windows 计算机包含若干设计用于接受应用程序请求的服务程序。许多服务程序在特殊的 _svchost.exe_ 进程（程序）内运行，不过也有一些作为独立进程运行。

由于沙盒的隔离，在 Sandboxie 下运行的程序不允许访问这些系统服务程序。相反，Sandboxie 提供自己的服务程序，它们与请求服务的程序运行在同一个沙盒中。

Sandboxie 服务程序按需启动。如果在任何给定时刻下列服务程序有未在运行的，这不是错误或问题。

* * *

### 远程过程调用（RPC）

```
    程序名称：SandboxieRpcSs.exe
    服务名称：rpcss
```

组件对象模型（COM）主服务。此服务向沙盒中的应用程序提供广泛的服务，包括一个应用程序启动另一个应用程序的机制。根据你沙盒化运行的程序，此服务可能需要也可能不需要启动。

此服务与 _DCOM 服务器进程启动器_（见下文）一起，使其他服务程序得以在沙盒中启动。

* * *

### DCOM 服务器进程启动器

```
    程序名称：SandboxieDcomLaunch.exe
    服务名称：dcomlaunch
```

此服务与_远程过程调用（RPC）_（见上文）一起，使其他服务程序得以在沙盒中启动。

注意：此服务在 Windows XP Service Pack 2 及更高版本的操作系统上可用。

* * *

### 加密服务

```
    程序名称：SandboxieCrypto.exe
    服务名称：cryptsvc
```

管理软件签名、安全证书和软件目录。此服务在沙盒中管理和存储由同一沙盒中运行的其他程序安装的任何数字证书或目录信息。

此服务偶尔会连接到互联网地址 _mscrl.microsoft.com_。此连接由运行在 SandboxieCrypto.exe 内的 Microsoft 代码发起，是验证或撤销网站和程序数字证书流程的一部分。

此连接并非 _SandboxieCrypto.exe_ 独有，运行在某个 _svchost.exe_ 进程下的“真正”服务程序也会发起。可以通过 [限制 > 互联网访问](RestrictionsSettings.md#互联网访问) 或防火墙阻止此连接。但这样做并不推荐。更多关于证书撤销的信息，请参阅 [维基百科上的证书撤销列表](https://en.wikipedia.org/wiki/Certificate_revocation_list)。

* * *

### 后台智能传输服务

```
    程序名称：SandboxieBITS.exe
    服务名称：bits
```

代表发出请求的应用程序在后台下载文件。某些安装程序（最常见的是 Microsoft 和 Google 产品）会请求此服务代表它们下载额外的资源文件。此服务把这些文件下载到沙盒中。

* * *

### 自动更新

```
    程序名称：SandboxieWUAU.exe
    服务名称：wuauserv
```

检查 Windows 更新并使用_后台智能传输服务_（见上文）下载它们。一旦更新被下载到沙盒中，此服务会尝试把它们安装到沙盒中。注意：在某些情况下，Windows 更新涉及修改核心系统文件。在 Sandboxie 的监管下进行此类修改可能失败或没有效果。

* * *

### Windows 安装程序

```
    程序名称：msiexec.exe
    服务名称：msiserver
```

安装使用 Windows Installer 技术准备的软件包。软件将被安装到沙盒中。在软件安装期间，通常会看到多个 _msiexec.exe_ 实例启动和停止。
