# SbieCtrl_HideMessage

SbieCtrl_HideMessage は [Sandboxie Ini](SandboxieIni.md) のユーザー設定です。ポップアップから非表示にすべき [SBIE Messages](SBIEMessages.md) を指定します。

```
   .
   .
   .
   [UserSettings_054A02CE]
   SbieCtrl_HideMessage=1101
   SbieCtrl_HideMessage=1102,Example Message
```

最初のパラメーターは必須で、非表示にする _SBIE Messages_ の ID 番号を指定します。

2 番目のパラメーターはオプションです。Sandboxie Plus で指定された場合、テキストに一致するメッセージのみが非表示になり、それ以外の場合はメッセージのすべての出現が非表示になります。

関連する Sandboxie Plus 設定: Global Settings > General Config > Notifications > SBIE Messages

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Messages From Sandboxie](MessagesFromSandboxie.md) ポップアップ ウィンドウ
