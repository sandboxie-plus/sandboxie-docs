# Job オブジェクト

## 概要

Sandboxie は通常、サンドボックス化されたプロセスを Sandboxie によって管理される Windows Job Object に割り当てます。この Job Object は、プロセスのグループ化とライフサイクル機能、選択された Windows Job Object GUI 制限、関連する設定ページに記載されているリソース制限、およびオプションの集合的終了動作を提供します。

Job Object は Sandboxie のアーキテクチャの 1 つのレイヤーにすぎません。トークン制限、ファイルシステムとレジストリの分離、IPC とオブジェクトの分離、ネットワーク制限、およびその他の GUI フックとポリシーは別々に実装されています。

## Sandboxie の Job Object

Sandboxie は通常、サンドボックスと Windows セッションの組み合わせごとに 1 つの Job Object を維持します。GuiServer は、サンドボックス化されたプロセスが開始するときに適切なオブジェクトを見つけるか作成します。

既存の Job Object にまだアクティブなプロセスが含まれている場合、Sandboxie はそれを再利用します。アクティブなプロセスがなくなった後、Sandboxie は古いハンドルを閉じ、次に必要になったときに新しい Job Object を作成します。したがって、Job Object が作成されたときに適用された設定は、新しく作成されたオブジェクトで有効になります。

Sandboxie は、プロセスの初期化中に影響を受ける各プロセスを割り当てます。そのルート Job Object は、アプリケーションと Windows Job の動作との互換性のためにブレイクアウェイを許可しますが、Sandboxie は依然として各サンドボックス化されたプロセスが開始するときにそれを評価し、ルート Job への関連付けを再度要求できます。Job Object からのブレイクアウェイは、それ自体でプロセスをサンドボックスの外に移動させたり、Sandboxie の他の分離レイヤーを無効にしたりしません。

## 既定の GUI 制限

通常の Sandboxie Job Object は現在、次の Windows Job Object UI 制限を適用します。

| 制限 | Job Object を通じた効果 |
| --- | --- |
| `JOB_OBJECT_UILIMIT_EXITWINDOWS` | Job 内のプロセスが、この制限によって制御される Windows のシャットダウンおよびログオフ操作を使用するのを防ぎます。 |
| `JOB_OBJECT_UILIMIT_HANDLES` | アクセスが明示的に許可されている場合を除き、Job の外で作成された USER ハンドルへのアクセスを制限します。 |
| `JOB_OBJECT_UILIMIT_SYSTEMPARAMETERS` | システム パラメーターへの変更を制限します。 |
| `JOB_OBJECT_UILIMIT_READCLIPBOARD` | Windows Job Object メカニズムを通じたクリップボードの読み取りを制限します。 |

Sandboxie は、必要な USER ハンドル アクセスを必要な場合に明示的に許可します。これにはデスクトップ ウィンドウへのアクセスが含まれます。これらの制限は追加の Windows Job Object レイヤーです。Sandboxie の GUI またはクリップボード分離のすべてを実装するものではありません。

次の設定は、プロセスを Sandboxie のルート Job Object から削除することなく、Sandboxie にこれらの基本的な Job Object UI 制限を省略させます。

- `OpenWndStation=y`
- `OriginalToken=y`
- `UnrestrictedToken=y`

これらの設定は、それ自体でプロセスのグループ化を削除したり、ルート Job によって運ばれるリソース制限を無効にしたりしません。`OpenWndStation` のウィンドウ ステーションおよびデスクトップの側面については、[サンドボックス デスクトップとウィンドウ ステーション](SandboxDesktop.md)を参照してください。

## `NoAddProcessToJob`

```ini
NoAddProcessToJob=y
```

`NoAddProcessToJob` はボックス全体の Boolean 設定です。その既定は存在しないか `n` です。

有効な場合、影響を受けるサンドボックス化されたプロセスは Sandboxie のルート Job Object に割り当てられません。その結果:

- ルート Job の GUI 制限はそれらのプロセスに適用されません。
- [プロセス メモリ制限](ProcessMemoryLimit.md)、[合計メモリ制限](TotalMemoryLimit.md)、[プロセス数制限](ProcessNumberLimit.md)、および [CPU レート制限](CpuRateLimit.md)はそのルート Job を通じて適用されません。
- ルート Job を通じた集合的終了は通常のメカニズムとして利用できません。
- サンドボックス化されたアプリケーションは、それらの Job が Sandboxie のルート Job の下にネストされることなく、独自の Job Object を使用できます。

この設定は Sandboxie を無効にしません。ファイルシステム、レジストリ、IPC、ネットワーク、トークン、GUI、およびその他の独立した制限は、独自の設定と実装によって引き続き管理されます。

`NoAddProcessToJob` は Sandboxie Plus 0.3.5 および Sandboxie Classic 5.42.1 以降で利用できます。

## `AllowBoxedJobs`

```ini
AllowBoxedJobs=y
```

`AllowBoxedJobs` はボックス全体の Boolean 設定です。現在の既定は存在しないか `n` です。

`NoAddProcessToJob` とは異なり、この設定はプロセスを Sandboxie のルート Job Object から削除しません。Windows 8、Windows Server 2012、およびネストされた Job Object をサポートする以降のバージョンでは、サンドボックス化されたアプリケーションが Sandboxie のルート Job の下にネストされた実際の追加の Job Object を作成および使用できるようにします。

`AllowBoxedJobs=n` の場合:

- サンドボックス化されたアプリケーションが使用する名前付き Job Object は、依然として Sandboxie のオブジェクト名前空間モデル内で処理されます。
- Sandboxie は、ボックス化された Job Object に対する実際の割り当ておよび終了制御を防ぎます。
- 割り当て要求は、実際のネストされた割り当てを作成する代わりに互換性のためにシミュレートできます。
- Job 完了ポートおよびプロセス作成 Job リスト操作のために、関連する互換性処理が使用されます。

サポートされている Windows バージョンで `AllowBoxedJobs=y` の場合:

- 実際のネストされた Job 割り当てが許可されます。
- サンドボックス オブジェクト ルールによって許可される場合、ボックス化された Job に対して割り当ておよび終了アクセスを付与できます。
- Sandboxie のルート Job は存在したままです。
- ルート Job の構成されたリソース制限はアクティブなままです。
- Sandboxie のオブジェクト名前空間分離が引き続き適用されます。

Sandboxie のルート Job が使用中である間、`AllowBoxedJobs=y` はアプリケーション所有のネストされた Job が Job Object UI 制限を追加または置き換えることを許可しません。サンドボックス化されたアプリケーションによる `JobObjectBasicUIRestrictions` を設定する要求は、互換性のために無視され、成功を報告しますが、Sandboxie のルート Job によって既に適用されている UI 制限は変更されないままです。

Sandboxie は、ユーザー モード API 処理とドライバー レベルの Job Object アクセス チェックの両方を通じてこれらの決定を強制します。

`AllowBoxedJobs` は Sandboxie Plus 0.8.5 および Sandboxie Classic 5.50.5 以降で利用できます。

## 比較

| 構成 | Sandboxie ルート Job | ルート Job の GUI 制限 | ルート Job のリソース制限 | アプリケーション所有の Job Object |
| --- | --- | --- | --- | --- |
| 通常/既定 | あり | あり (独立して抑制されない限り) | 利用可能で構成可能 | 既定で制限または互換性シミュレート |
| `NoAddProcessToJob=y` | なし | なし | なし | Sandboxie のルート Job の外で利用可能 |
| `AllowBoxedJobs=y` | あり | あり (独立して抑制されない限り) | アクティブなまま | サポートされている Windows バージョンで実際のネストされた Job |
| `NoSecurityIsolation=y` | なし | なし | なし | Sandboxie ルート Job が存在しないという理由だけではブロックされません |

要するに:

- `NoAddProcessToJob=y` は、プロセスのために Sandboxie のルート Job の使用を防ぎます。
- `AllowBoxedJobs=y` は Sandboxie のルート Job を保持し、アプリケーション所有のネストされた Job を許可します。

## リソース制限

Sandboxie のルート Job Object は、次のページに記載されている設定を運ぶことができます。

- [プロセス メモリ制限](ProcessMemoryLimit.md)
- [合計メモリ制限](TotalMemoryLimit.md)
- [プロセス数制限](ProcessNumberLimit.md)
- [CPU レート制限](CpuRateLimit.md)

`AllowBoxedJobs=y` はこれらの制限を削除しません。`NoAddProcessToJob=y`、[`NoSecurityIsolation=y`](NoSecurityIsolation.md)、または [`OpenWinClass=*`](OpenWinClass.md) によって Sandboxie がその Job を回避する場合、それらは Sandboxie のルート Job を通じて無効になります。

`OpenWndStation=y`、`OriginalToken=y`、および `UnrestrictedToken=y` は、上記の基本的な Job Object UI 制限のみを抑制できます。それ自体でルート Job またはそのリソース制限を削除しません。

## `TerminateJobObject`

```ini
TerminateJobObject=y
```

`TerminateJobObject` は、Sandboxie Plus 1.15.4 および Sandboxie Classic 5.70.4 で導入されたボックス全体の Boolean 設定です。その既定は存在しないか `n` で、現在専用の SandMan コントロールはありません。

有効な場合、該当するホスト側の **Terminate All** 処理は最初に Sandboxie のルート Job Object を終了しようとすることができます。Sandboxie のプロセス サービスはその後も残りのサンドボックス化されたプロセスを列挙して終了するため、Job の終了は唯一のクリーンアップ メカニズムではありません。このオプションは、すべての終了要求が Job を使用することを保証するものではなく、特にサンドボックスに使用可能なルート Job Object がない場合にそうです。

## アプリケーション コンパートメントと関連設定

次の場合:

```ini
NoSecurityIsolation=y
```

アプリケーション コンパートメント プロセスは Sandboxie のルート Job Object に割り当てられません。したがって、4 つのルート Job GUI 制限および上記のリソース制限は、その Job を通じて適用されません。これは、アプリケーション コンパートメント プロセスが独自の Job Object を使用できないことを意味しません。このボックス タイプのより広範な動作については、[セキュリティ分離なし](NoSecurityIsolation.md)を参照してください。

同様に、`OpenWinClass=*` は影響を受ける構成のために Sandboxie にそのルート Job Object を回避させます。その結果、ルート Job GUI 制限とリソース制限はその Job を通じて適用されません。その他のウィンドウ クラスの動作については、[Open Win Class](OpenWinClass.md)で説明しています。

## SandMan 構成

現在のコントロールは次にあります。

**Sandbox Options > Security Options > Job Object**

**Add sandboxed processes to job objects (recommended)**

- チェックあり: `NoAddProcessToJob` は存在しないか既定のままです。
- チェックなし: SandMan が `NoAddProcessToJob=y` を書き込みます。

**Allow use of nested job objects (works on Windows 8 and later)**

- チェックあり: SandMan が `AllowBoxedJobs=y` を書き込みます。
- チェックなし: SandMan が設定を削除し、既定を復元します。

SandMan は、アプリケーション コンパートメントおよび `OpenWinClass=*` のケースを含め、現在のボックス構成が Sandboxie のルート Job を使用できない場合、関連する Job Object コントロールを無効にします。`TerminateJobObject` は手動の INI オプションであり、専用チェックボックスによって公開されていません。これらのコントロールは New Box Wizard の一部ではありません。

## Sandboxie Control Classic

関連するランタイム コンポーネントは Sandboxie Plus と Classic で共有されているため、互換性のある手動の INI およびテンプレート構成を共有ランタイムで利用できます。

SandMan は `NoAddProcessToJob` と `AllowBoxedJobs` のための現在の専用コントロールを提供します。現在の Sandboxie Control Classic は、それらの設定または `TerminateJobObject` のための同等の専用コントロールを提供しません。Classic ユーザーは、該当する場合は手動で構成できます。

## 構成変更の適用

Job 割り当ての決定はプロセスの初期化中に行われます。`NoAddProcessToJob` または `AllowBoxedJobs` を変更した後は、影響を受けるサンドボックス化されたプロセスを再起動してください。

リソース制限と GUI 制限は、Sandboxie がルート Job Object を作成するときに構成されます。その Job にまだアクティブなプロセスが含まれている場合、Sandboxie はそれを再利用します。新しく構成された Job 設定が適用されるようにするには、サンドボックスを空にして、次のプロセスが開始するときに Sandboxie が新しい Job Object を作成できるようにしてください。Windows の再起動は通常は必要ありません。

## バージョン履歴

- **Sandboxie Plus 0.3.5 / Classic 5.42.1:** `NoAddProcessToJob` が導入されました。
- **Sandboxie Plus 0.5.5 / Classic 5.46.4:** 互換性の変更により、Chrome 関連のアプリケーションが `NoAddProcessToJob=y` で Job システムをより十分に利用できるようになりました。
- **Sandboxie Plus 0.8.5 / Classic 5.50.5:** `AllowBoxedJobs` が導入されました。
- **Sandboxie Plus 1.1.1 / Classic 5.56.1:** `AllowBoxedJobs=y` が既定になりました。
- **Sandboxie Plus 1.1.3 / Classic 5.56.3:** 互換性の問題の後、既定が `n` に戻されました。
- **Sandboxie Plus 1.15.4 / Classic 5.70.4:** `TerminateJobObject` が導入され、個別のプロセス終了が通常の既定パスとなりました。

## 関連ページ

- [プロセス メモリ制限](ProcessMemoryLimit.md)
- [合計メモリ制限](TotalMemoryLimit.md)
- [プロセス数制限](ProcessNumberLimit.md)
- [CPU レート制限](CpuRateLimit.md)
- [セキュリティ分離なし](NoSecurityIsolation.md)
- [Open Win Class](OpenWinClass.md)
- [サンドボックス デスクトップとウィンドウ ステーション](SandboxDesktop.md)
