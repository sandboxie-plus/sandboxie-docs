# 自动执行

_AutoExec_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。它指定每次沙盒最初被填充时执行的一系列命令。

示例：

```
   .
   .
   .
   [DefaultBox]
   AutoExec=regedit /s c:\defaultbox.reg
   AutoExec=cmd /c del /f "%windir%\system32\someExploitableDLL.dll"
```

第一个示例展示用 _AutoExec_ 以某种方式填充沙盒化的注册表。第二个示例展示用 _AutoExec_ 删除不需要的 DLL 文件。两种情况下，定制都只发生在沙盒内。

可以为单个沙盒指定多个 _AutoExec_ 设置。列出的命令逐条执行。这些命令（无论是一条还是任意多条）在特定沙盒的整个生命周期中只执行_一次_。要让 Sandboxie 再次执行这些命令，必须删除沙盒。

即使命令执行失败也是如此——除非沙盒被删除，否则它不会再次执行。

目前，没有对应的 [沙盒管理器](SandboxieControl.md) 配置用于此设置。

**技术细节**

每条 _AutoExec_ 命令被 Sandboxie 执行时，都会记录在该沙盒的注册表中，位于项 _HKEY_CURRENT_USER\Software\SandboxieAutoExec_。

如果命令已记录在沙盒化注册表中，则不会执行。因此，删除沙盒会清除所有已记录的 _AutoExec_ 命令，使它们在下次任何沙盒化程序在该沙盒中启动时再次执行。但也可以手动从该沙盒化注册表项中删除命令，让它们再次执行。
