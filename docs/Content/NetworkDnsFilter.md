# Network DNS Filtering

`NetworkDnsFilter` blocks or redirects matching hostname lookups made through Sandboxie's intercepted Windows Winsock service-lookup path. Rules can apply to all processes in a sandbox or to selected programs, and domain names can be matched with wildcard patterns.

This is a user-mode name-resolution filter, not a packet-level firewall. Blocking a hostname does not prevent a program from connecting directly to an IP address or from resolving the name through a path that Sandboxie does not intercept.

An applicable [Supporter Certificate](https://sandboxie-plus.com/supporter-certificate/) is required for the filter.

## Syntax

```ini
NetworkDnsFilter=[process,]domain[:ip_address[;ip_address...]]
```

* `process` is an optional [program selector](ProgramNamePrefix.md). If omitted, the rule applies to all processes in the sandbox.
* `domain` is the hostname or wildcard pattern to match. Matching is case-insensitive.
* `ip_address` is an optional IPv4 or IPv6 address returned instead of the normal result. Separate multiple addresses with semicolons. If the address portion is omitted, the matching lookup is blocked.

For example, this rule redirects matching lookups from every process in the box:

```ini
[DefaultBox]
NetworkDnsFilter=example.com:192.0.2.10
```

## Domain matching

Domain patterns use Sandboxie's wildcard matching, not regular expressions:

* `*` matches any sequence of characters.
* `?` matches one character.
* Matching is case-insensitive.

For example:

```ini
[DefaultBox]
NetworkDnsFilter=*.example.com
NetworkDnsFilter=example.com
```

The first rule blocks subdomains such as `www.example.com`; it does not also match the bare `example.com`, which is covered by the second rule.

Rule selection is not a simple last-rule-wins list. Rules are examined in configuration order, while process-match level and domain-pattern match length also participate in selection. A matching domain pattern that does not end in `*` ends the search; otherwise, a later candidate replaces the current match only when the implementation considers it a stronger match. Equal candidates retain the earlier entry. Put specific rules before broader overlapping wildcard rules and avoid relying on ambiguous overlaps.

## Blocking and redirection

Omit the address portion to return no result for a matching lookup:

```ini
[DefaultBox]
NetworkDnsFilter=blocked.example
```

Provide an address to synthesize a result without requesting the matching name from the normal system resolver through this lookup path:

```ini
[DefaultBox]
NetworkDnsFilter=redirected.example:192.0.2.20
```

Multiple valid addresses can be returned by one rule:

```ini
[DefaultBox]
NetworkDnsFilter=service.example:192.0.2.20;192.0.2.21
```

Invalid address entries are ignored. If a matching rule contains no valid address for the requested address family, the lookup returns no result. Validate manually written entries carefully.

## Process matching

The optional selector before the comma supports executable names, Sandboxie wildcard matching, configured process groups, and a leading `!` for a negative selector. Examples include:

```ini
[DefaultBox]
NetworkDnsFilter=browser.exe,example.com:192.0.2.30
NetworkDnsFilter=*.exe,telemetry.example
NetworkDnsFilter=<InternetAccess>,internal.example:192.0.2.40
NetworkDnsFilter=!updater.exe,updates.example
```

The last rule applies to processes other than `updater.exe`. Process selectors use executable names rather than full paths. An omitted selector or `*` applies to every process in the box.

## IPv4 and IPv6

Address selection follows the lookup's requested family:

* IPv4 (`A`) lookups return configured IPv4 addresses.
* IPv6 (`AAAA`) lookups return configured IPv6 addresses.
* When a rule contains only IPv4 addresses, Sandboxie also makes IPv4-mapped IPv6 results available to IPv6 lookups.
* When a rule contains any explicit IPv6 address, IPv6 lookups use the explicit IPv6 entries; Sandboxie does not also generate mapped IPv6 entries from that rule's IPv4 addresses.
* A rule containing only IPv6 addresses provides no result for an IPv4 lookup.

A mixed rule can supply both families:

```ini
[DefaultBox]
NetworkDnsFilter=dual-stack.example:192.0.2.50;2001:db8::50
```

## How the filter is applied

Sandboxie installs the filter when a sandboxed process initializes Winsock. It intercepts the standard Winsock service-lookup sequence used to begin, retrieve, and end a lookup. A matched rule is handled locally: Sandboxie either returns the configured addresses or reports that no result is available. An unmatched lookup continues through the normal system path.

This mechanism means the filter can handle a configured name even when the normal resolver would not know that name. The earlier limitation in which redirection depended on successful upstream resolution was removed in Sandboxie Plus 1.16.0 / Classic 5.71.0.

## Block DNS template

SandMan's separate **Block DNS, UDP port 53** option enables the `BlockDNS` template. The current template blocks direct outbound UDP traffic to port 53 for sandboxed programs:

```ini
Template=BlockDNS
```

This can complement `NetworkDnsFilter`, but it does not force every form of name resolution through the filter. It does not block TCP port 53, DNS over HTTPS, DNS over TLS, remote proxy name resolution, or another resolver path that does not use UDP port 53.

## SandMan configuration

Open **Sandbox Options > Network Options > DNS Filter**. The table contains **Program**, **Domain**, and **IP** columns. Use **Add Filter** and **Remove** to manage rows. The **IP** field accepts multiple addresses separated by semicolons.

Each row can be enabled or disabled. SandMan stores disabled rows as `NetworkDnsFilterDisabled`; that name is inactive UI storage rather than a second runtime filtering setting. Template-provided rows are displayed read-only.

## Applying configuration changes

Rules are loaded when the sandboxed process initializes Winsock; they are not dynamically rebuilt for a process that has already initialized networking. Restart affected sandboxed processes after changing the rules. Restarting SandMan, the Sandboxie service, or the driver is not normally required.

## Limitations and security boundaries

`NetworkDnsFilter` covers supported lookups that reach Sandboxie's intercepted Winsock service-lookup path. It does not provide a universal domain-access policy. In particular:

* Applications using their own resolver, raw DNS traffic, or an internal DNS-over-HTTPS implementation can avoid this lookup path.
* If a program sends a hostname to a proxy for remote resolution without resolving it locally, the local DNS filter does not receive that hostname.
* A program can still connect directly to a known IP address unless separate network policy blocks it.
* DNS filtering and [`DnsTrace`](SandboxieTrace.md) are separate. Tracing records supported lookup activity but does not enable filtering.

Use independent network restrictions when direct connections must be prevented. DNS filtering should not be treated as a firewall or as a guarantee that all DNS activity is blocked, redirected, or kept private.

## Version history

| Change | Version |
| --- | --- |
| DNS lookup interception, logging, filtering, and redirection introduced | Sandboxie Plus 1.14.0 / Classic 5.69.0 |
| Fixed a crash when a filtered domain had no configured IP address | Sandboxie Plus 1.15.5 / Classic 5.70.5 |
| Refactored matching so blocking and redirection no longer depend on a successful normal DNS result | Sandboxie Plus 1.16.0 / Classic 5.71.0 |

## Related pages

* [DNS Filter overview](../PlusContent/DNSFilter.md)
* [Sandboxie Trace](SandboxieTrace.md)
* [Sandboxie Ini](SandboxieIni.md)
