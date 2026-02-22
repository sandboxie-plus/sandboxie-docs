# Force Box Docs

_ForceBoxDocs_ 是 [沙盘配置](SandboxieIni.md) 中的一个全局设置（自 v1.17.0 / 5.72.0 版本引入）。启用后，如果某个程序在沙盘外启动，并携带了一个文件路径作为参数，而该文件位于某个沙箱内，沙盘会自动在同一个沙箱中启动该程序。

用法：

```ini
   [GlobalSettings]
   ForceBoxDocs=y
```

该设置的工作机制如下：

- 仅在进程是未在沙箱中启动时生效；如果进程已在沙箱中启动，则该设置不适用
- 检查命令行解析出的文件路径或文档参数
- 沙盘会忽略命令行中前置的开关（以 `-` 或 `/` 开头的选项，如 `/n` 或 `-Embedding`），以便正确识别目标文件路径
- 当被检查的进程为沙盘自身的 `Start.exe` 时，将跳过文件路径/文档参数检查
- 只会考虑当前用户/会话已启用的沙箱
- 含有 [DisableForceRules](DisableForceRules.md) 的沙箱会被跳过

当用户直接从沙箱路径打开文档，并希望相关应用程序能够自动在正确的沙箱中启动时，此设置十分有用

命令行示例：

```text
"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE" /n /dde "C:\Sandbox\Alice\DefaultBox\drive\C\Docs\Report.docx"
```

结果：该文件路径指向 `DefaultBox`，因此进程会被强制运行在 `DefaultBox` 中

```text
"C:\Windows\System32\notepad.exe" "C:\Users\Alice\Desktop\Notes.txt"
```

结果：该文件路径不在沙箱路径下，因此 `ForceBoxDocs` 不会强制进程进入沙箱

另请参见：

- [ForceFolder](ForceFolder.md)
- [ForceProcess](ForceProcess.md)