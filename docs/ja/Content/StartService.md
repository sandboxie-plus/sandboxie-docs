# Start Service

_StartService_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。サンドボックス内でサービス プログラムを実行できます。この設定は、サンドボックスの外部で定義されたサービス名 (識別子) を想定しています。例:

```
   .
   .
   .
   [DefaultBox]
   StartService=Adguard Service
```

この例は、サービス名 _Adguard Service_ がサンドボックス _DefaultBox_ 内で強制的にサンドボックス化されて実行されることを指定しています。

**技術的な詳細**

_StartService_ は [SandboxieRpcSs](ServicePrograms.md#remote-procedure-call-rpc) によって処理され、これは各サンドボックスで 1 回だけ実行されます。[AutoExec](AutoExec.md) 設定と同様に、最初のプログラムがサンドボックス内で実行を開始したときに処理されます。

アプリケーションについては、[StartProgram](StartProgram.md) を参照してください。
