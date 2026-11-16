# Hook Trace

`HookTrace` は、SbieDll の共通フック インストール パスを通じてインストールされた関数フックに関する診断情報を記録します。フックの互換性やプロセスの初期化の問題を調査するときに役立ちます。

```ini
[DefaultBox]

HookTrace=y
```

出力は、[Sandboxie Trace](SandboxieTrace.md) および Sandboxie Plus の [Trace Log](../PlusContent/TraceLog.md) で使用される共有モニターの Hook カテゴリに表示されます。一般的なエントリには次が含まれます:

```text
Hooking: module!function
FAILED Hooking: module!function
Skipped Hooking: module!function
Hooking (trace): module!function
```

プラットフォームまたは実装固有の注釈が追加で表示されることがあります。表示されるテキストは、安定した網羅的な形式ではなく診断出力です。

現在の出力には次の注釈が含まれることがあります:

* `(Chrome Hook Hooked)` は、Sandboxie の Chrome 固有のフック処理がそのフックに対して正常に使用されたことを示します。
* `(Chrome Hook Unresolved)` は、Chrome 固有のターゲットをそのパスを通じて解決できなかったことを示します。この注釈だけでは、アプリケーションが失敗することを確定するものではありません。
* `FFS Target not found, hooked x86 code instead` は ARM64EC 固有のフォールバックです。予期される Fast Forward Sequence ターゲットが利用できなかったため、Sandboxie は代わりに x86 側のコードをフックしました。

`HookTrace` はこの共通 SbieDll パスを通じてインストールされたフックをカバーします。Sandboxie のどこかで使用されるすべてのフック メカニズムを報告するわけではありません。プロセスの起動は大量の出力を生成することがあるため、トラブルシューティング中にのみ有効にしてください。

## アプリケーション フッキング記録

`HookTrace` がアクティブな場合、Sandboxie のインターセプトされた `WriteProcessMemory` パスを通じた特定の呼び出しが、次で始まる記録を生成することがあります:

```text
Application Hooking:
```

これらの記録は、サンドボックス化されたアプリケーションがそのパスを呼び出し、宛先アドレスを別のモジュールのエクスポートされた関数に関連付けることができる場合に表示されることがあります。現在の記録には、解決されたモジュールとエクスポート、オフセット、および書き込まれるバイトの 16 進数表現が含まれます。これは、Sandboxie 自身のフックと相互作用する可能性のあるアプリケーション レベルのコード パッチまたはフッキングの診断に役立ちます。

この記録は、すべての `WriteProcessMemory` 呼び出しがログに記録されること、Sandboxie がすべてのアプリケーション フッキングを検出すること、またはその活動が悪意のあるものであることを意味するものではありません。

この設定はプロセスごとに初期化されます。有効化、無効化、または変更した後は、影響を受けるサンドボックス化されたプロセスを再起動してください。

`HookTrace` は Sandboxie Plus 1.15.5 および Sandboxie Classic 5.70.5 で導入されました。

## 関連設定

* [Function Skip Hook](FuncSkipHook.md) は関数名によってフックを選択的に抑制します。
* [Skip Hook](SkipHook.md) は一致するプロセスに対して名前付きの Sandboxie フック グループを制御します。

## 関連ページ

* [Sandboxie Trace](SandboxieTrace.md)
* [Trace logging](../PlusContent/TraceLog.md)
