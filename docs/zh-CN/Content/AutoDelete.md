# 自动删除

AutoDelete 是 [Sandboxie Ini](SandboxieIni.md) 中的一个沙盒设置。通常指定为 AutoDelete=y，表示当最后一个沙盒进程终止时，沙盒的内容应该被自动删除。例如：

```
   .
   .
   .
   [DefaultBox]
   AutoDelete=y
```

相关 [Sandboxie Control](SandboxieControl.md) 设置：[沙盒设置 > 删除 > 调用](DeleteSettings.md#invocation)

相关 Sandboxie Plus 设置：沙盒选项 > 文件选项 > 沙盒删除选项 > 当最后一个沙盒进程终止时自动删除内容 