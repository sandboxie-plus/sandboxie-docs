# Prompt For File Migration

PromptForFileMigration は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。通常のコンテンツ移行の決定が有限の [CopyLimitKb](CopyLimitKb.md) しきい値に達するか超え、明示的な移行ルールがまだモードを選択していない場合に、Sandboxie が対話的な決定を要求するかどうかを制御します。詳細については [SBIE2102](SBIE2102.md) を参照してください。

有効な値が構成されていない場合、コンシューマーのフォールバックは `y` です。有効な値は、適用可能な有効なテンプレートまたは `[GlobalSettings]` フォールバックから取得することもできます。

```
   .
   .
   .
   [DefaultBox]
   PromptForFileMigration=n
```

_n_ を指定すると対話的な要求が無効になります。プロンプトが有効な場合、SandMan は要求を表示できますが、利用可能な対話的コンシューマーと使用可能な応答は保証されません。肯定的な回答はその試行のために完全なコンテンツの移行を選択しますが、コピーの成功は保証されません。否定的な回答、無効化されたプロンプト、または使用可能な応答がない場合は、非コピー パスを選択します。

最初の移行依存のオープンの場合、[CopyBlockDenyWrite](CopyBlockDenyWrite.md) が、書き込みおよび削除アクセスを削除したホスト オープンの再試行に対する拒否かどうかを決定します。再試行自体が失敗する可能性があります。プロンプトを無効にしても読み取り専用アクセスは保証されません。明示的な **No** の回答は、この決定パスから SBIE2102 を生成しません。使用可能な応答が返されない場合、[CopyLimitSilent](CopyLimitSilent.md) がそのメッセージを制御します。

SandMan は **Remember for this process** を提供します。記憶された回答は、同じファイルだけでなく、そのプロセスに対する以降の移行要求に適用されます。これはプロセス ローカルの UI 状態であり、永続的な INI の例外でも _CopyLimitKb_ の変更でもありません。

関連する Sandboxie Plus 設定: Sandbox Options > General Options > File Migration > **Prompt user for large file migration**。Sandboxie Control Classic は、同等の対話的移行プロンプト コンシューマーを提供しません。

## 変更の適用

キャッシュされたサイズ制限およびサイレント フラグとは異なり、この設定は対象となる巨大な移行の決定ごとに照会されます。有効な構成が再読み込みされた後、既に実行中のプロセスの以降の決定は変更された値を使用できます。既に進行中の要求は遡って変更されません。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [CopyLimitKb](CopyLimitKb.md)、[CopyLimitSilent](CopyLimitSilent.md)
