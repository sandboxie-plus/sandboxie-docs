# Block Fake Input

**This feature is no longer supported in SBIE v4 and up.**


_BlockFakeInput_ is a sandbox setting in [Sandboxie Ini](SandboxieIni). It specifies whether Sandboxie will allow sandboxed programs to manufacture fake keyboard input and send it to windows of applications running outside that sandbox.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BlockFakeInput=n
```

Keyboard input is received by the active, highlighted window. This is true whether the keyboard input was manufactured by a program (fake input), or coming from the keyboard (real input).

By default, Sandboxie will allow a program running in a sandbox to manufacture fake input, provided the recipient window belongs to an application which is running in the same sandbox.

If the fake input will end up in a window outside that sandbox, Sandboxie will discard the input and issue message [SBIE1304](SBIE1304).

Specifying _BlockFakeInput=n_ indicates that a sandboxed program should be allowed to manufacture fake keyboard input, regardless of the recipient of that input.

To experiemnt with this setting, you can run a sandboxed instance of _osk.exe_, the Windows on-screen keyboard.

Related [Sandboxie Control](SandboxieControl) setting: [Sandbox Settings > Restrictions > Hardware Access](RestrictionsSettings#hardware)
