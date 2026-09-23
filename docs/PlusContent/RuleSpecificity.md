# Rule Specificity

Sandboxie can evaluate conflicting File, Registry, and IPC resource rules in two modes. Classical evaluation gives fixed priority to access modes. Specificity-based evaluation compares the process selector and the resource-pattern match before deciding which access mode applies.

These are separate parts of the decision:

* the **process selector** determines which program-specific form of a rule matches;
* the **resource pattern** determines how the configured path or object name matches the requested resource;
* the **access mode** determines the action represented by the winning rule, such as Closed, Read, Write, Normal, or Open.

Rule Specificity does not reduce these parts to a simple "longest rule wins" calculation.

## When specificity-based evaluation is enabled

The effective state is:

```text
RestrictDevices OR UsePrivacyMode OR UseRuleSpecificity
```

`UseSecurityMode=y` enables the device-restriction behavior and therefore also enables Rule Specificity. Consequently, explicitly setting `UseRuleSpecificity=n` does not turn specificity off while Privacy Mode or Restrict Devices is active.

In an ordinary sandbox where none of those options enables the feature, classical evaluation is used. See [Use Rule Specificity](../Content/UseRuleSpecificity.md) for configuration and SandMan behavior.

## Classical evaluation

With Rule Specificity disabled, File and Registry rules use fixed classical priority:

```text
Closed > Write > Read > Open > Normal > default
```

A matching Closed, Write, or Read rule ends the comparison at its priority level. A Normal match can be selected, but a matching Open rule can replace it. Under this model, a Closed match therefore takes precedence over a conflicting Open match even when the Open pattern appears more narrowly scoped.

## Specificity-based evaluation

With Rule Specificity enabled, Sandboxie compares candidates from the relevant access lists. A later access list can replace an earlier candidate when the process selector is no worse and the resource-pattern match improves one of the characteristics considered by the matcher.

This means that neither a program-specific rule nor a longer-looking path is automatically the winner. Both the process selector and the actual pattern match matter.

### Process selectors

The current process match levels are:

| Selector | Internal level |
| --- | ---: |
| Matching positive process name, wildcard name, or ProcessGroup | 0 |
| Matching negated selector | 1 |
| Explicit `*` selector | 2 |
| No process selector | 3 |

For example:

```ini
OpenFilePath=firefox.exe,C:\Path
OpenFilePath=fire*.exe,C:\Path
OpenFilePath=<Browsers>,C:\Path
OpenFilePath=!firefox.exe,C:\Path
OpenFilePath=*,C:\Path
OpenFilePath=C:\Path
```

The first three forms can all receive the best level when they match. It is therefore more accurate to call level 0 a **matching positive process selector**, not an exact process-name match.

A better process level acts as a gate during cross-list comparison; it is not an absolute priority. A new candidate must not have a worse process level and must improve a relevant resource-match characteristic. For example:

```ini
OpenFilePath=firefox.exe,C:\*
ClosedFilePath=C:\Sensitive\Records\*
```

The positive Firefox selector does not, by itself, guarantee that the broad Open rule replaces a more-specific Closed candidate.

### Resource-pattern matching

Sandboxie's internal exact/non-exact distinction is not the same as "contains no wildcard." It is based primarily on whether the pattern ends in `*`:

```text
C:\Foo\*   non-exact
*foo*      non-exact
*.tmp      exact
foo?       can be exact
```

The match length describes how far the pattern successfully matched the tested resource. For wildcard patterns, it is not necessarily the literal number of characters in the configured rule.

For this reason, `*.tmp` can be a strong candidate: it can be classified as exact and its match can extend to the end of the requested path. It does not universally outrank every other rule. Process level, access-list comparison, other match properties, and ties still participate.

The matcher also distinguishes a direct match from certain compatibility matches produced by retrying a path with a trailing separator. A direct match can take priority when otherwise competing candidates are compared.

When candidates from different access lists have the same positive match length, a candidate with fewer internal wildcard segments can be preferred. This is not a universal rule that fewer wildcards always wins. In particular, it is not a general tie breaker between entries within the same list.

Within one access list, a longer qualifying match can replace an earlier candidate. An equal-length candidate normally does not replace the existing candidate solely because it has fewer wildcards. Configuration order can therefore still matter in a complete tie, but the detailed loading order of box, template, fallback, and internal rules should not be treated as a stable public precedence contract.

### Access-list comparison

For specificity-based File and Registry evaluation, the current traversal order is:

```text
Closed, Write, Read, Normal, Open
```

Later lists can replace an earlier candidate when their actual match is considered better. If all compared characteristics are tied, the earlier candidate remains. A complete tie therefore favors:

```text
Closed > Write > Read > Normal > Open
```

This is only tie behavior. It does not mean that Closed always wins while Rule Specificity is active.

## File and Registry rules

File and Registry matching uses five access lists:

| Access mode | General meaning |
| --- | --- |
| Normal | Apply Sandboxie's normal virtualization policy |
| Open | Access the host resource directly |
| Closed | Deny access |
| Read | Allow reading the real resource while denying modifications |
| Write / Box Only | Hide the host resource while keeping the sandbox copy available |

These are conceptual descriptions; individual File and Registry operations do not necessarily map identically at the Windows API level.

For example, with specificity enabled:

```ini
UseRuleSpecificity=y
ClosedFilePath=C:\Data\*
OpenFilePath=C:\Data\App\*
```

The more-specific Open rule can win for resources under `C:\Data\App\`. With specificity disabled, the matching Closed rule wins under classical evaluation.

## IPC differences

Generic named IPC-object matching does not use the same five-list comparison. It uses:

```text
NormalIpcPath
OpenIpcPath
ClosedIpcPath
```

When specificity is active, a more-specific Normal or Open IPC candidate can replace a broader Closed candidate under the same comparison principles. See [Normal IPC Path](../Content/NormalIpcPath.md).

`ReadIpcPath` is different. Its documented `$:` form belongs primarily to the separate process/thread access policy:

```ini
ClosedIpcPath=$:target.exe
OpenIpcPath=$:target.exe
ReadIpcPath=$:target.exe
```

Those target-process rules use their own matcher and relevant order of Closed, Open, then Read. They do not use the resource-path specificity levels described above. See [Read IPC Path](../Content/ReadIpcPath.md).

## Configuration pattern details

Configured File and Registry rules normally receive implicit suffix-star handling when the pattern contains no `*`. For example, a configured rule such as:

```ini
NormalFilePath=C:\Foo
```

may be loaded as the equivalent of `C:\Foo*`. This changes the rule's scope and its exact/non-exact classification. A leading `|` suppresses that automatic suffix and is removed before File/Registry matching.

IPC path lists do not receive the same implicit trailing `*`. Write an IPC wildcard explicitly when broader matching is intended.

## Version history

| Change | Version |
| --- | --- |
| Optional Rule Specificity and Normal rules introduced | Sandboxie Plus 1.0.0 / Classic 5.55.0 |
| Exact-versus-trailing-wildcard priority improved | Sandboxie Plus 1.3.0 / Classic 5.58.0 |
| Wildcard and tie handling improved | Sandboxie Plus 1.3.1 / Classic 5.58.1 |
| Primary matches given priority over auxiliary matches | Sandboxie Plus 1.8.0 / Classic 5.63.0 |

## Related pages

* [Use Rule Specificity](../Content/UseRuleSpecificity.md)
* [Normal File Path](../Content/NormalFilePath.md)
* [Normal Key Path](../Content/NormalKeyPath.md)
* [Normal IPC Path](../Content/NormalIpcPath.md)
* [Resource Access Settings](../Content/ResourceAccessSettings.md)
