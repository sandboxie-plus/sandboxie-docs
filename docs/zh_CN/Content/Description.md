# 描述

_Description_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它可以输入任意文本内容，例如，用于说明该沙箱的用途。

```
   .
   .
   .
   [DefaultBox]
   Description=示例<BR>文本
   .
   .
   .
   [PrivateBox]
   Description=拒绝访问敏感文件位置
   ClosedFilePath=%Personal%
   ClosedFilePath=D:\MyDocs
```

文本中的 `<BR>` 代表换行符。该区域设置的文本内容会在 _Run Sandboxed_ 沙箱选择对话框中以气泡弹窗中显示。