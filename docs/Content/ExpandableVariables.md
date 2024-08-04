# Expandable Variables


Some Sandboxie settings may include _variables_. These are placeholder names which are expanded to (replaced by) text which may be specific to a particular computer and user account. For example,

```
RecoverFolder=%Personal%\Song_Lyrics
```

In this simple example, Sandboxie expands the variable _Personal_ by the actual folder for the _Documents_ folder.

```
RecoverFolder=C:\Users\joe\Documents\Song_Lyrics
```

The following table lists the variables that Sandboxie recognizes.

| Variable Name | Expands To |
| :---          | :---       |
| SbieHome | Root path of Sandboxie installation |
| sandbox | Name of sandbox in which the program is running. <br> Example: DefaultBox |
| user <br> username | User account in which the program is running. <br> Example: joe |
| sid | SID string identifying the user account in which the program is running. <br> Example: S-1-5-21-414-171-1981-1005 |
| session | The number of the logon session in which the program is running. <br> Example: 1 |
| ProgramFiles | Location of program files folder. <br> Example: C:\Program Files |
| SystemRoot | Location of the Windows installation folder. <br> Example: C:\Windows |
| SystemDrive | First two characters of %SystemRoot%. <br> Example: C: |
| DefaultSpoolDirectory | Location of the print spool folder. <br> Example: C:\Windows\System32\spool\printers |
| UserProfile | Location of the user account root folder. <br> Example: C:\Users\joe |
| AllUsersProfile | Location of the shared user account root folder. <br> Example: C:\ProgramData |
| HomeDrive <br> HomePath <br> HomeShare | Partial locations of the user account root folder, as defined in the registry key: <br> HKEY_CURRENT_USER\Volatile Environment |
| temp <br> tmp | Location of the Windows temporary files folder as defined in the registry key: <br> HKEY_CURRENT_USER\Environment. <br> Example: C:\Windows\Temp |
| Personal <br> AppData <br> Local AppData <br> Favorites <br> And more | Locations of user account and system folders as are known to Windows Explorer. For more information, see [Shell Folders](ShellFolders.md). |

### Template Variables

Global templates are part of the Sandboxie installation and located in the file _Templates.ini_ in the Sandboxie installation folder. Additional local templates may be added to [Sandboxie Ini](SandboxieIni.md). Any template may reference template variables in the form _%Tmpl.SomeVariableName%_. These variable names are not built into the core of Sandboxie. They must be defined in _Templates.ini_ or _Sandboxie.ini_ in a [TemplateSettings] section.

### Overriding Variables

Any of the variables in the table above, including the [Shell Folders](ShellFolders.md) and template variables, can be overridden by the [Sandboxie Ini](SandboxieIni.md) configuration file. To override a variable, add a parameter prefixed with **Ovr.**.

For example:


```
    [GlobalSettings]
    Ovr.SystemRoot=X:\WIN
    Ovr.Tmpl.Firefox=C:\Firefox\Profiles\
```

```
    [DefaultBox]
    Ovr.Personal=Z:\MY_FILES
    RecoverFolder=%Personal%
    OpenFilePath=%SystemRoot%\Temp
```

When a variable is overridden in this way, its expanded value will always match the value specified in the configuration file.

### Registry Fallbacks

Some of the variables in the table above are taken from the system registry. Those variables are _ProgramFiles_ and any other variable that appears below _ProgramFiles_ in the table above. For these variables, it is possible to specify "fallback" values in the [Sandboxie Ini](SandboxieIni.md) configuration file. To specify a fallback for a variable, add a parameter prefixed with **Reg.**.

For example:

```
    [GlobalSettings]
    Reg.Desktop=%USERPROFILE%\Desktop
```

```
    [DefaultBox]
    Reg.Cookies=%USERPROFILE%\Cookies
```

Note that "Ovr." style overrides (described above) will cause Sandboxie to ignore the registry. On the other hand, Sandboxie only checks "Reg." style fallbacks if the expanded variable cannot be found in the registry. This means that if both Ovr.X and Reg.X are specified for the same variable X, the Ovr.X form will always apply when X is expanded, and the Reg.X form will never apply.

It is generally preferable to use "Ovr." style overrides than "Reg." style fallbacks.
