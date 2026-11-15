# Normal IPC Path

_NormalIpcPath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。一致する名前付き IPC オブジェクトに対して Sandboxie の通常/既定の IPC 処理を復元します。ホストへの直接アクセスを許可するものではありません。

[Rule Specificity](../PlusContent/RuleSpecificity.md) が有効な場合、より具体的な Normal ルールは、マッチャーがそれを選択したときに、より広範な Open または Closed IPC パス ルールを上書きできます。

```ini
[DefaultBox]
NormalIpcPath=\RPC Control\AudioSrv
```

IPC パス ルールは、Sandboxie がワイルドカードなしで File および Registry ルールに通常追加する暗黙の末尾 `*` を受け取りません。したがって、この例は構成された IPC パターン自体に従って一致します。より広範な一致を意図する場合は、ワイルドカードを明示的に追加してください。

関連する Sandboxie Plus 設定: **Sandbox Options > Resource Access > IPC > Add IPC Path > Access column > Normal**
