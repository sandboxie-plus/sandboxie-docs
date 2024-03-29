# Nt Namespace Isolation

_NtNamespaceIsolation_ is a sandbox setting in [Sandboxie Ini](SandboxieIni.md). It can be used to disable virtualization for CreateDirectoryObject and OpenDirectoryObject - which will reduce security and remove measures to prevent name squatting.

```
   .
   .
   .
   [DefaultBox]
   NtNamespaceIsolation=n
```
