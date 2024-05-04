# Closed File Path

_ClosedFilePath_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It specifies path patterns for which Sandboxie will deny _all_ access by sandboxed programs, including _read_ access. This setting essentially blocks files and folders from being accessed by sandboxed programs.

[Shell Folders](ShellFolders.md) may be specified. [Program Name Prefix](ProgramNamePrefix.md) may be specified.

Example:

```
   .
   .
   .
   [DefaultBox]
   ClosedFilePath=!iexplore.exe,%Cookies%
   ClosedFilePath=%Personal%
```

```
   ClosedFilePath=!iexplore.exe,\Device\RawIp
   ClosedFilePath=!iexplore.exe,\Device\Ip*
   ClosedFilePath=!iexplore.exe,\Device\Tcp*
   ClosedFilePath=!iexplore.exe,\Device\Afd*
```

The example blocks any program _other than_ Internet Explorer (_iexplore.exe_) from accessing the folder containing downloaded Internet cookies for the active user account. This would block any downloaded malicious software from spying on cookies.

(Note that this does not stop browser extensions, like add-on toolbars, from looking into the Cookies folder, because these extensions execute inside the Internet Explorer program process.)

The second example shows how to configure Sandboxie to block sandboxed programs from accessing the _Documents_ folder.

The value specified for ClosedFilePath can include wildcards. For more information on this, including examples that show the use of wildcards, see [OpenFilePath](OpenFilePath.md).

The third example (spanning four lines) disables Internet access within a sandbox _except_ for Internet Explorer (_iexplore.exe_). See also [Sandbox Settings > Restrictions > Internet Access](RestrictionsSettings.md#internet-access).

**Note:** Unlike the corresponding OpenFilePath setting, the _ClosedFilePath_ settings always applies to sandboxed programs, whether the program executable file resides within the sandbox, or out of it.

Related [Sandboxie Control](SandboxieControl.md) setting: [Sandbox Settings > Resource Access > File Access > Blocked Access](ResourceAccessSettings.md#file-access--blocked-access)

Related Sandboxie Plus setting: Sandbox Options > Resource Access > Files > Add File/Folder > Access column > Closed
