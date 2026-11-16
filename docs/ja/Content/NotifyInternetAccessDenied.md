# Notify Internet Access Denied

_NotifyInternetAccessDenied_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。既定は `y` です。

```ini
[DefaultBox]
NotifyInternetAccessDenied=y
```

Sandboxie のインターネット アクセス ポリシーがサンドボックス化されたプロセスを拒否した場合、この設定は [SBIE1307](SBIE1307.md) の生成を制御します。メッセージは通常、影響を受けるプロセスごとに 1 回発行されます。メッセージを無効にしてもインターネット アクセスが許可されたり、ネットワーク ポリシーが変更されたりすることはありません。

Sandboxie Plus では、**Sandbox Options > Network Options > Internet Access** を開き、**Issue message 1307 when a program is denied internet access** を使用します。Sandboxie Control Classic は、対応するオプションを [Sandbox Settings > Restrictions > Internet Access](RestrictionsSettings.md#internet-access) の下で公開しています。

値はサンドボックス化されたプロセスの状態にキャッシュされます。予測可能な動作のために、変更後は影響を受けるサンドボックス化されたプロセスを再起動してください。

このメッセージ スイッチは、ランタイム例外を付与するかどうかを尋ねることができる [Prompt For Internet Access](PromptForInternetAccess.md) とは別個です。より広範なメッセージ モデルについては [Notification Settings](NotificationSettings.md) を参照してください。
