# Network Access

`NetworkAccess` defines program, address, port, and protocol rules for Sandboxie's network rule engine. The same rule parser and comparison logic is used by the user-mode Winsock path and, when enabled, the [Windows Filtering Platform (WFP) path](../PlusContent/WFPSupport.md). Their enforcement coverage differs.

## Syntax and examples

```ini
NetworkAccess=[process,]Allow|Block[;Port=...][;Address=...][;Protocol=...]
```

For example:

```ini
[DefaultBox]
NetworkAccess=*,Block;Port=80,443
NetworkAccess=chrome.exe,Allow;Port=443;Address=192.0.2.10;Protocol=TCP
NetworkAccess=<Browsers>,Allow;Port=80,443;Protocol=TCP
```

The optional process selector can identify an executable, a matching executable pattern, or a [process group](ProcessGroup.md). Sandboxie's normal [program-name matching](ProgramNamePrefix.md) also supports negated selectors. Rules without a process selector apply more broadly than a matching explicit `*` selector in the rule comparison described below.

If no `NetworkAccess` rule matches, the rule engine permits the traffic. To build a default-deny rule set, add a broad applicable block and then narrower allows where needed:

```ini
NetworkAccess=*,Block
NetworkAccess=chrome.exe,Allow;Port=443
```

This rule-engine default is separate from the `AllowNetworkAccess` gate described in [WFP Support](../PlusContent/WFPSupport.md#allownetworkaccess).

## How a matching rule is chosen

For a candidate program and endpoint, Sandboxie strictly compares the first four criteria in this order. A later candidate replaces the current winner when it is better at the first of these criteria that differs:

| Order | Criterion | More specific or preferred match |
| --- | --- | --- |
| 1 | Process selector | Matching positive selector, then matching negated selector, then explicit `*`, then no selector |
| 2 | Combined endpoint | Both address and port constrained, ahead of rules constraining only one or neither |
| 3 | Port | Exact port, then range, then unconstrained |
| 4 | Address | Exact address, then range, then unconstrained |

A matching positive selector includes an executable name, wildcard image pattern, or `ProcessGroup`; the top category is not limited to exact executable names. The first three examples below are positive selectors. The remaining lines show a negated selector, explicit `*`, and no selector:

```ini
NetworkAccess=chrome.exe,Allow;Port=443
NetworkAccess=chr*.exe,Allow;Port=443
NetworkAccess=<Browsers>,Allow;Port=443
NetworkAccess=!chrome.exe,Block
NetworkAccess=*,Block
NetworkAccess=Block
```

Process matching is compared first, so a stronger process selector can outrank a rule with more precise address or port constraints. With equivalent process matches, a rule specifying both `Address` and `Port` outranks one specifying only either field. After that combined comparison, port specificity is checked before address specificity.

After the first four criteria tie, the current comparator handles action and protocol asymmetrically. A `Block` candidate immediately replaces an `Allow` winner. Otherwise, comparison can continue to protocol specificity, where a specified protocol outranks `Any`. Consequently, when one otherwise-tied rule favors `Block` while the other favors a more-specific protocol, rule order can affect the result.

If the comparator finds no reason to replace the current winner, the existing winner remains. Compatible rules may also be merged internally. `NetworkAccess` is not a last-rule-wins engine.

## Addresses, ports, and protocols

`Address` accepts single IPv4 or IPv6 addresses, address ranges, and comma-separated entries. For example:

```ini
Address=192.0.2.10
Address=192.0.2.10-192.0.2.50
Address=2001:db8::10
```

`Port` accepts single numeric ports, ranges, and comma-separated sets:

```ini
Port=80,443,49152-65535
```

The current rule language recognizes `Protocol=Any`, `TCP`, `UDP`, and `ICMP`; an unqualified rule defaults to `Any`. It does not define an `ICMPv6` keyword. The supported address syntax uses addresses and ranges, not CIDR notation; port names such as `http` are not numeric port values.

## Enforcement paths

Without WFP enforcement, SbieDll applies `NetworkAccess` through intercepted user-mode Winsock paths, including important outbound TCP and UDP operations such as `connect`, `WSAConnect`, `sendto`, and `WSASendTo`. Related receive hooks also participate in this implementation. This is primarily outbound rule enforcement and does not cover every Windows networking path. Code that bypasses or removes the user-mode hooks can bypass this layer.

With `NetworkEnableWFP=y`, Sandboxie uses kernel WFP callouts to evaluate the shared rules for tracked sandboxed processes at outbound connect and inbound receive/accept authorization layers. See [WFP Support](../PlusContent/WFPSupport.md) for the global switch, process mapping, and lifecycle.

Although the parser and SandMan editor recognize `ICMP`, the user-mode hooks focus on Winsock TCP connections and UDP send/receive. ICMP coverage depends on the enforcement path and traffic type; neither this setting nor WFP should be read as a guarantee for every raw or ICMPv6 path.

`AllowNetworkAccess=n` is a separate, image-aware access gate. Under WFP it can select blanket Internet blocking before normal `NetworkAccess` rule evaluation. A `NetworkAccess=...,Allow` rule does not necessarily override that gate. Runtime approvals from [Prompt For Internet Access](PromptForInternetAccess.md) can affect the gate for a process instance; they are not persistent `NetworkAccess` rules. [Block Local Loop](BlockLocalLoop.md) is also evaluated separately under WFP.

## SandMan and version context

The rule editor is at **Sandbox Options > Network Options > Network Firewall**. Its fields correspond to Program, Action, Protocol, IP/Address, and Port. The **Test Rules** controls offer a partial preview for an entered program, address, port, and protocol; they do not make a network connection. The preview does not handle wildcard or process-group selectors, skips template rules, and may consider disabled rules. Its highlighted result can therefore differ from the rule applied at runtime.

`NetworkAccess` was introduced in Sandboxie Plus 0.9.0. Rule coverage and update behavior depend on the enforcement path, so restart affected sandboxed applications after changing policy to ensure process-local state is rebuilt consistently. WFP rules can also be refreshed for existing tracked processes through Sandboxie's configuration update path.

## Related pages

- [WFP Support](../PlusContent/WFPSupport.md)
- [Block Local Loop](BlockLocalLoop.md)
- [Prompt For Internet Access](PromptForInternetAccess.md)
- [Process Group](ProcessGroup.md)
