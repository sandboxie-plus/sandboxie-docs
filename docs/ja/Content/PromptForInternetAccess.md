# Prompt For Internet Access

*PromptForInternetAccess* は、プロセスが Sandboxie のインターネット アクセス制限によってブロックされたときに、SandMan が対話的な例外を提供できるようにします。プロンプト自体はネットワーク強制メカニズムではありません。

この設定を有効にしてもインターネット アクセス制限は作成されず、通常の無制限のネットワーク アクティビティについてプロンプトは表示されません。付与する例外が存在するには、ブロックが既にそのプロセスに適用されている必要があります。

## 構成

```ini
PromptForInternetAccess=y
PromptForInternetAccess=n
```

これはボックス全体のブール設定です。実行可能ファイル修飾値を受け入れません。既定は `n` で、対話的な例外プロンプトを無効にします。

この設定は Sandboxie Plus 0.5.0 で導入されました。

## プロンプトが表示される場合

プロンプトは、別の Sandboxie ポリシーがそのプロセスのインターネットまたはネットワーク アクセスを拒否した後に関連します。現在の強制パスには、Windows Filtering Platform (WFP) ブロックと、インターネット関連のネットワーク デバイスへのアクセスのブロックが含まれます。

ダイアログはブロックされたプロセスに関するもので、個別に分類されたリモート宛先に関するものではありません。WFP パスでは、ソケットが作成されるとき、リモート宛先が知られる前に決定が要求されることがあります。したがって、各サーバー、LAN アドレス、または接続ごとの個別の承認として解釈すべきではありません。

SandMan は、プロセスにインターネット アクセスを許可すべきかを尋ねるときに、実行可能ファイルを識別し、その完全なパスを表示します。

## プロンプトの選択肢

| 選択肢 | 現在のプロセスへの影響 | 永続的な構成 |
| --- | --- | --- |
| **Yes** | 現在のプロセス インスタンス/PID にランタイムのインターネット例外を付与します。 | なし。 |
| **No** | 例外を付与しません。既存のブロックは有効なままです。 | なし。 |
| **Yes and add to allowed programs** | ランタイム例外を付与します。 | 実行可能ファイルを既存の `<InternetAccess>` 許可プログラム グループに追加します。 |
| **Terminate** | プロセスを終了します。 | なし。 |

**Remember for this process** は、インターネット アクセス プロンプトに対して最初に選択されています。これは別個の許可または拒否の操作ではありません。SandMan が、同じ実行中のプロセス インスタンスからの以降の要求に対して、選択された **Yes** または **No** の決定を再利用するようにします。記憶された決定はそのプロセスとともに終了し、`Sandboxie.ini` ルールを作成しません。

**Yes** のみを選択することも一時的です。実行可能ファイルを永続的なインターネット アクセス許可構成に追加すべき場合は、**Yes and add to allowed programs** を使用してください。

## 強制の動作

SandMan が免除の決定を処理する間、基になるインターネット アクセス制限が強制の責任を負います:

- WFP に裏打ちされたブロックでは、ランタイム例外が付与されない限り、ドライバーとネットワーク ポリシーが引き続きトラフィックをブロックします。
- ネットワーク デバイスのブロックでは、例外が付与されない限り、保護されたデバイス オープン操作は拒否されたままです。

SandMan が決定を提供できない場合、免除は付与されず、既存のブロックが有効なままです。プロンプトを待つだけでは、プロセスに無制限のネットワーク アクセスが与えられることはありません。

プロンプトは例外ワークフローであり、ファイアウォールでも完全なネットワーク ポリシーでもありません。許可プログラム モデルについては [Restrictions Settings](RestrictionsSettings.md#internet-access) を、別個のネットワーク強制メカニズムについては [Windows Filtering Platform](../PlusContent/WFPSupport.md) を参照してください。

[*NotifyInternetAccessDenied*](NotifyInternetAccessDenied.md) は独立しています。拒否されたアクセスの通知を制御しますが、*PromptForInternetAccess* は例外を提供できます。どちらか一方を有効にしても、もう一方が自動的に有効になるわけではありません。

## Sandboxie Plus インターフェイス

SandMan で次を開きます:

**Sandbox Options** > **Network Options** > **Process Restrictions**

チェックボックスのラベルは **Prompt user whether to allow an exemption from the blockade.** です。インターネット アクセスが無制限の **Allow access** モードに設定されている場合、免除できる構成済みブロックが存在しないため無効になります。

New Box Wizard も、インターネット アクセス ブロックが構成されているときにプロンプト オプションを提供します。

## ランタイムの変更

*PromptForInternetAccess* は、ブロックされたアクセス試行が決定を必要とするときに参照されます。したがって、設定を変更すると、サンドボックスを再作成したり SandMan や Sandboxie サービスを再起動したりすることなく、以降のブロックされたアクセス イベントに影響を与えることがあります。

既存のランタイム例外または現在のプロセス インスタンスに対して記憶された決定が、そのプロセスに対する別のプロンプトを妨げることがあります。**Yes and add to allowed programs** による永続的な承認は、通常のインターネット アクセス許可プログラム構成に従います。

## Sandboxie Plus と Classic

基になるネットワークおよびランタイムのメカニズムは共有されていますが、現在の対話的プロンプトは SandMan によって提供されます。ソースレビューでは、この要求に対する同等の現在の Sandboxie Control Classic ハンドラーは特定されませんでした。互換性のある管理インターフェイスが応答しない場合、ランタイム例外は付与されず、既存のブロックが有効なままです。

## バージョン履歴

- Sandboxie Plus 0.5.0 / Classic 5.45.0 時代のコードが、対話的なインターネット ブロック免除メカニズムを導入しました。
- Sandboxie Plus 0.5.5 / Classic 5.46.4 が、プログラムを永続的に許可するオプションを追加しました。
- Sandboxie Plus 1.14.2 が、New Box Wizard にプロンプト オプションを追加しました。

これらの歴史的に対応するバージョンは、現在の Classic インターフェイスが SandMan と同じ対話的プロンプトを提供することを意味しません。

## 関連設定

- [Restrictions Settings](RestrictionsSettings.md#internet-access) — インターネット アクセスの許可/ブロック モデルを構成します
- [Notify Internet Access Denied](NotifyInternetAccessDenied.md) — 例外を付与するのではなく拒否通知を制御します
- [Windows Filtering Platform](../PlusContent/WFPSupport.md) — Sandboxie の別個の WFP 強制について説明します
- [Sandboxie Ini](SandboxieIni.md) — 手動のサンドボックス構成について説明します
