# Open File Path

_OpenFilePath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie がファイルに対してサンドボックス化を適用しないパス パターンを指定します。これにより、サンドボックス化されたプログラムが_サンドボックスの外_のファイルとフォルダーを更新するために直接アクセスできます。この設定は本質的に、特定のフォルダーの場所でサンドボックスに_穴を開けます_。

[Shell Folders](ShellFolders.md) を指定できます。[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:
```
   .
   .
   .
   [DefaultBox]
   OpenFilePath=C:\Downloads\
   OpenFilePath=*.eml
   OpenFilePath=iexplore.exe,%Favorites%
   OpenFilePath=msimn.exe,*.eml
```

これらの例を確認する際は、Sandboxie が値の末尾に_ワイルドカード スター_を配置することを覚えておいてください。ただし、値のどこかに既にスターが現れている場合を除きます。たとえば、_C:\Downloads\_ は _C:\Downloads\*_ になりますが、_*.eml_ は変更されません。

_ワイルドカード スター_は、可変で未知の部分を持つパターンを指定するために使用されます。たとえば、_a.eml_ はその 1 つのファイルにのみ一致しますが、_*.eml_ は _a.eml_、_test.eml_、_important message.eml_ などに一致します。ただし、どちらの形式も _a.txt_ には一致しないことに注意してください。

最初の例の設定は、フォルダー _C:\Downloads_ (およびその下の任意のフォルダー) に作成されたすべてのファイル (またはフォルダー) がサンドボックス化されないことを指定します。文字列の末尾にスターが配置されるため、最後の円記号が重要であることに注意してください。

2 番目の例は、_*.eml_ ファイルがどこに作成されてもサンドボックス化から除外するためにワイルドカードを使用する方法を示しています。_.eml_ ファイルは通常、メッセージが明示的にディスクに保存されるときに Outlook と Outlook Express によって作成されます。

3 番目の例の設定は、アクティブなユーザー アカウントのお気に入りフォルダーを除外することを指定します。これは、新しいお気に入りショートカットがサンドボックスの外に追加されることを意味します。この例では ProgramNamePrefix が使用されているため、設定は Internet Explorer プログラム _iexplore.exe_ にのみ適用されます。

4 番目の例は、ワイルドカードを含むパスを特定のプログラムにのみ適用することで、前の 2 つの例を組み合わせています。

**注:** セキュリティ上の理由から、この設定はプログラムの実行可能ファイルがサンドボックス内に存在する場合は適用されません。これは、コンピューターにダウンロードされて実行された (潜在的に悪意のある) ソフトウェアがこの設定を利用できないことを意味します。

_常に_適用される、_OpenFilePath_ に似た設定は [OpenPipePath](OpenPipePath.md) です。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Resource Access > File Access > Direct Access](ResourceAccessSettings.md#file-access-direct-access)

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Files > Add File/Folder > Access column > Open
