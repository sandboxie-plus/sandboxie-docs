# 自动删除

自动删除是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置。通常指定为 AutoDelete=y，表示一旦最后一个沙盒化进程被终止，沙盒内容应立即自动删除。例如：
```
   .
   .
   .
   [DefaultBox]
   AutoDelete=y
```

相关 [沙盒管理器](SandboxieControl.md) 设置：[沙盒设置 > 删除 > 调用方式](DeleteSettings.md#调用方式)

相关 Sandboxie Plus 设置：沙盒选项 > 文件选项 > 沙盒删除选项 > 最后一个沙盒化进程终止时自动删除内容
