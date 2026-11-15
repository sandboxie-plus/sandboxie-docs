# Linger Exempt Wnds

_LingerExemptWnds_ は [Sandboxie Ini](SandboxieIni.md) のボックスごとのブール設定で、Sandboxie Plus 1.13.4 / Classic 5.68.4 以降で使用できます。既定は `y` です。

```ini
[DefaultBox]
LingerExemptWnds=n
```

自動 linger クリーンアップが発生する場合、`LingerExemptWnds=y` は、残っているサンドボックス プロセスが可視のトップレベル ウィンドウを持っている間、そのクリーンアップを防ぎます。`n` に設定すると、可視ウィンドウの例外が削除されます。

この設定はプロセスを lingerer にするものではなく、単独で終了をトリガーするものでもありません。[Linger Process](LingerProcess.md) は構成された linger 候補を識別し、`LingerLeniency` は別個の起動および猶予期間の例外を制御します。

Sandboxie Plus は、**Sandbox Options > Program Control > Stop Behaviour > Stop Options** の下で **Don't stop lingering processes with windows** としてこの設定を公開しています。チェックボックスは既定の `y` 動作に対して選択されています。

値は linger クリーンアップの評価中に読み取られます。関連するリーダー、linger、または寛容性ポリシーを変更した後に予測可能な動作を得るには、影響を受けるサンドボックス プロセス ツリーを再起動または再作成してください。

ライフサイクルの完全な概要については [Program Stop Settings](ProgramStopSettings.md) を参照してください。
