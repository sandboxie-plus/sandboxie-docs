# Config Level

**Note: In versions of Sandboxie before 3, ConfigLevel was a global setting in the [GlobalSettings] section. The global ConfigLevel setting is no longer used, and is ignored if it exists in the configuration file.**

_ConfigLevel_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It is used by [Sandboxie Control](SandboxieControl.md) to manage default configuration for a sandbox.

When ConfigLevel is missing, not a number, or a number below 2, Sandboxie Control will add the following configuration to the sandbox:

***

ConfigLevel=2
[AutoRecover](AutoRecover.md)=yes
[AutoRecoverIgnore](AutoRecoverIgnore.md)=.part
[AutoRecoverIgnore](AutoRecoverIgnore.md)=.jc!
[RecoverFolder](RecoverFolder.md)=%Desktop%
[RecoverFolder](RecoverFolder.md)=%Favorites%
[RecoverFolder](RecoverFolder.md)=%Personal%
[LingerProcess](LingerProcess.md)=acrord32.exe
[LingerProcess](LingerProcess.md)=jusched.exe
[LingerProcess](LingerProcess.md)=syncor.exe
[LingerProcess](LingerProcess.md)=devldr32.exe

***

In the future, more configuration levels may be added.
