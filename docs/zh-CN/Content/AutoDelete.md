# 自动删除

_AutoDelete_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙箱设置。通常设置为 AutoDelete=y，表示一旦最后一个沙箱进程终止，沙箱中的内容将会被自动删除。例如：
```
   .
   .
   .
   [DefaultBox]
   AutoDelete=y
```

相关的 [沙箱控制](SandboxieControl.md) 设置： [沙箱设置 > 删除 > 调用](DeleteSettings.md#invocation)

相关的 Sandboxie Plus 设置：沙箱选项 > 文件选项 > 沙箱删除选项 > 当最后一个沙箱内进程终止时自动删除内容
