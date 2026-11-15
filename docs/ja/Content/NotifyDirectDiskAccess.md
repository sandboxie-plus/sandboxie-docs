# Notify Direct Disk Access

_NotifyDirectDiskAccess_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。既定は `n` です。

```ini
[DefaultBox]
NotifyDirectDiskAccess=y
```

有効にすると、Sandboxie はディスク デバイスを直接開こうとする特定の拒否された試行に対して [SBIE1313](SBIE1313.md) を発行します。拒否されたすべてのディスク アクセス要求、またはデバイス配下のファイルとフォルダーへのアクセスを報告するわけではありません。

有効なファイル アクセス ルールがホスト アクセスを完全にブロックする場合 (`ClosedFilePath` や `WriteFilePath` など)、メッセージは生成されません。`ReadFilePath` ルールは常にメッセージを抑制するわけではありません。拒否された書き込み要求は依然としてそれを生成することがあります。

この設定は通知のみを制御します。直接のディスク アクセスを許可したり、要求を拒否したポリシーを変更したりしません。[Allow Raw Disk Read](AllowRawDiskRead.md)、[Open File Path](OpenFilePath.md)、[Open Pipe Path](OpenPipePath.md) などのアクセス関連の設定は別個です。

Sandboxie Plus では、**Sandbox Options > General Options > File Options** を開き、**Disk/File access** を見つけて、**Warn when an application opens a harddrive handle** を選択します。Sandboxie Control Classic には、同等の専用の現在のコントロールはありません。

値はサンドボックス化されたプロセスが初期化されるときにキャッシュされます。予測可能な動作のために、変更後は影響を受けるサンドボックス化されたプロセスを再起動してください。

アクセス ポリシー、メッセージの生成、および表示の区別については [Notification Settings](NotificationSettings.md) を参照してください。
