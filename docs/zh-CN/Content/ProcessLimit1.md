# 进程数量限制 1

**进程数量限制 1 和进程数量限制 2 已自 Sandboxie v0.7.1 / 5.48.5 起移除，由 [进程数量限制](ProcessLimit.md) 取代。**

_ProcessLimit1_ 和 _ProcessLimit2_ 曾是 [Sandboxie Ini](SandboxieIni.md) 中的沙盒设置。它们限制 Sandboxie 在同一时间允许沙盒中存在的最大进程数。
```
   .
   .
   .
   [DefaultBox]
   ProcessLimit1=100
   ProcessLimit2=200
```

进程数量限制 1：一旦沙盒同时有超过 X 个程序，每个新程序在开始运行前将被延迟十秒。X 是进程数量限制 1 中指定的数字。延迟时长（十秒）不可配置。

进程数量限制 2：一旦沙盒同时有超过 Y 个程序，每个新程序将被立即终止。Y 是进程数量限制 2 中指定的数字。

默认数字如上所述为 100 和 200。进程数量限制 2 不能小于进程数量限制 1。

创造性的值可以关闭一种或两种模式。例如，
```
	ProcessLimit2=999999
```

将有效禁用终止功能。另一方面，
```
	ProcessLimit1=50
	ProcessLimit2=50
```

将有效禁用延迟功能。
