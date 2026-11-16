# Byte Order Mark

**この機能は v0.6.5 / 5.47.0 以降で削除されました。**

_ByteOrderMark_ は [Sandboxie Ini](SandboxieIni.md) のグローバル設定でした。通常は ByteOrderMark=y として指定され ([Yes Or No Settings](YesOrNoSettings.md) を参照)、[Sandboxie Control](SandboxieControl.md) が構成ファイルの先頭に UTF-16 UNICODE バイト順マーク (BOM) 文字を挿入する必要があることを示していました。

使用法:

```
   .
   .
   .
   [GlobalSettings]
   ByteOrderMark=y
```

この設定は [Sandboxie Ini](SandboxieIni.md) に編集してから、Sandboxie 構成を手動で[再読み込み](ConfigureMenu.md#reload-configuration)する必要があります。その後、次に [Sandboxie Control](SandboxieControl.md) が構成を書き換えるときに、[Sandboxie Ini](SandboxieIni.md) 構成ファイルの最初の 2 バイトに UNICODE BOM 文字を挿入します。つまり (16 進) FF FE です。

この設定は、次の両方の記述が真である場合にのみ気にする必要があります:

*   [Sandboxie Ini](SandboxieIni.md) ファイルを手動で編集する予定がある。
*   使用しているテキスト エディターが、[Sandboxie Ini](SandboxieIni.md) ファイルが UNICODE テキスト ファイルであることを認識できない。
