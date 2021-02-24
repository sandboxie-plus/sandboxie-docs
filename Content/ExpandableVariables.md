# Expandable Variables


Some Sandboxie settings may include _variables_. These are placeholder names which are expanded to (replaced by) text which may be specific to a particular computer and user account. For example,

```
RecoverFolder=%Personal%\Song_Lyrics
```

In this simple example, Sandboxie expands the variable _Personal_ by the actual folder for the My Documents folder.

```
RecoverFolder=C:\Documents and Settings\joe\My Documents\Song_Lyrics
```

The following table lists the variables that Sandboxie recognizes.

<table style="width: 90%;">

<tbody>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">Variable Name</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">Expands To</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">sandbox</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">Name of sandbox in which the program is running.  
Example: DefaultBox</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">user  
username</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">User account in which the program is running.  
Example: joe</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">sid</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">SID-string identifying the user account in which the program is running.  
Example: S-1-5-21-414-171-1981-1005</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">session</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">The number of the logon session in which the program is running.  
Example: 1</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">ProgramFiles</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">Location of program files folder.  
Example: C:\Program Files (Windows XP)  
Example: C:\Programs (Windows Vista)</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">SystemRoot</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">Location of the Windows installation folder.  
Example: C:\Windows</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">SystemDrive</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">First two characters of %SystemRoot%.  
Example: C:</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">DefaultSpoolDirectory</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">Location of the print spool folder.  
Example: C:\Windows\System32\spool\printers</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">UserProfile</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">Location of the user account root folder.  
Example: C:\Documents and Settings\joe (Windows XP)  
Example: C:\Users\joe (Windows Vista)</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">AllUsersProfile</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">Location of the shared user account root folder.  
Example: C:\Documents and Settings\All Users (Windows XP)  
Example: C:\ProgramData (Windows Vista)</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">HomeDrive  
HomePath  
HomeShare</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">Partial locations of the user account root folder, as defined in the registry key:  
HKEY_CURRENT_USER\Volatile Environment</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">temp  
tmp</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">Location of the Windows temporary files folder as defined in the registry key:  
HKEY_CURRENT_USER\Environment.  
Example: C:\Windows\Temp</td>

</tr>

<tr>

<td style=" padding: 5px; border-bottom: solid black 1px; ">Personal  
AppData  
Local AppData  
Favorites  
And more  
</td>

<td style=" padding: 5px; border-bottom: solid black 1px; ">Locations of user-account and system folders as are known to Windows Explorer. For more information, see <a href="ShellFolders.md">ShellFolders</a>.</td>

</tr>

</tbody>

</table>

**Template Variables**

Global templates are part of the installation of Sandboxie and reside in the file _Templates.ini_ in the Sandboxie installation folder. Additional local templates may be added to [Sandboxie Ini](SandboxieIni.md). Any template may reference template variables in the form %Tmpl.SomeVariableName%. These variable names are not built into the core of Sandboxie. They must be defined in _Templates.ini_ or _Sandboxie.ini_ in a [TemplateSettings] section.

**Overriding Variables**

Any of the variables in the table above, including any of the [Shell Folders](ShellFolders.md) variable and any template variables, can be overridden by the [Sandboxie Ini](SandboxieIni.md) configuration file. To override a variable, add a setting with an **Ovr.** prefix.

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

When a variable is overriden in this way, its expanded value will always match the value specified in the configuration file.

**Registry Fallbacks**

Some of the variables in the table above are taken from the system registry. Those variables are _ProgramFiles_ and any other variable that appears below _ProgramFiles_ in the table above. For these variables, it is possible to specify "fallback" values in the [Sandboxie Ini](SandboxieIni.md) configuration file. To specify a fallback for a variable, add a setting with a **Reg.** prefix.

For example:

```
    [GlobalSettings]
    Reg.Desktop=%USERPROFILE%\Desktop
```

```
    [DefaultBox]
    Reg.Cookies=%USERPROFILE%\Cookies
```

Note that "Ovr."-style overrides (described above) will cause Sandboxie to not look in the registry at all. On the other hand, Sandboxie only considers "Reg."-style fallbacks if the expanded variable cannot be found in the registry. This means that if both Ovr.X and Reg.X are specified for the same variable X, the Ovr.X form will always apply when X is expanded, and the Reg.X form will never apply.

It is generally preferable to use "Ovr."-style overrides than "Reg."-style fallbacks.
