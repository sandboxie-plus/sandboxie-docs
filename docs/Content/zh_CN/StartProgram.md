# 启动程序

_StartProgram_ 是 [Sandboxie 配置文件](SandboxieIni.md)中的一项沙箱设置。它用于自动启动指定的程序。例如：

```
   .
   .
   .
   [DefaultBox]
   StartProgram=%ProgramFiles%\Google\Chrome\Application\chrome.exe
```

此示例指定谷歌浏览器（chrome.exe）将被强制在名为 _DefaultBox_ 的沙箱中运行。

**技术细节**

_StartProgram_ 由 [SandboxieRpcSs](ServicePrograms.md#远程过程调用-rpc) 处理，该服务在每个沙箱中仅运行一次。与 [AutoExec](AutoExec.md) 设置类似，它会在沙箱中第一个程序开始运行时进行处理。请注意，如果支持的话，_StartProgram_ 会以隐藏模式启动指定的应用程序。

有关服务的设置，请参阅 [StartService](StartService.md)。
