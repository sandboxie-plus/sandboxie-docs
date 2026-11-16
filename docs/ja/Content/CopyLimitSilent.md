# Copy Limit Silent

_CopyLimitSilent_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。通常は _CopyLimitSilent=y_ として指定され ([Yes Or No Settings](YesOrNoSettings.md) を参照)、Sandboxie がアラート メッセージ [SBIE2102](SBIE2102.md) を発行しないことを示します。

有効な値が構成されていない場合、コンシューマーのフォールバックは `n` です。該当するテンプレートおよび `[GlobalSettings]` が有効な値を提供できます。

使用法:

```
   .
   .
   .
   [DefaultBox]
   CopyLimitSilent=y
```

明示的な移行ルールが適用されず、有限の [CopyLimitKb](CopyLimitKb.md) しきい値に到達または超過した場合、SBIE2102 は、使用可能なプロンプト応答が返されず、かつこの設定が有効になっていない場合にのみ発行されます。これには、プロンプトの無効化、対話型コンシューマーが利用できない場合、またはタイムアウトが含まれます。肯定的な応答は SBIE2102 なしで移行を選択し、明示的な否定的な応答はこの決定パスから SBIE2102 なしで非コピーを選択します。

この設定はメッセージを変更し、移行の決定を変更しません。[大きなファイルのプロンプト](PromptForFileMigration.md)を無効にしたり、[NotifyNoCopy](NotifyNoCopy.md) のメッセージ SBIE2113/2114/2115 を制御したり、すべての移行またはプロンプト転送エラーを抑制したりするものではありません。

このフラグはプロセスの初期化中にキャッシュされます。変更後は影響を受ける新しいサンドボックス化されたプロセスを開始してください。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [CopyLimitKb](CopyLimitKb.md)、[PromptForFileMigration](PromptForFileMigration.md)。
