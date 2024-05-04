# Shell Folders

In Windows, each user account has associated personal folders, typically known as _Documents_, _Music_ and so on. The Windows shell records each user's personal folders, in the following registry keys.
```
  HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\
     . . . User Shell Folders
     . . . Shell Folders
```

This key contains several _registry values_, each identifies a specific personal folder, and contains its absolute folder path. Most registry values in this key are named the same as the "friendly" name of the folder: _Desktop_, _Favorites_, _Music_, and so on.

However, in some cases, the registry value differs:

*   _Personal_ stands for the _Documents_ folder.
*   _AppData_ stands for the primary _Application Data_ folder.
*   _Local AppData_ stands for the secondary _Application Data_ folder, located below the _Local Settings_ folder.

Please see the registry key noted above for a complete list of possible folder names.

For example, for the user joe, the registry value _Personal_ (which identifies the _Documents_ folder), may specify:
```
  C:\Users\joe\Documents
```

Configuration settings in Sandboxie that specify folder paths generally accept references to registry values in the Shell Folders key. This is more useful than specifying explicit folder locations. For example:
```
  [DefaultBox]
  RecoverFolder=%Desktop%
```

Indicates that [Quick Recovery](QuickRecovery.md) should look for sandboxed items in the desktop folder of whichever user is making the request.
