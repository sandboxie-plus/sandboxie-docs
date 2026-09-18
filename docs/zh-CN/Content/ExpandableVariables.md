# 可展开变量

某些 Sandboxie 设置可能包含_变量_。这些是占位名称，会被展开为（替换为）可能特定于某台计算机和某个用户帐户的文本。例如，

```
RecoverFolder=%Personal%\Song_Lyrics
```

在这个简单示例中，Sandboxie 把变量 _Personal_ 展开为_文档_文件夹的实际文件夹。

```
RecoverFolder=C:\Users\joe\Documents\Song_Lyrics
```

下表列出 Sandboxie 识别的变量。

| 变量名 | 展开为 |
| :---          | :---       |
| SbieHome | Sandboxie 安装的根路径 |
| sandbox | 程序运行所在沙盒的名称。 <br> 示例：DefaultBox |
| user <br> username | 程序运行所在的用户帐户。 <br> 示例：joe |
| sid | 标识程序运行所在用户帐户的 SID 字符串。 <br> 示例：S-1-5-21-414-171-1981-1005 |
| session | 程序运行所在的登录会话编号。 <br> 示例：1 |
| ProgramFiles | 程序文件文件夹的位置。 <br> 示例：C:\Program Files |
| SystemRoot | Windows 安装文件夹的位置。 <br> 示例：C:\Windows |
| SystemDrive | %SystemRoot% 的前两个字符。 <br> 示例：C: |
| DefaultSpoolDirectory | 打印后台文件夹的位置。 <br> 示例：C:\Windows\System32\spool\printers |
| UserProfile | 用户帐户根文件夹的位置。 <br> 示例：C:\Users\joe |
| AllUsersProfile | 共享用户帐户根文件夹的位置。 <br> 示例：C:\ProgramData |
| HomeDrive <br> HomePath <br> HomeShare | 用户帐户根文件夹的部分位置，如注册表项中所定义： <br> HKEY_CURRENT_USER\Volatile Environment |
| temp <br> tmp | Windows 临时文件文件夹的位置，如注册表项中所定义： <br> HKEY_CURRENT_USER\Environment。 <br> 示例：C:\Windows\Temp |
| Personal <br> AppData <br> Local AppData <br> Favorites <br> 等 | Windows 资源管理器所知的用户帐户和系统文件夹的位置。更多信息参见 [个人文件夹](ShellFolders.md)。 |

### 模板变量

全局模板是 Sandboxie 安装的一部分，位于 Sandboxie 安装文件夹中的 _Templates.ini_ 文件中。可以在 [Sandboxie Ini](SandboxieIni.md) 中添加额外的本地模板。任何模板都可以引用 _%Tmpl.SomeVariableName%_ 形式的模板变量。这些变量名不是 Sandboxie 核心内置的。它们必须在 _Templates.ini_ 或 _Sandboxie.ini_ 的 [TemplateSettings] 节中定义。

### 覆盖变量

上表中的任何变量，包括 [个人文件夹](ShellFolders.md) 和模板变量，都可以被 [Sandboxie Ini](SandboxieIni.md) 配置文件覆盖。要覆盖某个变量，请添加以 **Ovr.** 为前缀的参数。

例如：

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

以这种方式覆盖变量时，其展开值将始终匹配配置文件中指定的值。

### 注册表回退

上表中的某些变量取自系统注册表。这些变量是 _ProgramFiles_ 以及表中 _ProgramFiles_ 之下的任何其他变量。对于这些变量，可以在 [Sandboxie Ini](SandboxieIni.md) 配置文件中指定"回退"值。要为变量指定回退值，请添加以 **Reg.** 为前缀的参数。

例如：

```
    [GlobalSettings]
    Reg.Desktop=%USERPROFILE%\Desktop
```

```
    [DefaultBox]
    Reg.Cookies=%USERPROFILE%\Cookies
```

注意："Ovr." 风格的覆盖（如上所述）会让 Sandboxie 忽略注册表。另一方面，只有在注册表中找不到展开变量时，Sandboxie 才会检查"Reg." 风格的回退。这意味着如果对同一变量 X 同时指定了 Ovr.X 和 Reg.X，那么展开 X 时总是应用 Ovr.X 形式，而 Reg.X 形式永远不会应用。

通常，使用 "Ovr." 风格的覆盖优于 "Reg." 风格的回退。
