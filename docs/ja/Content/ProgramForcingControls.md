# プログラム強制のコントロール

自動強制は、プログラムがサンドボックスの外で起動しようとするときに、**新しいプロセスの起動**をどのように処理するかを決定します。ドライバーは `Process_GetForcedStartBox()` で中核的な選択を行います。構成された強制ルール、グローバル プログラム アラート、および一時的な **Pause Forcing Programs** 状態は、それぞれ異なる目的を果たします。いずれもすべての Sandboxie 分離のための一般的なスイッチではありません。

## 起動の評価方法

Sandboxie は、プロセスがすでにサンドボックス パスに関連付けられているかどうかを検討し、次に現在のユーザーとセッションで有効なボックスの構成された強制ルールを評価します。各ボックスは [Force Folder](ForceFolder.md)、[Force Process](ForceProcess.md)、および [Force Children](ForceChildren.md) ルールを提供できます。単一のグローバルな宛先ボックスはありません。[強制ルールの無効化](DisableForceRules.md)は、それらのルールのために構築された強制データからボックスを除外します。

通常の構成されたルールの場合、既存の詳細な順序は次のとおりです。実行可能ファイル ディレクトリの `ForceFolder` → `ForceProcess` / 構成された `ForceChildren` → 作業ディレクトリの `ForceFolder` → ドキュメント引数の `ForceFolder`。リンクされた設定ページが一致構文と例外をカバーしています。

通常の強制がボックスを選択しなかった場合、ドライバーはグローバル `AlertFolder`、次に `AlertProcess` のエントリをチェックします。通常のアラート リストの一致は、サンドボックス化されていない起動を報告または拒否します。サンドボックスを選択するのでは**ありません**。Mark-of-the-Web 強制を含む他の独立したパスは、後で評価される場合があります。正常な強制選択が成功した場合も、この通常のアラート リスト分岐を通過しません。

| メカニズム | スコープ | 永続性 | 新しい起動への影響 |
| --- | --- | --- | --- |
| `DisableForceRules=y` | 1 つのボックス | 構成 | そのボックスを通常の強制データへの参加から除外します。 |
| **Pause Forcing Programs** | Windows セッション | 一時的な時間制限付き状態 | アクティブな間、一致する通常の強制ルールの割り当てをスキップします。 |
| `AlertFolder` / `AlertProcess` | グローバル | 構成 | 通知または拒否のためにサンドボックス外の起動を一致させます。ボックスを選択しません。 |
| `StartRunAlertDenied=y` | グローバル | 構成 | 通常のアラート リストの一致で起動を拒否させます。 |
| `AllowForceSystem=y` | グローバル | 構成 | メインの強制/アラート評価から既定の ID ベースの除外を削除します。ルールは依然として一致する必要があります。 |

これらのメカニズムは互いの代用ではありません。SandMan は、チェックされていない個々の強制エントリを無効な UI エントリとして保持する場合もあります。それらはアクティブな強制ルールでも、`DisableForceRules` またはセッション一時停止と同じでもありません。

## グローバル プログラム アラートとブロック {#global-program-alerts-and-blocking}

`AlertFolder` と `AlertProcess` は `[GlobalSettings]` の下のグローバル リストであり、ボックスごとの宛先ルールではありません。

```ini
[GlobalSettings]
AlertFolder=C:\Example
AlertProcess=example.exe
```

[Alert Folder](AlertFolder.md)は、プロセス起動時に実行可能ファイル自体のパス/ディレクトリをテストします。`ForceFolder` とは異なり、アラート一致のために作業ディレクトリまたはドキュメント引数を検査しません。通常のフォルダー エントリはそのフォルダーの下で再帰的に一致し、ワイルドカード エントリはパターン マッチングを使用します。[Alert Process](AlertProcess.md)は通常のエントリをイメージ名として一致させ、`*` を含むエントリは正規化された実行可能ファイル パスに対する大文字と小文字を区別しないパターンとして扱われます。どちらのリストも、起動後の任意のファイル アクセスやアクティビティを監視しません。

既定では `StartRunAlertDenied=n` です。通常のアラート リストの一致は、このメカニズムが起動をブロックすることなく [SBIE1301](SBIE1301.md) を生成できます。`StartRunAlertDenied=y` の場合、通常のアラート リストの一致は代わりに起動を拒否します。`AlertStartRunAccessDenied` は既定で `y` で、その拒否が [SBIE1308](SBIE1308.md) を報告するかどうかを制御します。拒否自体は制御しません。このグローバル アラート ポリシーは、サンドボックスの **Start/Run Access** 制限とは別個です。

SandMan は **Global Settings > Program Control > Program Alerts** の下でリストを公開し、**Add Program** と **Add Folder** を提供します。**Prevent the listed programs from starting on this system** は `StartRunAlertDenied` にマップされ、**Issue message 1308 when a program fails to start** はこのグローバル パスの `AlertStartRunAccessDenied` にマップされます。

## 一時的な一時停止と永続的なボックスごとの無効化

SandMan の **Pause Forcing Programs** メニュー アクションは、一時停止を開始するときに期間を要求します。ツールバーとホットキーのアクションは要求しません。ドライバーは関連する Windows セッションの一時停止タイムスタンプを保存します。ボックスに `DisableForceRules=y` を設定したり、既に実行中のプロセスを中断したりしません。一時停止が有効な間、一致する `ForceFolder`、`ForceProcess`、または `ForceChildren` ルールは新しい起動でスキップされます。

スキップされた強制一致はその一時停止された強制ステータスを保持します。`StartRunAlertDenied` はその一致をブロックされた起動に変え**ません**。`NotifyForceProcessDisabled=y` の場合、代わりに SBIE1301 を生成できます。強制ルールが一致しなかった場合、通常の `AlertFolder` / `AlertProcess` チェックは依然として実行され、`StartRunAlertDenied=y` の下でブロックする場合があります。強制の一時停止は、グローバル アラート/ブロック リストを無効にしません。

[Force Disable Seconds](ForceDisableSeconds.md)は一時停止の期間を制御します。メニュー プロンプトは最初に構成された値を提供するか、設定が存在しない場合は 60 秒を提供します。ツールバーとホットキーのアクションは構成された値またはドライバーの 10 秒のフォールバックを使用します。構成されたグローバル `ForceDisableSeconds=0` は、時間制限付き一時停止を無効にします。ゼロは無期限の一時停止または強制の恒久的な無効化を意味しません。API は供給された期間が正の場合にのみ保存するため、メニューでゼロを入力しても、ゼロ値の INI 設定が必ずしも書き込まれるわけではありません。正の期間が構成として保存された場合でも、一時停止状態は一時的なままです。

[Force Disable Admin Only](ForceDisableAdminOnly.md)は既定で `n` です。グローバル `ForceDisableAdminOnly=y` の場合、一時停止 API は管理者アカウントに制限されます。常に昇格された管理者トークンを要求するわけではありません。SandMan はこれを **Only Administrator user accounts can use Pause Forcing Programs command** とラベル付けしています。基になるドライバーは、制御呼び出し元が信頼されていることも検証します。

## システム サービス ID {#system-service-identities}

`AllowForceSystem` は、既定で `n` の高度な手動グローバル Boolean です。既定のガードは、`S-1-5-18` (LocalSystem)、`S-1-5-19` (LocalService)、または `S-1-5-20` (NetworkService) として実行されているターゲット プロセスのメインの強制ルール、アラート ルール、および Mark-of-the-Web 評価をスキップします。親が DcomLaunch として識別されるこれらの ID のいずれかを持つプロセスは、このガードに対する明示的な互換性例外です。これはすべての SYSTEM を親とするプロセスに一般化されません。

```ini
[GlobalSettings]
AllowForceSystem=y
```

これを有効にすると、それらの ID が通常の評価に参加できるようになります。すべてのサービスを自動的に強制したり、このゲート外の他の処理を変更したりするわけではありません。この設定は Sandboxie Plus 1.16.0 / Classic 5.71.0 で追加されました。専用の現在の SandMan コントロールは特定されていません。

## 通知、ライフサイクル、および制限

同じグローバル **Program Alerts** 領域で、**Issue message 1301 when forced processes has been disabled** は `NotifyForceProcessDisabled` にマップされ、**Issue message 1321 when a process has been forced into a sandbox** は `NotifyForceProcessEnabled` にマップされます。どちらも既定で `n` です。1 つ目は一時停止中のスキップされた強制一致を報告し、2 つ目は強制割り当ての成功を報告します。どちらの通知設定も強制を有効化、無効化、または一時停止しません。[通知設定](NotificationSettings.md)を参照してください。

強制およびアラート構成は、構成が適用または再読み込みされた後の後続のプロセス起動決定に影響します。セッション一時停止はライブ ドライバー状態であり、その期間に従って期限切れになります。これらのコントロールは、プロセスを遡って移動、終了、または中断したり、ファイルまたはレジストリの分離または Sandboxie 自体を無効にしたり、サンドボックスの Start/Run 制限を置き換えたり、昇格を付与したりしません。Windows の再起動は、通常、これらのコントロールのためだけには必要ありません。
