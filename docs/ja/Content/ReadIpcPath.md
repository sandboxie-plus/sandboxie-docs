# Read IPC Path

_ReadIpcPath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 1.0.16 / Classic 5.55.16 以降で使用できます。文書化されたプロセス ターゲット形式は、サンドボックス化されたプログラムから、サンドボックス化されていないプロセスまたは別のサンドボックス内のプロセスへの制限された読み取りアクセスを許可します。

```ini
[DefaultBox]
ReadIpcPath=$:program.exe
```

オプションの [Program Name Prefix](ProgramNamePrefix.md) で、このルールが適用されるサンドボックス化されたソース プロセスを限定できます。例:

```ini
ReadIpcPath=source.exe,$:target.exe
```

ここで `source.exe` はアクセス試行を行うサンドボックス化されたプロセスを選択し、`$:target.exe` は外部ターゲット プロセスを識別します。ソース セレクターはそのサンドボックス化されたプロセスに対してルールが読み込まれるかどうかを決定し、`$:` ターゲットは別個のプロセス/スレッド アクセス マッチャーによって評価されます。

`$:` プレフィックスはターゲット プロセスを識別します。このパスのプロセス名の照合は大文字と小文字を区別しません。サポートされている文書化された形式は、実行可能ファイル名と、明示的な全プロセスの特殊ケースです:

```ini
ReadIpcPath=$:program.exe
ReadIpcPath=$:*
```

`$:service*.exe` などの形式を一般的なワイルドカード一致として扱わないでください。現在のターゲット プロセス マッチャーはその動作を提供しません。

ターゲット プロセス アクセスの場合、関連するルールの順序は Closed、次に Open、次に Read です:

* 一致する `ClosedIpcPath=$:...` ルールはアクセスを拒否します。
* 一致する `OpenIpcPath=$:...` ルールはより広範なプロセス/スレッド アクセスを付与できます。
* 一致する `ReadIpcPath=$:...` ルールは制限された読み取りカテゴリを許可します。

このターゲット プロセス ポリシーは [Rule Specificity](../PlusContent/RuleSpecificity.md) とは別個です。`UseRuleSpecificity` は `$:` アクションの順序を変更しません。

一般的な名前付き IPC オブジェクト アクセスは、主に Normal、Open、および Closed IPC パス ルールによって制御されます。`ReadIpcPath` は、任意の名前付きオブジェクトに対する `ReadFilePath` の直接の IPC 相当として扱うべきではありません。Sandboxie コンポーネントは、この設定に対して追加の限定的なコンシューマーを持つことがあります。

組み込み構成には、互換性のために `explorer.exe` への読み取りアクセスが含まれています。サンドボックスに対してそれを上書きするには、次を使用します:

```ini
[DefaultBox]
ClosedIpcPath=$:explorer.exe
```

関連する Sandboxie Plus 設定:

* **Sandbox Options > Resource Access > IPC > Add IPC Path > Access column > Read Only**
* **Sandbox Options > General Options > Restrictions > Other restrictions > Allow to read memory of unsandboxed processes (not recommended)**
