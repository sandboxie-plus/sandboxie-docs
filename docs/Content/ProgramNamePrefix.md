# Program Name Prefix

In several settings in the [Sandboxie Ini](SandboxieIni.md) configuration file, a program name can be specified. This tells the setting to take effect only for sandboxed processes that match the program name criteria.

The prefix is specified as the name of the executable, with an extension, but _without_ a folder path:

*   _iexplore.exe_ - right
*   _C:\Program Files\Internet Explorer\iexplore.exe_ - wrong

The prefix may start with an exclamation point (!) to indicate negative criteria.

A comma (,) separates the prefix from the rest of the setting specification.

For example:
```
    .
    .
    .
    [DefaultBox]
    OpenFilePath=iexplore.exe,%Favorites%
    ClosedFilePath=!iexplore.exe,%Favorites%
```

This combination means that Internet Explorer (_iexplore.exe_) has direct access to the Favorites folder and the shortcuts within it.

On the other hand, any _other_ program (NOT _iexplore.exe_, note the exclamation point) is denied _any_ kind of access to that same folder.
