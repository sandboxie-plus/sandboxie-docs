# Advanced Loader and SxS Compatibility

These advanced settings address specific process-creation, Side-by-Side (SxS) activation-context, early DLL-loading, and Windows-version compatibility problems. They are troubleshooting controls, not general security improvements or a way to reproduce a different Windows installation.

| Setting | Current scope |
| --- | --- |
| `PreferExternalManifest` | Selects Sandboxie's dummy-manifest workaround by the **child executable** being created. |
| `ExternalManifestHack` | Selects that workaround by the **sandboxed parent** creating the child. |
| `DisableBoxedWinSxS` | Uses an alternate activation-context path instead of Sandboxie's boxed SxS service for matching processes. |
| `DelayLoadDll` | Makes a named DLL unavailable during early process initialization and records its path. |
| `OverrideOsBuild` | Changes results from selected version-query APIs in a sandboxed process. |

## Manifest compatibility during process creation

`PreferExternalManifest` is disabled by default. Despite its name, it does not simply tell Windows to prefer an application's own external `.manifest` file. When enabled for a child executable, Sandboxie can intercept opens of that child's manifest or configuration file during process creation and substitute files shipped with Sandboxie. It can also redirect relevant SxS registry access to Sandboxie's service-side compatibility key. The application's actual manifest is not edited.

When Sandboxie's process-creation path marks the child as `asInvoker`—for example, after finding an explicit `requestedExecutionLevel`—the substituted files are a small `asInvoker` manifest and a minimal configuration file. Otherwise Sandboxie substitutes an empty file so that Windows can still apply its UAC elevation heuristics. These substitutions are specific to the process-creation compatibility path, not a general replacement of all application manifests.

For example:

```ini
[DefaultBox]
PreferExternalManifest=legacyapp.exe,y
```

The optional executable selector refers to the **child being created**. A box-wide `PreferExternalManifest=y` enables the workaround generally; a more specific `legacyapp.exe,n` can turn it off for that child. Normal box, global, and enabled-template configuration lookup applies.

`ExternalManifestHack` is a separate, disabled-by-default way to select the same compatibility path:

```ini
[DefaultBox]
ExternalManifestHack=parent.exe,y
```

Here the selector refers to the **already-running sandboxed parent** that creates the child, not to the child. If the parent matches an enabled `ExternalManifestHack` rule, the workaround is selected before the child-oriented `PreferExternalManifest` check. Therefore these two executable-qualified settings are not interchangeable. The parent-oriented option was added for an Edge compatibility case following Windows 11 KB5014019; the old Edge template entries are currently commented out and should not be treated as active defaults.

The current image-aware lookup also accepts wildcard patterns and configured process groups. Use executable-qualified rules only for applications that need the workaround; a specific matching value can take precedence over a general value.

## `DisableBoxedWinSxS`

Sandboxie's normal `CreateActCtxW` handling can ask its boxed RpcSs SxS service to generate activation-context data. `DisableBoxedWinSxS=y` is a compatibility alternative to that route, **not** a switch that turns off WinSxS assemblies. For matching processes, SbieDll instead calls the system `CreateActCtxW` path, translating a sandboxed source-file path when needed.

```ini
[DefaultBox]
DisableBoxedWinSxS=explorer.exe,y
```

The SbieDll choice is image-aware, even though the setting metadata describes only a box-wide boolean. Shipped ARM64 compatibility templates use executable-qualified values. The alternate path is also selected automatically inside SandboxieRpcSs itself and for processes with an AppContainer token.

There is a second consumer in boxed RpcSs. At startup it reads an ordinary effective boolean for `DisableBoxedWinSxS`; a box-wide `y` prevents its `RPCSS_SXS` service thread from initializing. This lookup does **not** perform the same executable-name matching as SbieDll. A process-qualified entry should therefore be understood as selecting the alternate path for matching processes, not as a reliable way to disable the boxed SxS service for the entire box.

## `DelayLoadDll`

`DelayLoadDll` takes a DLL **basename**, with case-insensitive exact matching; the current driver check does not implement path or wildcard matching:

```ini
[DefaultBox]
DelayLoadDll=guard64.dll
```

Before SbieDll has initialized in a newly starting process, a matching DLL open is made to appear as though the file does not exist. The driver records the DLL's full path in a per-process queue, and an API exists to retrieve queued paths. However, no current in-tree caller of that API—or other current in-tree path that completes the intended later DLL load—was found. Do not rely on `DelayLoadDll` as a guarantee that the DLL will subsequently be loaded. Existing compatibility templates still contain entries for products such as Comodo, ThreatFire, and Logitech Process Monitor; their presence does not establish that a later-load path remains active.

## `OverrideOsBuild`

`OverrideOsBuild` accepts a decimal Windows **build number**, optionally qualified by the executable being started:

```ini
[DefaultBox]
OverrideOsBuild=legacyapp.exe,7601
```

For a box-wide value, use `OverrideOsBuild=7601`. The current parser uses `_wtoi()`; a full version string such as `10.0.19045.6216` is **not** valid build-number syntax—it would be parsed as the initial number `10`. When the parsed build is nonzero, SbieDll hooks `RtlGetVersion`, `GetVersionExW`, and `GetVersionExA` for that process.

Sandboxie reports the configured build number through those hooks and derives a corresponding major/minor version and service-pack level. For example, build `7601` maps to Windows 7 SP1 (`6.1`), `9200` to Windows 8 (`6.2`), `9600` to Windows 8.1 (`6.3`), and builds above `9600` to major/minor `10.0`. This does not change the actual OS, available APIs, product edition, or build revision. It also does not cover every version-detection method; `VerifyVersionInfoW` is not hooked by this mechanism.

The executable selector is matched against the sandboxed process whose version-query APIs are hooked. Normal box, global, and enabled-template lookup applies, with a matching image-specific value preferred over a general value.

## SandMan configuration

The box-wide `PreferExternalManifest` checkbox is under **Sandbox Options > Various Options > Compatibility**, labeled **Force usage of custom dummy Manifest files (legacy behaviour)**. It is unchecked by default.

Executable-qualified `PreferExternalManifest` entries and general or executable-qualified `ExternalManifestHack` entries are available in **Sandbox Options > Advanced Options > Miscellaneous** through the advanced **Add Option** editor. `ExternalManifestHack` has no dedicated checkbox. That editor can show entries inherited from templates separately.

The current SandMan special-options list has no dedicated controls for `DisableBoxedWinSxS`, `DelayLoadDll`, or `OverrideOsBuild`; configure them in [Sandboxie Ini](SandboxieIni.md) or through an applicable compatibility template. A template's presence does not mean the setting applies unless that template is enabled.

## Applying changes

The manifest workaround is queried during child-process creation. After a configuration reload, a running sandboxed parent can use changed `PreferExternalManifest` or `ExternalManifestHack` rules for later children; an already created child is unaffected.

The `DisableBoxedWinSxS` alternate-path decision is made during SbieDll initialization. Restart affected sandboxed processes after changing it. For a box-wide change that controls the boxed RpcSs SxS thread, recreate the sandbox process tree so RpcSs starts with the new value.

`DelayLoadDll` is checked by the driver only on qualifying DLL opens before SbieDll initialization, so changes chiefly matter to newly starting processes. `OverrideOsBuild` installs its hooks during process initialization; restart affected processes after changing it. Neither setting retroactively changes an already loaded DLL or an already initialized process.

## Version history

- Sandboxie Plus 0.4.5 / Classic 5.44.1 disabled the older application-manifest hack by default; `PreferExternalManifest=y` retained that legacy behavior.
- Plus 0.7.2 / Classic 5.49.0 added `OverrideOsBuild=7601`; Plus 0.7.5 / Classic 5.49.8 added per-process `PreferExternalManifest` configuration.
- Plus 1.0.3 / Classic 5.55.3 fixed a `GetVersionExW` issue affecting `OverrideOsBuild`.
- Plus 1.1.1 / Classic 5.56.1 improved `PreferExternalManifest` and fixed an Edge issue after KB5014019. Current metadata lists `ExternalManifestHack` as added in 1.1.2.

The current metadata does not establish an introduction version for `DisableBoxedWinSxS` or `DelayLoadDll`. In particular, metadata descriptions for `PreferExternalManifest` and `DisableBoxedWinSxS` are broader than their current executable behavior.

## Related pages

- [Sandboxie Ini](SandboxieIni.md)
- [RPC Compatibility](RpcCompatibility.md)
- [Code Injection](CodeInjection.md)
