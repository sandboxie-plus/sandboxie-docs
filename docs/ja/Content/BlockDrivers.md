# Block Drivers

**この機能は SBIE バージョン 4.+ 以降で削除されました。現在は利用できません。**

_BlockDrivers_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定でした。Sandboxie がサンドボックス化されたプログラムによるオペレーティング システムへのドライバーの読み込みを許可するかどうかを指定していました。ただし、この設定は新しいドライバーの _インストール_ を制御するものではあり _ません_ -- 詳細は以下を参照してください。

使用法:

```
   .
   .
   .
   [DefaultBox]
   BlockDrivers=n
```

_n_ を指定すると、サンドボックス化されたプログラムがオペレーティング システムにドライバーを読み込むことができることを示します。これを行わない場合、Sandboxie はドライバーの読み込み試行を拒否し、代わりにメッセージ [SBIE2103](SBIE2103.md) を発行します。

**注:** BlockDrivers によって提供される保護を無効にすることは推奨されません。

**ドライバーのインストール**

ドライバーを読み込む前に、まずインストールする必要があります。ドライバーのインストールは BlockDrivers 設定の影響を受けません。ドライバーのインストールを許可するには、次の OpenKeyPath 設定を追加する必要があります:

```
OpenKeyPath=HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services
```

さらに、OpenFilePath を使用してドライバー ファイルを _開く_ 必要があります。これは、(CurrentControlSet\Services の下に作成されるキーで) レジストリに設定されるドライバー パスが、通常はサンドボックス内を指さないためです。

```
OpenFilePath=c:\program files\MyNewSoftware\SoftwareDriver.sys
```

**注:** サンドボックス化されたプログラムによるドライバーのインストールを許可することは推奨されません。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Restrictions > Low-Level Access](RestrictionsSettings.md#low-level-access-removed)
