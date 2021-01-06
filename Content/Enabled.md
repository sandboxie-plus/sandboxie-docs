# Enabled

_Enabled_ is a sandbox setting in [Sandboxie Ini](SandboxieIni). It is typically specified as _Enabled=y_ (see [Yes Or No Settings](YesOrNoSettings)), and indicates that programs can be launched in that sandbox. For example:

```
   .
   .
   .
   [InstallBox]
   Enabled=y
   Enabled=y,Administrators
```

The first example is the typical form of _Enabled_, a required part of any sandbox section in the configuration file. It indicates that the sandbox _InstallBox_ can be used for sandboxing.

The second example similarly defines the sandbox _InstallBox_ while also restricting its use to the Administrators user accounts group. Any user account or group that is recognized by the local Windows system can be specified. Multiple _Enabled_ lines may be specified if the list of user accounts does not fit in one line.

A sandbox that has been restricted to specific users is considered _hidden_ to all other user accounts. Those other user accounts will not see the sandbox listed in [Sandboxie Control](SandboxieControl), and any [Force Process](ForceProcess) or [Force Folder](ForceFolder) settings will not apply to those user accounts.

Attempts to explicitly start a program in a sandbox that does not have an associated _Enabled=y_ setting will fail.

Related [Sandboxie Control](SandboxieControl) setting: [Sandbox Settings > User Accounts](UserAccountsSettings)

Related [Sandboxie Control](SandboxieControl) command: [Sandbox Menu > Reveal Hidden Sandbox](SandboxMenu#reveal)
