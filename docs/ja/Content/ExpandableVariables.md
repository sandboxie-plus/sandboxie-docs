# Expandable Variables


一部の Sandboxie 設定には _変数_ を含めることができます。これらは、特定のコンピューターおよびユーザー アカウントに固有のテキストに展開 (置換) されるプレースホルダー名です。たとえば、

```
RecoverFolder=%Personal%\Song_Lyrics
```

この単純な例では、Sandboxie は変数 _Personal_ を _Documents_ フォルダーの実際のフォルダーに展開します。

```
RecoverFolder=C:\Users\joe\Documents\Song_Lyrics
```

次の表は、Sandboxie が認識する変数を示しています。

| 変数名 | 展開先 |
| :---          | :---       |
| SbieHome | Sandboxie インストールのルート パス |
| sandbox | プログラムが実行されているサンドボックスの名前。 <br> 例: DefaultBox |
| user <br> username | プログラムが実行されているユーザー アカウント。 <br> 例: joe |
| sid | プログラムが実行されているユーザー アカウントを識別する SID 文字列。 <br> 例: S-1-5-21-414-171-1981-1005 |
| session | プログラムが実行されているログオン セッションの番号。 <br> 例: 1 |
| ProgramFiles | program files フォルダーの場所。 <br> 例: C:\Program Files |
| SystemRoot | Windows インストール フォルダーの場所。 <br> 例: C:\Windows |
| SystemDrive | %SystemRoot% の最初の 2 文字。 <br> 例: C: |
| DefaultSpoolDirectory | 印刷スプール フォルダーの場所。 <br> 例: C:\Windows\System32\spool\printers |
| UserProfile | ユーザー アカウントのルート フォルダーの場所。 <br> 例: C:\Users\joe |
| AllUsersProfile | 共有ユーザー アカウントのルート フォルダーの場所。 <br> 例: C:\ProgramData |
| HomeDrive <br> HomePath <br> HomeShare | レジストリ キーで定義されている、ユーザー アカウントのルート フォルダーの部分的な場所: <br> HKEY_CURRENT_USER\Volatile Environment |
| temp <br> tmp | レジストリ キーで定義されている、Windows の一時ファイル フォルダーの場所: <br> HKEY_CURRENT_USER\Environment。 <br> 例: C:\Windows\Temp |
| Personal <br> AppData <br> Local AppData <br> Favorites <br> その他 | Windows エクスプローラーで認識されているユーザー アカウントおよびシステム フォルダーの場所。詳細については [Shell Folders](ShellFolders.md) を参照してください。 |

### テンプレート変数 {#template-variables}

グローバル テンプレートは Sandboxie インストールの一部であり、Sandboxie インストール フォルダーの _Templates.ini_ ファイルにあります。追加のローカル テンプレートを [Sandboxie Ini](SandboxieIni.md) に追加できます。任意のテンプレートが _%Tmpl.SomeVariableName%_ の形式でテンプレート変数を参照できます。これらの変数名は Sandboxie のコアに組み込まれていません。[TemplateSettings] セクションで _Templates.ini_ または _Sandboxie.ini_ に定義する必要があります。

`[TemplateSettings]` には共有テンプレート変数の定義が含まれます。これは選択可能な `[Template_Name]` 互換テンプレートとは別個です。テンプレートとそのメタデータがどのように使用されるかについては [Template Architecture](TemplateArchitecture.md) を参照してください。

### 変数の上書き

上記の表の任意の変数 ([Shell Folders](ShellFolders.md) およびテンプレート変数を含む) は、[Sandboxie Ini](SandboxieIni.md) 構成ファイルによって上書きできます。変数を上書きするには、**Ovr.** をプレフィックスとするパラメーターを追加します。

例:


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

この方法で変数が上書きされると、その展開された値は常に構成ファイルで指定された値と一致します。

### レジストリのフォールバック

上記の表の一部の変数はシステム レジストリから取得されます。それらの変数は _ProgramFiles_ および上記の表で _ProgramFiles_ より下に表示されるその他の変数です。これらの変数に対して、[Sandboxie Ini](SandboxieIni.md) 構成ファイルで「フォールバック」値を指定できます。変数のフォールバックを指定するには、**Reg.** をプレフィックスとするパラメーターを追加します。

例:

```
    [GlobalSettings]
    Reg.Desktop=%USERPROFILE%\Desktop
```

```
    [DefaultBox]
    Reg.Cookies=%USERPROFILE%\Cookies
```

「Ovr.」スタイルの上書き (上記で説明) は Sandboxie にレジストリを無視させることに注意してください。一方、Sandboxie は展開された変数がレジストリで見つからない場合にのみ「Reg.」スタイルのフォールバックをチェックします。これは、同じ変数 X に対して Ovr.X と Reg.X の両方が指定されている場合、Ovr.X 形式が X の展開時に常に適用され、Reg.X 形式は決して適用されないことを意味します。

一般に、「Reg.」スタイルのフォールバックよりも「Ovr.」スタイルの上書きを使用する方が好ましいです。
