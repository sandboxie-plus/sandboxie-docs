# BlockInterferePower

_BlockInterferePower_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since Sandboxie Plus 1.13.2. It is disabled by default and is currently marked as Experimental.

For example:

```ini
[DefaultBox]
BlockInterferePower=y
```

When enabled, the setting prevents selected mechanisms used by sandboxed processes from interfering with host power and session behavior. It is not complete power-management isolation.

## SetThreadExecutionState

Sandboxie blocks calls to `SetThreadExecutionState` while this setting is enabled. The implementation does not selectively allow individual execution-state flags.

Consequently, requests using flags such as `ES_SYSTEM_REQUIRED`, `ES_DISPLAY_REQUIRED`, or `ES_AWAYMODE_REQUIRED` do not keep the host system or display active through this API.

This behavior is limited to `SetThreadExecutionState`. Modern power-request mechanisms such as `PowerSetRequest` are not covered.

## Shutdown behavior

The setting covers two shutdown-related paths:

- `ShutdownBlockReasonCreate` is blocked, so an application cannot register a shutdown-block reason through that API.
- For intercepted `WM_QUERYENDSESSION` messages, Sandboxie returns success without calling the application's original handler. This prevents the application from vetoing shutdown through that path.

_BlockInterferePower_ does not block Windows shutdown. In these cases, it reduces the ability of a sandboxed application to prevent shutdown. It does not generally block shutdown, restart, or suspend APIs.

## Limitations

The setting does not cover every power-management mechanism. The current implementation does not apply this setting to:

- `PowerCreateRequest`
- `PowerSetRequest`
- `PowerClearRequest`
- `SetSuspendState`
- power-plan APIs

Other shutdown and session-management APIs should not be assumed to be covered.

## Compatibility

Applications that use the affected APIs may behave differently when the setting is enabled. For example:

- media players using `SetThreadExecutionState` may no longer keep the display or system awake;
- games and presentation software using that API may lose the same behavior;
- long-running applications relying on it may no longer inhibit sleep;
- applications cannot register a shutdown-block reason through `ShutdownBlockReasonCreate`;
- applications cannot veto end-session through the intercepted `WM_QUERYENDSESSION` path.

These effects apply only to applications that use the covered mechanisms.

## Compartment Mode

This setting is intended for normal security-isolation boxes and is not supported as a complete feature in Compartment Mode.

## Runtime and scope

The primary restrictions are installed when a sandboxed process initializes. Enabling the setting after a process has already started does not retroactively install them. Existing sandboxed applications should therefore be restarted after changing the option.

Some individual paths may consult the current configuration dynamically, but restarting affected sandboxed applications is the reliable way to apply changes.

These restrictions are implemented primarily through user-mode API interception inside sandboxed processes. They should not be described as kernel-enforced protection or as covering alternative, unhooked APIs.

## Sandboxie Plus interface

The option is available under:

**Sandbox Options > General Options > Restrictions > Prevent sandboxed processes from interfering with power operations (Experimental)**

It is unchecked by default. The interface disables this option when security isolation is disabled.

## Version history

_BlockInterferePower_ was introduced in Sandboxie Plus 1.13.2 and later received interface and configuration-persistence maintenance. Its default has remained disabled.

## Related settings

- [Sandboxie Ini](SandboxieIni.md)
- [BlockInterferenceControl](BlockInterferenceControl.md)
