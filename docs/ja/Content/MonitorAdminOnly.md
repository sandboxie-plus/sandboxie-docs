# Monitor Admin Only

_MonitorAdminOnly_ は [Sandboxie Ini](SandboxieIni.md) のグローバル設定です。指定すると、Administrators グループのメンバーではないユーザー アカウントで実行されている [Sandboxie Control](SandboxieControl.md) は、[Resource Access Monitor](ResourceAccessMonitor.md) 機能を呼び出せなくなります。

その根拠は、Resource Access Monitor が呼び出される各ユーザー セッションに対して 64K バイトのシステム メモリを消費するため、ネットワーク管理者がユーザーによるその機能の呼び出しを防ぎたい場合があることです。

使用法:

```
   .
   .
   .
   [GlobalSettings]
   MonitorAdminOnly=y
```

この設定は、ネットワーク管理者による使用を目的としています。
