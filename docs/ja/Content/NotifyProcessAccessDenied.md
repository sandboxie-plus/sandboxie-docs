# Notify Process Access Denied

_NotifyProcessAccessDenied_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 1.0.18 / Classic 5.55.18 以降で使用できます。既定は `n` です。

```ini
[DefaultBox]
NotifyProcessAccessDenied=y
```

有効にすると、Sandboxie は、プロセスと IPC 保護パスによって拒否されたサポート対象の明示的なプロセスまたはスレッド アクセス要求 (関連する拒否された `OpenProcess` および `OpenThread` 要求を含む) に対して [SBIE2111](SBIE2111.md) を発行します。これは、可能なすべてのプロセス ハンドル失敗が SBIE2111 を生成することを意味しません。

この設定は通知のみを制御します。基になるプロセス アクセス制限を緩和しません。

Sandboxie Plus では、**Sandbox Options > General Options > Restrictions > Other restrictions** を開き、**Issue message 2111 when a process access is denied** を選択します。同等の専用の現在の Sandboxie Control Classic コントロールは見つかりませんでした。

値はサンドボックス化されたプロセスが初期化されるときにキャッシュされます。予測可能な動作のために、変更後は影響を受けるサンドボックス化されたプロセスを再起動してください。

より広範なメッセージ モデルについては [Notification Settings](NotificationSettings.md) を参照してください。
