# Program Name Prefix

[Sandboxie Ini](SandboxieIni.md) 構成ファイルのいくつかの設定では、プログラム名を指定できます。これは、設定がプログラム名の基準に一致するサンドボックス化されたプロセスに対してのみ有効になることを示します。

プレフィックスは、拡張子付きの実行可能ファイルの名前として指定されますが、フォルダー パスは_付けません_:

*   _iexplore.exe_ - 正しい
*   _C:\Program Files\Internet Explorer\iexplore.exe_ - 間違い

プレフィックスは、否定的な基準を示すために感嘆符 (!) で始まることがあります。

コンマ (,) がプレフィックスを設定指定の残りの部分から分離します。

例:
```
    .
    .
    .
    [DefaultBox]
    OpenFilePath=iexplore.exe,%Favorites%
    ClosedFilePath=!iexplore.exe,%Favorites%
```

この組み合わせは、Internet Explorer (_iexplore.exe_) がお気に入りフォルダーとその中のショートカットに直接アクセスできることを意味します。

一方、_他の_プログラム (NOT _iexplore.exe_、感嘆符に注意) は、その同じフォルダーへの_あらゆる_種類のアクセスを拒否されます。
