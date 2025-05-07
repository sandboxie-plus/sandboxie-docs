# 编辑密码

_EditPassword_ 是 [Sandboxie Ini](SandboxieIni.md) 文件中的全局设置。该设置由沙盒服务进行管理，并指定由配置密码生成的 160 位 [SHA1 哈希值](https://en.wikipedia.org/wiki/SHA_hash_functions)。

用法：

```
   .
   .
   .
   [GlobalSettings]
   EditPassword=0D03090004070E09050C0A010100000108010B03
```

当 [Sandboxie Ini](SandboxieIni.md) 配置文件包含此设置时，沙盒服务会始终锁定该配置文件，以防止未经授权的修改。

另请参阅：[配置保护](ConfigurationProtection.md)。