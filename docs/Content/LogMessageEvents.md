# Log Message Events

_LogMessageEvents_ is a global setting in [Sandboxie Ini](SandboxieIni.md) available since v1.15.2 / 5.70.2. It indicates that Sandboxie should log all Sandboxie messages to the Windows [System Event Log](SystemEventLog.md).

## Usage

```ini
[GlobalSettings]

LogMessageEvents=y
```

## Overview

When enabled, this setting causes all Sandboxie messages (SBIE codes) to be written to the Windows System Event Log with a source of `SbieDrv`[^1]. This provides a centralized location for viewing and monitoring all Sandboxie activity, including errors, warnings, and informational messages that would normally only appear in popup dialogs or the Sandboxie message log.

## Behavior

The `LogMessageEvents` setting affects how Sandboxie handles message logging at the driver level[^2]. When a message is generated:

1. The message is first processed through the normal Sandboxie message system[^3].
2. If `LogMessageEvents` is enabled, the message is additionally sent to the Windows Event Log as an informational event[^4].
3. The event includes the formatted message text and is tagged with the appropriate SBIE message code[^5].

## Usage Scenarios

This setting is particularly useful for:

- **System Administrators**: Monitoring Sandboxie activity across multiple systems through centralized log management.
- **Debugging**: Capturing a complete record of Sandboxie operations for troubleshooting.
- **Compliance**: Maintaining audit logs of sandboxed application behavior.
- **Automation**: Allowing monitoring tools to watch for specific Sandboxie events through standard Windows Event Log APIs.

## Message Filtering

Not all Sandboxie messages are logged to the event log when this setting is enabled. The following message types are specifically excluded from event logging[^6]:

- **MSG_2199**: Auto Recovery notifications.
- **MSG_2198**: File Migration progress notifications.
- **MSG_1399**: Process Start notifications.

These exclusions prevent the event log from being overwhelmed with routine operational messages that occur frequently during normal Sandboxie operation.

## Performance Considerations

Enabling `LogMessageEvents` has minimal performance impact under normal circumstances. However, in environments with high sandbox activity, the additional event log writes may contribute to system overhead. The setting should be used judiciously in production environments where maximum performance is critical.

## Implementation Notes

The `LogMessageEvents` functionality is implemented at both the kernel driver level and the service level[^7]:

- The driver component (SbieDrv) checks the setting during configuration loading[^8]
- Messages are processed through the service component which formats and writes them to the event log[^9]
- The setting is cached for performance and re-read when the configuration is reloaded[^10]

## Troubleshooting

If `LogMessageEvents` is enabled but events are not appearing in the Windows Event Log:

1. Verify the setting is properly configured in the `[GlobalSettings]` section.
2. Check that the Sandboxie service has appropriate permissions to write to the Event Log.
3. Restart the Sandboxie service after changing the setting.
4. Verify that Windows Event Log service is running.

## Historical Context

This feature was introduced in Sandboxie Plus version 1.15.2 / 5.70.2 as part of enhanced monitoring capabilities[^11]. A critical bug that could cause system crashes (BSoD) when using this setting was fixed in version 1.15.4[^12].

[^1]: Source: `LogMessage_Event` function in `/Sandboxie/core/svc/main.cpp`.
[^2]: Source: `Log_LogMessageEvents` boolean variable definition in `/Sandboxie/core/drv/log.c`.
[^3]: Source: `Log_Popup_Msg` function call logic in `/Sandboxie/core/drv/log.c`.
[^4]: Source: `ReportEvent` call in `/Sandboxie/core/svc/main.cpp`.
[^5]: Source: Message formatting in `SbieDll_FormatMessage2` call in `/Sandboxie/core/svc/main.cpp`.
[^6]: Source: Message filtering logic in `/Sandboxie/core/svc/DriverAssistLog.cpp`.
[^7]: Source: Data communication via `Api_SendServiceMessage` in `/Sandboxie/core/drv/log.c`.
[^8]: Source: Configuration loading in `Conf_Get_Boolean` call in `/Sandboxie/core/drv/conf.c`.
[^9]: Source: `LogMessage` function in `/Sandboxie/core/svc/DriverAssistLog.cpp`.
[^10]: Source: `Log_LogMessageEvents` global variable caching in `/Sandboxie/core/drv/log.h`.
[^11]: Source: CHANGELOG.md entry for version 1.15.2 / 5.70.2 
[^12]: Source: CHANGELOG.md entry for version 1.15.4 / 5.70.4 BSoD fix