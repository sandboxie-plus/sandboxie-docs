# Use Rule Specificity

_UseRuleSpecificity_ is a Boolean sandbox setting in [Sandboxie Ini](SandboxieIni.md). It enables specificity-based comparison when multiple File, Registry, or IPC resource rules match. The standard sandbox default is disabled.

```ini
[DefaultBox]
UseRuleSpecificity=y
```

See [Rule Specificity](../PlusContent/RuleSpecificity.md) for the process-selector, resource-pattern, access-list, and classical-priority rules.

## Effective state

The runtime enables Rule Specificity when any of these conditions is true:

```text
RestrictDevices OR UsePrivacyMode OR UseRuleSpecificity
```

`UseSecurityMode=y` enables Restrict Devices behavior and therefore indirectly forces Rule Specificity. As a result, `UseRuleSpecificity=n` cannot turn the behavior off while Privacy Mode or Restrict Devices is active.

## SandMan interface

The control is located at:

**Sandbox Options > Resource Access > Access Policies**

Its label is:

> **Prioritize rules based on their Specificity and Process Match Level**

When Privacy Mode or Restrict Devices is active, SandMan shows the option as active and disables the individual checkbox. This reflects the effective behavior; it does not necessarily mean that SandMan writes a separate `UseRuleSpecificity=y` entry.

## Availability

Direct use of Rule Specificity is subject to Sandboxie's supporter-certificate security-feature capability. When that capability is unavailable, the runtime can log the unavailable feature and schedule affected ordinary processes for termination after the evaluation period rather than rejecting every process immediately. If another security feature forces specificity, that forcing feature may be identified instead.

## Applying changes

The effective value is stored when a sandboxed process initializes. After changing the setting, restart affected sandboxed processes, preferably the complete sandbox process tree. A Windows reboot is not normally required.

## Version history

Rule Specificity and the Normal resource rules were introduced as optional behavior in Sandboxie Plus 1.0.0 / Classic 5.55.0. Later releases refined wildcard, tie, and primary-match handling; the current algorithm is described on the [Rule Specificity](../PlusContent/RuleSpecificity.md) page.
