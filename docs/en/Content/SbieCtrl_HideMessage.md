# SbieCtrl_HideMessage

SbieCtrl_HideMessage is a user setting in [Sandboxie Ini](SandboxieIni.md). It specifies which of the [SBIE Messages](SBIEMessages.md) should be hidden from popping up.

```
   .
   .
   .
   [UserSettings_054A02CE]
   SbieCtrl_HideMessage=1101
   SbieCtrl_HideMessage=1102,Example Message
```

The first parameter is mandatory and specifies the ID number of the _SBIE Messages_ to be hidden.

The second parameter is optional. If specified in Sandboxie Plus, only messages that match the text will be hidden, otherwise all occurrences of the message will be hidden.

Related Sandboxie Plus setting: Global Settings > General Config > Notifications > SBIE Messages

Related [Sandboxie Control](SandboxieControl.md) setting: [Messages From Sandboxie](MessagesFromSandboxie.md) pop-up window
