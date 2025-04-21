# 自动删除

自动删除是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。通常设置为 AutoDelete=y，表示一旦最后一个沙盒进程终止，沙盒中的内容将会被自动删除。例如：
```
   .
   .
   .
   [DefaultBox]
   AutoDelete=y
```

相关的 [Sandboxie 控制](SandboxieControl.md) 设置： [沙盒设置 > 删除 > 调用](DeleteSettings.md#invocation)

相关的 Sandboxie Plus 设置：沙盒选项 > 文件选项 > 沙盒删除选项 > 当最后一个沙盒内进程终止时自动删除内容