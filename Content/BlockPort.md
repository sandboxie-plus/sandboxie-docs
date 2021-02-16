# Block Port

_BlockPort_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies IP port numbers which will be blocked for outgoing communications.

Usage:

```
   .
   .
   .
   [DefaultBox]
   BlockPort=137-139,445
   BlockPort=*,80,8080
```

The port numbers listed above are associated with the SMB/CIFS network file sharing subsystem.

The primary purpose of this setting is to block outgoing communications on SMB/CIFS ports, in order to prevent a rogue sandboxed program from accessing files through the SMB/CIFS subsystem, rather than by issuing direct requests to the local system.

The setting can be specified repeatedly over multiple lines and the effects will accumulate. Port ranges may be specified as shown in the first example. The second example shows negated use: Block all ports except those specified following the asterisk (star) character.

This setting is not configurable through Sandboxie Control, except to enable or disable a pre-defined list of default blocked ports:

[Sandbox Settings > Applications > Miscellaneous](ApplicationsSettings.md#misc) > Default list of blocked TCP/IP ports

Note that this setting will prevent programs such as [smbclient](http://www.samba.org/samba/docs/man/manpages-3/smbclient.1) from properly running under Sandboxie. In case this is required, the setting can be turned off.
