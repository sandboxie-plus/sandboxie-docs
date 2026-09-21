# Block Network Files

*BlockNetworkFiles* controls access to files and folders on network shares from sandboxed processes. It is a file-path restriction, not a firewall or a block on Internet connections.

## Configuration and defaults

```ini
[DefaultBox]
BlockNetworkFiles=y
```

With `y`, network-share paths start blocked for both reading and writing unless a matching file-access rule permits access. With `n`, they follow normal sandbox file-access rules, which may still restrict them. A separate network policy can also prevent a connection needed to reach a share.

The driver uses `n` as its fallback when no effective value exists, although the setting metadata lists `y` as the default. Normally, newly initialized boxes created by SandMan or Sandboxie Control Classic explicitly receive `BlockNetworkFiles=y`. A box-specific value takes precedence over a value inherited from `[GlobalSettings]`.

## Network-file scope and exceptions

The restriction covers file access through recognized network redirector paths, including ordinary UNC shares and mapped network drives. It applies to network filesystem paths rather than blocking SMB packets or ports. Access through other providers remains subject to the paths Sandboxie recognizes and to other applicable rules.

More specific file-access rules can permit access to selected network paths. For example, a matching `OpenFilePath` can allow direct host-file access, while `ReadFilePath` can allow reading without writes. In rule-specificity mode, `NormalFilePath` can restore normal sandbox file handling for a matched path. These rules can also use supported program or process-group selectors. The result depends on the matching rules and their precedence; an opening rule should not be assumed to override every separate closing rule.

`BlockNetworkFiles` does not replace [Block WinRM](BlockWinRM.md), Internet-access rules, or [WFP Support](../PlusContent/WFPSupport.md). Conversely, setting it to `n` does not guarantee that a share will be reachable when separate network or device restrictions apply.

## User interface

In SandMan, use **Sandbox Options > Network Options > Other Options > Block network files and folders, unless specifically opened.**

When creating a box with advanced options, **Sandbox Isolation options > Network Access > Allow access to network files and folders** has inverted meaning: checked writes `BlockNetworkFiles=n`; unchecked writes `y`. The wizard defaults this access checkbox to unchecked and disables it for hardened box types.

SandMan may display **Net Share** in a box's status when network-file blocking is disabled. The status indicator is not a substitute for checking the effective file and network rules.

Sandboxie Control Classic also provides a network-files checkbox in its Sandbox Settings interface.

## Applying changes

The driver reads this option while initializing each sandboxed process. Restart affected sandboxed processes after changing it; already-running processes do not have their stored value rebuilt by the change. A SandMan, service, or driver restart is not normally needed for newly started processes.

## Version history

The setting metadata does not specify an introduction version. Sandboxie Plus 1.7.1 / Classic 5.62.1 fixed an interaction with `RestrictDevices=y` that had allowed access to mapped network drives despite `BlockNetworkFiles=y` ([issue #2629](https://github.com/sandboxie-plus/Sandboxie/issues/2629)).

## Related pages

- [Block WinRM](BlockWinRM.md)
- [Sandboxie Ini](SandboxieIni.md)
- [WFP Support](../PlusContent/WFPSupport.md)
