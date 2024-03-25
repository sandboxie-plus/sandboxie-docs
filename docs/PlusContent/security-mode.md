# Security Hardened Mode

**NOTE: This feature requires a [supporter certificate](https://sandboxie-plus.com/supporter-certificate/).**

The security hardened box and the concept of security hardened mode was introduced in **Sandboxie Plus v1.3.0**. It restricts NT syscall elevation to approved known safe/filtered syscalls. It also provides device security by restricting device access to known safe/filtered endpoints.

The setting for a security hardened box can be enabled by adding `UseSecurityMode=y` to the box settings section of **[Sandboxie Ini](../Content/SandboxieIni.md)**. It can also be enabled in the Sandman UI. Right-click on a box and select "Sandbox Options" from the drop-down menu (or simply double-click on a box) to bring up the Box Options UI. Select the box type preset as "Security Hardened Sandbox" (with an **orange** box icon) and click OK to apply changes. The status column of Sandman UI labels this box as **Enhanced Isolation**.

![](../Media/Box_SecurityMode.png)

Internally, the security hardened mode is based on four settings:

```
DropAdminRights=y
RestrictDevices=y
SysCallLockDown=y
UseRuleSpecificity=y
```

1. **[DropAdminRights](../Content/DropAdminRights.md):** Prior to **Sandboxie Plus v1.3.0**, any box with `DropAdminRights=y` was considered **hardened** and labeled "Enhanced Isolation" in the Sandman UI status column. Starting with **Sandboxie Plus v1.3.0**, only boxes with `UseSecurityMode=y` have their status listed as "Enhanced Isolation".

2. **SysCallLockDown:** The setting `SysCallLockDown=y` limits the use of NT system calls. Only those calls that are included as defaults in the file **Templates.ini** or calls configured in the [GlobalSettings] section of **[Sandboxie Ini](../Content/SandboxieIni.md)** as `ApproveWinNtSysCall=...` or `ApproveWin32SysCall=...` are executed with the original token. Any NT syscalls that are not approved are executed with the sandboxed token and may break compatibility in certain scenarios. To find which syscalls may be needed to make a particular program work is tedious and involves trial and error.  But once these syscalls are found, they can be added to the [GlobalSettings] section of **[Sandboxie Ini](../Content/SandboxieIni.md)**. Note that **the configuration must be reloaded using "Options -> Reload configuration" for these settings to take effect**.

3. **RestrictDevices:** An earlier **"DeviceSecurity"** template was replaced by a dedicated setting `RestrictDevices=y` in **Sandboxie Plus v1.3.0** to harden box security even further. A security enhanced sandbox does not have access to drivers installed on the host. However, the use of appropriate **[Normal](../Content/NormalFilePath.md)** path directives can allow one to open specific devices as needed.

4. **[Rule Specificity](../PlusContent/RuleSpecificity.md):** The setting `UseRuleSpecificity=y` allows rules to be prioritized based on their "specificity". When rule specificity is combined with `Normal[File/Key/Ipc]Path` entries, selected subpaths can be made readable/writeable while parent paths are still protected. A security hardened box works in a **default allow** mode: every path is a `Normal[File/Key/Ipc]Path` (which allows read/write changes to a sandbox) unless specifically blocked by an overriding rule.

**Comparison with Other Box Types:** RuleSpecificity along with `Normal[File/Key/Ipc]Path` entries is also used in **blue** ([privacy enhanced](../PlusContent/privacy-mode.md)) boxes and in **red** boxes (that combine enhanced privacy and enhanced security). These two box types work in a **default block** mode: all drive paths are set to `WriteFilePath`. This hides all files and folders outside the sandbox, but allows new files and folders to be created in the sandbox (unless specifically allowed by an overriding rule).

**Recent Changes:** Starting with **Sandboxie Plus v1.8.0**, all built-in access rules for a security hardened box have been moved to a dedicated template (included in the file **Templates.ini** under the `[TemplateSModPaths]` section) for easier management.
