# Edit Password

_EditPassword_ は [Sandboxie Ini](SandboxieIni.md) のグローバル設定です。Sandboxie サービスによって管理され、構成パスワードから生成された 160 ビットの [SHA1 ハッシュ](https://en.wikipedia.org/wiki/SHA_hash_functions)を指定します。

使用法:

```
   .
   .
   .
   [GlobalSettings]
   EditPassword=0D03090004070E09050C0A010100000108010B03
```

[Sandboxie Ini](SandboxieIni.md) 構成ファイルにこの設定が含まれている場合、Sandboxie サービスは不正な変更を防ぐために、構成ファイルを永続的にロックしたままにします。

参照: [Configuration Protection](ConfigurationProtection.md)。
