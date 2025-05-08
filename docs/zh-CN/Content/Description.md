# 描述

_Description_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定自由文本，可以用于解释沙盒的用途等。

```
   .
   .
   .
   [DefaultBox]
   Description=示例<BR>文本。
   .
   .
   .
   [PrivateBox]
   Description=拒绝访问敏感文件位置
   ClosedFilePath=%Personal%
   ClosedFilePath=D:\MyDocs
```

文本中的 `<BR>` 序列用于表示换行。自由文本显示在_在沙盒中运行_沙盒选择对话框的气泡提示中。 