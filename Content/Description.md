# Description

The _Description_ setting in [Sandboxie Ini](SandboxieIni.md) allows you to provide explanatory text about the purpose of a specific sandbox. This information is displayed in a balloon pop-up within the _Run Sandboxed_ sandbox selection dialog box.

To set the description, include it in the sandbox section, such as [DefaultBox] or [PrivateBox], and add the desired free text. You can use the `<BR>` sequence for line breaks, as illustrated below:

```ini
[DefaultBox]
Description=Example<BR>text.

[PrivateBox]
Description=Access denied to sensitive file locations
ClosedFilePath=%Personal%
ClosedFilePath=D:\MyDocs
```

In this example, the text "Example text" will be displayed for the [DefaultBox] sandbox, and for the [PrivateBox] sandbox, it informs about access denial to specific file locations with the associated closed file paths.
