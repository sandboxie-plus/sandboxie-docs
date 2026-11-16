# Hide Other Boxes

_HideOtherBoxes_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、v0.3 / 5.42 以降で使用できます。そのランタイム フォールバックは `y` です。別のサンドボックスに割り当てられたプロセスのエントリは、Sandboxie のフィルター処理されたネイティブ プロセス リストの結果から削除されます。同じボックスに割り当てられたエントリ、またはサンドボックス関連付けのないエントリは、この設定によって削除されません。この特定のフィルターを無効にするには:

```
   .
   .
   .
   [DefaultBox]
   HideOtherBoxes=n
```

`HideOtherBoxes=n` を設定しても、他のボックスのプロセスがすべての列挙方法を通じて現れることは保証されず、この設定自体が既知の PID によるプロセスへのアクセスを制御することもありません。

SandMan では、チェックボックスは Sandbox Options > Advanced Options > Processes > Process Hiding > Don't allow sandboxed processes to see processes running in other boxes です。ボックス側の直接の既定値はチェック済みです。構成を通じて継承された有効な値は、直接のチェックボックスの状態と異なることがあります。

値は以降の列挙時に読み取られるため、`NtQuerySystemInformation` フックがそのプロセスにインストールされていれば、構成の再読み込みが既に実行中のプロセスに影響を与えることがあります。フックと WMI の制限については [Hide Non System Processes](HideNonSystemProcesses.md) を参照してください。
