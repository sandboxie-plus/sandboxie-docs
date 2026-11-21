# Custom Process Command Line

_CustomProcessCommandLine_ transforms the arguments of matching sandboxed processes.

Rules use Sandboxie's normal process and ProcessGroup prefix. Sandboxie applications and
programs launched from the Sandboxie installation directory are exempt.

## Usage

```ini
[DefaultBox]

CustomProcessCommandLine=app.exe,Add=--verbose
```

## Syntax

```ini
CustomProcessCommandLine=<selector>,<action>[;<condition-or-option>...]
```

## Selectors

- `app.exe` or `app*.exe`: Match an image using the common Sandboxie process pattern.
- `<Group>`: Match a configured ProcessGroup, including nested groups.
- `*`: Match every process.
- `!app.exe`: Negate the selector.
- `<Special:Chrome>`, `<Special:Firefox>`, `<Special:Thunderbird>`,
  `<Special:Browser>`, `<Special:Mail>`, or `<Special:Plugin>`: Match the
  corresponding SpecialImage classification.

## Actions

- `Clear=Arguments`: Remove every argument while preserving the executable token.
- `Set=<arguments>`: Replace the entire argument list.
- `Remove=<pattern>`: Remove matching arguments.
- `RemoveSequence=<sequence>`: Remove a contiguous sequence of matching arguments.
- `Replace=<pattern>;With=<arguments>`: Replace matching arguments in place.
- `ReplaceSequence=<sequence>;With=<arguments>`: Replace a contiguous sequence in place.
- `Add=<arguments>`: Add arguments at the end by default.

Every enabled rule must contain exactly one action. The executable token uses
program-name quoting: quotes group spaces, and backslashes remain literal.
Later arguments retain normal command-line backslash/quote escaping.

For `Add`, use `At=Start|End`, `Before=<pattern>`, or `After=<pattern>` to
control placement. `Duplicate=Skip` is the default; `Duplicate=Allow` permits
duplicates. `Remove`, `Replace`, `RemoveSequence`, and `ReplaceSequence` accept
`Occurrences=First|Last|All` (default: `All`). `Last` selects only the rightmost
match in the current argument list, before the action modifies it. For
`RemoveSequence`, overlapping matches are included when locating the last match.
With `Match=Pattern`, each element in a sequence is matched independently.
Write the value as a normal command-line fragment; quote individual elements
that contain spaces.

For example, `app.exe a a a b` with `RemoveSequence=a a;Occurrences=Last`
becomes `app.exe a b`, removing the second and third `a` arguments.

## Variable Expansion

Add, Set, and With payloads expand process environment variables first, followed
by unresolved Sandboxie variables such as %USER%, %SANDBOX%, and %SBIEHOME%.
`Expand=y|n` controls both steps for each rule and defaults to `y`. Use `Expand=n`
to keep the output payload literal. The option is valid only on Add, Set, Replace,
and ReplaceSequence rules; for replacements it controls With, not the pattern.
Invalid or repeated values, and explicit use on other actions, invalidate the rule.
Quote expanded paths that may contain spaces; expansion does not add quoting or
provide capture/template substitution.

Existing rules that contain literal percent-delimited text in these payloads
may need `Expand=n` after updating, because expansion is enabled by default.
For example, quote a path in the rule itself so it remains one argument after
expansion:

```ini
CustomProcessCommandLine=app.exe,Add=--profile "%USERPROFILE%\My Profile"
```

Expansion occurs after rule parsing, so commas and semicolons in variable values
remain payload text, not rule fields. Selectors, matching patterns, conditions,
IDs, and Before/After anchors are not expanded. Payloads are prepared once and
shared by API transformation and PEB replay.

Failed driver-variable queries retain the original token, including unknown
variables. The first failed status per payload is reported in Resource Access
Monitor with a literal-fallback outcome, without arguments or expanded values.
The driver collapses some underlying causes into the same status as unknown
variables, so these failures cannot be classified more precisely here.

Identifiable query buffer errors (`STATUS_BUFFER_TOO_SMALL` or
`STATUS_BUFFER_OVERFLOW`) and local capacity/sizing failures discard the entire
plan before API or PEB publication, not just the affected rule. Existing fatal
preparation errors also discard the plan. A later fatal error overrides an earlier
fallback status in that payload's diagnostic. `Expand=n` bypasses expansion queries
and expansion-failure diagnostics; payloads without expansion attempts are not logged.

The compatibility setting CustomChromiumFlags retains its existing literal
payload behavior.

## Other Rule Fields

- `If=<pattern>`: Apply only when the condition matches. Repeated fields use AND.
- `Skip=<pattern>`: Skip when the condition matches. Repeated fields use OR.
- `IfArg=<pattern>` / `SkipArg=<pattern>`: Match an argument without interpreting
  reserved condition names. These still use the rule's Match and CaseSensitive
  settings; for example, `IfArg=Empty` matches an argument literally named Empty
  with the default exact mode.
- `IfSequence=<sequence>` / `SkipSequence=<sequence>`: Match contiguous decoded
  arguments together, using the same fragment quoting and matching rules as
  RemoveSequence. For example, `IfSequence=--profile "Work profile"` tests the
  option and its value together.

### Argument-State Conditions

These inspect the argument list selected by `ConditionSource`, except
`InputArgCount`, which always uses the original input.

| Condition | Meaning |
| --- | --- |
| `Empty` | No arguments after the executable name. |
| `NotEmpty` | At least one argument after the executable name. |
| `ArgCount>=2` | The selected argument count satisfies the comparison; this example requires at least two. By default, it counts arguments produced by preceding rules. |
| `InputArgCount>=2` | The original argument count, before any rules ran, satisfies the comparison; this example requires at least two. |

### Process-State Conditions

| Condition | Meaning | Process flag |
| --- | --- | --- |
| `Forced` | Sandboxie recorded the process as forced into the sandbox by a forcing rule, such as `ForceProcess`, `ForceFolder` or `ForceChildren`. | `SBIE_FLAG_FORCED_PROCESS` |
| `ForcedChild` | The process carries `ForceChildren` provenance, including descendants that inherit the flag from their parent. | `SBIE_FLAG_FORCED_CHILD_PROCESS` |
| `ParentWasStartExe` | Its recorded parent was Sandboxie's `Start.exe`. | `SBIE_FLAG_PARENT_WAS_START_EXE` |
| `DropRights` | Drop-rights mode is enabled for this process. This is distinct from the separate flag indicating that rights were actually dropped. | `SBIE_FLAG_DROP_RIGHTS` |
| `FakeAdmin` | Fake-administrator mode is flagged; this does not test actual administrator privileges. | `SBIE_FLAG_FAKE_ADMIN` |
| `OpenAllWinClass` | The broad all-window-classes-open flag is set. A specific window-class exception alone does not satisfy this condition. | `SBIE_FLAG_OPEN_ALL_WIN_CLASS` |
| `AppCompartment` | Application Compartment / `NoSecurityIsolation` mode is flagged. | `SBIE_FLAG_APP_COMPARTMENT` |
| `ProcessInAppPkg` | Sandboxie detected the process as being in an app package. This is separate from `AppCompartment` mode. | `SBIE_FLAG_PROCESS_IN_APP_PKG` |
| `PCA` | The Program Compatibility Assistant job flag is set, not merely a general compatibility-mode setting. The process may be restarted outside that job. | `SBIE_FLAG_PROCESS_IN_PCA_JOB` |

These conditions test the process flags queried at DLL initialization; they do
not change sandbox settings or process privileges. All named conditions work
with both `If=` and `Skip=` and their names are case-insensitive. They are
reserved names, evaluated before argument matching.

For example, `CustomProcessCommandLine=app.exe,Add=--restricted;If=DropRights`
adds an argument only when `SBIE_FLAG_DROP_RIGHTS` is set.
`CustomProcessCommandLine=app.exe,Add=--safe-mode;Skip=AppCompartment`
skips the rule when `SBIE_FLAG_APP_COMPARTMENT` is set.

### Combining Conditions

All positive spellings (`If`, `IfArg`, `IfSequence`) share an eight-condition
limit and use AND. All skip spellings share another eight-condition limit and
use OR. Preparing a condition must succeed: an allocation or pattern-preparation
failure discards the private plan rather than being treated as a nonmatch.

```ini
CustomProcessCommandLine=app.exe,Add=--restricted;If=Forced;If=DropRights;Skip=AppCompartment
```

This requires both `Forced` and `DropRights` and skips the rule when `AppCompartment`
is true. Conditions inspect state; they do not enable those modes.

`Id:<name>` is a separate applied-rule predicate, not a process-state flag.
See [Applied-ID Conditions](#applied-id-conditions).

### Condition Source and Matching

`ConditionSource=Current` is the default. `ConditionSource=Input` evaluates
argument-based conditions against the immutable argument list from before any
rules ran. This includes argument/sequence matches, Empty, NotEmpty and ArgCount.
InputArgCount always refers to the original count; process-flag and applied-ID
conditions do not depend on ConditionSource. Actions always modify the current argument list.
For example, a later rule can test an input argument that an earlier rule removed.

The count excludes the executable token. Comparisons support `=`, `<`, `<=`,
`>`, and `>=`.

`Match=Exact` is the default. `Match=Pattern` uses the common Sandboxie pattern
engine. `Match=Text` matches text within one decoded argument. Argument matching
is case-sensitive by default; use `CaseSensitive=n` for case-insensitive matching.

Use `;;` when an action or condition needs a literal semicolon.

## Identity and Ordering

- `Id=<name>` gives a rule a case-insensitive identity.
- A more local sandbox rule with the same ID replaces an inherited rule.
- `Disabled=y` with an ID suppresses the inherited rule.
- `Order=0..9999` explicitly positions the rule.
- `Stop=y` stops later rules after this rule successfully applies.

Default orders are Clear/Set 100, Remove/RemoveSequence 200, Replace/ReplaceSequence 300, and Add 400.
Rules with the same order retain their effective configuration sequence.

## Applied-ID Conditions

`If=Id:SomeID` is true only after an earlier effective rule with that ID has
successfully reported its action applied. `Skip=Id:SomeID` suppresses the current
rule after that same result. References compare IDs exactly and case-insensitively,
independently of Match, CaseSensitive and ConditionSource.

- Missing, disabled, condition-skipped and not-yet-executed IDs are false.
- No-match removal/replacement and duplicate-skipped Add do not activate a gate.
- Applied does not mean a net text change: Clear/Set and a matching same-value
  Replace retain their existing successful-action reporting.
- Rules run once by Order, then effective configuration order for ties.
  References never reorder, defer or rerun rules. A reference to a later rule is
  false; therefore a Skip referring to that later rule does not suppress anything.
- Give the gate a lower Order when default action ordering would place a child
  first. Defaults already place Remove before Add, but Add before Remove needs
  an explicit override. Across inherited/template rules, explicit orders make
  the dependency unambiguous.
- Children keep their own IDs or no IDs. Repeating the gate ID would invoke
  override handling, not create group membership.
- Stop=y still stops all subsequent rules, including dependent children.
- The Id: prefix is reserved in generic If/Skip conditions. To match an argument
  literally named Id:SomeID, use `IfArg=Id:SomeID` / `SkipArg=Id:SomeID`.

For example, the first rule consumes an input marker and activates two children;
when the marker is absent, only the alternative Add runs:

```ini
CustomProcessCommandLine=app.exe,Id=SafeProfile;Order=100;Remove=--safe-profile
CustomProcessCommandLine=app.exe,Order=200;Add=--disable-plugins;If=Id:SafeProfile
CustomProcessCommandLine=app.exe,Order=200;Add=--verbose;If=Id:SafeProfile
CustomProcessCommandLine=app.exe,Add=--normal-mode;Skip=Id:SafeProfile
```

These results are local to the current transformation. If a later action or
publication fails, the entire plan, including its internal gate results, is
discarded; no applied state is carried into another process or transformation.

## PEB Publication

`UpdatePEB=y|n|KeepOriginal` controls each rule's contribution to the PEB command
line. The default is `y`:

| Value | Effect when the rule's action applies |
| --- | --- |
| `y` | Include the action in the PEB result. |
| `n` | Omit the action from the PEB result, but retain it in the API result. |
| `KeepOriginal` | Preserve the entire original PEB command line, overriding all other rules' PEB modes. |

`GetCommandLineW` and `GetCommandLineA` still expose the full transformed result.
Conditions, `ConditionSource=Current|Input`, applied-ID gates, ordering and `Stop`
are evaluated once using that full state, including actions marked `n`.
Skipped, disabled and duplicate-skipped rules do not affect PEB publication.

When an applied rule uses `n`, the PEB result starts from the original arguments
and replays only applied `y` actions in order. Each action rematches against
that independent state; conditions and ID gates are not re-evaluated. For
example, a replacement targeting an argument introduced only by an `n` action
will not find that argument in the PEB result.

```ini
CustomProcessCommandLine=app.exe,Add=--api-only;UpdatePEB=n
CustomProcessCommandLine=app.exe,Add=--visible
```

The API result contains both added arguments; the PEB result contains only
`--visible`. With `UpdatePEB=KeepOriginal` on either applied rule, the PEB retains
the original command line instead. An action can apply without a net text
change, so such a rule can still control publication. If preparing either
result fails, neither result is published.

`CustomChromiumFlags` actions retain their existing behavior and participate in
PEB publication with the default `y` mode.

## Notes

- All effective sandbox, template, and global rules are collected before execution.
- Conditions inspect the command line produced by earlier ordered rules unless ConditionSource=Input is selected.
- Invalid rules are ignored without partially modifying the command line.
- The final command line is published only after the complete plan succeeds.
- `CustomChromiumFlags` uses the same transformation path.

## Limits and Diagnostics

- Up to 128 valid selector-matching rules are retained, including generated
  compatibility rules, before ID overrides are resolved. Later matching rules
  are ignored at the limit; rules for unrelated images do not consume slots.
- Positive and skip conditions have separate eight-condition limits, shared across
  the generic, argument-only and sequence spellings.
- A parsed command line or argument fragment supports up to 512 tokens,
  including its executable token (or the internal fragment placeholder).
- Explicit options on enabled rules must be valid for the action, even at defaults:
  `Occurrences` is only for removal/replacement actions; `Duplicate` is only for Add.
- With Resource Access Monitor active and process monitoring enabled,
  reason-only `CustomProcessCommandLine:` trace messages report invalid or
  oversized rules, relevant-rule overflow, token limits and discarded plans.
  They contain no rule text or argument values and are not persistent popup logs.
- Invalid or oversized individual rules are ignored. Preparation, action or
  publication failure discards the private plan and keeps the original command
  line. This includes argument-pattern preparation failures during actions,
  not just during conditions. Ordinary no-match and unchanged results are not
  reported as failures.
- If Add would insert inside an unterminated quoted argument, the entire plan
  is discarded and the original command line is kept. This applies to appending
  at the end or after that argument; no closing quote is synthesized.

## Examples

```ini
CustomProcessCommandLine=<Special:Chrome>,Add=--disable-background-networking;Skip=--type=*;Match=Pattern
CustomProcessCommandLine=app.exe,Clear=Arguments;Skip=InputArgCount>8
CustomProcessCommandLine=ping.exe,RemoveSequence=-w *;Match=Pattern
CustomProcessCommandLine=app.exe,Set="--mode clean";If=Empty
CustomProcessCommandLine=app.exe,Add=--box=%SANDBOX%;Expand=y
CustomProcessCommandLine=app.exe,Add=--literal=%SANDBOX%;Expand=n
CustomProcessCommandLine=<Browsers>,Remove=--bad-flag
CustomProcessCommandLine=app.exe,Replace=--mode=old;With=--mode=new
CustomProcessCommandLine=app.exe,Remove=--verbose;Occurrences=Last
CustomProcessCommandLine=app.exe,ReplaceSequence=--profile old;With=--profile new;Occurrences=Last
CustomProcessCommandLine=app.exe,Add=--work;IfSequence=--profile "Work profile"
CustomProcessCommandLine=app.exe,Add=--literal;IfArg=Empty
CustomProcessCommandLine=app.exe,Remove=--role=worker
CustomProcessCommandLine=app.exe,Add=--worker-mode;IfArg=--role=worker;ConditionSource=Input
CustomProcessCommandLine=app.exe,Replace=--mode=*;With=--mode=new;Match=Pattern;Occurrences=Last
CustomProcessCommandLine=firefox.exe,Add="-P SSH01";If=-no-remote;Skip=-contentproc
CustomProcessCommandLine=*,Id=CommonMode;Order=400;Add=--common-mode
CustomProcessCommandLine=app.exe,Id=CommonMode;Disabled=y
```
