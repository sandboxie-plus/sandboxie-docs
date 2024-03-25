# Configuration Protection

Initially, anyone operating [Sandboxie Control](SandboxieControl.md) can change any aspect of the Sandboxie configuration, which is stored in the [Sandboxie Ini](SandboxieIni.md) configuration file. Additionally, anyone with access to the configuration text file can also manipulate the configuration and reload it into Sandboxie.

It is possible to activate protection of [Sandboxie Ini](SandboxieIni.md) configuration file from unauthorized changes. Sandboxie offers two modes of protection:

*   Only Administrator user accounts can make changes (See also: [EditAdminOnly](EditAdminOnly.md).)

*   Password must be entered in order to make changes (See also: [EditPassword](EditPassword.md).)

Either or both modes can be active at the same time.

The protection applies to the **Global Settings**, **Sandbox Settings** and **Template Settings** sections of the [Sandboxie Ini](SandboxieIni.md) configuration file. It does not apply to any **User Settings** sections, which store per-user preferences.

To activate the protection, use the [Sandboxie Control > Configure menu > Lock Configuration](ConfigureMenu.md#lock-configuration) command.

* * *

To prevent circumvention of the protection, please consider the following points:

**Placement of the configuration file:** As discussed in the [Sandboxie Ini](SandboxieIni.md) page, Sandboxie looks for its configuration file in the Windows folder first, and in the Sandboxie installation folder second. The protection should be applied to a configuration file that is located in the Windows folder.

If the protection is applied to the configuration file in the Sandboxie installation folder, an attacker might create an empty configuration file in the Windows folder. This will effectively deactivate the protection the next time Sandboxie reads its configuration. This would happen because Sandboxie would switch to using the new empty configuration file, for which protection is not activated.

**Access to the configuration file:** Adjust the permissions on the [Sandboxie Ini](SandboxieIni.md) configuration file to allow write access only to the SYSTEM account. Any other user account must still be able to read the configuration, so read access should be allowed to the user group **Authenticated Users** or **Everyone**.
