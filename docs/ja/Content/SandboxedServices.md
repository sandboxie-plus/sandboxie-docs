# サンドボックス化されたサービス

Sandboxie は、選択された Windows サービス コントロール マネージャー (SCM) 操作を傍受およびエミュレートして、特定のサービスがサンドボックスに関連付けられたプロセスとして実行されるようにできます。これは、SbieDll API 傍受、サンドボックス化されたサービス構成と状態、SbieSvc によって実行される特権操作、およびホスト サービス操作が必要な場合の実際の Windows SCM へのアクセスの組み合わせです。

これは、Windows SCM の完全なクローンまたは完全な仮想化ではありません。Sandboxie は SCM 操作を選択的に傍受およびエミュレートし、サンドボックス化されたサービス構成と状態をサンドボックス内に保持し、特権操作または実際の SCM との通信に SbieSvc を使用します。

## SandboxService

`SandboxService` は、Sandboxie のサンドボックス化されたサービス モデルを使用するサービスを選択します。

```ini
SandboxService=ServiceName
```

複数のエントリがサポートされています。

```ini
SandboxService=ServiceOne
SandboxService=ServiceTwo
```

既定は空のリストです。サービス名は完全一致かつ大文字と小文字を区別せずに照合されます。ワイルドカード、否定、および実行可能ファイル修飾形式はサポートされていません。

`SandboxService` はそれ自体では SYSTEM ID を選択しません。一致するサービスがサンドボックス化されたサービスとして処理されるかどうかにのみ影響します。

## サービスがサンドボックス化される条件

Sandboxie は、他の内部パスの中でも特に、次の場合にサービスをサンドボックス化されているものとして分類できます。

- それがサンドボックス内で作成され、サンドボックス化されたサービス状態に表示される場合。
- その名前が `SandboxService` エントリに一致する場合。
- Sandboxie がそのサービスの組み込み処理を持っている場合。

組み込みのケースは実装の詳細であり、`SandboxService` でサポートされるサービスの一般的なリストとして扱うべきではありません。

## サンドボックス化されたサービスの開始

傍受された `StartService` 要求がボックス化されているものとして分類されたサービスを対象とする場合、Sandboxie は単にホスト SCM に既存のホスト インスタンスを開始するよう要求するのではありません。高レベルでは、フローは次のとおりです。

```text
sandboxed StartService request
       |
       v
Sandboxie classifies service as boxed
       |
       v
virtual state -> START_PENDING
       |
       v
SbieSvc launches service executable through Sandboxie
       |
       v
service process becomes associated with the box
       |
       v
sandboxed service state -> RUNNING
```

この図は、正確な Windows SCM のタイミングを指定するのではなく、Sandboxie の状態処理を要約したものです。

既に実行中のホスト サービスは、サンドボックスに自動的に移動、終了、またはサンドボックス化されたインスタンスとして採用されることはありません。サービスが別個のサンドボックス化されたインスタンスをサポートするかどうかは、そのサービスに依存します。サービスが存在しないか、サンドボックス化されたサービス パスを通じて開始できない場合、操作は失敗し、実際のホスト サービスの開始に意図的にフォールバックすることはありません。

## サンドボックス化された SCM モデル

SbieDll は、サービスのオープン、作成、開始、クエリ、およびディスパッチャー パスを傍受します。サンドボックス内で作成されたサービス構成は、仮想化されたレジストリ状態を通じて保存でき、Sandboxie は必要に応じて合成ハンドルまたはサービス状態を維持します。SbieSvc は特権アクションを実行し、操作がホスト サービスを対象とする場合は実際の SCM と通信します。

この分担により、サンドボックス化されたプロセスは、すべての SCM 動作が完全に仮想化されることを意味することなく、使い慣れた SCM API を使用できます。

## RunServiceAsSystem

`RunServiceAsSystem` は、名前付きサンドボックス化サービスのための SYSTEM ソース ID を選択します。

```ini
RunServiceAsSystem=ServiceName
```

複数のエントリがサポートされています。既定は空のリストです。一致は完全一致かつ大文字と小文字を区別しません。ワイルドカード、否定、および実行可能ファイル修飾形式はサポートされていません。

`RunServiceAsSystem` は、一致するサンドボックス化されたサービスを起動するために使用されるソース ID を変更します。それ自体ではホスト サービスをサンドボックスに移動しません。サービスは、たとえば `SandboxService` を通じて、別途サンドボックス化されているものとして分類される必要があります。

## RunServicesAsSystem

広範な形式は次のとおりです。

```ini
RunServicesAsSystem=y
```

その既定は `n`（無効）です。有効な場合、サービス開始パスは、現在の特殊ケース ロジックの対象で、サンドボックス化されたサービスのために SYSTEM ID を広範に選択できます。

RpcSs と DcomLaunch に言及する歴史的なメタデータの文言は、現在の実行可能ファイル動作の完全な説明ではありません。この設定はそれらの 2 つの名前に限定されず、特殊ケースに関係なくすべてのサンドボックス化されたサービスが SYSTEM を使用するという無条件の保証でもありません。

### 選択的および広範な形式

`RunServiceAsSystem=<name>` は名前付きサービスのみを対象とします。`RunServicesAsSystem=y` はより広範な SYSTEM ソース選択を有効にするため、選択的設定で名前が付けられていないサービスも、現在のロジックが許す場合は広範なパスを使用できます。選択的エントリを追加しても、他のサービスに対するグローバル設定は取り消されません。

選択的形式は、特定のサービスのみが SYSTEM ソース ID を必要とする場合に有用です。

## RunRpcssAsSystem

`RunRpcssAsSystem` は、SbieSvc がサンドボックス関連の RpcSs プロセスを開始するときに使用されるソース ID を制御します。

```ini
RunRpcssAsSystem=y
```

既定は `n` です。明示的な `y` は、SbieSvc がサンドボックス化された RpcSs の起動のためにその SYSTEM ソース トークンを複製するようにします。結果として得られる `SandboxieRpcSs` プロセスはサンドボックスに関連付けられたままです。この設定は、サンドボックス化されていないホスト RpcSs サービスを開始または採用しません。

> [!WARNING]
> SYSTEM ソース トークンからサンドボックス化された RpcSs を開始すると、そのプロセスに開かれたままのアクセスの影響が大きくなります。この互換性オプションは必要な場合にのみ使用してください。それ自体では、RpcSs をサンドボックスから削除しません。

### アプリケーション コンパートメントと OriginalToken

現在のサービス起動ロジックは、次の両方が真の場合に同じ SYSTEM ソース パスを自動的に選択できます。

1. 呼び出し元がアプリケーション コンパートメント モードであるか、`OriginalToken=y` が構成されている。かつ
2. `MsiInstallerExemptions=y` または `RunServicesAsSystem=y` のいずれかが有効である。

したがって、アプリケーション コンパートメントだけでは、サンドボックス化された RpcSs が SYSTEM ソース トークンを使用するよう自動的にはなりません。

サンドボックス化された DcomLaunch は、サンドボックス化された RpcSs/サーバー フローを通じて開始されます。上記の明示的なトークン ソースの決定は RpcSs の起動に対して行われ、別個の同一の DcomLaunch トークン選択ルールに一般化すべきではありません。

### SandMan コントロール

コントロールは **Sandbox Options > Security Options > Advanced Security** の下にあり、ラベルは次のとおりです。

> Start the sandboxed RpcSs as a SYSTEM process (not recommended)

SandMan は明示的な `RunRpcssAsSystem` 値からこのチェックボックスを読み込みます。アプリケーション コンパートメント モードでは、広範な `RunServicesAsSystem` 動作または `MsiInstallerExemptions` のいずれかが上記の自動ランタイム条件をすでに引き起こしている場合、直接コントロールを無効にします。

バインディング解決、エンドポイント フィルタリング、タイムアウト動作、およびサンドボックス化された RpcSs 起動アーキテクチャについては、[RPC 互換性](RpcCompatibility.md)を参照してください。

## 「SYSTEM として」の意味

このサービス開始パスでは、Sandboxie は LocalSystem として実行される SbieSvc からソース トークンを取得し、プライマリ トークンを複製し、そのセッションを調整し、それを使用してサンドボックス化されたサービス プロセスを起動します。Sandboxie はまた、該当する場合は既定でサービス側の特権除去を適用します。

したがって「SYSTEM として実行」は、サンドボックス化されたサービスを開始するために使用されるソース ID を表します。サンドボックスの外で実行される無制限の LocalSystem プロセスを意味するものではありません。

通常の分離ボックスでは:

- プロセスはサンドボックスに関連付けられたままです。
- 通常の Sandboxie トークンと分離パイプラインが依然として適用されます。
- ファイル、レジストリ、IPC、およびその他の分離メカニズムは別個のままです。

`NoSecurityIsolation` / アプリケーション コンパートメントは後続のトークンと分離の動作を変更するため、このページの設定はすべてのボックス モードで 1 つの同一の最終トークンを保証しません。

## 関連する特殊ケース

[Msi Installer Exemptions](MsiInstallerExemptions.md)は MSIServer の処理を変更でき、CryptSvc には現在の特殊ケース動作があります。これらのメカニズムはサービス ID に関連していますが、ここで文書化されている設定の一般的な代替ではありません。

## Chromium 昇格テンプレート

現在の `Chromium_Elevation` テンプレートはこのパターンを使用します。

```ini
OpenSamEndpoint=y

SandboxService=MicrosoftEdgeElevationService
RunServiceAsSystem=MicrosoftEdgeElevationService

SandboxService=MicrosoftEdgeDevElevationService
RunServiceAsSystem=MicrosoftEdgeDevElevationService

SandboxService=MicrosoftCopilotElevationService
RunServiceAsSystem=MicrosoftCopilotElevationService

SandboxService=GoogleChromeElevationService
RunServiceAsSystem=GoogleChromeElevationService

SandboxService=GoogleChromeDevElevationService
RunServiceAsSystem=GoogleChromeDevElevationService

SandboxService=BraveElevationService
RunServiceAsSystem=BraveElevationService
```

テンプレートは、互換性フローの 3 つの別個の部分を提供します。

`SandboxService`
: 名前付き昇格サービスを Sandboxie のサンドボックス化されたサービス モデルを通じてルーティングします。

`RunServiceAsSystem`
: その名前付き昇格サービスのみに SYSTEM ソース ID を使用します。

`OpenSamEndpoint`
: この互換性フローで必要な SAM メッセージ フィルターを削除します。[システム エンドポイント](SystemEndpoints.md)を参照してください。

テンプレートは、広範な `RunServicesAsSystem=y` 動作から選択的な `RunServiceAsSystem=...` エントリに移行しました。これにより、SYSTEM ソース選択が名前付き昇格サービスに限定され、広範な設定が他のサンドボックス化されたサービスに適用されなくなります。

テンプレートは Sandboxie によって維持されており、通常、手動でコピーする必要はありません。

## DPAPI との関係

Sandboxie には、別個の DPAPI 互換性とプロキシ処理があります。最近の Chromium 昇格作業では、SYSTEM として実行されるサービスを伴う DPAPI シナリオで使用される ID が調整されました。

`OpenSamEndpoint` は DPAPI を実装せず、資格情報を復号しません。互換性は依然として、有効な Windows ID、Windows DPAPI ルール、Chromium の動作とポリシー、アプリ バインド暗号化または関連メカニズム、および昇格サービスの可用性と構成に依存します。このページの設定は、ホスト資格情報へのアクセスを保証しません。

## 失敗時の動作

サンドボックス化されたサービス パスには、ボックス化された起動が失敗した後で実際のホスト サービスを開始する一般的なフォールバックはありません。

- 存在しないまたは利用できないサービスは開始に失敗します。
- ドライバー サービスおよびサポートされていない非 Win32 サービス タイプは、ボックス化されたサービス パスによって拒否されます。
- 既に実行中のホスト インスタンスは自動的に採用されません。
- SYSTEM ソース トークンの取得または複製、あるいはサンドボックス化されたプロセスの作成に失敗すると、サービスの開始が失敗します。
- 別の、制限の少ないホスト トークンへの意図的なフォールバックは特定されていません。

正確な Windows エラーは、失敗の時点に依存する場合があります。

## 変更の適用

`SandboxService` は、サービスの分類と開始操作中に評価されます。新しい値は後の開始に影響を与える可能性がありますが、既に実行中のサービス インスタンスを移動しません。

`RunServiceAsSystem` と `RunServicesAsSystem` は、サービス プロセスが開始されるときに関連します。いずれかの設定を変更しても、既に割り当てられたサービス トークンが遡って置き換えられることはありません。

サービス ID 設定を変更した後は、影響を受けるサンドボックス化されたサービスまたはプロセスを再起動してください。クリーンな構成テストが必要な場合は、サンドボックス化されたプロセス ツリーを再作成してください。SandMan、SbieSvc、またはドライバーの再起動は、通常は必要ありません。

## SandMan 構成

広範な設定は **Sandbox Options > Security Options > Advanced Security** の下に公開されており、ラベルは次のとおりです。

> Do not start sandboxed services using a system token (recommended)

チェックボックスは `RunServicesAsSystem` に対して反転されたセマンティクスを持ちます。

- 選択すると、広範な `RunServicesAsSystem=y` 動作が無効になります。
- クリアすると、SandMan は `RunServicesAsSystem=y` を書き込むことができます。

`SandboxService` と `RunServiceAsSystem` には専用の現在の SandMan コントロールがありません。それらは手動またはテンプレート設定です。New Box ウィザードはこれらのコントロールを公開していません。

## Sandboxie Plus と Classic

ランタイムは共有 Sandboxie コンポーネントに実装されています。SandMan は現在の `RunServicesAsSystem` コントロールを提供し、`SandboxService` と `RunServiceAsSystem` は手動またはテンプレート設定のままです。これは、Sandboxie Control Classic における同等の現在のコントロールを意味するものではありません。

## バージョン履歴

| 設定または変更 | 導入 |
| --- | --- |
| `RunServicesAsSystem` | Sandboxie Plus 0.5.4 / Classic 5.46.0 |
| `RunServiceAsSystem` | Sandboxie Plus 0.5.4b / Classic 5.46.1 |
| `SandboxService` | Sandboxie Plus 0.5.5 / Classic 5.46.4 |
| `RunRpcssAsSystem` | Sandboxie Plus 0.9.7 |
| Chromium 昇格と DPAPI 互換性の作業 | Sandboxie Plus 1.18.0 / Classic 5.73.0 の時代 |
| 選択的 Chromium 昇格テンプレート | Sandboxie Plus 1.18.1 / Classic 5.73.1 |

これらのサービス設定は、現在の Chromium 昇格での使用より前に存在していました。

## 関連ページ

- [RPC 互換性](RpcCompatibility.md)
- [システム エンドポイント](SystemEndpoints.md)
- [サービス プログラム](ServicePrograms.md)
- [Start Service](StartService.md) — ライフサイクル/起動設定であり、`SandboxService` の同等物ではありません
- [Msi Installer Exemptions](MsiInstallerExemptions.md)
- [Sandboxie Ini](SandboxieIni.md)
