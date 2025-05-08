# 删除命令

DeleteCommand 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定用于物理删除沙盒内容的命令。其主要目的是使第三方安全删除工具能够集成到 Sandboxie 中。参见 [安全删除沙盒](SecureDeleteSandbox.md)。

用法：
```
   .
   .
   .
   [DefaultBox]
   DeleteCommand=%SystemRoot%\System32\cmd.exe /c RMDIR /s /q "%SANDBOX%"
```

此示例是未明确指定 DeleteCommand 时使用的默认设置，它调用 Windows RMDIR 命令来删除沙盒文件夹。

更多示例，请参见 [安全删除沙盒](SecureDeleteSandbox.md)。

***

在指定此设置时，请确保在命令中包含 **"%SANDBOX%"**（带引号）。

***

注意：安全删除是一种隐私措施，而不是安全措施。常规删除和安全删除都能有效地移除收集到沙盒中的不需要的软件。参见 [安全删除沙盒](SecureDeleteSandbox.md)。

相关 [Sandboxie Control](SandboxieControl.md) 设置：[沙盒设置 > 删除 > 命令](DeleteSettings.md#command) 