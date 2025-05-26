# Fake Admin Rights

**FakeAdminRights** is a sandbox setting in [Sandboxie Ini](SandboxieIni.md) available since 0.7.1 / 5.48.5. It specifies whether Sandboxie will simulate Administrator rights for programs running in this sandbox.

## Syntax

```ini
FakeAdminRights=[process,]y|n
```

* **process** (optional): The name of the executable to which the rule applies. If omitted, the rule applies to all sandboxed applications.
* **y|n**:

    - `y` enables fake admin rights for the specified process (or all processes if none specified)  
    - `n` disables fake admin rights for the specified process  


This option is recommended to be used in combination with [DropAdminRights](DropAdminRights.md) to improve security. Most installers should still work with both options enabled.

## Usage Examples

### 1. Enable Fake Admin Rights for All Sandboxed Programs

This makes all applications in the sandbox believe they have administrator privileges:

```ini
[DefaultBox]
FakeAdminRights=y
```

### 2. Enable Fake Admin Rights for a Specific Installer

Some installers require admin rights to proceed. This grants fake admin rights only to `installer.exe` while other programs run normally:

```ini
[DefaultBox]
FakeAdminRights=installer.exe,y
```

### 3. Enable Fake Admin Rights Globally But Disable for Security-Sensitive Programs

This configuration gives fake admin rights to all programs except security-sensitive ones like `CredentialUIBroker.exe`:

```ini
[DefaultBox]
FakeAdminRights=y
FakeAdminRights=CredentialUIBroker.exe,n
```

### 4. Using Negation (!) to Reverse Rules

You can use `!` to reverse the logic of a rule. This is particularly useful for creating exceptions:

```ini
[DefaultBox]
FakeAdminRights=!Start.exe,y
```

This means "enable fake admin rights for all programs EXCEPT Start.exe".

These examples demonstrate:

1. Global fake admin rights
2. Targeted fake admin rights for specific applications
3. A mixed approach for compatibility with security-sensitive programs
4. Using negation for exception-based rules

The third example is particularly useful when most programs need elevated privileges but certain system components must run with real permissions to function correctly.

### What does FakeAdmin do?

When **FakeAdmin** is enabled:

- The sandboxed process is tricked into believing it is running with administrator privileges.
- This is useful for testing or running applications that require admin rights, without granting them actual admin access.
- It helps with compatibility for programs that check for admin rights but don't really need them to function.

## Related Configuration

This setting corresponds to the GUI option in **Sandboxie Plus** under the following path:

**Sandbox Options** > **Security Options** > **Security Hardening**: _Make applications think they are running elevated (allows to run installers safely)_

**Sandbox Options** > **Advanced Options** > **Miscellaneous** > **Add Option**: _FakeAdminRights_
