# 安全删除沙箱

典型的文件删除操作会使操作系统和程序无法访问数据，但数据实际上并未从硬盘存储介质中物理擦除，数据恢复技术人员仍有可能恢复这些数据。为了增加数据恢复的难度，存在一些第三方软件可以执行“安全删除”操作。这通常是通过在删除数据之前多次覆盖数据来实现的。

更多信息，请参阅[维基百科上的数据残留](https://en.wikipedia.org/wiki/Data_remanence)。

默认情况下，Sandboxie 使用标准的 Windows 命令（_RMDIR_）来删除沙箱。这确保了沙箱的内容（包括恶意软件）能从操作系统中正确移除。但如上所述，这会使数据容易被取证专家检查和恢复。

担心敏感数据隐私的用户可以将第三方安全删除工具集成到 Sandboxie 中，以替代标准的删除命令。

您可以通过 Sandboxie 控制界面或手动编辑 [Sandboxie 配置文件](SandboxieIni.md) 来配置自定义删除命令。

**在 Sandboxie 控制界面中**

使用 [沙箱设置 > 删除 > 命令](DeleteSettings.md#command)。以下是一些删除命令的示例：

* 调用 [Heidi Computers 公司的 Eraser](https://eraser.heidi.ie/) 来安全删除内容：
```
    %SystemRoot%\System32\eraserl.exe -folder "%SANDBOX%" -subfolders -method DoD_E -resultsonerror -queue
```

* 调用 [SysInternals/Microsoft 公司的 SDelete](https://technet.microsoft.com/en-us/sysinternals/bb897443.aspx) 来安全删除内容。
```
    "C:\Program Files\Sysinternals\SDelete\sdelete.exe" -p 3 -s -q "%SANDBOX%"
```

**在 Sandboxie.ini 配置文件中**

要为特定沙箱配置自定义删除命令，请在 [Sandboxie 配置文件](SandboxieIni.md) 的沙箱部分编辑或插入 [DeleteCommand](DeleteCommand.md) 设置。

要配置全局自定义删除命令，请在 [Sandboxie 配置文件](SandboxieIni.md) 的 [GlobalSettings] 部分编辑或插入 [DeleteCommand](DeleteCommand.md) 设置。

指定此设置时，请确保在命令中包含 **"%SANDBOX%"**（带引号）。

在启动删除命令之前，Sandboxie 会扫描沙箱，以确保所有文件都能被正确删除，具体请参阅 [删除沙箱内容](StartCommandLine.md#delete-contents-of-sandbox)。

* * *

前往 [帮助主题](HelpTopics.md)。
