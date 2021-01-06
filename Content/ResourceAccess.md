# Resource Access

In sandboxie various [Resource Access settings](ResourceAccesssettings) apply only to programs installed outside of sandboxie as not to be bypassed by sandboxed programs changing their exe name. The following table shows which settings apply to what installation locations.



|                 | Outside | Inside |
|-----------------|---------|--------|
|[ClosedFilePath](ClosedFilePath)   | Yes     | Yes    |
|[ClosedIpcPath](ClosedIpcPath)    | Yes     | Yes    |
|[ClosedKeyPath](ClosedKeyPath)    | Yes     | Yes    |
|[OpenClsid](OpenClsid)        | Yes     | Yes    |
|[OpenFilePath](OpenFilePath)     | Yes     | No       |
|[OpenIpcPath](OpenIpcPath)      | Yes     | Yes      |
|[OpenKeyPath](OpenKeyPath)      | Yes     | No       |
|[OpenPipePath](OpenPipePath)     | Yes     | Yes    |
|[OpenWinClass](OpenWinClass)     | Yes     | Yes    |


Note that all `Close...=!<program>,...` excludes only programs from outside the sandbox.