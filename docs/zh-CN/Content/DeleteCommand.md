# 删除命令

DeleteCommand 是 [Sandboxie Ini](SandboxieIni.md) 文件中的一个沙箱设置项。它用于指定物理删除沙箱内容的命令。其主要目的是使用户能够将第三方安全删除工具集成到 Sandboxie 中。详见 [安全删除沙箱](SecureDeleteSandbox.md)。

用法：
```
   .
   .
   .
   [DefaultBox]
   DeleteCommand=%SystemRoot%\System32\cmd.exe /c RMDIR /s /q "%SANDBOX%"
```

上述示例是 DeleteCommand 未被明确指定时的默认设置，调用了 Windows 的 RMDIR 命令来移除沙箱文件夹。

更多示例，请参见 [安全删除沙箱](SecureDeleteSandbox.md)。

***

在指定此设置时，请确保在命令中包含 **"%SANDBOX%"**（包括引号）。

***

注意：安全删除是一项隐私措施，而非安全措施。无论是常规删除还是安全删除，实际上都可以有效移除收集到沙箱中的不需要的软件。详见 [安全删除沙箱](SecureDeleteSandbox.md)。

相关的 [沙箱控制](SandboxieControl.md) 设置项：[沙箱设置 > 删除 > 命令](DeleteSettings.md#command)