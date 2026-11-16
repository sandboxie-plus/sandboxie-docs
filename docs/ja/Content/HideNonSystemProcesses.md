# Hide Non System Processes

_HideNonSystemProcesses_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。そのランタイム フォールバックは `n` です。

```
   .
   .
   .
   [DefaultBox]
   HideNonSystemProcesses=y
```

`HideNonSystemProcesses=y` の場合、Sandboxie はフィルター処理されたネイティブ プロセス リストの結果から、サンドボックスに関連付けられていない多くのエントリを削除します。

> [!CAUTION]
> システムおよびサービスの SID 例外は、サンドボックス関連付けのないエントリを保護しません。これは、サンドボックス化された呼び出し元が使用するクエリ API がそれらのターゲットの SID を返さないためです。したがって、正当なシステムまたはサービス プロセスも非表示になることがあります。

この設定は、あらゆるメカニズムを通じた検出を防いだり、既知の PID によるプロセスへのアクセスを拒否したりするものではありません。WMI はプロセス情報を公開する可能性のある別個のパスです。SandMan は別個の WMI ブロック オプションを提供していますが、この設定が一般的な WMI フィルターになるわけではありません。

SandMan では、チェックボックスは Sandbox Options > Advanced Options > Processes > Process Hiding > Don't allow sandboxed processes to see processes running outside any boxes です。ボックス側の直接の既定値はオフです。構成を通じて継承された有効な値は、直接のチェックボックスの状態と異なることがあります。

値は以降の列挙時に読み取られるため、`NtQuerySystemInformation` フックがそのプロセスにインストールされていれば、構成の再読み込みが既に実行中のプロセスに影響を与えることがあります。そのフックがプロセスの初期化時に [SkipHook](SkipHook.md) (`ntqsi`) を通じてスキップされた場合、この値を変更しても遡ってインストールされることはありません。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [Hide Host Process](HideHostProcess.md)、[Hide Other Boxes](HideOtherBoxes.md)、および [Hide Sandboxie Processes](HideSbieProcesses.md)。
