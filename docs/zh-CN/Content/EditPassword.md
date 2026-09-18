# 编辑密码

_EditPassword_ 是 [Sandboxie Ini](SandboxieIni.md) 中的一项全局设置。它由 Sandboxie 服务管理，指定从配置密码生成的 160 位 [SHA1 哈希](https://en.wikipedia.org/wiki/SHA_hash_functions)。

用法：

```
   .
   .
   .
   [GlobalSettings]
   EditPassword=0D03090004070E09050C0A010100000108010B03
```

当 [Sandboxie Ini](SandboxieIni.md) 配置文件包含此设置时，Sandboxie 服务将使配置文件保持永久锁定，以防止未授权修改。

另请参阅：[配置保护](ConfigurationProtection.md)。
