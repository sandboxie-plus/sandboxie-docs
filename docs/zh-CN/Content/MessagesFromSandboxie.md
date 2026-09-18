# 来自 Sandboxie 的消息

每当 Sandboxie 记录至少一条错误或信息性消息时，_来自 Sandboxie 的消息_窗口会自动显示。（关于 Sandboxie 消息的更多信息，参见 [SBIE 消息](SBIEMessages.md)。）

该窗口每行显示一条消息，如下例所示。

![](../Media/MessagesFromSandboxie.png)

点击 _帮助_ 按钮会打开网页浏览器，并导航到高亮消息的文档页面。

点击 _隐藏_ 按钮表示你不想再收到此消息。如果消息包含信息详情，_隐藏_ 按钮只会结合该特定详情隐藏消息。

例如，上面显示的 [SBIE1304](SBIE1304.md) 消息带有详情 _osk.exe_。在这种情况下，_隐藏_ 按钮将隐藏 [SBIE1304](SBIE1304.md) 针对 _osk.exe_ 的未来出现。如果 [SBIE1304](SBIE1304.md) 因其他程序名称而发出，它仍会显示。

点击 _关闭_ 按钮关闭窗口。

## 将消息记录到文件

可以通过注册表中的简单配置，把_来自 Sandboxie 的消息_记录到文件：
```cmd
reg.exe add "HKLM\SYSTEM\CurrentControlSet\Services\SbieSvc" /t REG_SZ /v LogFile /d "2;C:\Windows\System32\LogFiles\Sandboxie.log" /f
```
`LogFile` 值包含两部分信息：

- `2` 是日志级别。只有两个值是正确的：`2`（经典日志）或 `3`（带进程 SID 的日志）
- `C:\Windows\System32\LogFiles\Sandboxie.log` 是日志的完整路径

日志级别为 2 时的输出示例：
```
2022-09-02 01:04:18 SBIE1308 Program cannot start due to restrictions - powershell.exe [ChromeBox]
2022-09-02 01:04:18 SBIE1308 Program cannot start due to restrictions - powershell.exe [ChromeBox]
2022-09-02 01:04:18 SBIE1308 Program cannot start due to restrictions - HelpPane.exe [ChromeBox]
```

自版本 1.3.3 / 5.58.3 起，可以传递详细模式日志以获取目标进程所用帐户的 SID。

日志级别为 3 时的输出示例：
```
2022-09-02 01:04:18 SBIE1308 Program cannot start due to restrictions - powershell.exe [ChromeBox] (DESKTOP-RZ4242\administrator)
2022-09-02 01:04:18 SBIE1308 Program cannot start due to restrictions - powershell.exe [ChromeBox] (DESKTOP-RZ4242\administrator)
2022-09-02 01:04:18 SBIE1308 Program cannot start due to restrictions - HelpPane.exe [ChromeBox] (DESKTOP-RZ4242\administrator)
```

另一个注册表项允许按特定消息过滤和拆分日志：
```cmd
reg.exe add "HKLM\SYSTEM\CurrentControlSet\Services\SbieSvc" /t REG_SZ /v LogFile /d "2;C:\Windows\System32\LogFiles\Sandboxie.log" /f
reg.exe add "HKLM\SYSTEM\CurrentControlSet\Services\SbieSvc" /t REG_SZ /v MultiLog /d "1308,1307" /f
```
这个简单配置将：

- 把所有未过滤的日志放入 `C:\Windows\System32\LogFiles\Sandboxie.log`
- _按沙盒各创建一个文件_（例如：`C:\Windows\System32\LogFiles\Sandboxie_DefaultBox.log`），其中只包含事件 1308 和 1307
