# Service Programs


### Overview

A Windows computers includes several service programs which are designed to accept requests from application programs. Many service programs run inside special _svchost.exe_ processes (programs), although some others run as standalone processes.

Programs running under Sandboxie are not allowed to reach those system service programs, due to the isolation of the sandbox. Instead, Sandboxie provides its own service programs, which run in the same sandbox as the program requesting the service.

The Sandboxie service programs are started on demand. It is not an error or a problem if any of the service programs listed below are not running at any given moment.

* * *

### Remote Procedure Call (RPC)
```
    Program Name:  SandboxieRpcSs.exe
    Service Name:  rpcss
```

The Component Object Model (COM) main service. This service provides a wide range of services to applications in the sandbox, including mechanisms for one application to start another application. Depending on the programs you run sandboxed, the service may or may not need to start.

This service, along with the _DCOM Server Process Launcher_ (see below) makes it possible for other service programs to start in the sandbox.

* * *

### DCOM Server Process Launcher
```
    Program Name:  SandboxieDcomLaunch.exe
    Service Name:  dcomlaunch
```

This service, along with the _Remote Procedure Call (RPC)_ (see above) makes it possible for other service programs to start in the sandbox.

Note that this service is available on Windows XP Service Pack 2 and later operating systems.

* * *

### Cryptographic Services
```
    Program Name:  SandboxieCrypto.exe
    Service Name:  cryptsvc
```

Manages software signing, security certificates and software catalogs.. This service manages and stores in the sandbox any digital certificates or catalog information that was installed by other programs running in the same sandbox.

This service occasionally connects to the Internet address _mscrl.microsoft.com_. This connection is initiated by Microsoft code running within SandboxieCrypto.exe and it is part of the procedure which verifies or revokes digital certificates for Web sites and programs.

This connection is not unique to _SandboxieCrypto.exe_ and is initiated also by the "real" service program running under one of the _svchost.exe_ processes. It is possible to block this connection through [Restrictions > Internet Access](RestrictionsSettings.md#internet-access) or through a firewall. However, this is not recommended. Please see [Certificate revocation list on Wikipedia](https://en.wikipedia.org/wiki/Certificate_revocation_list) for more information about certificate revocation.

* * *

### Background Intelligent Transfer Service
```
    Program Name:  SandboxieBITS.exe
    Service Name:  bits
```

Downloads files in the background on behalf of a requesting applications. Some installation programs (most commonly for Microsoft and Google products) ask this service to download additional resource files on their behalf. The service downloads these files into the sandbox.

* * *

### Automatic Updates
```
    Program Name:  SandboxieWUAU.exe
    Service Name:  wuauserv
```

Checks for Windows updates and downloads them using the _Background Intelligent Transfer Service_ (see above). Once the updates are downloaded into the sandbox, this service will try to install them into the sandbox. Note that in some cases, updates to Windows involve the modification of core system files. Such modification might fail or have no effect, when carried out under the supervision of Sandboxie.

* * *

### Windows Installer
```
    Program Name:  msiexec.exe
    Service Name:  msiserver
```

Installs software packages that were prepared using Windows Installer technology. The software will be installed into the sandbox. It is typical to see several instances of _msiexec.exe_ start and stop during software installation.
