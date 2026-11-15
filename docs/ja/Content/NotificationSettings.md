# 通知設定

Sandboxie の通知設定は、一般に、特定のイベントが発生したときに SBIE メッセージが生成されるかどうかを制御します。操作を許可または拒否したポリシーを変更するものではありません。たとえば、`NotifyInternetAccessDenied` を無効にするとその拒否メッセージが抑制されますが、インターネット アクセスは付与されません。

メッセージの生成は、表示とも別個です。SandMan または Sandboxie Control Classic は、独自の表示設定に従って、生成されたメッセージをログ、ポップアップ、またはその他のインターフェイスに表示する場合があります。専用のユーザー インターフェイス コントロールを持つ通知設定は一部のみです。

このページの設定は、1 つの通知サブシステムではなく、いくつかの Sandboxie コンポーネントによって実装されています。サンドボックス化されたプロセスの初期化時にキャッシュされるものもあれば、イベントの発生時に読み取られるものもあります。ここで取り上げる Boolean 設定には、実行可能ファイル修飾構文はありません。

一般的なボックス設定:

```ini
[DefaultBox]
NotifyInternetAccessDenied=y
```

一般的なグローバル設定:

```ini
[GlobalSettings]
NotifyForceProcessEnabled=y
```

## リファレンス {#reference}

| 設定 | 既定 | スコープ | トリガーまたはメッセージ | 変更の適用 / UI の注意 |
| --- | --- | --- | --- | --- |
| `AlwaysShowReminder` | `n` | グローバル | サポート/リマインダー ダイアログのスケジュール。SBIE イベント メッセージではありません | [サポート リマインダー](#support-reminder)を参照。 |
| `NotifyBoxProtected` | `n` | 保護されたボックス | ホスト プロセスが保護されたサンドボックス化されたプロセスへのアクセスを拒否されたときの SBIE1318 | イベント時。SandMan チェックボックスは現在この設定のみを変更します。 |
| `NotifyDirectDiskAccess` | `n` | ボックス | ディスク デバイスを直接開こうとする特定の拒否された試行に対する [SBIE1313](SBIE1313.md)。すべての拒否されたディスク アクセス要求ではありません | サンドボックス化されたプロセスのためにキャッシュされます。例外については[Notify Direct Disk Access](NotifyDirectDiskAccess.md)を参照。 |
| `NotifyForceProcessDisabled` | `n` | グローバル | 強制が一時的に無効になっているために強制ルールに一致するプロセスが強制されないときの [SBIE1301](SBIE1301.md) | イベント時。グローバル Program Alerts チェックボックス。 |
| `NotifyForceProcessEnabled` | `n` | グローバル | プロセスが強制に一致し、サンドボックスに割り当てられたときの SBIE1321 | イベント時。グローバル Program Alerts チェックボックス。 |
| `NotifyImageLoadDenied` | `y` | ボックス | [Protect Host Images](ProtectHostImages.md)が、ボックス化されたイメージまたは DLL が保護されたホスト イメージ プロセスにマップされるのをブロックしたときの SBIE1305 | イベント時。SandMan チェックボックス。 |
| `NotifyInternetAccessDenied` | `y` | ボックス | Sandboxie のインターネット アクセス ポリシーがプロセスを拒否したときの [SBIE1307](SBIE1307.md)。通常、影響を受けるプロセスごとに 1 回 | プロセスのためにキャッシュされます。[Notify Internet Access Denied](NotifyInternetAccessDenied.md)を参照。 |
| `NotifyMsiInstaller` | `y` | ボックス | MSI インストーラーが、推奨される [Msi Installer Exemptions](MsiInstallerExemptions.md) 動作を有効にせずに開始されたときの SBIE2194 | プロセスの起動中に評価されます。専用の SandMan チェックボックスは見つかりませんでした。 |
| `NotifyNoCopy` | `n` | ボックス | 文書化されたファイル移行ケースに対する SBIE2113、SBIE2114、または SBIE2115 | プロセスのためにキャッシュされます。[Notify No Copy](NotifyNoCopy.md)を参照。 |
| `NotifyProcessAccessDenied` | `n` | ボックス | Sandboxie の保護パスによって拒否された、サポートされている明示的なプロセスまたはスレッド アクセス要求に対する [SBIE2111](SBIE2111.md) | プロセスのためにキャッシュされます。[Notify Process Access Denied](NotifyProcessAccessDenied.md)を参照。 |
| `NotifyRootProtected` | `n` | グローバル | 別のプロセスまたはボックスによる保護されたサンドボックス ルートへのアクセスが拒否されたときの SBIE1317 | 拒否が発生したときに読み取られます。この設定のための機能する専用の SandMan チェックボックスはありません。 |
| `NotifyStartRunAccessDenied` | `y` | ボックス | ボックスの Start/Run 制限メカニズムが関連する操作を拒否したときの [SBIE1308](SBIE1308.md)。通常、影響を受けるプロセスごとに 1 回 | プロセスのためにキャッシュされます。[Notify Start Run Access Denied](NotifyStartRunAccessDenied.md)を参照。 |
| `AlertStartRunAccessDenied` | `y` | グローバル | 別個のグローバル プログラム アラート拒否パスからの [SBIE1308](SBIE1308.md) | イベント時。グローバル Program Alerts チェックボックス。`NotifyStartRunAccessDenied` とは独立。 |

## ポリシー、生成、および表示

通知設定はメッセージの生成のみを制御します。基になるディスク、ネットワーク、プロセス、起動、イメージ読み込み、またはサンドボックス保護ルールを無効にするものではありません。同様に、`NotifyForceProcessDisabled` と `NotifyForceProcessEnabled` は強制メカニズムによって行われた決定を報告します。強制をオンまたはオフにするものではありません。

コンポーネントが SBIE メッセージを生成した後、SandMan または Sandboxie Control Classic がそれをどのように表示するかを決定します。SandMan の一般的なポップアップとメッセージ ログのオプションは **Global Settings > General Config > Notifications** の下にあります。ポップアップを抑制することは、ソース メッセージの生成を無効にすることとは異なります。

SandMan チェックボックス **Issue message 1318/1317 when a host process tries to access a sandboxed process/the box root** は、その現在の構成処理よりも広範です。これは `NotifyBoxProtected` を読み書きし、SBIE1318 を制御します。`NotifyRootProtected` は SBIE1317 を別途制御し、現在のインターフェイスには機能する専用チェックボックスがありません。

`NotifyImageLoadDenied` も同様に強制とは別個です。そのメッセージをオフにしても [Protect Host Images](ProtectHostImages.md) は無効にならず、メッセージはすべての失敗した DLL 読み込みではなく、その保護によって拒否されたイメージ マッピングに固有です。

`NotifyMsiInstaller` はすべての MSI 起動を報告するわけではありません。インストーラーが推奨される [Msi Installer Exemptions](MsiInstallerExemptions.md) 動作を有効にせずに開始されたときに警告を生成します。他の MSI または COM 失敗メッセージとは別個です。

## 変更の適用

プロセス状態でキャッシュされる設定を変更した後は、影響を受けるサンドボックス化されたプロセスを再起動してください。

- `NotifyDirectDiskAccess`
- `NotifyInternetAccessDenied`
- `NotifyNoCopy`
- `NotifyProcessAccessDenied`
- `NotifyStartRunAccessDenied`

次の設定は現在、イベントの発生時に照会され、影響を受けるプロセス状態を再構築することなく、通常の構成更新または再読み込み後に後のイベントに影響を与えることができます。

- `NotifyBoxProtected`
- `NotifyImageLoadDenied`
- `NotifyRootProtected`
- `NotifyForceProcessDisabled`
- `NotifyForceProcessEnabled`
- `AlertStartRunAccessDenied`

複数の通知設定を一緒に変更する場合は、影響を受けるプロセス ツリーを再起動するのが最も予測可能な方法です。

## Start/Run メッセージと確認

`NotifyStartRunAccessDenied` と `AlertStartRunAccessDenied` は独立した設定です。どちらも SBIE1308 を生成できますが、異なる拒否パスによって消費されます。いずれかの設定を無効にしても、対応するメッセージが抑制されるだけで、拒否は取り消されません。

[Alert Before Start](AlertBeforeStart.md)は異なります。対象となるサンドボックスの起動前に確認を要求でき、ユーザーの回答がその起動を続行するかどうかを決定できます。単に情報提供の SBIE メッセージを抑制するスイッチではありません。

## サポート リマインダー {#support-reminder}

`AlwaysShowReminder` は、Sandboxie のサポート/リマインダー ダイアログのスケジュールに影響するグローバル設定です。既定は `n` で、SBIE イベント メッセージを生成したり、許可/拒否ポリシーに参加したりしません。

## ユーザー インターフェイスの可用性

SandMan は次のコントロールを公開します。

- **Sandbox Options > General Options > File Options > Disk/File access > Warn when an application opens a harddrive handle** は `NotifyDirectDiskAccess` を制御します。
- **Sandbox Options > Network Options > Internet Access > Issue message 1307 when a program is denied internet access** は `NotifyInternetAccessDenied` を制御します。
- **Sandbox Options > General Options > Restrictions > Other restrictions > Issue message 2111 when a process access is denied** は `NotifyProcessAccessDenied` を制御します。
- **Sandbox Options > Program Control > Start Restrictions > Issue message 1308 when a program fails to start** は `NotifyStartRunAccessDenied` を制御します。
- **Sandbox Options > Security Options > Box Protection > Issue message 1318/1317 when a host process tries to access a sandboxed process/the box root** は `NotifyBoxProtected` を制御します。ラベルにもかかわらず、`NotifyRootProtected` は保存しません。
- **Sandbox Options > Various Options > Dlls & Extensions > Image Protection > Issue message 1305 when a program tries to load a sandboxed dll** は `NotifyImageLoadDenied` を制御します。
- **Global Settings > Program Control > Program Alerts** は、**Issue message 1301 when forced processes has been disabled**、**Issue message 1321 when a process has been forced into a sandbox**、およびグローバル **Issue message 1308 when a program fails to start** コントロールを提供します。

Sandboxie Control Classic は、Internet Access および Start/Run Access の通知コントロールを提供します。`NotifyDirectDiskAccess`、`NotifyProcessAccessDenied`、`NotifyBoxProtected`、または `NotifyImageLoadDenied` に対する同等の専用の現在の Classic コントロールは見つかりませんでした。互換性のある INI 設定は共有ランタイムを通じて引き続き利用できます。`NotifyRootProtected` または `NotifyMsiInstaller` に対する専用の SandMan コントロールは見つかりませんでした。

## バージョン履歴

- 設定メタデータには、`AlwaysShowReminder` がバージョン 1.3.0 で追加されたと記載されています。
- `NotifyForceProcessDisabled` は Sandboxie Plus 1.3.2 / Classic 5.58.2 で追加されました。
- 設定メタデータには、`AlertStartRunAccessDenied` がバージョン 1.6.0 で追加されたと記載されています。
- 設定メタデータには、`NotifyNoCopy` がバージョン 1.7.0 で追加されたと記載されています。
- 設定メタデータには、`NotifyImageLoadDenied` がバージョン 1.9.0 で追加されたと記載されています。
- 設定メタデータには、`NotifyBoxProtected` がバージョン 1.9.4 で追加されたと記載されています。
- `NotifyProcessAccessDenied` は Sandboxie Plus 1.0.18 / Classic 5.55.18 で追加されました。
- `NotifyMsiInstaller` は Sandboxie Plus 1.15.2 / Classic 5.70.2 で追加されました。
- `NotifyForceProcessEnabled` は Sandboxie Plus 1.15.3 / Classic 5.70.3 で追加されました。
- 設定メタデータには、`NotifyRootProtected` がバージョン 1.15.5 で追加されたと記載されています。
