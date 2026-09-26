# Open Clsid

_OpenClsid_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It lets Sandboxie's COM handling attempt to access a specified host COM class through its brokered path. The component must still be installed, and Windows COM permissions, server behavior, and other Sandboxie restrictions can prevent activation.

For example:

```ini
[DefaultBox]
OpenClsid={D713F357-7920-4B91-9EB6-49054709EC7A}
```

This example identifies the HP Universal Printer Status Monitor pop-up component. It treats that CLSID as open for the sandbox; it does not guarantee that the component can be activated on every system.

## Program-qualified rules

An optional program name or [Process Group](ProcessGroup.md) can precede the CLSID:

```ini
OpenClsid=program.exe,{CLSID}
OpenClsid=<GroupName>,{CLSID}
```

`{CLSID}` is a placeholder for a valid class identifier. In normal client-side COM handling, the prefix selects the sandboxed **calling process**, not the COM server. Executable names match exactly and without case sensitivity; this setting does not support wildcard or negated program selectors. Omit the prefix for a rule that is not restricted to a particular caller; `*` is not an all-program selector here. Process groups can contain other groups.

The program prefix filters client-side activation handling, but Sandboxie's COM broker evaluates open CLSIDs at box scope. A program-qualified `OpenClsid` rule is therefore **not** a complete per-executable authorization boundary. An unrelated sandboxed program does not automatically gain successful activation: the ordinary intercepted client path normally filters a nonmatching caller before choosing the broker, and other access conditions still apply.

## Configuration and changes

Effective `OpenClsid` values can come from the box, applicable enabled templates, or `[GlobalSettings]` fallback. SandMan's disabled rows are not active rules. A sandboxed process caches its client-side CLSID list; restart affected sandboxed applications after changing the setting. The broker rebuilds its box-level open list for later requests after a normal configuration reload, but this does not refresh a list already cached in a running sandboxed process.

In the intercepted `CoGetClassObject`, `CoCreateInstance`, and `CoCreateInstanceEx` paths, a matching [Closed Clsid](ClosedClsid.md) rule is checked before an open rule. This precedence should not be generalized to every COM activation route.

In Sandboxie Plus, use **Sandbox Options > Resource Access > COM > Add COM Object**, choose **Open** in the Access column, and optionally select a Program. The separate **Don't use virtualized COM, Open access to hosts COM infrastructure (not recommended)** checkbox changes COM routing more broadly; it is not equivalent to adding one `OpenClsid` entry.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Resource Access > COM Access](ResourceAccessSettings.md#com-access).
