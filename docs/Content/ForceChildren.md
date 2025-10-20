# Force Child Processes

`ForceChildren` is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) (introduced in v1.14.5 / 5.69.5) that forces specific child processes of a parent process to start inside a specified sandbox. This is useful when you want any processes launched by a known parent to be automatically sandboxed.

## Syntax

The general form:

```ini
[DefaultBox]

ForceChildren=<program>
```

Where `<program>` may be one of:

- An image path with wildcards, e.g. `C:\Users\*\App\*.exe` — wildcard patterns are matched case-insensitively against canonical paths.
- An image name (without backslashes), e.g. `dopus.exe` — matches by image name using the driver image matching rules.

Notes:

- Paths in `ForceChildren` are canonicalized and normalized (duplicate backslashes removed and reparse points translated) before matching.[^1]
- When a wildcard pattern is used, a pattern matcher is created and matched case-insensitively against the translated path.[^2]

## Behavior and matching rules

- `ForceChildren` entries are evaluated when a new process is created. If a parent process matches a `ForceChildren` rule for any enabled box, the child process will be forced into that box.[^3]

- Matching attempts (in priority order, roughly):

    - The parent's image name is compared to `ForceChildren` entries that are image names or image patterns.[^4]
    - The parent's canonicalized image path and/or working directory may be compared against wildcard path patterns from `ForceChildren` entries (entries containing `*`).[^5]

- Rules that contain wildcards use a pattern engine; rules without wildcards use NLS-aware string comparison and image matching helper routines for correct language-aware checks.[^2][^4]

- A `ForceChildren` match for a box is subject to the box being enabled for the current user/session and having force rules enabled. Settings such as `DisableForceRules` in a box will prevent force rules for that box from being applied.[^6]

- Certain system processes and Sandboxie internals are exempt from forcing. The home directory of Sandboxie is never forced.[^7]

## Examples

1. Force children of a specific parent binary (image name):

    ```ini
    [MyBox]
    
    ForceChildren=parentapp.exe
    ```

2. Use a wildcard pattern to match parent image paths:

    ```ini
    [MyBox]
    
    ForceChildren=C:\Users\*\Downloads\*\app.exe
    ```

## Command-line switches

See [StartCommandLine](StartCommandLine.md#force_children-or-fcp) for details.

### Relevant switches:

- `/force_children` — enable/affect force-children behavior from the command line.
- `/fcp` — shorthand for `/force_children` (where supported).

## Interaction with alerts and other force settings

- `ForceChildren` entries are evaluated along with `ForceFolder` and `ForceProcess` entries when the driver determines which box (if any) a newly-started process should use.

- If alerting is enabled for a matching rule (e.g., when force rules are restricted by policy), the driver may show an alert instead of forcing the process. The driver tracks an "alert" state that can prevent forcing and optionally log or notify the user.[^8]

- The `ForceChildren` setting complements `ForceProcess` (which directly forces named processes regardless of parent) and `ForceFolder` (which forces processes based on folder paths). Use `ForceChildren` when you want to force processes that are spawned by particular parents.

## Implementation notes (driver behavior)

- The driver builds an in-memory list of force rules per enabled box at process-creation time. Each `ForceChildren` entry is translated into an internal `FORCE_ENTRY` element, which either stores a canonicalized path or a compiled PATTERN when wildcards are present.[^2]

- When matching by image name the driver uses a helper `Process_MatchImage` which implements language-aware and image-name-specific matching logic.[^4]

- The code ensures duplicate backslashes are removed and reparse points are resolved before use; translation to NT-style paths is performed where possible. If translation cannot be performed, the original path is used for matching.[^1][^5]

## See also

- [ForceProcess](ForceProcess.md) — force processes by name or path.
- [ForceFolder](ForceFolder.md) — force processes by folder path or pattern.
- [DisableForceRules](DisableForceRules.md) — per-box setting to disable all force rules for a box.

## GUI (Sandboxie Manager / SandMan)

### Where to find it:

- Open Sandboxie Manager (SandMan).
- Open the sandbox's options: right-click a sandbox and choose "Sandbox Options".
- In the Options window locate the Program Control / Force Programs area where forced entries are listed.

### How to add a Force Children entry:

1. In the Options window Program Control / Force Programs area you'll see a list of forced entries and the buttons "Force  Program", "Force Children" and "Force Folder".
2. Click "Force Children" to add an entry by selecting an executable (or use the Browse variant which opens a file dialog).
3. The item appears in the list with the type label "Children". Checked entries are saved to `ForceChildren`; unchecked entries  are saved to `ForceChildrenDisabled`.
4. To remove an entry select it and click "Remove".

### Notes and references:

- The UI tree widget is `ui.treeForced` in `OptionsWindow.ui`. The Options window loads/saves these lists in `OptionsForce.cpp`  (LoadForced/SaveForced/AddForcedEntry).
- The "Disable forced Process and Folder for this sandbox" checkbox shown on the same page is `ui.chkDisableForced` and maps to the `DisableForceRules` setting.

## Footnotes

[^1]: The driver removes duplicate backslashes and translates reparse points before storing entries. See how `Process_AddForceFolders` normalizes `expnd` into `buf` and calls `File_TranslateReparsePoints`.

[^2]: Wildcard entries create a PATTERN object using `Pattern_Create` and are matched with `Pattern_Match` against a lowercased canonical path.

[^3]: `Process_FcpInsert`, `Process_FcpCheck`, and related routines implement parent-based forcing maps so newly created child processes can be added to a map keyed by PID and later checked during child creation.

[^4]: Image-name matching delegates to `Process_MatchImage` (used by the driver when entries don't contain backslashes).

[^5]: The driver translates DOS-style paths to NT-style paths using `Process_TranslateDosToNt` which wraps `File_TranslateDosToNt` and falls back to copying the original if translation fails with a syntax error.

[^6]: Only boxes that are enabled for the current SID/session and that don't have `DisableForceRules` set are considered when building the force-data lists.

[^7]: Paths under the Sandboxie home directory are excluded from forcing; the code explicitly checks and skips matches under `Driver_HomePathNt`.

[^8]: When alerting rules match, the driver may set an alert state (`IsAlert`) and defer forcing. Alerts may produce logged messages and, depending on settings, can prevent the process from starting under a box.
