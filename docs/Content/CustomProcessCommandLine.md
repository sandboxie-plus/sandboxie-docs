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

The compatibility settings CustomChromiumFlags and InjectCmdLine retain their
existing literal payload behavior.

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

Legacy `InjectCmdLine` and `CustomChromiumFlags` actions retain their existing
behavior and participate in PEB publication with the default `y` mode.

## Notes

- All effective sandbox, template, and global rules are collected before execution.
- Conditions inspect the command line produced by earlier ordered rules unless ConditionSource=Input is selected.
- Invalid rules are ignored without partially modifying the command line.
- The final command line is published only after the complete plan succeeds.
- `CustomChromiumFlags` uses the same transformation path.

## Legacy InjectCmdLine

`InjectCmdLine` permits duplicate arguments. To preserve that behavior when
replacing a rule, include `Duplicate=Allow`:

```ini
CustomProcessCommandLine=app.exe,Add=--foo;At=Start;Duplicate=Allow;Skip=--type=*;Match=Pattern
```

Without `Duplicate=Allow`, the default `Duplicate=Skip` suppresses an addition
when the argument sequence is already present. Unlike the first-matching
legacy setting, multiple matching generic rules are cumulative.

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

## Regression Scenarios

These scenarios are specified for future native validation and **have not been
executed**. Static source checks do not prove Windows runtime behavior.

| Case | Setup and input | Expected result |
| --- | --- | --- |
| Relevant budget | 128 distinct valid other.exe rules, then app.exe Add=--wanted | app.exe still receives --wanted. |
| Actual overflow | 129 valid matching rules, no compatibility rules | First 128 retained; one reason-only overflow trace, with later rules ignored. |
| Strict options | Add=--x;Occurrences=All or Remove=--x;Duplicate=Skip | Invalid rule ignored and diagnosed; other valid rules can still run. |
| Existing exact matching | Input app.exe a A; Remove=a | app.exe A, preserving default case sensitivity and argv0. |
| Existing replacement | Input app.exe a a; Replace=a;With=a b | app.exe a b a b; inserted matches are not revisited. |
| Sequence replacement All | Input app.exe a b a b; ReplaceSequence=a b;With=a b z | app.exe a b z a b z, without rescanning inserted tokens. |
| Sequence replacement First/Last | Input app.exe a a a b; ReplaceSequence=a a;With=x | First gives app.exe x a b; Last gives app.exe a x b. |
| Existing overlapping Last removal | Input app.exe "a" a a b; RemoveSequence=a a;Occurrences=Last | app.exe "a" b; the first raw quoted token is preserved. |
| Contiguous conditions | Input app.exe --profile "Work profile"; IfSequence=--profile "Work profile" | Positive matches; the corresponding SkipSequence suppresses an action. Separated tokens do not match. |
| Literal reserved names | Input app.exe Empty ArgCount; IfArg=Empty and IfArg=ArgCount | Both are literal argument checks, not reserved predicates. |
| Source selection | Remove=--role=worker before Add=--worker;IfArg=--role=worker | Current does not add; ConditionSource=Input adds after removal. |
| Source counts | Input has one argument, then Clear=Arguments; later If=ArgCount=1 | Current is false, Input is true; InputArgCount=1 remains true for either source. |
| Combined condition limits | Eight positive or eight skip fields mixing all spellings; then a ninth | Eight accepted, ninth invalidates that rule; positive and skip counters remain independent. |
| Case/pattern options | Quoted sequence values, Match=Pattern or Match=Text, CaseSensitive=n | Each decoded element uses the requested existing match/case semantics. |
| Token limit | Command line or fragment exceeds 512 tokens including executable/placeholder | No partial plan is published; token-limit and discard diagnostics are monitor-only. |
| Condition preparation failure | Allocation-failure injection during a positive or skip predicate | Entire private plan discarded; failure must not turn a skip into permission. Requires a native fault-injection harness. |
| Action preparation failure | An earlier Add has applied; inject a matching-preparation failure in Remove/Replace with First/Last/All, or in Add Before/After | Entire private plan discarded, including earlier edits and ID results; Last must not fall back to an earlier match. Requires a native fault-injection harness. |
| Add quote boundary | Input app.exe "old; Add=--new, or Add=--new;After=old | Entire plan discarded; original text retained without a merged argument, applied ID or Stop. |
| Add quoted trailing backslash | Input app.exe "old\; Add=--new | Entire plan discarded; no closing quote is synthesized and the trailing backslash is retained. |
| Existing Add placement | Input app.exe "old value" tail; Add=--new with At=Start, At=End, Before=tail or After=tail | A separate --new argument is inserted at the requested position; "old value" and tail remain unchanged. |
| Legacy duplicate handling | Input app.exe --foo; compare InjectCmdLine=app.exe,--foo with the generic replacement above | Both contain two --foo arguments; the generic form with default Duplicate=Skip instead retains one. |
| Applied gate | Input app.exe --safe-profile with the SafeProfile example above | app.exe --disable-plugins --verbose; alternative skipped. Without the marker: app.exe --normal-mode. |
| Unknown/disabled/skipped gate | A child refers to an ID that is missing, suppressed by a local tombstone, or skipped by conditions | If is false; Skip does not suppress. No inherited shadowed action activates the gate. |
| Case and source independence | Gate ID SafeProfile, reference Id:safeprofile with CaseSensitive=y and ConditionSource=Input | The earlier applied gate is still found case-insensitively. |
| Duplicate Add gate | Input already contains the Add fragment and Duplicate=Skip remains default | Gate is not applied; its If children do not run. Duplicate=Allow reports applied normally. |
| No net change gate | Clear on an empty argument list, Set to the same list, or matching same-value Replace before a child | Existing applied reporting activates the child even when the gate alone would not change the final text. |
| Later/self/cyclic reference | A rule references itself or an ID that executes later; rules mutually depend only on each other | No deferred or recursive evaluation; unseen IDs are false. A Skip to a later ID does not suppress the earlier rule. |
| Inheritance and order | Local rule replaces an inherited same-ID rule; children execute after the selected rule by Order | Only the effective selected rule can activate that ID; equal orders retain effective sequence. |
| Stop and rollback | Gate has Stop=y, or a later required condition/action/publication fails | Stop prevents children; failures publish none of the private plan and retain no gate state. |
| Default PEB publication | Input app.exe; Add=--visible without UpdatePEB | API and PEB both expose app.exe --visible, including legacy InjectCmdLine and CustomChromiumFlags actions. |
| Selective PEB publication | Input app.exe; Add=--api-only;UpdatePEB=n, then Add=--visible | API contains both arguments; PEB contains only --visible. |
| Keep original PEB | An applied action uses UpdatePEB=KeepOriginal alongside y and n actions | API contains all applied actions; PEB remains exactly original. |
| Applied-only PEB control | A KeepOriginal or n rule is disabled, condition-skipped, duplicate-skipped, or follows an applied Stop=y | That rule has no publication effect. |
| Full-state PEB eligibility | Add=--marker;UpdatePEB=n before Add=--visible;IfArg=--marker | Both actions apply in API state; PEB contains only --visible without rechecking the condition. |
| Selective action rematching | Order=100;Add=--marker;UpdatePEB=n before Order=200;Replace=--marker;With=--replaced | API contains --replaced; PEB remains original because the replacement has no matching argument there. |
| PEB-only net change | Input app.exe; Order=100;Add=--x, then Order=200;Remove=--x;UpdatePEB=n | API text equals input; PEB still publishes app.exe --x. |
| PEB option validation | UpdatePEB=Y, UpdatePEB=N, or UpdatePEB=keeporiginal; invalid value or repeated UpdatePEB | Values are case-insensitive; invalid or repeated fields invalidate the rule. |
| PEB preparation rollback | Fail selective-state allocation, action preparation, length validation, or ANSI conversion | Neither API nor PEB changes are published. Requires native fault injection for allocation/conversion failures. |
| Preserved process flag | ForcedChild If/Skip conditions with the forced-child flag set or unset | Existing local flag-based matching remains active with every PEB mode. |
| Executable quoting | Input "C:\dir\" arg; Remove=arg | Only arg is removed; the executable token, including its trailing backslash and quotes, is preserved. |
| Ordinary argument escaping | Input app.exe "C:\dir\\" arg; Remove=arg | The ordinary quoted argument retains its original escaping and decodes to C:\dir\. |
| Expanded Add/Set/With | Use a process variable pointing to a path with spaces in individually quoted Add, Set, Replace With, and ReplaceSequence With payloads | The expanded path is used; unknown variables remain literal. |
| Sandboxie variables | Add="--box=%SANDBOX%" and With="%SBIEHOME%" | Existing Sandboxie variable expansion is used without changing selectors or matching patterns. |
| Expansion grammar isolation | A variable contains commas or semicolons followed by Id= or Stop=; expand it in Add or With | The text remains in the action payload and cannot create rule fields. |
| Expansion control | Add, Set, Replace With, and ReplaceSequence With payloads contain process and Sandboxie variables; compare omitted Expand, Expand=y, and Expand=n | Omitted/y expands; n preserves the payload literally, with no expansion queries or failure diagnostic. Matching patterns and conditions stay unchanged. |
| Expansion option validation | Add=--x;Expand=invalid, repeated Expand fields, or explicit Expand on Clear, Remove, RemoveSequence, or a disabled ID-only rule | Invalid rule is ignored and diagnosed; other valid rules remain eligible. |
| Literal fallback status | An otherwise valid payload has a failed driver-variable query, including an unknown variable or a driver-collapsed generic failure | The original token is retained; API/PEB use the same prepared payload; one status/outcome-only fallback diagnostic is emitted for that payload. |
| Expansion buffer rollback | Inject STATUS_BUFFER_TOO_SMALL/STATUS_BUFFER_OVERFLOW or exhaust local expansion capacity after another planned rule | Entire plan is discarded before API/PEB publication; a status/outcome-only discard diagnostic is emitted. Requires native fault injection for reported query errors. |
| Expansion failure precedence | A payload first has ordinary fallback, then a fatal query-buffer or local capacity failure | Fatal status replaces the earlier fallback status; no private plan is published and no duplicate generic preparation diagnostic is emitted. |
| Successful expansion diagnostics | Expand an existing environment/Sandboxie variable successfully, or use a payload without percent tokens | Existing expanded/literal behavior remains; no expansion-failure diagnostic is emitted. |
| Expanded PEB replay | An expanded Add uses UpdatePEB=y after an API-only action | API and PEB use the same prepared payload; replay does not expand it again. |
| Existing compatibility payloads | CustomChromiumFlags or InjectCmdLine contains %SANDBOX% | The compatibility setting retains its previous literal behavior. |
| Nested special group | A selected ProcessGroup contains a nested group containing <Special:Chrome> and an ordinary image pattern | Special and ordinary selectors still match through the shared traversal; legacy group callers retain their previous matching and depth behavior. |
| Program runner expansion | RunProgram uses process and Sandboxie variables, unknown variables, or an empty command | Existing expansion, unknown-variable fallback, empty-command rejection, and launch timeout behavior are retained. |
