# Closed Ipc Path

_ClosedIpcPath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。サンドボックス化されたプログラムによる _すべて_ のアクセス ( _読み取り_ アクセスを含む) を Sandboxie が拒否するパス パターンを指定します。この設定は基本的に、サンドボックス化されたプログラムがリソースにアクセスするのをブロックします。

[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:

```
   .
   .
   .
   [DefaultBox]
   ClosedIpcPath=\RPC Control\AudioSrv
```

サンドボックス化されたファイル、フォルダー、およびレジストリ キーとは異なり、Sandboxie は一般にサンドボックス化されたプログラムがサンドボックス化されていないリソースにアクセスすることを許可しません。このルールの例外は、リソースが [OpenIpcPath](OpenIpcPath.md) 設定で指定されている場合、または Sandboxie が既定でそのリソースを認識し、サンドボックス内で使用できるように公開している場合です。

_ClosedIpcPath_ 設定は通常、Sandboxie が既定で認識するリソースをブロックするのに役立ちます。上記の例では、AudioSrv リソースがブロックされています。このリソースはオーディオ ハードウェアへのアクセスを提供します。つまり、サンドボックス化されたプログラムが音声を生成できるようにします。これをブロックすることで、サンドボックス化されたプログラムは事実上ミュートになります。

この設定はワイルドカードを受け入れます。_OpenXxxPath_ および _ClosedXxxPath_ 設定でのワイルドカードの使用の詳細については、[OpenFilePath](OpenFilePath.md) を参照してください。

**注:** 対応する [OpenIpcPath](OpenIpcPath.md) 設定とは異なり、_ClosedIpcPath_ 設定は、プログラムの実行可能ファイルがサンドボックス内にあるか外にあるかに関係なく、常にサンドボックス化されたプログラムに適用されます。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Resource Access > IPC Access > Blocked Access](ResourceAccessSettings.md#ipc-access-blocked-access)

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > IPC > Add IPC Path > Access column > Closed
