# Edit Admin Only

_EditAdminOnly_ は [Sandboxie Ini](SandboxieIni.md) のグローバル設定です。指定すると、Administrators グループのメンバーでないユーザー アカウントで実行されている [Sandboxie Control](SandboxieControl.md) または [Sandman](PlusMigrationGuide.md) は、グローバル設定セクションまたはサンドボックス セクションで構成を変更できなくなります。ただし、その場合でも、ユーザー設定セクションでは変更できます。

使用法:

```
   .
   .
   .
   [GlobalSettings]
   EditAdminOnly=y
```

この設定は、ネットワーク管理者による使用を目的としています。
