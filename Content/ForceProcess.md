# Force Process in Sandboxie

**ForceProcess** is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), allowing the specification of program names. If any of these programs are initiated outside any sandbox, they will be automatically sandboxed in a specified sandbox. Here is an example configuration:

```ini
   [DefaultBox]
   ForceProcess=iexplore.exe
   ForceProcess=firefox.exe
   ForceProcess=App*.exe
   ForceProcess=App?.exe
   [MailBox]
   ForceProcess=outlook.exe
   ForceProcess=cl?cke?.exe
```

- `*` represents any character.
- `?` represents one character.

In this example, Internet Explorer (iexplore.exe), Firefox (firefox.exe), App* (Appga, App03, etc.), and App? (App1, Appg, Appa, etc.) will be forced to run sandboxed in the _DefaultBox_ sandbox. Outlook.exe and cl?cke? (clicker, clicked, etc.) will be forced to run sandboxed in the _MailBox_ sandbox.

Note that the _ForceProcess_ settings only apply to programs that start unsandboxed. If a program is specifically started in a sandbox or started by a program that is already sandboxed, then _ForceProcess_ settings are not applied.

See also: [ForceFolder](ForceFolder.md). If both a _ForceFolder_ and a _ForceProcess_ are applicable to a program that is starting, the ForceFolder setting takes precedence.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Program Start > Forced Programs](ProgramStartSettings.md#forced-programs)

See also: [Program Settings](ProgramSettings.md#page-1).
