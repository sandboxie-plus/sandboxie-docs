# Block Net Param

_BlockNetParam_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie がサンドボックス化されたプログラムによるネットワークおよびファイアウォール パラメーターの変更を許可するかどうかを指定します。

使用法:

```
   .
   .
   .
   [DefaultBox]
   BlockNetParam=n
```

_n_ を指定すると、サンドボックス化されたプログラムがネットワークおよびファイアウォール パラメーターを変更する要求を発行することが許可されることを示します。
