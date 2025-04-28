# Edit Password

_EditPassword_ is a global setting in [Sandboxie Ini](SandboxieIni.md). It is managed by the Sandboxie service and specifies a 160-bit [SHA1 hash](https://en.wikipedia.org/wiki/SHA_hash_functions) generated from the configuration password.

Usage:

```
   .
   .
   .
   [GlobalSettings]
   EditPassword=0D03090004070E09050C0A010100000108010B03
```

When the [Sandboxie Ini](SandboxieIni.md) configuration file includes this setting, the Sandboxie service will keep the configuration file permanently locked, in order to prevent unauthorized modifications.

See also: [Configuration Protection](ConfigurationProtection.md).
