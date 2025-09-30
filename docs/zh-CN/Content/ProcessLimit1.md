# 进程数量限制 1

**自沙盘（Sandboxie）v0.7.1 / 5.48.5 版本起，_ProcessLimit1_ 和 _ProcessLimit2_ 已被移除，转而使用 [进程限制](ProcessLimit.md)。**

_ProcessLimit1_ 和 _ProcessLimit2_ 是 [沙盘配置文件（Sandboxie Ini）](SandboxieIni.md) 中的沙箱设置。它们限制了沙盘在同一时间允许沙箱中运行的最大进程数。
```ini
   .
   .
   .
   [DefaultBox]
   ProcessLimit1=100
   ProcessLimit2=200
```

进程限制 1（ProcessLimit1）：一旦沙箱中同时运行的程序数量超过 X 个，每个新程序将在启动前延迟十秒。X 是 _ProcessLimit1_ 中指定的数字。延迟时间为十秒，不可配置。

进程限制 2（ProcessLimit2）：一旦沙箱中同时运行的程序数量超过 Y 个，每个新程序将立即终止。Y 是 _ProcessLimit2_ 中指定的数字。

如上所述，默认值分别为 100 和 200。_ProcessLimit2_ 不能小于 _ProcessLimit1_。

通过设置特定的值可以关闭其中一种或两种模式。例如，
```
	ProcessLimit2=999999
```

这将有效禁用终止功能。另一方面，
```
	ProcessLimit1=50
	ProcessLimit2=50
```

这将有效禁用延迟功能。
