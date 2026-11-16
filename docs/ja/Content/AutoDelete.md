# Auto Delete

AutoDelete は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。AutoDelete=y の場合、SandMan は、アクティブなプロセス数がゼロに達した後にボックスが閉じるのを観測すると、自動的なコンテンツ クリーンアップを開始します。この設定は存在しない場合はオフです。保存されたコンテンツをクリーンアップまたはリセットしますが、サンドボックス定義は削除しません。例:

```
   .
   .
   .
   [DefaultBox]
   AutoDelete=y
```

SandMan は、該当する場合、自動クリーンアップの前に [Quick Recovery](QuickRecovery.md) を提供します。[NeverDelete](NeverDelete.md) はこの自動パスをブロックします。スナップショットが保持されている場合、クリーンアップはボックスを空のままにするのではなく、保存された状態を復元することがあります。[AutoDeleteSnapshotTarget](AutoDeleteSnapshotTarget.md) を参照してください。コンテンツのクリーンアップと定義の削除の区別については、[Sandbox Deletion and Removal Lifecycle](SandboxRemoval.md) を参照してください。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Delete > Invocation](DeleteSettings.md#invocation)

関連する Sandboxie Plus 設定: Sandbox Options > File Options > Box Delete options > Auto delete content changes when last sandboxed process terminates
