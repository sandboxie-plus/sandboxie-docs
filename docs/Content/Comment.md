# Comment

_Comment_ is not a setting that Sandboxie itself reads or enforces. Writing `Comment=text` is the form recommended in [Sandboxie Ini](SandboxieIni.md) for keeping a human-readable note inside the configuration file.

Usage:

```
   .
   .
   .
   [DefaultBox]
   Comment=Notes about what this sandbox is used for
```

The setting is not enforced in any way and does not change how the sandbox behaves.

## Behavior

Classic Sandboxie Control regularly rewrote the Sandboxie.ini file, and such a rewrite discarded comments. Unrecognized settings, however, were preserved across rewrites, so notes written as `Comment=text` survived, while ordinary `#` comments did not. This is why the [Sandboxie Ini](SandboxieIni.md) documentation recommended the `Comment=` form for notes.

The modern SandMan implementation rebuilds the configuration file from its in-memory cache and writes every cached entry back, so entries and comments it does not manage, including `Comment=text`, survive a rewrite. Neither SandMan nor the classic Sandboxie Control read the value back and display it in the user interface; it remains plain text inside the configuration file for human readers.

## SandMan configuration

There is no control for this setting in SandMan. Notes can be added directly in the INI editor (**Options > Edit Sandboxie.ini**), either as `Comment=text` entries or as ordinary `#` comments.

## Related pages

- [Sandboxie Ini](SandboxieIni.md)
