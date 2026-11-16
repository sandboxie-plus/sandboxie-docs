# No Rename Win Class

_NoRenameWinClass_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie によって変換されるべきでないウィンドウ クラス名を指定します。

使用法:
```
   .
   .
   .
   [DefaultBox]
   NoRenameWinClass=ExampleWinClass
   NoRenameWinClass=program.exe,*
```

最初の設定は、_ExampleWinClass_ ウィンドウ クラス名をサンドボックス化されたプログラムからアクセス可能にすることで変換しないよう Sandboxie に指示し、さらにいくつかの他のウィンドウ関連の Sandboxie 機能を無効にします。これにより、Sandboxie インジケーター [#] がウィンドウ タイトルに表示されなくなることもあります。

2 番目の設定は、_program.exe_ によって作成されたウィンドウ クラス名をサンドボックス化されたプログラムからアクセス可能にすることで変換しないよう Sandboxie に指示し、さらにいくつかの他のウィンドウ関連の Sandboxie 機能を無効にします。これにより、Sandboxie インジケーター [#] がウィンドウ タイトルに表示されなくなることもあります。

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Wnd > Add Wnd Class > Access column > No Rename
