# Never Delete

_NeverDelete_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。_NeverDelete=y_ の場合、SandMan はボックスが閉じるときに [`AutoDelete`](AutoDelete.md) クリーンアップを開始せず、通常の完全クリーンアップ パスはコンテンツの削除を拒否します。これは、すべての手動スナップショットまたはイメージ バッキング操作に対する絶対的な保護でも、ファイルシステムのアクセス許可の境界でもありません。例:

```
   .
   .
   .
   [DefaultBox]
   NeverDelete=y
```

`NeverRemove` は別個です。これは通常の手動 **Remove Sandbox** アクション (ボックス定義を削除する) を保護します。SandMan では、**Sandbox Options > File Options > Box Delete options > Protect this sandbox from deletion or emptying** はトライステート コントロールです。チェックすると両方の保護が保存されます。部分的にチェックすると `NeverRemove=y` が保存され、`NeverDelete` は保存されません。クリーンアップ後の現在の自動 `AutoRemove` 遷移は `NeverRemove` を参照しません。パス固有の制限と相互作用については [Sandbox Deletion and Removal Lifecycle](SandboxRemoval.md) を参照してください。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Delete > Invocation](DeleteSettings.md#invocation)
