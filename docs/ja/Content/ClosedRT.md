# Closed RT

_ClosedRT_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、v0.5.3a / 5.45.2 以降で利用できます。サンドボックス化されたプログラムがアクセスできないようにする必要がある、問題のある Windows RT インターフェイスを指定します。

使用法:
```
   .
   .
   .
   [DefaultBox]
   ClosedRT=ExampleRT
```

この例は、_ExampleRT_ インターフェイスをサンドボックス化されたプログラムからアクセスできないようにします。

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > COM > Add COM Object > Access column > Closed RT
