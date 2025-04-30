# Auto Exec

_AutoExec_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。它指定了一组命令，这些命令会在沙箱每次被初始填充时执行。

示例：

```
   .
   .
   .
   [DefaultBox]
   AutoExec=regedit /s c:\defaultbox.reg
   AutoExec=cmd /c del /f "%windir%\system32\someExploitableDLL.dll"
```

第一个示例展示了如何使用 _AutoExec_ 以某种方式填充沙箱注册表。第二个示例则展示了如何使用 _AutoExec_ 删除不需要的 DLL 文件。在这两种情况下，所有定制操作都只发生在沙箱内部。

对于同一个沙箱，可以指定多个 _AutoExec_ 设置。列出的命令会依次执行。这些命令（无论是一条还是多条）在某个特定沙箱的生命周期内只会执行 _一次_。如果希望 Sandboxie 再次执行这些命令，必须删除该沙箱。

即使命令执行失败，也不会再次执行，除非删除该沙箱。

目前，对于该设置，没有对应的 [Sandboxie Control](SandboxieControl.md) 配置选项

**技术细节**

每个 _AutoExec_ 命令在被 Sandboxie 执行时，都会被记录到该沙箱的注册表中，具体路径为 _HKEY_CURRENT_USER\Software\SandboxieAutoExec_。

如果某个命令已经被记录在沙箱注册表中，则不会再次执行。因此，清除沙箱会删除所有已记录的 _AutoExec_ 命令，这样在下次有任何程序以沙箱模式启动时，这些命令会再次被执行。同时，也可以通过手动从该沙箱注册表键中删除相应命令，使其再次执行。
