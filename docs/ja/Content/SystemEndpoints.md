# システム エンドポイント

Sandboxie は、機密性の高いエンドポイントに特殊なメッセージ レベルのフィルターを適用しながら、Windows システム サービスとの一部の IPC および RPC 通信を許可します。このページの設定は、互換性のために必要な場合に、それらのエンドポイント固有のフィルターの 1 つを無効にします。

それらは LSA、SAM、または WPAD を一般的に開放するものではありません。汎用 IPC 到達可能性、通常の Windows アクセス チェック、および無関係な Sandboxie 制限は別個のままです。

一般的な構成は次のとおりです。

```ini
OpenLsaEndpoint=y
OpenSamEndpoint=y
OpenWPADEndpoint=y
```

3 つの設定はすべてボックス全体の Boolean オプションで、既定では無効で、実行可能ファイル修飾ではありません。テンプレートを含む通常の有効な Sandboxie 構成を通じて継承できます。

## IPC 到達可能性とエンドポイント フィルタリング

Sandboxie は、汎用 IPC 到達可能性とエンドポイント固有の要求フィルタリングを別個のレイヤーとして処理します。

```text
sandboxed process
       |
       v
generic IPC path/object policy
       |
       +-- denied -> connection fails
       |
       v
endpoint reachable
       |
       v
endpoint-specific operation filter
       |
       v
request allowed or denied
```

[Open IPC Path](OpenIpcPath.md)は IPC オブジェクトを到達可能にでき、[Closed IPC Path](ClosedIpcPath.md)は到達可能性を拒否できます。ここで文書化されている `Open...Endpoint` 設定は、後段の特殊な操作フィルターに影響します。IPC パスを開いてもそのフィルターが本質的に削除されるわけではなく、エンドポイント設定が閉じた IPC オブジェクトを本質的に到達可能にするわけでもありません。

## OpenLsaEndpoint

```ini
OpenLsaEndpoint=y
```

既定は `n`（無効）です。

Sandboxie は、次の固定エンドポイントを SbieDrv 内で直接処理します。

```text
\RPC Control\LSARPC_ENDPOINT
```

既定では、Sandboxie は選択された機密性の高い LSA RPC 操作に拒否リストを適用します。フィルターは、ポリシーまたはセキュリティ状態、監査構成、アカウントと信頼されたドメイン、アカウント権限と特権、クォータとシステム アクセス状態、およびプライベート データ状態を変更する操作をカバーします。LSA クエリまたは列挙を普遍的にブロックするわけではありません。

`OpenLsaEndpoint` は、`LSARPC_ENDPOINT` 上の機密操作に対する Sandboxie の特殊なフィルターを無効にします。LSA への無制限アクセスを付与したり、通常の Windows アクセス チェックを無効にしたりしません。

### セキュリティの履歴

LSA エンドポイント フィルターは、後にセキュリティ問題 ID-8 / CVE-2019-13502 として追跡された問題に対応して、Sandboxie Plus 0.5.4 / Classic 5.46.0 で導入されました。フィルターは既定で有効のままです。`OpenLsaEndpoint=y` は、フィルターが拒否する操作を必要とするソフトウェアのための互換性緩和です。

## OpenSamEndpoint

```ini
OpenSamEndpoint=y
```

既定は `n`（無効）です。

Sandboxie は、この固定エンドポイントも SbieDrv 内で直接処理します。

```text
\RPC Control\samss lpc
```

通常の SAM 要求フィルターは、ユーザーおよびアカウントの作成または削除、グループおよびエイリアスの変更、メンバーシップの変更、パスワードの変更、アカウント属性とポリシー、およびセキュリティ変更などの機密性の高い変更カテゴリをカバーします。すべての SAM 要求が拒否されることを意味するものではありません。

`OpenSamEndpoint` は Sandboxie の SAM エンドポイント要求フィルターを無効にします。それ自体では、すべての SAM データを公開したり、Windows アクセス チェックをバイパスしたり、ホスト資格情報を提供したりしません。

フィルターとその互換性設定は、昇格されたサンドボックス化されたプロセスがアカウントまたはパスワード状態を変更することを伴うセキュリティ問題の後、Sandboxie Plus 0.7.0 / Classic 5.48.0 で導入されました。

### Chromium 昇格サービス

現在の Chromium 昇格互換テンプレートは、このパターンで設定を組み合わせています。

```ini
SandboxService=<service>
RunServiceAsSystem=<service>
OpenSamEndpoint=y
```

`SandboxService` は昇格サービスを Sandboxie のサンドボックス化されたサービス モデルに配置し、`RunServiceAsSystem` はそのサービスに必要なソース ID を提供し、`OpenSamEndpoint` は互換性フローで必要な SAM フィルターを削除します。`OpenSamEndpoint` だけでは DPAPI 互換性を実装したり、ホスト資格情報へのアクセスを付与したりしません。[サンドボックス化されたサービス](SandboxedServices.md)を参照してください。

## OpenWPADEndpoint

```ini
OpenWPADEndpoint=y
```

既定は `n`（無効）です。この設定は Sandboxie Plus 1.15.0 / Classic 5.70.0 で導入されました。

この設定は、Windows Web Proxy Auto-Discovery と `WinHttpAutoProxySvc` に関連付けられた動的 RPC エンドポイントに関するものです。固定の LSA および SAM エンドポイントとは異なり、WPAD エンドポイントは実行時に検出および登録されます。

```text
SbieDll
  |
  v
requests dynamic RPC endpoint resolution
  |
  v
SbieSvc / EpMapperServer
  |
  v
resolves the WPAD service endpoint
  |
  v
registers endpoint + filter with SbieDrv
  |
  v
driver applies the message filter
```

Sandboxie は通常、プロキシ構成、ポリシー、および資格情報に関連する選択された機密操作のためのフィルターを使用してこのエンドポイントを登録します。`OpenWPADEndpoint=y` の場合、エンドポイントはその特殊なフィルターなしで登録されます。

したがって `OpenWPADEndpoint` は、Sandboxie が本来フィルターする WPAD 操作を許可します。無制限のネットワーク、プロキシ、WinHTTP、またはインターネット アクセスを提供しません。

## 固定および動的実装

設定は概念的に類似した効果を持ちますが、異なる実装パスを使用します。

| 設定 | エンドポイント処理 | 有効時の効果 |
| --- | --- | --- |
| `OpenLsaEndpoint` | SbieDrv で直接フィルターされる固定エンドポイント | 特殊な LSA 操作フィルターをスキップします |
| `OpenSamEndpoint` | SbieDrv で直接フィルターされる固定エンドポイント | 特殊な SAM 要求フィルターをスキップします |
| `OpenWPADEndpoint` | SbieDll と SbieSvc を通じて解決され、次に SbieDrv に登録される動的エンドポイント | 特殊なメッセージ フィルターなしで WPAD を登録します |

## BlockPassword との関係

[`BlockPassword`](BlockPassword.md)は、別個のレガシー LSA 認証およびパスワード関連フィルターを制御します。現在のランタイムは依然としてそれを参照しますが、最新のパスワード変更互換性ケースでは `OpenSamEndpoint` に取って代わられました。これは `OpenLsaEndpoint` または `OpenSamEndpoint` のエイリアスではありません。`OpenLsaSSPI` は現在の INI 設定として確認されていません。

## SandMan 構成

コントロールは **Sandbox Options > General Options > Isolation** の下にあります。

| 設定 | 現在のラベル |
| --- | --- |
| `OpenLsaEndpoint` | Open access to Windows Local Security Authority |
| `OpenSamEndpoint` | Open access to Windows Security Account Manager |
| `OpenWPADEndpoint` | Open access to Proxy Configurations |

ラベルは、このページで説明されている正確な操作フィルター動作よりも広範です。コントロールは既定でチェックされていない状態で読み込まれ、有効な場合は `y` を書き込み、無効な場合は明示的なキーを削除します。それらは `NoSecurityIsolation` / アプリケーション コンパートメント動作がアクティブな場合は無効になります。この UI 状態は、そのモードですべてのエンドポイント パスが無制限であるという保証として解釈すべきではありません。

これらのコントロールは現在、New Box ウィザードでは提供されていません。

## 変更の適用

LSA および SAM 設定は、サンドボックス化されたプロセスの IPC 初期化中にキャッシュされます。それらを変更した後は、影響を受けるサンドボックス化されたプロセスを再起動するか、サンドボックス化されたプロセス ツリーを再作成してください。

影響を受けるアプリケーションを開始する前に `OpenWPADEndpoint` を構成してください。変更後は影響を受けるサンドボックス化されたプロセス ツリーを再起動することを推奨します。動的エンドポイントは別途解決および登録され、その現在のキャッシュ動作は、1 つのアプリケーションのみを再起動すると常にグローバル エンドポイント フィルター状態が再構築されるという保証として扱うべきではありません。

SandMan、SbieSvc、またはドライバーの再起動は、これらの設定によって普遍的に必要とされるものではありません。

## 失敗時の動作

通常の特殊なフィルターによって選択された LSA および SAM 操作は拒否されます。WPAD エンドポイントの解決または登録が失敗した場合、対応する RPC またはバインディング操作が失敗する可能性があります。無制限のフォールバックは確立されていません。汎用 IPC ポリシーは、エンドポイント固有のフィルタリングに到達する前に通信を拒否することもできます。観察可能なエラーは失敗したレイヤーに依存するため、1 つのエラー コードがすべてのケースを説明するわけではありません。

## Sandboxie Plus と Classic

ランタイム サポートは共有 Sandboxie コンポーネントに実装されています。SandMan は上記のコントロールを提供し、互換性のある手動設定は共有ランタイムによって消費されます。これは、Sandboxie Control Classic が同等の現在のコントロールを提供することを意味するものではありません。

## バージョン履歴

| 設定 | 導入 |
| --- | --- |
| `OpenLsaEndpoint` | Sandboxie Plus 0.5.4 / Classic 5.46.0 |
| `OpenSamEndpoint` | Sandboxie Plus 0.7.0 / Classic 5.48.0 |
| `OpenWPADEndpoint` | Sandboxie Plus 1.15.0 / Classic 5.70.0 |

## 関連ページ

- [RPC 互換性](RpcCompatibility.md)
- [Open IPC Path](OpenIpcPath.md)
- [Closed IPC Path](ClosedIpcPath.md)
- [Block Password](BlockPassword.md)
- [サンドボックス化されたサービス](SandboxedServices.md)
- [Sandboxie Ini](SandboxieIni.md)
