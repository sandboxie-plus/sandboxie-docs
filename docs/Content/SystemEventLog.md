# System Event Log

The System Event Log is a Windows component that collects informational and error messages issued by Windows itself and other third-party software. Sandboxie issues some messages to the System Event Log. The messages are listed with a Source value of SbieDrv. To access the log and view messages, use the Event Viewer tool:

Windows Start Menu > Control Panel > Administrative Tools > Event Viewer

For more information about the System Event Log, see [Event Viewer in Wikipedia](https://en.wikipedia.org/wiki/Event_Viewer).

If any Sandboxie messages are issued due to an error which prevents successful initialization, [Sandboxie Control](SandboxieControl.md) will display a flashing exclamation mark icon. Right-click the flashing icon and select _Show Errors_ to view any related messages.

_Messages From Sandboxie_ are not stored in the _Windows Event Log_, a workaround is available to [store the logs in a flat file](MessagesFromSandboxie.md#log-messages-to-a-file).

See also: [SBIE Messages](SBIEMessages.md).
