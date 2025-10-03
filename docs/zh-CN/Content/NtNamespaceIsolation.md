# Nt 命名空间隔离

_NtNamespaceIsolation_ 是自 v1.8.0 / 5.63.0 版本起，在 [Sandboxie Ini](SandboxieIni.md) 中可用的沙箱设置。它可用于禁用对 CreateDirectoryObject 和 OpenDirectoryObject 的虚拟化 —— 这样会降低安全性，并移除防止名称抢占的保护措施。

```ini
   .
   .
   .
   [DefaultBox]
   NtNamespaceIsolation=n
```