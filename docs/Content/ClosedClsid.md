# Closed Clsid

_ClosedClsid_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since v0.5.3a / 5.45.2. It blocks specified COM class identifiers in Sandboxie's intercepted client-side activation paths.

For example:

```ini
[DefaultBox]
ClosedClsid={8BC3F05E-D86B-11D0-A075-00C04FB68820}
```

This WMI class rule denies matching intercepted COM activation attempts for that CLSID. It does not establish that every way to use Windows Management Instrumentation is blocked.

## Program-qualified rules

Like [Open Clsid](OpenClsid.md), this setting accepts a plain `{CLSID}` or a `program.exe,{CLSID}` or `<GroupName>,{CLSID}` value. The optional selector is checked against the sandboxed calling process. Executable-name matching is exact and case-insensitive; wildcard and negated program selectors are not supported. Omit the prefix to avoid restricting the rule to one caller; `*` is not an all-program selector here. [Process Groups](ProcessGroup.md) can be nested.

## Scope and precedence

Sandboxie checks `ClosedClsid` in its intercepted `CoGetClassObject`, `CoCreateInstance`, and `CoCreateInstanceEx` paths. A match returns `E_ACCESSDENIED` before a matching `OpenClsid` rule can select the COM broker. This is a path-specific precedence rule: the intercepted `CoGetObject` elevation-moniker path does not perform the same closed-list check, and the SbieSvc broker checks open eligibility without consulting `ClosedClsid`. Do not rely on this setting as a universal block on every COM or RPC route.

Effective values can include box configuration, applicable enabled templates, and `[GlobalSettings]` fallback. SandMan's disabled rows are not active rules. The client-side list is cached after initialization, so restart affected sandboxed applications after changing `ClosedClsid`; a routine service restart or Windows reboot is not required for this client-side setting.

In Sandboxie Plus, use **Sandbox Options > Resource Access > COM > Add COM Object** and choose **Closed** in the Access column. The editor also has a Program column.
