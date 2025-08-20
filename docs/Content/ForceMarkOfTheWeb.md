# Force Mark of The Web

_ForceMarkOfTheWeb_ is a global setting in [Sandboxie Ini](SandboxieIni.md). When enabled, it forces all files with the Mark of The Web (MOTW) to be automatically sandboxed in a designated sandbox. This provides enhanced security by ensuring that files downloaded from the internet or received via email are automatically isolated.

## Settings

The feature uses two global settings:

### ForceMarkOfTheWeb

```
[GlobalSettings]
ForceMarkOfTheWeb=y
```

Enables automatic sandboxing of files with the Mark of The Web attribute.

### MarkOfTheWebBox

```
[GlobalSettings]
MarkOfTheWebBox=Web_Box
```

Specifies which sandbox should be used for MOTW files. The default value is `DefaultBox` if not specified.

## What is Mark of The Web?

The Mark of The Web (MOTW) is a security feature in Windows that marks files as having originated from the internet or other untrusted locations. Windows automatically applies this mark to:

- Files downloaded from web browsers
- Email attachments 
- Files extracted from ZIP archives that were downloaded
- Files received through instant messaging applications
- Files copied from network shares marked as internet zones

## Important Notes

- This is a **global setting** that affects all sandboxes on the system
- The specified sandbox must already exist and be enabled in your Sandboxie configuration
- The sandbox name is case-sensitive and must match exactly
- Files that are already running in any sandbox are not affected by this setting

## Troubleshooting

If MOTW files are not being sandboxed:

1. **Verify both settings are configured:**
   - `ForceMarkOfTheWeb=y` is set in `[GlobalSettings]`
   - `MarkOfTheWebBox=SandboxName` points to an existing sandbox
2. **Check sandbox name:** Ensure the sandbox name matches exactly (case-sensitive)
3. **Confirm sandbox exists and is enabled**
4. **Verify files have MOTW attribute:** Use `dir /r filename` to check for `Zone.Identifier` stream

## Similar Settings

- [ForceProcess](ForceProcess.md): Forces specific programs into sandboxes
- [ForceFolder](ForceFolder.md): Forces files from specific folders into sandboxes

## User Interface

This setting can be configured in Sandboxie Plus through:
**Global Settings > Program Control > Force Process Options**

![Force Mark of The Web Settings](../Media/ForceMarkOfTheWeb.png)