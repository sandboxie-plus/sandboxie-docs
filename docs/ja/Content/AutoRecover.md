# Auto Recover

_AutoRecover_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。_AutoRecover=y_ の場合、SbieDll は有効な [RecoverFolder](RecoverFolder.md) および [AutoRecoverIgnore](AutoRecoverIgnore.md) エントリを使用して、プロセス側の [Immediate Recovery](ImmediateRecovery.md) 検出を初期化します。該当するファイルを復元 UI に報告しますが、それ自体がファイルをホストに移動するわけではありません。

有効な値が存在しない場合、検出器の実行時フォールバックは無効になります。Classic の新規ボックスの既定では明示的に有効になり、現在の SandMan の新規ボックス ウィザードでは既定で有効になっています。[Quick Recovery](QuickRecovery.md) は、その SandMan スキャンが別個であるため、_AutoRecover=n_ でも利用できます。自動検出の設定を変更した後は、影響を受けるサンドボックス化されたプロセスを再起動してください。

使用法:

```
   .
   .
   .
   [DefaultBox]
   AutoRecover=y
```

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Recovery > Immediate Recovery](RecoverySettings.md#immediate-recovery)

ワークフロー全体については [File Recovery Architecture](RecoveryArchitecture.md) を参照してください。
