# Force Folder

_ForceFolder_ is a sandbox setting in [Sandboxie.ini](SandboxieIni.md) which allows to force folder contents to run inside a specific sandbox. If any files or programs in these folders* (or in a sub-folder of one of these folders) are started outside any sandbox, they will be automatically sandboxed into a particular sandbox. For example:

```
   .
   .
   .
   [DefaultBox]
   ForceFolder=C:\Download
   ForceFolder=E:\
```

The first example specifies that files/programs started from the C:\Download folder (or any folders below contained in those folders) will be forced to run sandboxed in the sandbox _DefaultBox_.

The second example specifies that any files/programs started from drive E will be forced to run sandboxed in the sandbox _DefaultBox_. For CDROM and DVD drives, this includes forcing the _AutoRun_ programs that are automatically started by Windows.

* Please keep in mind that shortcuts located inside a ForceFolder, that are pointing to a path that is not a ForceFolder, will not start a Sandboxed application. For example: if you place a shortcut inside C:\ForcedFolder and it points to C:\SomeOtherPathThatIsNotForced, then the shortcut will trigger a non-sandboxed application.

Another consideration is that Modern / Store Apps are not supported. If your default application for opening a specific file type is a Windows Modern app (such as the Photos app in Windows 10), the application will not launch at all. For more information, please see the [Known Conflicts](KnownConflicts.md#uwp--modern--microsoft-store-apps) page.

See also: [ForceProcess](ForceProcess.md). If both a _ForceFolder_ and a _ForceProcess_ are applicable to a program that is starting, the ForceFolder setting takes precedence.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Program Start > Forced Folders](ProgramStartSettings.md#forced-folders)
