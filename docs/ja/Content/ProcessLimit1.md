# Process Limit 1

**ProcessLimit1 と ProcessLimit2 は、[ProcessLimit](ProcessLimit.md) を優先して Sandboxie v0.7.1 / 5.48.5 以降で削除されました。**

_ProcessLimit1_ と _ProcessLimit2_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定でした。Sandboxie がサンドボックス内で同時に許可するプロセスの最大数を制限しました。
```
   .
   .
   .
   [DefaultBox]
   ProcessLimit1=100
   ProcessLimit2=200
```

ProcessLimit1: サンドボックスが同時に X 個を超えるプログラムを持つと、新しい各プログラムは実行を開始する前に 10 秒間遅延されます。X は ProcessLimit1\ で指定された数です。遅延の長さ (10 秒) は構成できません。

ProcessLimit2: サンドボックスが同時に Y 個を超えるプログラムを持つと、新しい各プログラムは即座に終了されます。Y は ProcessLimit2\ で指定された数です。

既定の数は上記のとおり 100 と 200 です。ProcessLimit2 は ProcessLimit1 より小さくすることはできません。

独創的な値で一方または両方のモードをオフにできます。たとえば、
```
	ProcessLimit2=999999
```

は終了機能を事実上無効にします。一方、
```
	ProcessLimit1=50
	ProcessLimit2=50
```

は遅延機能を事実上無効にします。
