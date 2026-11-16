# Force Disable Admin Only

_ForceDisableAdminOnly_ は [Sandboxie Ini](SandboxieIni.md) のグローバル設定です。指定すると、[Disable Forced Programs](FileMenu.md#disable-forced-programs) モードは Administrators グループのメンバーであるユーザー アカウントでのみ利用可能になります。

使用法:
```
   .
   .
   .
   [GlobalSettings]
   ForceDisableAdminOnly=y
```

この設定は、ネットワーク管理者による使用を目的としています。
