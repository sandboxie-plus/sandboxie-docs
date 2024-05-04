# Restrictions Settings

### "Restrictions" Settings Group

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Restrictions

![](../Media/RestrictionsSettings.png)

Settings in this section are intended to alter the default set of restrictions that Sandboxie places on programs running in the sandbox.

*   You can place additional restrictions on programs, to tighten the security of the sandbox.
*   You can relax some of the default restrictions, which is normally not recommended, but may enable some esoteric programs to work.

* * *

### Internet Access

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Restrictions > Internet Access

![](../Media/InternetAccessSettings.png)

Use these settings to select which programs, if any, will be allowed to access the Internet in the sandbox. Initially, all programs in the sandbox can access the Internet.

Use the _Add by Name_ button to add a program by typing its explicit executable name. Alternatively, use the _Add by File_ button to navigate to the program folder and select its program executable. ~~Blocking of SMB/CIFS which you can block as well by visiting [BlockPort](BlockPort.md)~~


When _any_ restrictions are in effect, programs that are installed (or downloaded) into the sandbox will never be allowed to access the Internet.


Use the _Remove_ button to remove some program previously added to the list.

The button _Block All Programs_ prevents all programs in the sandbox from accessing the Internet. When this mode is in effect, the button changes to _Allow All Programs_, and when clicked, will undo the effect of blocking all programs.

_Issue message [SBIE1307](SBIE1307.md) when access is denied_: When a program is restricted due to this setting, Sandboxie can issue a notification message. Use this checkbox setting to indicate whether you would like to receive these notifications. See also message [SBIE1307](SBIE1307.md).

You can also configure this setting in the [Program Settings](ProgramSettings.md) window.


Related [Sandboxie Ini](SandboxieIni.md) settings: [ClosedFilePath](ClosedFilePath.md), [Notify Internet Access Denied](NotifyInternetAccessDenied.md).

* * *

### Start/Run Access

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Restrictions > Start/Run Access

![](../Media/StartRunAccessSettings.png)

Use these settings to select which programs, if any, will be allowed to start and run in the sandbox. Initially, all programs in the sandbox can start and run in the sandbox.

Use the _Add by Name_ button to add a program by typing its explicit executable name. Alternatively, use the _Add by File_ button to navigate to the program folder and select its program executable.


When _any_ Start/Run restrictions are in effect, programs that are installed (or downloaded) into the sandbox will never be allowed to start or run.


Use the _Remove_ button to remove some program previously added to the list. The _Allow All Programs_ has the same effect as clicking _Remove_ on each and every entry that appears in the list.

_Issue message [SBIE1308](SBIE1308.md) when access is denied_: When a program is restricted due to this setting, Sandboxie can issue a notification message. Use this checkbox setting to indicate whether you would like to receive these notifications. See also message [SBIE1308](SBIE1308.md).


You can also configure this setting in the [Program Settings](ProgramSettings.md) window.


Related [Sandboxie Ini](SandboxieIni.md) settings: [ClosedIpcPath](ClosedIpcPath.md), [Notify Start Run Access Denied](NotifyStartRunAccessDenied.md).

* * *

### Drop Rights

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Restrictions > Drop Rights

![](../Media/DropRightsSettings.png)

The setting in this page causes Sandboxie to strip administrative rights from programs running in this sandbox.

Specifically, the security credentials used to start the sandboxed program will not include membership in the Administrators and Power Users groups.

Note that this has little effect if you are already running under a non-Administrator user account.

Related [Sandboxie Ini](SandboxieIni.md) settings: [DropAdminRights](DropAdminRights.md).

* * *

### Low-Level Access -REMOVED

## Hardware Access has been removed from Sandboxie v4 and up.

### Previous versions of Sandboxie should not be used and they may not function.

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Restrictions > Low-Level Access

![](../Media/LowLevelAccessSettings.png)

This category manages restrictions for several types of global operations which are restricted in some way within the sandbox. Please see the associated [Sandboxie Ini](SandboxieIni.md) settings for more information.

*   _Permit programs in this sandbox to load kernel mode drivers into the operating system_
    *   Related [Sandboxie Ini](SandboxieIni.md) settings: [BlockDrivers](BlockDrivers.md)

*   _Permit programs in this sandbox to load application (Win32) hooks into other programs_
    *   Related [Sandboxie Ini](SandboxieIni.md) settings: [BlockWinHooks](BlockWinHooks.md)

*   _Permit programs in this sandbox to change desktop wallpaper and other system parameters_
    *   Related [Sandboxie Ini](SandboxieIni.md) settings: [BlockSysParam](BlockSysParam.md)

*   _Permit programs in this sandbox to change user account password_
    *   Related [Sandboxie Ini](SandboxieIni.md) settings: [BlockPassword](BlockPassword.md)
    *   See also message [SBIE1309](SBIE1309.md).

* * *

### Hardware Access -REMOVED

## Hardware Access has been removed from Sandboxie v4 and up.

### Previous versions of Sandboxie should not be used and they may not function.

[Sandboxie Control](SandboxieControl.md) > [Sandbox Settings](SandboxSettings.md) > Restrictions > Hardware Access

![](../Media/HardwareAccessSettings.png)

This category manages restrictions for three types of global operations which are restricted in some way within the sandbox. Please see the associated [Sandboxie Ini](SandboxieIni.md) settings for more information.

*   _Permit programs in this sandbox to simulate keyboard and mouse input_
    *   Related [Sandboxie Ini](SandboxieIni.md) settings: [BlockFakeInput](BlockFakeInput.md)
    *   See also message [SBIE1304](SBIE1304.md).

*   _Permit programs in this sandbox to manage hardware device configuration_
    *   Related [Sandboxie Ini](SandboxieIni.md) settings: _Template=PlugPlay_
    *   This setting permits a program to update configuration and drivers for hardware devices.

You are advised to keep the hardware access settings in their default, disabled state.

However, when running games or other full screen applications in the sandbox, it may be useful to permit the simulation of keyboard and mouse input.
