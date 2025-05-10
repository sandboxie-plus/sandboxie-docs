# 来自沙盒的消息

每当沙盒日志记录至少一条错误或信息消息时，_来自沙盒的消息_ 窗口会自动显示。（关于沙盒消息的更多信息，请参见 [SBIE 消息](SBIEMessages.md)）。

该窗口每行显示一条消息，如下图所示。

![](../Media/MessagesFromSandboxie.png)

点击 _帮助_ 按钮会打开网页浏览器，并跳转到所选消息的文档页面。

点击 _隐藏_ 按钮表示你不希望再次收到该消息。如果该消息包含信息详情，_隐藏_ 按钮仅会针对该特定详情隐藏消息。

例如，上图所示的 [SBIE1304](SBIE1304.md) 消息详细信息为 _osk.exe_。在此情况下，_隐藏_ 按钮将隐藏所有与 _osk.exe_ 相关的 [SBIE1304](SBIE1304.md) 后续消息。如果某一条 [SBIE1304](SBIE1304.md) 消息出现在其他程序名下，则仍然会显示出来。

点击 _关闭_ 按钮可关闭该窗口。

## 记录日志消息到文件

可以通过在注册表中的简单配置，将 _来自沙盒的消息_ 日志记录到文件：

```cmd
reg.exe add "HKLM\SYSTEM\CurrentControlSet\Services\SbieSvc" /t REG_SZ /v LogFile /d "2;C:\Windows\System32\LogFiles\Sandboxie.log" /f
```

`LogFile` 值包含两部分信息：

- `2` 是日志级别。只允许两个值：`2`（经典日志）或 `3`（包含进程 SID 的日志）
- `C:\Windows\System32\LogFiles\Sandboxie.log` 是日志的完整路径

日志级别为 2 时的输出示例：
```
2022-09-02 01:04:18 SBIE1308 Program cannot start due to restrictions - powershell.exe [ChromeBox]
2022-09-02 01:04:18 SBIE1308 Program cannot start due to restrictions - powershell.exe [ChromeBox]
2022-09-02 01:04:18 SBIE1308 Program cannot start due to restrictions - HelpPane.exe [ChromeBox]
```

自 1.3.3 / 5.58.3 版本起，可以通过详细模式输出日志，以显示目标进程所用账户的 SID。

日志级别为 3 时的输出示例：
```
2022-09-02 01:04:18 SBIE1308 Program cannot start due to restrictions - powershell.exe [ChromeBox] (DESKTOP-RZ4242\administrator)
2022-09-02 01:04:18 SBIE1308 Program cannot start due to restrictions - powershell.exe [ChromeBox] (DESKTOP-RZ4242\administrator)
2022-09-02 01:04:18 SBIE1308 Program cannot start due to restrictions - HelpPane.exe [ChromeBox] (DESKTOP-RZ4242\administrator)
```

另一个注册表键可用于对特定消息进行过滤与分日志：

```cmd
reg.exe add "HKLM\SYSTEM\CurrentControlSet\Services\SbieSvc" /t REG_SZ /v LogFile /d "2;C:\Windows\System32\LogFiles\Sandboxie.log" /f
reg.exe add "HKLM\SYSTEM\CurrentControlSet\Services\SbieSvc" /t REG_SZ /v MultiLog /d "1308,1307" /f
```

此简单配置将会：

- 无筛选地将所有日志输出到 `C:\Windows\System32\LogFiles\Sandboxie.log`
- 针对事件 1308 和 1307，为每个沙箱单独创建一个文件（如：`C:\Windows\System32\LogFiles\Sandboxie_DefaultBox.log`），日志中只包含这两类事件