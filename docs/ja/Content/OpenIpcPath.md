# Open Ipc Path

_OpenIpcPath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie がプロセス間オブジェクトに対してサンドボックス化を適用しないパス パターンを指定します。これにより、サンドボックス化されたプログラムがサンドボックスの外で実行されているプログラムによって提供されるリソースとサービスにアクセスできます。

[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:
```
   .
   .
   .
   [DefaultBox]
   OpenIpcPath=\RPC Control\IcaApi
   OpenIpcPath=\RPC Control\seclogon
   OpenIpcPath=$:program.exe
```

[Sandboxie Trace](SandboxieTrace.md) で説明されているように、一部のサンドボックス化されたプログラムは、正しく機能するためにサンドボックスの外のシステム リソースへのアクセスを必要とすることがあります。Sandboxie トレース機能を使用して必要なリソースを特定した後、この設定を使用して、サンドボックス化されたプログラムが使用するためのリソースを公開します。

```
OpenIpcPath=\RPC Control\IcaApi
```

最初の例は、ターミナル サービス サブシステムによって提供されるリソースを公開します。これにより、サンドボックス化されたプログラムがそのサブシステムと通信し、コンピューター内でアクティブな他のターミナル サーバー セッションを検出できます。ただし、このリソースは Sandboxie の制御外のプログラムを終了させるためにも使用できます。

```
OpenIpcPath=\RPC Control\seclogon
```
2 番目の例は、Windows の _Run As_ サービスによって提供されるリソースを公開します。これにより、サンドボックス化されたプログラムが別のユーザーの資格情報を使用して別のプログラムを起動できます。起動されたプログラムは、サンドボックス内で実行する [v0.7.3 / 5.49.5](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.7.3) まで Sandboxie の制御外で実行されていました。

この設定はワイルドカードを受け入れます。_OpenXxxPath_ および _ClosedXxxPath_ 設定でのワイルドカードの使用の詳細については、[OpenFilePath](OpenFilePath.md) を参照してください。

```
OpenIpcPath=$:program.exe
```
3 番目の例は、サンドボックス内で実行されているプログラムが、サンドボックスの外で実行されているターゲット プロセスのアドレス空間に完全にアクセスできるようにします。ターゲット プロセスのプロセス名は、設定で指定された名前と一致する必要があります。この設定が指定されていない場合、Sandboxie はサンドボックス化されたプロセスによるサンドボックスの外のプロセスへの読み取りアクセスのみを許可します。この形式の _OpenIpcPath_ 設定はワイルドカードをサポートしません。

**注:** このページの例を適用すると、サンドボックス内に脆弱性が作成されます。これらは、一部のリソースがブロックされる理由と、必要に応じてそれらをブロック解除して使用のために公開する方法を示すことのみを目的としています。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Resource Access > IPC Access > Direct Access](ResourceAccessSettings.md#ipc-access-direct-access)

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > IPC > Add IPC Path > Access column > Open
