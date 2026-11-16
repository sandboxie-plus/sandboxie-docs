# Open Pipe Path

_OpenPipePath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie がファイルに対してサンドボックス化を適用しないパス パターンを指定します。

これは [OpenFilePath](OpenFilePath.md) 設定と同じですが、_OpenFilePath_ はアプリケーションがサンドボックスの外にあるファイルまたはフォルダーから実行されている場合にのみ適用されるのに対し、この設定は常に適用される点が異なります。

一般的な使用手順については [OpenFilePath](OpenFilePath.md) を参照してください。

_OpenPipePath_ 設定は主に、サンドボックス化されたプログラムがファイル通信デバイス リソースにアクセスできるようにすることを目的としており、これらは [Sandboxie Trace](SandboxieTrace.md) を使用して識別できます。

ただし、サンドボックス自体の中から実行されているプログラムに対しても、除外すべきファイルとフォルダーを定義するために使用できます (_OpenFilePath_ がファイルを除外する方法と同様)。

使用例:
```
   .
   .
   .
   [DefaultBox]
   OpenPipePath=\Device\NamedPipe\wkssvc
   OpenPipePath=\Device\NamedPipe\srvsvc
```

サンドボックス化されたプログラムが、リソース _wkssvc_ および _srvsvc_ を通じてコンピューター上の共有とユーザー アカウントを管理できるようにします。

**注:** この特定の例は、サンドボックスの保護を弱めるため、推奨されません。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Resource Access > File Access > Full Access](ResourceAccessSettings.md#file-access-full-access)

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Files > Add File/Folder > Access column > Open for All
