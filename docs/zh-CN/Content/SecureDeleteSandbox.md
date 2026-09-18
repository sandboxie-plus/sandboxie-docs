# 安全删除沙盒

普通的文件删除会让操作系统和程序无法访问数据，但数据并未从硬盘存储介质上物理抹除，数据恢复技术人员仍可能将其找回。为了使这种恢复更加困难，市面上存在能够执行_安全删除_的第三方软件。其典型做法是在删除前多次覆写数据。

更多信息参见 [维基百科：数据残留](https://en.wikipedia.org/wiki/Data_remanence)。

默认情况下，Sandboxie 使用标准的 Windows 删除文件夹命令——_RMDIR_——来删除沙盒。这能确保沙盒的内容（包括恶意软件）被正确地从操作系统中移除。但如上所述，它仍会让数据暴露在取证专家的检查和恢复之下。

关注敏感数据隐私的用户，可以把第三方安全删除工具接入 Sandboxie，以替代标准命令。

你可以通过沙盒管理器配置自定义删除命令，也可以手动编辑 [Sandboxie Ini](SandboxieIni.md) 配置文件。

**在沙盒管理器中**

使用 [沙盒设置 > 删除 > 命令](DeleteSettings.md#命令)。下面是删除命令的两个示例：

* 调用 [Heidi Computers 的 Eraser](https://eraser.heidi.ie/) 安全删除内容：
```
    %SystemRoot%\System32\eraserl.exe -folder "%SANDBOX%" -subfolders -method DoD_E -resultsonerror -queue
```

* 调用 [SysInternals/Microsoft 的 SDelete](https://technet.microsoft.com/en-us/sysinternals/bb897443.aspx) 安全删除内容：
```
    "C:\Program Files\Sysinternals\SDelete\sdelete.exe" -p 3 -s -q "%SANDBOX%"
```

**在 Sandboxie.ini 配置文件中**

要为特定沙盒配置自定义删除命令，请在 [Sandboxie Ini](SandboxieIni.md) 的沙盒小节中编辑或插入 [删除命令](DeleteCommand.md) 设置。

要配置全局自定义删除命令，请在 [Sandboxie Ini](SandboxieIni.md) 的 [GlobalSettings] 小节中编辑或插入 [删除命令](DeleteCommand.md) 设置。

指定此设置时，务必在命令中包含 **"%SANDBOX%"**（带引号）。

在启动删除命令前，Sandboxie 会扫描沙盒，确保所有文件都能被正确删除，如 [删除沙盒内容](StartCommandLine.md#删除沙盒内容) 中所述。

* * *

跳转到 [帮助主题](HelpTopics.md)。
