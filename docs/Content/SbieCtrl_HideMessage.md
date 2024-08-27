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

The second parameter is optional, displayed as "Message Text" in UI. Notice: Even if this is configured, All messages of such will be hidden regardless of its text.

Related Sandboxie Plus setting: Global Settings > General Config > Notifications > SBIE Messages
