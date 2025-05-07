# 可扩展变量

某些沙盒设置可能包含 _变量_。这些是占位名称，将被替换为可能针对特定计算机和用户账户的实际文本。例如：

```
RecoverFolder=%Personal%\Song_Lyrics
```

在这个简单的示例中，沙盒会将 _Personal_ 变量扩展为 _文档_ 文件夹的实际路径。

```
RecoverFolder=C:\Users\joe\Documents\Song_Lyrics
```

下表列出了沙盒能够识别的变量。

| 变量名称 | 展开为 |
| :--- | :--- |
| SbieHome | 沙盒安装的根路径 |
| sandbox | 程序运行所在的沙箱名称。<br>示例：DefaultBox |
| user <br> username | 程序运行所在的用户账户。<br>示例：joe |
| sid | 标识程序运行用户账户的 SID 字符串。<br>示例：S-1-5-21-414-171-1981-1005 |
| session | 程序运行所在的登录会话编号。<br>示例：1 |
| ProgramFiles | 程序文件夹的位置。<br>示例：C:\Program Files |
| SystemRoot | Windows 安装文件夹的位置。<br>示例：C:\Windows |
| SystemDrive | %SystemRoot% 的前两个字符。<br>示例：C: |
| DefaultSpoolDirectory | 打印缓冲文件夹的位置。<br>示例：C:\Windows\System32\spool\printers |
| UserProfile | 用户账户根文件夹的位置。<br>示例：C:\Users\joe |
| AllUsersProfile | 共享用户账户根文件夹的位置。<br>示例：C:\ProgramData |
| HomeDrive <br> HomePath <br> HomeShare | 由注册表键 HKEY_CURRENT_USER\Volatile Environment 定义的用户账户根文件夹的部分位置。|
| temp <br> tmp | 由注册表键 HKEY_CURRENT_USER\Environment 定义的 Windows 临时文件夹位置。<br>示例：C:\Windows\Temp |
| Personal <br> AppData <br> Local AppData <br> Favorites <br> 及其他 | Windows 资源管理器已知的用户账户和系统文件夹的位置。详情请参见 [Shell Folders](ShellFolders.md) |

### 模板变量

全局模板是沙盒安装的一部分，位于沙盒安装文件夹的 _Templates.ini_ 文件中。可以在 [Sandboxie Ini](SandboxieIni.md) 中另行添加本地模板。任何模板都可以以 _%Tmpl.SomeVariableName%_ 形式引用模板变量。这些变量名不是沙盒核心自带的，必须在 _Templates.ini_ 或 _Sandboxie.ini_ 文件的 [TemplateSettings] 节中定义。

### 变量覆盖

上表中的任何变量，包括 [Shell 文件夹](ShellFolders.md) 和模板变量，都可以通过 [Sandboxie Ini](SandboxieIni.md) 配置文件进行覆盖。要覆盖变量，只需添加以 **Ovr.** 前缀开头的参数。

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

当以这种方式覆盖变量时，其展开值将始终与配置文件中指定的值一致。

### 注册表回退

上表中的某些变量取自系统注册表。这些变量包括 _ProgramFiles_ 及其后所有出现在表内的变量。对于这些变量，可以在 [Sandboxie Ini](SandboxieIni.md) 配置文件中指定“回退”值。要为变量指定回退方式，添加以 **Reg.** 前缀开头的参数。

例如：

```
    [GlobalSettings]
    Reg.Desktop=%USERPROFILE%\Desktop
```

```
    [DefaultBox]
    Reg.Cookies=%USERPROFILE%\Cookies
```

请注意，上文描述的 “Ovr.” 覆盖方式会让沙盒忽略注册表。另一方面，只有当在注册表中找不到需要展开的变量时，沙盒才会检查 “Reg.” 的回退值。这意味着，如果为同一个变量 X 同时指定了 Ovr.X 和 Reg.X，则变量展开时始终使用 Ovr.X，Reg.X 则不会生效。

通常建议首选 “Ovr.” 覆盖方式，而不是 “Reg.” 回退方式。