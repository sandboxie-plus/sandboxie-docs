# Notify Start Run Access Denied

_NotifyStartRunAccessDenied_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。既定は `y` です。

```ini
[DefaultBox]
NotifyStartRunAccessDenied=y
```

サンドボックスの Start/Run 制限メカニズムが関連する起動またはアクセス操作を拒否した場合、この設定は [SBIE1308](SBIE1308.md) の生成を制御します。メッセージは通常、影響を受けるプロセスごとに 1 回発行されます。これを無効にしても起動が許可されたり、基になる Start/Run ポリシーが変更されたりすることはありません。

Sandboxie Plus では、**Sandbox Options > Program Control > Start Restrictions** を開き、**Issue message 1308 when a program fails to start** を使用します。Sandboxie Control Classic は、対応するオプションを [Sandbox Settings > Restrictions > Start/Run Access](RestrictionsSettings.md#startrun-access) の下で公開しています。

値はサンドボックス化されたプロセスの状態にキャッシュされます。予測可能な動作のために、変更後は影響を受けるサンドボックス化されたプロセスを再起動してください。

`AlertStartRunAccessDenied` は、プログラム アラート メカニズムによって使用される別個のグローバル設定です。2 つの設定は独立して使用され、異なる拒否パスから SBIE1308 を生成できます。これらはエイリアスではありません。

より広範なメッセージ モデルについては [Notification Settings](NotificationSettings.md) を、別個の起動前確認機能については [Alert Before Start](AlertBeforeStart.md) を参照してください。
