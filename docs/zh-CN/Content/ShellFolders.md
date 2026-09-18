# 个人文件夹

在 Windows 中，每个用户帐户都有相关联的个人文件夹，通常称为_文档_、_音乐_等。Windows Shell 在以下注册表项中记录每个用户的个人文件夹。
```
  HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\
     . . . User Shell Folders
     . . . Shell Folders
```

此注册表项包含若干_注册表值_，每个值标识一个特定的个人文件夹，并包含其绝对文件夹路径。此注册表项中的大多数注册表值与文件夹的"友好"名称同名：_Desktop_、_Favorites_、_Music_ 等。

不过，在某些情况下注册表值有所不同：

*   _Personal_ 代表_文档_文件夹。
*   _AppData_ 代表主要的_应用程序数据_文件夹。
*   _Local AppData_ 代表次要的_应用程序数据_文件夹，位于 _Local Settings_ 文件夹之下。

可能的文件夹名称的完整列表，请参见上述注册表项。

例如，对于用户 joe，注册表值 _Personal_（标识_文档_文件夹）可能指定：
```
  C:\Users\joe\Documents
```

Sandboxie 中指定文件夹路径的配置设置，通常接受对 Shell Folders 注册表项中注册表值的引用。这比指定显式文件夹位置更有用。例如：
```
  [DefaultBox]
  RecoverFolder=%Desktop%
```

表示 [快速恢复](QuickRecovery.md) 应在发出请求的用户（无论是谁）的桌面文件夹中查找沙盒化项目。
