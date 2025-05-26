# Prompt On Secure Desktop

**PromptOnSecureDesktop** is a global sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since v1.16.0 / 5.71.0. It controls whether User Account Control (UAC) elevation prompts from sandboxed applications appear on the secure desktop while not affecting host system behavior.

**Note:** This setting is only effective when [UseSandboxieUAC](UseSandboxieUAC.md) is enabled.

Usage:

```ini
   .
   .
   .
   [GlobalSettings]
   PromptOnSecureDesktop=n
```

This setting ensures that UAC prompts from sandboxed applications do not appear on the secure desktop, even if the system is configured otherwise.


