# Description

_Description_ is a sandbox settings in [Sandboxie Ini](SandboxieIni.md). It specifies free text, which can explain, for example, the purpose of the sandbox.

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

The `<BR>` sequence in the text is used to indicate a line break. The free text is displayed in a balloon pop-up in the _Run Sandboxed_ sandbox selection dialog box.
