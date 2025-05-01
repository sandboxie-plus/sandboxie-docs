# SbieCtrl_HideMessage

SbieCtrl_HideMessage 是 [Sandboxie 配置文件](SandboxieIni.md) 中的一项用户设置。它指定了哪些 [SBIE 消息](SBIEMessages.md) 不应弹出显示。
```
   .
   .
   .
   [UserSettings_054A02CE]
   SbieCtrl_HideMessage=1101
   SbieCtrl_HideMessage=1102,Example Message
```

第一个参数是必需的，它指定了要隐藏的 _SBIE 消息_ 的 ID 号。

第二个参数是可选的。如果在 Sandboxie Plus 中指定了该参数，则仅隐藏与指定文本匹配的消息；否则，将隐藏该消息的所有出现情况。

相关的 Sandboxie Plus 设置：全局设置 > 常规配置 > 通知 > SBIE 消息

相关的 [Sandboxie 控制](SandboxieControl.md) 设置：[来自 Sandboxie 的消息](MessagesFromSandboxie.md) 弹出窗口
