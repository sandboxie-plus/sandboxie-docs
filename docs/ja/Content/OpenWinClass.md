# Open Win Class

_OpenWinClass_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。サンドボックス化されたプログラムからアクセス可能にすべき、サンドボックス化されていないウィンドウのクラス名を指定します。

例:
```
   .
   .
   .
   [DefaultBox]
   OpenWinClass=ConsoleWindowClass
   OpenWinClass=$:program.exe/IgnoreUIPI
   OpenWinClass=#
   OpenWinClass=*
```

最初の例は、_cmd.exe_ プロセスによって作成されたコンソール ウィンドウをサンドボックス化されたプログラムからアクセス可能にします。

通常、Sandboxie はサンドボックス化されたプログラムがサンドボックスの外のウィンドウにアクセス、通信、閉じる、または破棄することを許可しません。_OpenWinClass_ 設定はこのルールに対する例外を作り、特定のサンドボックス化されていないウィンドウをアクセス可能にします。

**特殊な形式**
```
   OpenWinClass=$:program.exe/IgnoreUIPI
```

これにより、サンドボックス内で実行されているプログラムが PostThreadMessage API を使用して、サンドボックスの外で実行されているターゲット プロセスのスレッドに直接メッセージを送信できます。この形式の _OpenWinClass_ 設定はワイルドカードをサポートしないため、ターゲット プロセスのプロセス名は設定で指定された名前と一致する必要があります。
```
   OpenWinClass=#
```

この設定は、サンドボックス化されたプログラムによって作成されたウィンドウ クラス名を Sandboxie が変更しないように指示します。通常、Sandboxie はサンドボックス化されたプログラムに属するウィンドウをシステム内の他のウィンドウからより適切に分離するために、_IEFrame_ などのクラス名を _Sandbox:DefaultBox::IEFrame_ に変換します。

ただし、場合によっては、サンドボックスの外のプログラムがウィンドウ クラス名に特定の名前を期待することがあり、そのためサンドボックス化されたプログラムによって作成されたウィンドウを認識しないことがあります。OpenWinClass=# を指定するとこの問題が解決されますが、分離の程度が低くなります。

OpenWinClass=# はサンドボックスの外の任意のウィンドウとの通信を許可せず、一部のドラッグ アンド ドロップ操作に干渉する可能性があることに注意してください。
```
   OpenWinClass=*
```

この設定は、上記のようにウィンドウ クラス名を変換しないよう Sandboxie に指示し、さらにシステム内のすべてのウィンドウをサンドボックス化されたプログラムからアクセス可能にし、いくつかの他のウィンドウ関連の Sandboxie 機能を無効にします。これにより、Sandboxie インジケーター [#] がウィンドウ タイトルに表示されなくなることもあります。

OpenWinClass=* はサンドボックスの外のすべてのウィンドウとの完全な通信を許可しますが、一部のドラッグ アンド ドロップ操作に干渉する可能性があることに注意してください。

`OpenWinClass=*` がアクティブな場合、Sandboxie の通知領域の互換性プロキシは既定で有効になります。この動作は [Use Shell Notify Icon Proxy](UseShellNotifyIconProxy.md) で上書きできます。

**ウィンドウ クラス名の識別**

サンドボックス化されていないウィンドウは、_ウィンドウ クラス名_ によって識別されます。これは、ウィンドウを作成したアプリケーションによって付けられた内部名です。[WinSpy](https://www.catch22.net/software/winspy) などのツールを使用してウィンドウ クラス名を識別できます。Sandboxie Classic の [Resource Access Monitor](ResourceAccessMonitor.md) ツールと Sandboxie Plus の [Trace Logging](../PlusContent/TraceLog.md) ツールもウィンドウ クラス名を表示します。

関連する Sandboxie Plus 設定:

Sandbox Options > Resource Access > Wnd > Add Wnd Class > Access column > Open

Sandbox Options > Resource Access > Wnd > Add Wnd Class > Access column > Ignore UIPI

Sandbox Options > Resource Access > Wnd > Don't alter window class names created by sandboxed programs

参照: [No Rename Win Class](NoRenameWinClass.md)。
