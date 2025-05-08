# 自动执行

_AutoExec_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。它指定了每次沙盒初始化时要执行的命令列表。

示例：

```
   .
   .
   .
   [DefaultBox]
   AutoExec=regedit /s c:\defaultbox.reg
   AutoExec=cmd /c del /f "%windir%\system32\someExploitableDLL.dll"
```

第一个示例展示了使用 _AutoExec_ 以某种方式填充沙盒注册表。第二个示例展示了使用 _AutoExec_ 删除不需要的 DLL 文件。在这两种情况下，自定义都只在沙盒内进行。

可以为单个沙盒指定多个 _AutoExec_ 设置。列出的命令会一个接一个地执行。这些命令（无论是一个还是多个）在特定沙盒的生命周期中只执行_一次_。要让 Sandboxie 再次执行这些命令，必须删除沙盒。

即使命令执行失败也是如此 - 除非删除沙盒，否则不会再次执行。

目前，[Sandboxie Control](SandboxieControl.md) 中没有与此设置相对应的配置。

**技术细节**

每个 _AutoExec_ 命令在被 Sandboxie 执行时，都会记录在该沙盒的注册表中，键名为 _HKEY_CURRENT_USER\Software\SandboxieAutoExec_。

如果命令已经记录在沙盒注册表中，则不会再次执行。因此，删除沙盒会清除所有记录的 _AutoExec_ 命令，这样下次任何沙盒程序在该沙盒中启动时，这些命令就会再次执行。但也可以通过手动从沙盒注册表键中删除命令来让它们再次执行。 