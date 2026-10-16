# Default Folder

_DefaultFolder_ is a repeatable sandbox setting in [Sandboxie Ini](SandboxieIni.md), available since Sandboxie Plus 1.15.12 / Classic 5.70.12. It requests directory preparation within the sandboxed filesystem view during eligible process initialization when [Privacy Mode](../PlusContent/privacy-mode.md) is enabled. Sandboxie attempts to create the directories when path and access conditions permit; their existence is not guaranteed.

## Usage

```ini
[DefaultBox]

DefaultFolder=%SystemRoot%
DefaultFolder=%USERPROFILE%
DefaultFolder=%APPDATA%\MyApplication
DefaultFolder=C:\SomeSpecificPath
```

Custom entries use the initializing process's Windows environment. Even familiar variables such as `%USERPROFILE%` and `%APPDATA%` depend on that environment; they are not necessarily taken from the unsandboxed interactive user's session.

In SandMan, enter these values through **Sandbox Options > Edit ini Section > Edit ini**. Privacy Mode is a separate control under **Sandbox Options > Resource Access > Access Policies**. Sandboxie Control Classic provides **Configure > Edit Configuration**. These editors save configuration; they do not themselves create the directories.

## Overview

When a sandbox operates in Privacy Mode (`UsePrivacyMode=y`), many host locations are hidden from applications, but programs may still expect common directory structures to exist. `DefaultFolder` can help prepare those structures without copying the host directories' file contents.

Preparation occurs during eligible sandboxed process initialization, not just when a box definition is created. Restricted-token and AppContainer-token conditions can exclude this customization step, and earlier initialization failures can prevent it. Later eligible processes may attempt preparation again; this is not a one-time box operation.

## How It Works

Sandboxie processes two lists in order during eligible Privacy Mode process initialization[^1]:

1. **Built-in defaults**: Sandboxie explicitly reads the `DefaultFolder` entries in `[TemplateDefaultFolders]`. They use Sandboxie's configuration expansion, including Registry-backed folder substitutions. This special section does not require enabling an ordinary template with `Template=DefaultFolders`.
2. **Custom effective configuration**: Sandboxie reads applicable sandbox, enabled-template, and `GlobalSettings` entries. Sandboxie's own variable expansion is suppressed for this list; the consumer instead uses Windows `ExpandEnvironmentStringsW` and then translates the resulting path.

Both paths attempt creation through the existing sandbox filesystem mapping. Applicable file-path rules still apply: an open path skips boxed directory creation, while a closed path is rejected. Other applicable paths can have missing directory ancestors created, and existing directories can be reused when their access and deletion state permit.

A failed configuration query ends the current list. In particular, a built-in expansion failure can stop the remaining built-in entries; the separate custom list still follows. Invalid custom expansion or translation results are skipped individually. Returned directory-creation failures do not stop later entries and are not treated as fatal process-initialization errors by this routine.

## Template Integration

The shipped `[TemplateDefaultFolders]` section in `Templates.ini`[^2] supplies a maintained list of system, user-profile, public, application-data, and Windows-related directories. The list can change between releases; neither every placeholder nor every directory is usable on every installation or under every process identity.

A local section with the same name can contribute entries rather than replace the entire shipped list. Ordinary customization should use `DefaultFolder` values in the sandbox's configuration.

The examples below belong to this built-in list. Names such as `%Desktop%`, `%Personal%`, and the GUID-style placeholders use Sandboxie's Registry-backed folder information. They are not automatically Windows environment variables for custom entries: a custom `DefaultFolder=%Desktop%` requires an actual `Desktop` environment variable in the initializing process.

### System Directories

- `%SystemRoot%` (Windows directory)
- `%TEMP%` (Temporary files)
- `%ProgramFiles%` and `%ProgramFiles(x86)%`
- `%CommonProgramFiles%` and `%CommonProgramFiles(x86)%`

### User Profile Directories

- `%USERPROFILE%` (User profile root)
- `%Desktop%` (User desktop)
- `%Personal%` (Documents folder)
- `%{374DE290-123F-4565-9164-39C4925E467B}%` (Downloads folder)
- `%Favorites%` (Internet favorites)
- `%{BFB9D5E0-C6A9-404C-B2B2-AE6DB6AF4968}%` (Links folder)
- `%My Music%`, `%My Pictures%`, `%My Video%` (Media folders)
- `%{4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}%` (Saved Games)
- `%LOCALAPPDATA%` (Local application data)

### Public Directories

- `%PUBLIC%` and its subdirectories

## Use Cases

- **Privacy Mode**: Prepare directory structures that applications may expect when host locations are hidden.
- **Application Compatibility**: Help applications that check for standard directories, without guaranteeing compatibility.
- **Custom Application Directories**: Request application-specific directories in the sandboxed view.

## Limitations

- Preparation requires Privacy Mode and an eligible process initialization.
- Custom entries must expand to usable paths, such as absolute drive-letter or ordinary UNC paths. Relative or unsupported path forms can fail translation; successful translation does not guarantee creation.
- Custom expansion uses a fixed-size output buffer. Unsuccessful or oversized results, and any result still containing `%`, are skipped. This also rejects literal percent characters. Do not rely on recursive or unlimited expansion.
- Creation remains subject to file-path rules, filesystem permissions, conflicts with existing files, sharing or deletion state, and available storage.
- Creation is best effort, not transactional: some parent directories can remain after a later failure, with no guaranteed rollback or recovery.

`DefaultFolder` is not an access-rule exemption. It does not disable Privacy Mode, override closed paths or Windows permission checks, change host filesystem ACLs, or grant access to host file contents. New boxed directories can receive their own security descriptors; that is distinct from changing host permissions. A created directory does not prove that later application access will succeed.

## Examples

### Custom Application Directory

```ini
[ApplicationBox]

UsePrivacyMode=y
DefaultFolder=C:\MyApp\Data
DefaultFolder=%APPDATA%\MyApplication
```

Expansion, sandbox mapping, and applicable access conditions still determine whether these requests succeed.

Apply changes through the normal configuration save/reload workflow, then start a new eligible sandboxed process. Restarting an affected application can provide that opportunity; an ordinary `DefaultFolder` change does not inherently require restarting SbieSvc, the driver, or Windows. Already initialized processes do not automatically reprocess the list. Removing an entry does not delete an existing directory, and reload does not reconcile filesystem contents. A later eligible process can retry an unsuccessful preparation attempt, without a guarantee of success.

## Related Settings

- [UsePrivacyMode](UsePrivacyMode.md) - Enables Privacy Mode, required for this preparation routine.
- [NormalFilePath](NormalFilePath.md) - Applies normal sandbox file-path policy to matching paths.
- [FileRootPath](FileRootPath.md) - Configures the sandbox file-container root.

[^1]: [`File_CreateBaseFolders()`](https://github.com/sandboxie-plus/Sandboxie/blob/0863e12a68b7d7d452be1d90eb4f1960aaba6751/Sandboxie/core/dll/file_dir.c#L3550-L3594) processes the explicitly queried defaults followed by custom effective values. See also the [Privacy Mode caller](https://github.com/sandboxie-plus/Sandboxie/blob/0863e12a68b7d7d452be1d90eb4f1960aaba6751/Sandboxie/core/dll/custom.c#L74-L86) and [process eligibility check](https://github.com/sandboxie-plus/Sandboxie/blob/0863e12a68b7d7d452be1d90eb4f1960aaba6751/Sandboxie/core/dll/dllmain.c#L529-L550).

[^2]: The maintained [`[TemplateDefaultFolders]` section](https://github.com/sandboxie-plus/Sandboxie/blob/0863e12a68b7d7d452be1d90eb4f1960aaba6751/Sandboxie/install/Templates.ini#L440-L680) supplies the built-in directory list.
