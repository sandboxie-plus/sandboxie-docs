# RPC 互換性

Sandboxie には、Windows リモート プロシージャ コール (RPC) を使用するアプリケーションのための互換性処理が含まれています。この処理は、サンドボックス化されたプロセスが適切なバインディングを構築し、動的ローカル エンドポイントを解決し、通信タイムアウト調整を適用し、Windows RPC ランタイムを置き換えることなく選択されたホスト サービスに接続するのに役立ちます。

これらのメカニズムは汎用の RPC ファイアウォールではありません。汎用 IPC 到達可能性、Windows アクセス チェック、エンドポイント固有の要求フィルタリング、およびサンドボックス化されたサービス プロセスの ID は、全体的なモデルの別個の部分です。

## アーキテクチャの概要

RPC 互換性は、いくつかの Sandboxie コンポーネントにまたがっています。

```text
sandboxed application
        |
        v
SbieDll RPC binding interception
        |
        +-- optional binding preset and timeout decision
        |
        +-- optional dynamic endpoint request
                    |
                    v
             SbieSvc endpoint mapper helper
                    |
                    +-- Windows endpoint mapper or service process lookup
                    |
                    v
             SbieDrv dynamic-port registration and optional filter
                    |
                    v
             Windows RPC endpoint
```

組み込みテンプレートは、サポートされている互換性ケースで必要な維持されたマッピングを提供します。LSA、SAM、WPAD、および関連サービスに対するエンドポイント固有のセキュリティ動作は、[システム エンドポイント](SystemEndpoints.md)の下に文書化されています。

## RPC バインディング プリセット

`RpcPortBinding` は、RPC バインディングのための高度な互換性プリセットを提供します。各プリセットは、呼び出し元モジュールと、バインディング操作によって供給される識別子に一致します。

- `RpcBindingCreateW` の場合、識別子はバインディング テンプレートのオブジェクト UUID です。
- `RpcBindingFromStringBindingW` の場合、構成されたパターンが完全な文字列バインディングに対して一致させられます。

このマッチングに使用されるオブジェクト UUID は、エンドポイント ルックアップに使用される RPC インターフェイス UUID と混同しないでください。

要するに: **オブジェクト UUID = どのオブジェクト; インターフェイス UUID = どの操作; 文字列バインディング = それに到達する方法。**

概略形式は次のとおりです。

```ini
RpcPortBinding=<module>,<object-UUID-or-string-binding-pattern>[,Resolve=<port-id>][,TimeOut=y|n]
```

プリセットが一致すると、Sandboxie はローカル エンドポイントを供給し、通信タイムアウトを調整できます。`Resolve=<port-id>` は、以下で説明するマッピングを使用したエンドポイント ルックアップを要求します。`RpcBindingCreateW` パスでは、エンドポイント置換は、まだエンドポイントを指定していないローカル RPC バインディングに適用されます。

プリセットが一致しない場合、Sandboxie は通常のバインディング パスを続行します。一致しないプリセットはアクセスを拒否しません。

パーサーは、維持されたテンプレートで使用される内部形式もサポートします。サポートされているすべての形式またはエンドポイント識別子を安定した手動構成インターフェイスとして扱うのではなく、それらのテンプレートを優先してください。

### 動的エンドポイント マッピング {#dynamic-endpoint-mappings}

2 つの関連する設定が、`Resolve=` に必要な情報をエンドポイント マッパー ヘルパーに提供します。

- `RpcPortBindingIfId` は、論理ポート識別子を RPC インターフェイス UUID にマップします。SbieSvc は次に、一致する現在のエンドポイントを Windows エンドポイント マッパーに問い合わせることができます。
- `RpcPortBindingSvc` は、論理ポート識別子を Windows サービス名にマップします。SbieSvc はサービス プロセスを識別し、そのプロセスの現在の動的 RPC ポートをドライバーに問い合わせます。

これらの設定は主に維持されたテンプレートおよびサービス解決の配管です。インターフェイス UUID とサービス エンドポイントの詳細は Windows と共に変更される可能性があり、テンプレートから盲目的にコピーすべきではありません。

## 動的ポート フィルタリング {#dynamic-port-filtering}

`RpcPortFilter` は、Sandboxie がドライバーにグローバルに登録する動的に解決されたポートの要求フィルタリングをサポートします。SbieSvc は維持されたフィルター エントリを読み取り、解決されたポートとフィルター識別子を SbieDrv に送信します。ドライバーはサービス専用パスを通じてこの登録を受け入れ、登録されたポートに送信された要求を検査し、構成された一致をアクセス拒否で拒否します。

フィルター エントリ内の省略可能な関数名は情報提供用です。現在の強制は、そのラベルではなく構成された要求識別子を使用します。サポートされている特別なエンドポイントの場合、`Open<Name>Endpoint` オプションは、エンドポイントが登録されたときに対応するフィルターを抑制できます。

> [!WARNING]
> `RpcPortFilter` で使用される要求識別子は、プロトコルとバージョンに敏感な実装の詳細です。不正確な値は正当な RPC アクティビティをブロックする可能性があります。安定した RPC 認可 API であるかのようにエントリを考案したりメッセージ識別子をコピーしたりするのではなく、Sandboxie の維持されたテンプレートを優先してください。

`RpcPortFilter` はすべての RPC エンドポイントをフィルターせず、汎用の RPC ファイアウォールではありません。サポートされているエンドポイント固有の互換性コントロールについては、[システム エンドポイント](SystemEndpoints.md)を参照してください。

## RPC 通信タイムアウト {#rpc-communication-timeout}

Sandboxie は通常、バインディング ハンドルに RPC 通信タイムアウト調整を適用します。`RpcMgmtSetComTimeout` の現在のランタイム既定は、設定が存在しない場合に有効です。

既定の調整を明示的に無効にするには:

```ini
[DefaultBox]
RpcMgmtSetComTimeout=n
```

この設定は互換性とタイミングの動作を変更します。エンドポイント アクセスを付与したり、エンドポイントをブロックしたり、ファイアウォールを提供したりしません。

SandMan では、コントロールは **Sandbox Options > Various Options > Compatibility** の下にあり、次のようにラベル付けされています。

> Disable the use of RpcMgmtSetComTimeout by default (this may resolve compatibility issues)

チェックボックスは設定に対して反転されています。

- 選択すると `RpcMgmtSetComTimeout=n` を書き込みます。
- クリアすると通常の有効な動作を保持します。

### 呼び出し元モジュールの上書き {#calling-module-override}

`UseRpcMgmtSetComTimeout` は、現在のバインディングがまだタイムアウト決定を供給していない場合に使用される、高度な呼び出し元モジュール修飾の上書きです。たとえば、維持されたテンプレートは、特定の DLL から発信された呼び出しに対して異なるタイムアウト動作を選択できます。

`UseRpcMgmtSetComTimeout` は、DLL などの特定のモジュールから発信された呼び出しに対して異なるタイムアウト動作を許可します。Sandboxie は、一致する `RpcPortBinding` プリセットを探す前にこの設定をチェックします。

一致するプリセットに `TimeOut=` が含まれる場合、その値がモジュール固有の決定を上書きします。そうでなければ、バインディング プリセットが一致しても、モジュール固有の決定が有効なままです。どちらも上書きを提供しない場合、Sandboxie はプロセスの `RpcMgmtSetComTimeout` 既定を使用します。

## サンドボックス化された RpcSs の起動 {#sandboxed-rpcss-startup}

Sandboxie は通常、プロセスがサンドボックス化されたエンドポイント マッパーを必要とするときに、そのサンドボックス関連の RpcSs を開始します。その RpcSs は、特別なサーバー起動フローを通じてサンドボックス化された DcomLaunch プロセスを開始できます。これらは、サンドボックス化されていないホスト サービス インスタンスではなく、ボックスに関連付けられた Sandboxie サービス実行可能ファイルです。

`NoSandboxieRpcSs` は、特別なサーバー起動ヘルパーが、関連するエンドポイント要求のためにサンドボックス化された RpcSs または DcomLaunch を開始する前に戻るようにします。Windows RPC を無効にしたり、すべての RPC 通信をブロックしたり、`RpcPortBinding` を無効にしたりしません。このオプションのサポートされている一般的なユーザー ワークフローは文書化されていないため、日常的な構成コントロールではなく内部互換性動作として扱うべきです。

サンドボックス化された RpcSs を起動するために使用される ID は別途制御されます。[サンドボックス化されたサービス](SandboxedServices.md#runrpcssassystem)を参照してください。

## 変更の適用

RPC タイムアウト既定は各サンドボックス化されたプロセスで初期化され、モジュール固有のバインディング決定はバインディングが作成されるときに行われます。動的エンドポイントも必要に応じて解決および登録されます。これらの設定を変更した後は、影響を受けるサンドボックス化されたプロセスを再起動するか、サンドボックス化されたプロセス ツリーを再作成して、既存のバインディングとキャッシュされたエンドポイント情報が再利用されないようにしてください。

RpcSs 起動 ID への変更は、サンドボックス化された RpcSs プロセスの再起動を必要とします。SandMan、SbieSvc、またはドライバーの再起動は、通常、これらの構成変更のためだけには必要ありません。

## バージョン履歴

| 設定またはメカニズム | 導入 |
| --- | --- |
| `RpcMgmtSetComTimeout` | Sandboxie Plus 0.6.7 |
| `UseRpcMgmtSetComTimeout` | Sandboxie Plus 0.7.1 |
| `RpcPortBinding`、`RpcPortBindingIfId`、および `RpcPortBindingSvc` | Sandboxie Plus 0.7.3 |
| `NoSandboxieRpcSs` | Sandboxie Plus 1.5.0 |
| `RpcPortFilter` | Sandboxie Plus 1.14.2 |

## 関連ページ

- [システム エンドポイント](SystemEndpoints.md)
- [サンドボックス化されたサービス](SandboxedServices.md)
- [Open IPC Path](OpenIpcPath.md)
- [Closed IPC Path](ClosedIpcPath.md)
- [Sandboxie Ini](SandboxieIni.md)
