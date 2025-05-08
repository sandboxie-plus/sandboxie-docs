# 可扩展变量

一些 Sandboxie 设置可能包含_变量_。这些是占位符名称，它们会被扩展（替换）为特定计算机和用户账户的文本。例如：

```
RecoverFolder=%Personal%\Song_Lyrics
```

在这个简单的例子中，Sandboxie 将变量 _Personal_ 扩展为实际的 _Documents_ 文件夹。

```
RecoverFolder=C:\Users\joe\Documents\Song_Lyrics
```

下表列出了 Sandboxie 识别的变量。

| 变量名称 | 扩展为 |
| :---     | :---   |
| SbieHome | Sandboxie 安装的根路径 |
| sandbox | 程序运行的沙盒名称。<br> 示例：DefaultBox |
| user <br> username | 程序运行的用户账户。<br> 示例：joe |
| sid | 标识程序运行用户账户的 SID 字符串。<br> 示例：S-1-5-21-414-171-1981-1005 |
| session | 程序运行的登录会话编号。<br> 示例：1 |
| ProgramFiles | 程序文件文件夹的位置。<br> 示例：C:\Program Files |
| SystemRoot | Windows 安装文件夹的位置。<br> 示例：C:\Windows |
| SystemDrive | %SystemRoot% 的前两个字符。<br> 示例：C: |
| DefaultSpoolDirectory | 打印假脱机文件夹的位置。<br> 示例：C:\Windows\System32\spool\printers |
| UserProfile | 用户账户根文件夹的位置。<br> 示例：C:\Users\joe |
| AllUsersProfile | 共享用户账户根文件夹的位置。<br> 示例：C:\ProgramData |
| HomeDrive <br> HomePath <br> HomeShare | 用户账户根文件夹的部分位置，在注册表项中定义：<br> HKEY_CURRENT_USER\Volatile Environment |
| temp <br> tmp | Windows 临时文件文件夹的位置，在注册表项中定义：<br> HKEY_CURRENT_USER\Environment。<br> 示例：C:\Windows\Temp |
| Personal <br> AppData <br> Local AppData <br> Favorites <br> 等等 | Windows 资源管理器已知的用户账户和系统文件夹位置。更多信息，请参见 [Shell Folders](ShellFolders.md)。 |

### 模板变量

全局模板是 Sandboxie 安装的一部分，位于 Sandboxie 安装文件夹中的 _Templates.ini_ 文件中。可以在 [Sandboxie Ini](SandboxieIni.md) 中添加额外的本地模板。任何模板都可以引用模板变量，形式为 _%Tmpl.SomeVariableName%_。这些变量名称不是 Sandboxie 核心内置的。它们必须在 _Templates.ini_ 或 _Sandboxie.ini_ 的 [TemplateSettings] 部分中定义。

### 覆盖变量

上表中的任何变量，包括 [Shell Folders](ShellFolders.md) 和模板变量，都可以被 [Sandboxie Ini](SandboxieIni.md) 配置文件覆盖。要覆盖变量，添加以 **Ovr.** 为前缀的参数。

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

当以这种方式覆盖变量时，其扩展值将始终匹配配置文件中指定的值。

### 注册表回退

上表中的一些变量是从系统注册表中获取的。这些变量是 _ProgramFiles_ 和表中 _ProgramFiles_ 以下的任何其他变量。对于这些变量，可以在 [Sandboxie Ini](SandboxieIni.md) 配置文件中指定"回退"值。要指定变量的回退值，添加以 **Reg.** 为前缀的参数。

例如：

```
    [GlobalSettings]
    Reg.Desktop=%USERPROFILE%\Desktop
```

```
    [DefaultBox]
    Reg.Cookies=%USERPROFILE%\Cookies
```

请注意，"Ovr." 样式的覆盖（如上所述）将导致 Sandboxie 忽略注册表。另一方面，Sandboxie 只有在注册表中找不到扩展变量时才会检查 "Reg." 样式的回退。这意味着如果为同一变量 X 同时指定了 Ovr.X 和 Reg.X，则在扩展 X 时始终应用 Ovr.X 形式，而 Reg.X 形式永远不会应用。

通常，使用 "Ovr." 样式的覆盖比 "Reg." 样式的回退更可取。 