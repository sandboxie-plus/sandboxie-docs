# Config Level

**Note: In versions of Sandboxie before 3, ConfigLevel was a global setting in the [GlobalSettings] section. The global ConfigLevel setting is no longer used, and is ignored if it exists in the configuration file.**

_ConfigLevel_ is a sandbox setting in [Sandboxie Ini](SandboxieIni). It is used by [Sandboxie Control](SandboxieControl) to manage default configuration for a sandbox.

When ConfigLevel is missing, not a number, or a number below 2, Sandboxie Control will add the following configuration to the sandbox:

***

ConfigLevel=2
[AutoRecover](AutoRecover)=yes
[AutoRecoverIgnore](AutoRecoverIgnore)=.part
[AutoRecoverIgnore](AutoRecoverIgnore)=.jc!
[RecoverFolder](RecoverFolder)=%Desktop%
[RecoverFolder](RecoverFolder)=%Favorites%
[RecoverFolder](RecoverFolder)=%Personal%
[LingerProcess](LingerProcess)=acrord32.exe
[LingerProcess](LingerProcess)=jusched.exe
[LingerProcess](LingerProcess)=syncor.exe
[LingerProcess](LingerProcess)=devldr32.exe

***

In the future, more configuration levels may be added.
