# Shell Folders

Windows では、各ユーザー アカウントに個人フォルダーが関連付けられており、通常は _Documents_、_Music_ などとして知られています。Windows シェルは各ユーザーの個人フォルダーを次のレジストリ キーに記録します。
```
  HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\
     . . . User Shell Folders
     . . . Shell Folders
```

このキーにはいくつかの_レジストリ値_が含まれており、それぞれが特定の個人フォルダーを識別し、その絶対フォルダー パスを含んでいます。このキーのほとんどのレジストリ値は、フォルダーの「フレンドリ」名と同じ名前です: _Desktop_、_Favorites_、_Music_ など。

ただし、場合によってはレジストリ値が異なります:

*   _Personal_ は _Documents_ フォルダーを表します。
*   _AppData_ はプライマリ _Application Data_ フォルダーを表します。
*   _Local AppData_ は、_Local Settings_ フォルダーの下に位置するセカンダリ _Application Data_ フォルダーを表します。

考えられるフォルダー名の完全なリストについては、上記のレジストリ キーを参照してください。

たとえば、ユーザー joe の場合、レジストリ値 _Personal_ (_Documents_ フォルダーを識別する) は次を指定することがあります:
```
  C:\Users\joe\Documents
```

Sandboxie のフォルダー パスを指定する構成設定は、一般に Shell Folders キーのレジストリ値への参照を受け入れます。これは明示的なフォルダーの場所を指定するよりも便利です。例:
```
  [DefaultBox]
  RecoverFolder=%Desktop%
```

これは、[Quick Recovery](QuickRecovery.md) が要求を行っているユーザーに関係なく、そのユーザーのデスクトップ フォルダー内のサンドボックス化された項目を検索すべきことを示します。
