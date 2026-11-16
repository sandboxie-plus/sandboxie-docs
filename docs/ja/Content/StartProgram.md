# Start Program

_StartProgram_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。指定されたプログラムの自動起動を提供します。例:

```
   .
   .
   .
   [DefaultBox]
   StartProgram=%ProgramFiles%\Google\Chrome\Application\chrome.exe
```

この例は、Google Chrome (chrome.exe) がサンドボックス _DefaultBox_ 内で強制的にサンドボックス化されて実行されることを指定しています。

**技術的な詳細**

_StartProgram_ は [SandboxieRpcSs](ServicePrograms.md#remote-procedure-call-rpc) によって処理され、これは各サンドボックスで 1 回だけ実行されます。[AutoExec](AutoExec.md) 設定と同様に、最初のプログラムがサンドボックス内で実行を開始したときに処理されます。_StartProgram_ は、サポートされている場合、指定されたアプリケーションを非表示モードで起動することに注意してください。

サービスについては、[StartService](StartService.md) を参照してください。
