# Nt 命名空间隔离

_NtNamespaceIsolation_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项沙盒设置，自 v1.8.0 / 5.63.0 起可用。它可以用于禁用对 CreateDirectoryObject 和 OpenDirectoryObject 的虚拟化——这会降低安全性，并移除防止名称抢占的措施。

```
   .
   .
   .
   [DefaultBox]
   NtNamespaceIsolation=n
```
