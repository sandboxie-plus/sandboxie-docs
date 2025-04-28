# Sandboxie Ini

Some aspects of the operation of Sandboxie can be altered or fine-tuned through the use of a human-readable textual configuration file called Sandboxie.ini. This section describes the structure and contents of the file.

As a general rule, manual editing of the configuration file is discouraged. You are advised to use [Sandboxie Control](SandboxieControl.md) to make configuration changes. See [Sandbox Settings](SandboxSettings.md).

## Location

Sandboxie looks for the file Sandboxie.ini in the following folders, in this order:

* In the Windows folder: `C:\Windows` on most Windows installations
* In the Sandboxie installation folder: typically `C:\Program Files\Sandboxie` or `C:\Program Files\Sandboxie-Plus`

The search for Sandboxie.ini ends when an instance of the file is found, and all other instances are ignored.

When [Sandboxie Control](SandboxieControl.md) updates the configuration, it rewrites the file Sandboxie.ini file in the folder from which the configuration was last read. Thus, if the file is manually moved, Sandboxie configuration must be manually [reloaded](ConfigureMenu.md#reload-configuration). (Restarting the computer would have the same effect.)

**Note:** Sandboxie does not support any other custom location for the Sandboxie.ini file.

## Structure

Configuration settings in the file are split into groups, or sections. A section begins with a line that specifies its name enclosed within square brackets. For example: [SomeSectionName]. The section continues to the end of the file, or until another section begins. There are three types of sections:

* The Global Settings section contains settings global to Sandboxie. These apply in one way or another to all sandboxes and all user accounts. There can be only one Global Settings section, typically at the top of the configuration file.
* One Sandbox Settings section for each sandbox known to Sandboxie. A valid sandbox name is a string of letters and digits, and has a maximum length of 32 characters. The Sandbox Settings section should contain the setting [Enabled](Enabled.md)=y.
* One User Settings section for each user account. These settings record the state of [Sandboxie Control](SandboxieControl.md) for a particular user account, and include such information as the size of the window. These settings are not documented here, but see a brief discussion below.

A simple Sandboxie.ini file may look like this.

```
   # Sample Sandboxie Configuration File
   [GlobalSettings]
   FileRootPath=C:\Sandbox\%USER%\%SANDBOX%
   # Settings for sandbox DefaultBox
   [DefaultBox]
   Enabled=y
   # Settings for sandbox InstallBox
   [InstallBox]
   Enabled=y
   FileRootPath=D:\Sandbox\Install
   # Sandboxie Control settings for some user
   [UserSettings_054A02CE]
   SbieCtrl_UserName=tzuk
```

The example shows four sections: The global section (GlobalSettings), two sandbox sections (DefaultBox and InstallBox), and one user account section (UserSettings_054A02CE).

Lines that begin with a hash sign (#) are comments. These lines are skipped.

**Note:** During its operation, [Sandboxie Control](SandboxieControl.md) regularly rewrites the Sandboxie.ini file, and this rewrite loses all comments. However, unrecognized settings are not lost during the rewrite, so one workaround is to write comments in the form Comment=text.

The configuration file can contain up to 30,000 lines of text. Each line can be up to 1000 characters long.

The file is UNICODE-encoded, which means each character is composed of two bytes. Many text file editors, including the system Notepad, handle this encoding properly.

## Settings

### Global Settings:

* Listed in the navigation bar on the right under the heading Global Settings.
* Settings apply to the general operation of Sandboxie, not to any particular sandbox.
* Global settings must be placed in the GlobalSettings section, and cannot be overridden by also including them in a sandbox section.
* Sandbox settings may appear in the GlobalSettings section, and can be overridden by also including them in a sandbox section.

### Sandbox Settings:

* Listed in the navigation bar on the right under the heading Sandbox Settings.
* Settings apply to a particular sandbox when specified in the associated sandbox section.
* Settings apply to all sandboxes when specified in the [GlobalSettings] section.
* Settings in the sandbox section override corresponding settings from [GlobalSettings].

In the example above, the sandbox setting [FileRootPath](FileRootPath.md) appears in [GlobalSettings] and applies to all sandboxes, but note that it is overridden in section [InstallBox].

* Sandbox settings can be applied to a specific program. See [Program Name Prefix](ProgramNamePrefix.md).
* Some sandbox settings are [Yes Or No Settings](YesOrNoSettings.md).
* Sandbox settings may specify [Expandable Variables](ExpandableVariables.md) that Sandboxie recognizes.

### User Settings

* Settings record the state of [Sandboxie Control](SandboxieControl.md), for instance the position of the window.
* Each user account is directed to a different [UserSettings_XXXXXXXX] section.
* When a new [UserSettings_XXXXXXXX] is created, default values are taken from the [UserSettings_Default] section, if it exists.
* If the section [UserSettings_Portable] exists, all user accounts are directed to use this section.

## Automation

Sandboxie includes a command-line utility to query or update the Sandboxie.ini configuration file. The utility is suitable for direct command-line interaction as well as invocation from a script or a program. The utility can be found as SbieIni.exe in the Sandboxie installation directory. For further details, see [Create a sandbox by command line](https://github.com/sandboxie-plus/Sandboxie/issues/278#issuecomment-856207910) and [SbieIni.exe usage](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica6bca6bc.html#p126947) section.
