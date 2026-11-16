# Block Fake Input

**この機能は SBIE バージョン 4 以降で削除されました。現在は利用できません。**


_BlockFakeInput_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定でした。Sandboxie がサンドボックス化されたプログラムによる偽のキーボード入力の生成と、そのサンドボックス外で実行されているアプリケーションのウィンドウへの送信を許可するかどうかを指定していました。

使用法:

```
   .
   .
   .
   [DefaultBox]
   BlockFakeInput=n
```

キーボード入力は、アクティブで強調表示されているウィンドウによって受信されます。これは、キーボード入力がプログラムによって生成された場合 (偽の入力) でも、キーボードから来た場合 (実際の入力) でも当てはまります。

既定では、Sandboxie は、受信側のウィンドウが同じサンドボックス内で実行されているアプリケーションに属している限り、サンドボックス内で実行されているプログラムによる偽の入力の生成を許可します。

偽の入力がそのサンドボックス外のウィンドウに到達する場合、Sandboxie はその入力を破棄し、メッセージ [SBIE1304](SBIE1304.md) を発行します。

_BlockFakeInput=n_ を指定すると、サンドボックス化されたプログラムが、その入力の受信者に関係なく、偽のキーボード入力を生成できるようにすることを示します。

この設定を試すには、Windows のオンスクリーン キーボードである _osk.exe_ のサンドボックス化されたインスタンスを実行できます。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Restrictions > Hardware Access](RestrictionsSettings.md#hardware-access-removed)
