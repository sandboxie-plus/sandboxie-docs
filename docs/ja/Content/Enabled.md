# Enabled

_Enabled_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。通常は _Enabled=y_ として指定され ([Yes Or No Settings](YesOrNoSettings.md) を参照)、そのサンドボックスでプログラムを起動できることを示します。例:

```
   .
   .
   .
   [InstallBox]
   Enabled=y
   Enabled=y,Administrators
```

最初の例は _Enabled_ の典型的な形式であり、構成ファイル内の任意のサンドボックス セクションの必須部分です。サンドボックス _InstallBox_ をサンドボックス化に使用できることを示します。

2 番目の例も同様にサンドボックス _InstallBox_ を定義しつつ、その使用を Administrators ユーザー アカウント グループに制限します。ローカル Windows システムによって認識される任意のユーザー アカウントまたはグループを指定できます。ユーザー アカウントのリストが 1 行に収まらない場合は、複数の _Enabled_ 行を指定できます。

特定のユーザーに制限されたサンドボックスは、他のすべてのユーザー アカウントに対して _非表示_ と見なされます。それらの他のユーザー アカウントは、[Sandboxie Control](SandboxieControl.md) にサンドボックスがリストされているのを確認できず、[Force Process](ForceProcess.md) または [Force Folder](ForceFolder.md) 設定もそれらのユーザー アカウントには適用されません。

関連付けられた _Enabled=y_ 設定を持たないサンドボックスでプログラムを明示的に起動しようとすると失敗します。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > User Accounts](UserAccountsSettings.md)

関連する [Sandboxie Control](SandboxieControl.md) コマンド: [Sandbox Menu > Reveal Hidden Sandbox](SandboxMenu.md#reveal-hidden-sandbox)
