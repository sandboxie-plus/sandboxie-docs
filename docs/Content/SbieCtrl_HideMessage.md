# SbieCtrl_HideMessage 

SbieCtrl_HideMessage is a user setting in [Sandboxie Ini](SandboxieIni.md). It specifies which of the SBIE messages should be hidden from popping up.

```
   .
   .
   .
   [UserSettings_054A02CE]
   SbieCtrl_HideMessage=1101
   SbieCtrl_HideMessage=1102,Example Message
```

The first parameter is mandatory, specifies the id of the SBIE Messages to be hidden.

The second parameter is optional, displayed as "Message Text" in UI. In SBIE plus if it is set only messages with text matching will be hidden, otherwise all instances of this message will be hidden.

Related Sandboxie Plus setting: Global Settings > General Config > Notifications > SBIE Messages
