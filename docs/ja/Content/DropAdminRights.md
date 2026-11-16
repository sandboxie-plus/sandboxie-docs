# Drop Admin Rights

_DropAdminRights_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie がこのサンドボックス内で実行されるプログラムから管理者権限を削除するかどうかを指定します。

使用法:

```
   .
   .
   .
   [DefaultBox]
   DropAdminRights=y
```

このページの設定により、Sandboxie はこのサンドボックス内で実行されるプログラムから管理権限を削除します。

具体的には、サンドボックス化されたプログラムを起動するために使用されるセキュリティ資格情報に、Administrators および Power Users グループのメンバーシップが含まれなくなります。

既に非管理者ユーザー アカウントで実行している場合は、これによる影響はほとんどないことに注意してください。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Restrictions > Drop Rights](RestrictionsSettings.md#drop-rights)
