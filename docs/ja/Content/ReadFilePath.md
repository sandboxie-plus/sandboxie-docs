# Read File Path

_ReadFilePath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie がファイルに対してサンドボックス化を適用せず、書き込みも許可しないパス パターンを指定します。

[Shell Folders](ShellFolders.md) を指定できます。[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:
```
   .
   .
   .
   [DefaultBox]
   ReadFilePath=C:\WINDOWS
```

この例は、C:\WINDOWS フォルダーとその下のすべてを、サンドボックス化されたプログラムから読み取り可能にするよう強制しますが、書き込み (または削除) はできません。

注: _ReadFilePath_ は [OpenFilePath](OpenFilePath.md) の制限された形式です。_OpenFilePath_ と同様に、指定されたファイルまたはフォルダーの場所に対して既に存在するサンドボックス化されたコンテンツは無視されます。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Resource Access > File Access > Read-Only Access](ResourceAccessSettings.md#file-access-read-only-access)

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Files > Add File/Folder > Access column > Read Only
