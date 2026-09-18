# 删除命令

删除命令是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定用于物理删除沙盒内容的命令。其主要目的是让第三方安全删除工具能够接入 Sandboxie。参见 [安全删除沙盒](SecureDeleteSandbox.md)。

用法：
```
   .
   .
   .
   [DefaultBox]
   DeleteCommand=%SystemRoot%\System32\cmd.exe /c RMDIR /s /q "%SANDBOX%"
```

此示例是未显式指定删除命令时使用的默认设置，它调用 Windows RMDIR 命令删除沙盒文件夹。

更多示例参见 [安全删除沙盒](SecureDeleteSandbox.md)。

***

指定此设置时，务必在命令中包含 **"%SANDBOX%"**（带引号）。

***

注意：安全删除是隐私措施，而非安全措施。常规删除和安全删除都能有效移除收集到沙盒中的不需要的软件。参见 [安全删除沙盒](SecureDeleteSandbox.md)。

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 删除 > 命令](DeleteSettings.md#命令)
