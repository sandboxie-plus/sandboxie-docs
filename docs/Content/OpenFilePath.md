# Open File Path

_OpenFilePath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for which Sandboxie will not apply sandboxing for files. This lets sandboxed programs have direct access to update files and folders _outside the sandbox_. This setting essentially _punches a hole_ in the sandbox, at a particular folder location.

[Shell Folders](ShellFolders.md) may be specified. [Program Name Prefix](ProgramNamePrefix.md) may be specified.

Examples:
```
   .
   .
   .
   [DefaultBox]
   OpenFilePath=C:\Downloads\
   OpenFilePath=*.eml
   OpenFilePath=iexplore.exe,%Favorites%
   OpenFilePath=msimn.exe,*.eml
```

When reviewing these examples, keep in mind that Sandboxie places a _wildcard star_ at the end of the value, _unless a star already appears anywhere in the value_. So for example, _C:\Downloads\_ becomes _C:\Downloads\*_, while _*.eml_ remains unchanged.

_Wildcard stars_ are used to specify patterns with variable, unknown parts. For example, _a.eml_ matches only that one file, whereas _*.eml_ matches _a.eml_, _test.eml_, _important message.eml_ and so on. But note that neither form matches _a.txt_.

The first example setting specifies that any files (or folders) created in the folder _C:\Downloads_ (and in any folder below it) will not be sandboxed. Note that the final backslash character is important, because a star will be placed at the end of the string.

The second example shows how wildcards can be used to exempt _*.eml_ files from sandboxing, regardless of where they are created. _.eml_ files are typically created by Outlook and Outlook Express, when a message is explicitly saved to disk.

The third example setting specifies that the Favorites folder of the active user account should be exempted. This means that new Favorite shortcuts will added outside the sandbox. In this example, a ProgramNamePrefix is used, so the setting only applies to the Internet Explorer program, _iexplore.exe_

The fourth example combines the previous two examples, by showing a path containing a wildcard, applied only to a specific program.

**Note:** For security reasons, this setting does not apply when the program executable file resides within the sandbox. This means that (potentially malicious) software downloaded into your computer and executed, cannot take advantage of this setting.

A setting similar to _OpenFilePath_, which is _always_ applied, is [OpenPipePath](OpenPipePath.md).

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Resource Access > File Access > Direct Access](ResourceAccessSettings.md#file-access--direct-access)

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Files > Add File/Folder > Access column > Open
