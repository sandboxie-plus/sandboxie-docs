# Resource Access

In Sandboxie, various [Resource Access Settings](ResourceAccessSettings.md) apply only to programs installed outside of Sandboxie, as not to be bypassed by sandboxed programs changing their exe name. The following table shows which settings apply to what installation locations.



|                 | Outside | Inside |
|-----------------|---------|--------|
|[ClosedFilePath](ClosedFilePath.md)   | Yes     | Yes    |
|[ClosedIpcPath](ClosedIpcPath.md)    | Yes     | Yes    |
|[ClosedKeyPath](ClosedKeyPath.md)    | Yes     | Yes    |
|[OpenClsid](OpenClsid.md)        | Yes     | Yes    |
|[OpenFilePath](OpenFilePath.md)     | Yes     | No       |
|[OpenIpcPath](OpenIpcPath.md)      | Yes     | Yes      |
|[OpenKeyPath](OpenKeyPath.md)      | Yes     | No       |
|[OpenPipePath](OpenPipePath.md)     | Yes     | Yes    |
|[OpenWinClass](OpenWinClass.md)     | Yes     | Yes    |


Note that all `Close...=!<program>,...` excludes only programs from outside the sandbox.
