# 进程数量限制

_ProcessLimit_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v0.9.7 / 5.52.1 起可用。此设置允许你限制 Sandboxie 在同一时间允许沙盒中存在的最大进程数。

**注意：** 达到设定限制的 80% 时，新进程的启动会延迟 3 秒。一旦达到限制，将不允许任何新进程启动（直到另一个进程被终止）。

```
   .
   .
   .
   [DefaultBox]
   ProcessLimit=100
```
