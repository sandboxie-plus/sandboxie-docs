# Description

_Description_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。たとえばサンドボックスの目的を説明できる自由テキストを指定します。

```
   .
   .
   .
   [DefaultBox]
   Description=Example<BR>text.
   .
   .
   .
   [PrivateBox]
   Description=Access denied to sensitive file locations
   ClosedFilePath=%Personal%
   ClosedFilePath=D:\MyDocs
```

テキスト内の `<BR>` シーケンスは改行を示すために使用されます。自由テキストは、_Run Sandboxed_ サンドボックス選択ダイアログ ボックスにバルーン ポップアップで表示されます。
