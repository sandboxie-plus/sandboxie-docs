# 描述

_Description_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定自由文本，可以解释例如沙盒的用途。

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

文本中的 `<BR>` 序列用于指示换行。自由文本显示在 _以沙盒方式运行_ 沙盒选择对话框中的气球弹出提示中。
