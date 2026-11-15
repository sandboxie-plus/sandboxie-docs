# Enable EFS

_EnableEFS_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、v1.15.0 / 5.70.0 以降で利用できます。Application Compartment モード以外で選択された EFS 関連のファイル オープン要求が、ネイティブのアクセス拒否結果の後で Sandboxie のセッション ユーザー ファイル プロキシを通じて再試行できるようにします。再試行は依然として証明書の機能、ファイル ポリシーのチェック、および Windows ファイルシステムの認可の対象です。

> [!NOTE]
> プロキシの再試行には、暗号化機能を備えた現在有効な高度な[サポーター証明書](https://sandboxie-plus.com/supporter-certificate/)が必要です[^1]。これはファイルの復号に必要な Windows EFS 資格情報とは別個です。

## 使用法

```ini
[DefaultBox]

EnableEFS=y
```

コンシューマーのフォールバックは無効です。有効な値が `EnableEFS` を有効にしない場合、この追加の再試行は有効になりません。有効な構成は、ボックス、該当する有効なテンプレート、または `GlobalSettings` フォールバックから取得できます。直接のボックス値は継承された値よりも優先されます。`EnableEFS=n` は継承された有効化値を明示的に上書きします。DLL は呼び出し元プロセスのボックスに対して設定を解決し、ワーカーは呼び出し元から解決された名前付きボックスをチェックします。これはボックス Boolean であり、プログラムで修飾された設定ではありません。

DLL は対象となる操作中に設定を照会し、ワーカーはプロキシ要求ごとにそれを再チェックします。構成の再読み込み後、後の対象となる要求は、サンドボックス化されたアプリケーション、SbieSvc、SbieDrv、または Windows の再起動を本質的に必要とせずに、変更された値を使用できます。既存のハンドルは自動的に取り消されず、設定を変更しても既に送信された作業のキャンセルが確立されるわけではありません。ファイル ポリシー リストには独自の再読み込みライフサイクルがあり、証明書の状態の更新は通常の構成の再読み込みとは別個です。

## Sandboxie Manager GUI による有効化

次の手順で、特定のサンドボックス (または DefaultBox) に対して Sandboxie Manager (SandMan とも呼ばれます) から設定を有効にできます:

1. SandMan を開きます。
2. 構成するサンドボックスを右クリックし、"Sandbox Options" を選択します。
3. 設定ダイアログで、左側の "General Options" カテゴリを選択します。
4. "File Options" タブに切り替え、"Disk/File access" セクションまでスクロールします。
5. "Allow sandboxed processes to open files protected by EFS" とラベル付けされたオプションをチェックします。
6. "Apply" または "OK" をクリックして設定を保存します。

チェックボックスは直接のボックス設定を読み取り、必ずしも継承された有効な構成を読み取るわけではありません。通常、チェックすると `EnableEFS=y` が書き込まれ、チェックを外すと `n` を書き込むのではなく通常の直接値が削除されるため、継承された `y` が有効なままになることがあります。直接の `EnableEFS=n` はその継承を上書きできますが、チェックボックスをオフにした状態での後の保存はその直接の `n` も削除することがあります。

SandMan は、暗号化機能が利用できないときに高度な証明書バッジを表示します。バッジ自体はチェックボックスを無効にしたり、ランタイム チェックをバイパスしたりしません。チェックボックスは [Application Compartment](NoSecurityIsolation.md) モードでは無効になり、そこでは通常の DLL EFS 再試行が除外されます。

## 概要

暗号化ファイル システム (EFS) は、ファイルシステム レベルの暗号化を提供する Windows の機能です。`EnableEFS` は追加の互換性再試行を制御するものであり、無効時にすべての EFS アクセスを拒否する包括的なルールではありません。ネイティブ アクセスは、選択された Sandboxie ファイル ルーティング パス、Windows の権限と EFS 資格情報、ファイルシステムと共有の条件、および該当する Sandboxie の制限に依存します。

この設定は EFS 秘密キーを提供したり、すべての暗号化ファイル操作をプロキシしたり、アクセスの成功を保証したりするものではありません。Sandboxie サポーター証明書はプロキシ機能を認可するものであり、Windows EFS の復号資格情報ではありません。

## 動作の仕組み

EFS 再試行パスに到達する、選択された真のファイル オープンの場合:

1. **ネイティブ試行**: Sandboxie は最初にネイティブ オープンを試みます。非コンパートメント モードでの元の `STATUS_ACCESS_DENIED` 結果のみが、有効な `EnableEFS` が有効な状態で EFS チェックに進みます[^2]。
2. **EFS 検出**: DLL は、選択されたターゲットまたは特定のターゲット欠落ケースではその親に対して `FILE_ATTRIBUTE_ENCRYPTED` をチェックします。この親チェックはファイル作成要求にのみ限定されるものではありません。検出だけでは認可、復号、または使用可能なハンドルは確立されません[^2]。
3. **プロキシ要求**: 検出が成功し EFS を報告する場合、DLL は要求をセッション固有の UserServer ワーカーに送信します[^4]。
4. **ワーカーの認可**: ワーカーは呼び出し元と Windows セッションを検証し、有効な `EnableEFS` を再チェックし、証明書の機能を検証し、デバイス パスとプロセス ファイル ポリシーの適格性をチェックします[^3][^6]。
5. **オープンと転送**: ワーカーは提供されたパラメーターで要求されたオブジェクトを開こうとし、ハンドルをサンドボックス化された呼び出し元に転送します。SbieSvc はワーカーを調整しますが、オープンはメイン サービスの SYSTEM トークンではなく Windows セッション ユーザー トークンを使用します。必ずしも呼び出し元の制限されたトークンではありません。Windows の認可は依然として適用され、ワーカー側のオープンは使用可能な転送済みハンドルを保証するものではありません[^5]。

成功したネイティブ オープンにはこの再試行は不要であり、他のネイティブ障害はこの分岐をトリガーしません。非 EFS の検出または属性の取得失敗はディスパッチを妨げることがあります。通常のサンドボックス コピー作成を含む他のルーティング パスは、このヘルパーを使用する必要はありません。

## セキュリティ上の考慮事項

- **直接オブジェクト アクセス**: プロキシ アクセスは、サンドボックス コピーを作成する代わりに、基になるオブジェクトへのハンドルを公開する可能性があります。ホスト ファイルへの書き込み可能なハンドルが許可される場合、そのハンドルを通じた書き込みはホスト ファイルに直接影響を与えることがあります。これはすべてのサンドボックス分離を無効にするものではありません。ワーカーのチェック、Windows のアクセス許可、ハンドルの権限、および他の Sandboxie 操作固有の制御は引き続き関連します[^5]。
- **パスの検証**: プロキシ要求は、有効な場合は Rule Specificity を含む、呼び出し元のプロセス固有のファイル ポリシー リストに対する追加のチェックの対象です。勝ち残った closed-path 分類はプロキシの認可を拒否します。プロキシの認可が、すべての通常のファイル ルーティング動作を再現すると想定すべきではありません[^6]。
- **書き込みアクセスの制御**: 読み取り分類と書き込み分類の要求には、異なる認可要件があります。アクセス ビット、`FILE_OPEN` 以外の作成 disposition、および delete-on-close は、既存の内容への意図された変更がなくても、要求を書き込み可能にすることがあります。書き込み可能な要求にはプロキシの open-path 認可が必要です。`EnableEFS=y` は無制限の書き込みを許可しません[^7]。

EFS を有効にするためだけに `OpenFilePath` のアクセス許可を広げないでください。プロキシの認可を通過しても、Windows アクセスやハンドルの配信は依然として保証されません。

## 証明書の要件

ランタイムは、証明書状態の照会の成功と、暗号化機能 (`opt_enc`) を備えたアクティブな証明書を必要とします[^3][^8]。プロジェクトの UI はこれをアクティブな高度なサポーター証明書と呼びますが、ワーカーはそのラベルだけに依存するのではなく機能フラグを適用します。必要な機能を備えていない汎用のサポーター証明書では不十分です。

インストール、名目上の証明書レベル、または有効期限だけでは、現在の受け入れを確立しません。この機能は他の暗号化/保護機能にも関連付けられており、そのランタイム動作は別個です。Windows EFS 資格情報に代わるものではありません。

## 関連するメッセージ

- [SBIE2225](SBIE2225.md) - "An attempt was made to access an EFS file" - 設定が有効でない、またはプロキシ試行なしの非コンパートメント ファイル ルーティング中の EFS 検出、または失敗した対象のプロキシ再試行を報告できます。メッセージだけでは最終的な操作が失敗したことを証明しません。証明書または転送の診断と共存することがあります[^9]。
- [SBIE6004](SBIE6004.md) - EFS ワーカーでは、証明書状態の取得失敗または利用可能なアクティブな暗号化機能の欠如が、この診断とそのプロキシ要求の即時拒否を引き起こします[^3]。すべてのネイティブ EFS アクセスに対して発行されるわけではなく、このワーカー チェック自体が 5 分間のプロセス終了をスケジュールするわけではありません。別個のドライバー機能適用パスが同じメッセージを異なる結果で使用することがあります。

## 制限

- ワーカーは、大文字と小文字を区別しないプレフィックス `\Device\HarddiskVolume` を持つネイティブ パスを受け入れます。これはパス形式の制限であり、物理ディスクの種類、EFS 対応ファイルシステム、利用可能なキー、または使用可能なアクセスの証明ではありません。通常のネットワーク/UNC パスは、単にドライブ文字にマップされているだけでは該当しません[^10]。
- プロキシは、サンドボックスのファイル [resource access rules](ResourceAccess.md) とワーカーの追加の認可チェックの対象のままです。万能の copy-on-write パスや Windows 認可の代替ではありません。
- Application Compartment はこの通常の再試行をスキップします。それはネイティブ EFS アクセスの成功または拒否のいずれをも保証するものではありません。
- サポートされていないオブジェクト属性形式、呼び出し元/セッションまたはポリシーの拒否、ネイティブ オープンの失敗、ハンドル転送の問題、および転送エラーまたはタイムアウトは、アクセスを妨げることがあります。応答レイヤーが異なるため、すべてのプロキシ障害に対して単一の保証されたアプリケーション可視の Windows エラーはありません[^4][^5]。

[^1]: [`UserServer::OpenFile()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L641-L652) は有効な有効化を再チェックし、状態の取得成功後に `CertInfo.active && CertInfo.opt_enc` を必要とします。
[^2]: [`File_GetFileType()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/file.c#L5016-L5077) は `FILE_ATTRIBUTE_ENCRYPTED` を識別します。[`File_NtCreateTrueFile()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/file.c#L4624-L4690) はネイティブ優先の再試行と条件付き親チェックを実装します。`File_NtCreateFileImpl()` もルーティング中に EFS 検出を使用します。
[^3]: [ドライバー状態の照会](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/api.c#L1246-L1255) が証明書状態を提供します。[ワーカー チェック](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L648-L652) は SBIE6004 をログに記録し、取得が失敗したかアクティブな暗号化機能がない場合に要求を拒否します。
[^4]: [`File_NtCreateFileProxy()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/file.c#L4726-L4798) は要求を構築して応答を処理します。[`SbieDll_CallProxySvr()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/callsvc.c#L800-L864) は転送、拒否、およびタイムアウトの結果を処理します。
[^5]: [`UserServer::StartWorker()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L181-L246) はセッション ユーザー トークンを取得および複製してワーカーを作成します。[`UserServer::OpenFile()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L720-L759) は送信されたネイティブ オブジェクトを開き、呼び出し元へのハンドル転送を試みます。
[^6]: [ワーカー ポリシー パス](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L660-L714) はデバイス プレフィックスをチェックし、プロセス パス リストを取得し、[`SbieDll_MatchPathImpl()`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/dllpath.c#L506-L595) を使用して追加の認可を適用します。
[^7]: [書き込みの分類と認可](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L663-L714) はアクセス マスク、disposition、および `FILE_DELETE_ON_CLOSE` を考慮し、書き込み可能な要求には open-path 認可を必要とし、closed/write 分類を拒否します。
[^8]: [`SCertInfo`](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/verify.h#L24-L44) は EFS および他の暗号化/保護機能のために `opt_enc` を定義します。[証明書の検証](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/verify.c#L982-L1085) は単純な有効期限テストではなく機能とアクティビティを確立します。
[^9]: SBIE2225 は [`File_NtCreateFileImpl()` 検出サイト](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/file.c#L3862-L3865) と [`File_NtCreateTrueFile()` 再試行失敗サイト](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/file.c#L4672-L4685) で発行されます。
[^10]: [デバイス プレフィックス チェック](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/UserServer.cpp#L660-L661) は `\Device\HarddiskVolume` 名プレフィックスを受け入れます。ファイルシステムの暗号化機能を独立して検証するものではありません。
