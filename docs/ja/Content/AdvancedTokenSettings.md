# 詳細なトークン設定

このページの設定は、Sandboxie が Windows アクセス トークンをフィルタリングまたは再構築する方法を変更します。ほとんどは、Sandboxie が通常削除または制限するプロパティを保持する、高度な互換性またはデバッグ オプションです。これらは一般に、互換性または特殊なテストのために必要な場合にのみ使用すべきです。

これらの設定はトークン ベースの分離にのみ影響します。ファイルシステムとレジストリの仮想化、IPC コントロール、ネットワーク制限、GUI 分離、およびその他の独立した Sandboxie メカニズムは別個のままです。

<div id="token-processing-stages"></div>

## トークン処理の段階

トークン処理の関連部分は次のように簡略化できます。

```text
元のプライマリ トークン
    |
    v
事前フィルタリング
    |
    |-- UnfilteredToken はこの段階をスキップできます
    |
    v
制限 / 再構築
    |
    |-- UnrestrictedToken はこの段階をスキップできます
    |
    |-- 通常の最新パスはトークンを再構築します
    |
    v
サンドボックス プライマリ トークン
```

事前フィルターと、後の制限または再構築の段階は別個です。したがって、*UnfilteredToken* はトークンが無制限であることを意味せず、*UnrestrictedToken* は事前フィルタリングによって削除されたプロパティを復元しません。両方を有効にすると、どちらか一方のみを有効にするよりも、ソース トークンの特性が実質的により多く保持されます。

Sandboxie には最新のトークン構築パスと従来のフィルタリング パスがあります。現在の通常の構成は一般に、*SandboxieAllGroup* のランタイム既定が有効であるため、最新の `Token_CreateToken` パスを使用します。*UseCreateToken* もそのパスを選択できます。この区別は特に *UnstrippedToken* にとって重要で、その動作は 2 つのパスで異なります。

これはトークン処理の概念的概要であり、完全な Sandboxie 分離モデルではありません。

## 共通の構文とスコープ

このページのすべての設定はボックス全体の Boolean 設定です。

```ini
SettingName=y
SettingName=n
```

現在のランタイム ルックアップは実行可能ファイル修飾されていないため、これらの設定では `SettingName=program.exe,y` などの構文はサポートされていません。通常の Sandboxie 構成とテンプレートの継承は、ボックスの有効な構成に依然として影響を与える可能性があります。

## NoUntrustedToken

```ini
NoUntrustedToken=y
```

```ini
NoUntrustedToken=n
```

*NoUntrustedToken* は、設定メタデータと現在のランタイムの両方で既定 `n` です。通常の制限付きサンドボックス トークンは、Windows の **Untrusted** 整合性レベルを使用します。*NoUntrustedToken* が有効な場合、Sandboxie は代わりに **Low** 整合性を使用します。

この設定は、トークン置換または制限を無効にしたり、ソース整合性レベルを保持したり、セキュリティ分離を無効にしたりしません。サンドボックス トークンの引き下げられた整合性レベルを Untrusted から Low に変更し、残りのトークン分離ステップはアクティブなままにします。

*KeepTokenIntegrity* が有効な場合、通常の整合性低下はスキップされ、Untrusted 対 Low の選択は無関係になります。この設定は、[`NoSecurityIsolation=y`](NoSecurityIsolation.md)が通常のプライマリ トークン置換をバイパスする場合にも冗長です。

SandMan はこの設定を次で公開しています。

**Sandbox Options > Security Options > Advanced Security**

チェックボックスは **Use LOW integrity token instead of UNTRUSTED (reduces isolation)** とラベル付けされています。

## UnfilteredToken

```ini
UnfilteredToken=y
```

```ini
UnfilteredToken=n
```

*UnfilteredToken* は既定 `n` です。Sandboxie の事前トークン フィルタリング段階をスキップします。その段階は通常、固定された一連の機密特権を削除し、構成されている場合は [`DropAdminRights`](DropAdminRights.md) フィルタリングも適用します。

後の制限または再構築は依然として発生します。したがって、結果のトークンは、トークン ユーザーの置換または整合性レベルの低下を受けたり、グループが deny-only に変換されたり、再構築中に特権を失ったり、Sandboxie 固有のトークン グループを受け取ったりする可能性があります。

要するに、*UnfilteredToken* は事前フィルタリング段階をスキップします。後のトークン制限または再構築ステップは依然としてトークンを変更する場合があります。現在のコードは、関連する偽装トークン検証および WTS トークン処理中にもこの動作を参照します。

*DropAdminRights* は事前フィルターに参加するため、*UnfilteredToken* は管理者関連グループと選択された特権のその事前削除をバイパスできます。後の Sandboxie 制限を削除するものではありません。

## UnrestrictedToken

```ini
UnrestrictedToken=y
```

```ini
UnrestrictedToken=n
```

*UnrestrictedToken* は既定 `n` です。重いトークン制限または再構築の段階をスキップし、Sandboxie に以前の段階から受け取ったトークンを複製させます。

そのトークンは、事前フィルタリングによってすでに変更されている可能性があります。*UnrestrictedToken* のみを有効にしても、以前に削除されたグループ、特権、またはその他のプロパティが復元されません。

*UnrestrictedToken* は通常の重いトークン制限段階をスキップしますが、他の Sandboxie 分離メカニズムはアクティブなままであり、以前のトークン フィルタリングがすでにトークンを変更している可能性があります。ファイルシステムまたはレジストリの仮想化と分離、IPC コントロール、ネットワーク制限、またはその他の独立したサンドボックス メカニズムを無効にしません。

## UnfilteredToken と UnrestrictedToken

| 構成 | 事前フィルター | 制限/再構築 |
|---|---|---|
| 通常 | 適用 | 適用 |
| `UnfilteredToken=y` | スキップ | 依然として適用 |
| `UnrestrictedToken=y` | 依然として適用 | スキップ |
| 両方有効 | スキップ | スキップ |

両方のオプションを使用すると、どちらか一方のみよりも、ソース トークンの特性が実質的により多く保持されます。他の分離レイヤーは独立したままであるため、Sandboxie が完全に無効になるわけではありません。

## ReplicateToken

```ini
ReplicateToken=y
```

```ini
ReplicateToken=n
```

*ReplicateToken* は既定 `n` で、特に最新の `Token_CreateToken` 再構築パスに適用されます。ソース トークンから実質的により多くのプロパティを保持しながら新しいトークンを作成します。元のトークン オブジェクトを単に複製するわけではありません。

再構築されたトークンは、ソース トークン ユーザー、グループ、特権、トークン タイプ、偽装レベル、認証 ID、有効期限、所有者、プライマリ グループ、既定 DACL、およびトークン ソースを保持または再利用します。また、Sandboxie または Anonymous トークン ユーザー置換、グループの deny-only への変換、通常の特権削減、および *SandboxieAll* グループの通常の追加を含む、いくつかの通常の変換を回避します。

*ReplicateToken* はさらに、明示的な `CopyDeviceGroups=n` または `CopyTokenAttributes=n` 値に関係なく、オプションのデバイス グループ取得とトークン セキュリティ属性のコピーを有効にします。どちらのオプション操作も保持の成功を保証しません。それらの別個の動作と制限については、以下のセクションを参照してください。

この段階に渡されるソース トークンは、*UnfilteredToken* も有効でない限り、すでに事前フィルタリングを受けている可能性があります。したがって、*ReplicateToken* は以前に削除されたグループまたは特権を必ずしも復元しません。

実装はすべてのトークン情報クラスを明示的にコピーしません。調査では `TokenRestrictedSids`、`TokenOrigin`、`TokenSessionId`、または AppContainer 機能の明示的なコピーは確認されませんでした。*ReplicateToken* は、ソース トークンの特性を実質的により多く保持しながらサンドボックス トークンを再構築します。すべてのトークン フィールドの正確な複製として扱うべきではありません。

## CopyDeviceGroups

```ini
CopyDeviceGroups=y
```

```ini
CopyDeviceGroups=n
```

*CopyDeviceGroups* は、最新のトークン再構築中にソース トークンの `TokenDeviceGroups` の保持を要求します。有効な値が構成されていない場合、そのコンシューマー フォールバックは `n` です。これはボックス全体の Boolean 設定です。該当する有効なテンプレートと `GlobalSettings` フォールバックは有効な構成に寄与できますが、実行可能ファイル固有のセレクターはサポートされていません。

これは[トークン処理の段階](#token-processing-stages)で説明されている最新の再構築に適用され、従来のフィルタリングまたは *UnrestrictedToken* によって選択される複製には適用されません。明示的な `UseCreateToken=y` は必要ありません。最新パスは *SandboxieAllGroup* によって、または従来のフィルターが利用できない場合にも選択できます。*CopyDeviceGroups* を有効にしても、それ自体がそのパスを選択するわけではありません。

*ReplicateToken* は、`CopyDeviceGroups=n` が明示的に構成されている場合でもデバイス グループ コピーの決定を有効にします。これらの設定はエイリアスではありません。*CopyDeviceGroups* はこのオプション フィールドのみを要求し、*ReplicateToken* によって実行されるより広範な保持は要求しません。

取得はベスト エフォートです。Sandboxie は使用可能なソース トークン ハンドルを必要とし、デバイス グループ情報のクエリとスペースの割り当てに成功しなければなりません。ハンドルが利用できない、割り当てが失敗する、またはクエリが情報を取得できない場合、構築はそれなしで続行できます。

転送は使用可能なトークン コンストラクターにも依存します。拡張された `ZwCreateTokenEx` パスはデバイス グループを受け入れますが、古い `ZwCreateToken` フォールバックは受け入れません。拡張コンストラクターの失敗は、デバイス グループなしでの再試行を自動的にトリガーしません。したがって、この設定を有効にしても、すべてのサポートされているシステムで保持が保証されるわけではありません。

デバイス グループは、通常のトークン グループ (`TokenGroups`)、トークン セキュリティ属性 (`TokenSecurityAttributes`)、および AppContainer 機能とは別個です。それらはハードウェア デバイスのリストではありません。この設定は、通常のグループ メンバーシップまたは deny-only 変換、*SandboxieAll* グループ挿入、ユーザー SID 置換、整合性低下、特権削減、または別個の *CopyTokenAttributes* 操作を制御しません。

デバイス グループ情報を保持することは、それ自体で管理者特権を復元したり、デバイス ACL を変更したり、Sandboxie のデバイス制限またはファイルとレジストリの仮想化を無効にしたり、他のセキュリティ コントロールをバイパスしたり、無制限のホスト デバイス アクセスを付与したりしません。アプリケーションの互換性を保証するものでもありません。

## CopyTokenAttributes

```ini
CopyTokenAttributes=y
```

```ini
CopyTokenAttributes=n
```

*CopyTokenAttributes* は最新の `Token_CreateToken` パスに適用され、特に `TokenSecurityAttributes` を指します。Sandboxie はソース トークンからこれらのセキュリティ属性を読み取り、新しく作成されたトークンに追加します。この設定はすべてのトークン情報クラスをコピーするものではなく、AppContainer 機能がコピーされることを意味しません。

メタデータと現在のランタイム既定の間には重要な違いがあります。

- 設定メタデータは既定 `n` をリストしています。
- 現在の `Token_CreateToken` 実装は、設定が存在しない場合のランタイム既定として `true` を使用します。

その結果、現在の実装ではそのパスでトークン セキュリティ属性が既定でコピーされます。`CopyTokenAttributes=n` を明示的に設定すると、このオプションのコピーが無効になります。*ReplicateToken* を有効にすると、明示的な *CopyTokenAttributes* 値に関係なくコピー動作が強制されます。

属性のコピーは、新しいトークンが作成された後に発生し、ベスト エフォートです。`TokenSecurityAttributes` のクエリ、割り当て、または適用中の失敗は、それ以外は正常に作成されたトークンを無効にしません。

## KeepTokenIntegrity

```ini
KeepTokenIntegrity=y
```

```ini
KeepTokenIntegrity=n
```

*KeepTokenIntegrity* は既定 `n` です。Sandboxie は通常、ソース整合性 SID を引き下げられたサンドボックス整合性レベルに置き換えます。この設定を有効にすると、代わりにソース トークンの整合性レベルが保持されるため、High 整合性で始まるトークンは High 整合性のままになります。

整合性レベル、グループ メンバーシップ、および特権は別個のトークン プロパティです。*KeepTokenIntegrity* はソース整合性レベルを保持します。トークン グループと特権は独立してフィルタリングされます。*DropAdminRights* を元に戻したり、[`FakeAdminRights`](FakeAdminRights.md) の互換性の動作を変更したりしません。

この設定を有効にすると、*NoUntrustedToken* が無関係になります。また、通常のプライマリ トークン置換が *NoSecurityIsolation* によってバイパスされる場合にも冗長です。

## KeepUserGroup

```ini
KeepUserGroup=y
```

```ini
KeepUserGroup=n
```

*KeepUserGroup* は既定 `n` です。ここで「ユーザー グループ」とは、SID がトークンの `TokenUser` に一致するトークン グループ エントリを意味します。特に `BUILTIN\Users`、*SandboxieAll* グループ、またはログオン SID を意味するものではありません。

通常のグループ制限中に、Sandboxie はグループを無効にするか deny-only に変換できます。*KeepUserGroup* が有効な場合、トークン ユーザー SID に一致するグループは、その通常の処理を受けずに保持されます。`TokenUser` ID 自体は、後の通常の Anonymous Logon または Sandboxie SID パスによって依然として置換される可能性があります。

## UnstrippedToken

```ini
UnstrippedToken=y
```

```ini
UnstrippedToken=n
```

*UnstrippedToken* は既定 `n` です。選択されたストリッピング操作をスキップしますが、正確に保持されるプロパティはトークン構築パスに依存します。

### 最新のトークン構築パス

最新の `Token_CreateToken` パスでは、*UnstrippedToken* を有効にすると、通常のグループ制限変換と整合性レベル置換がスキップされます。通常のトークン ユーザー置換は依然として発生し、特権は依然として最新パスの制限付き特権セットに削減され、通常は `SeChangeNotifyPrivilege` を保持します。

したがって、すべてのトークン コンポーネントを保持するわけではありません。

### 従来のフィルタリング パス

従来のパスでは、整合性処理は *UnstrippedToken* の早期リターンの前に発生します。後のグループ ストリッピングと制限のステップはスキップされます。したがって、この設定は両方の実装にわたって *KeepTokenIntegrity* を一律に意味するものではありません。

*UnstrippedToken* は *UnfilteredToken* よりも遅く、より狭く作用し、*UnrestrictedToken* よりも包括的ではなく、どちらのエイリアスでもありません。最新の動作は現在の通常の構成に最も関連しますが、従来の区別は他の構成またはプラットフォーム条件下でも依然として存在します。

## NoSecurityIsolation との相互作用

[`NoSecurityIsolation=y`](NoSecurityIsolation.md) の場合、Sandboxie は通常、プライマリ トークン置換をバイパスします。したがって、このページで説明されている設定は、通常のプライマリ トークンに対して一般に冗長であるか、到達しません。

- *NoUntrustedToken*
- *ReplicateToken*
- *CopyDeviceGroups*
- *CopyTokenAttributes*
- *UnfilteredToken*
- *UnrestrictedToken*
- *KeepTokenIntegrity*
- *KeepUserGroup*
- *UnstrippedToken*

そのモードのより広範な効果については、[セキュリティ分離なし](NoSecurityIsolation.md)を参照してください。

## 管理者権限設定との相互作用

[`DropAdminRights`](DropAdminRights.md) は、管理者関連グループの無効化と選択された特権の削除を含む、実際のトークン フィルタリングを実行します。*UnfilteredToken* はその事前フィルタリング段階をバイパスできますが、*UnrestrictedToken* のみではそこで既に削除されたプロパティを復元しません。*KeepTokenIntegrity* は、管理者グループまたは特権を復元することなく High 整合性レベルを保持できます。

[`FakeAdminRights`](FakeAdminRights.md) は異なります。その現在の実装は、主に互換性フックを使用して、選択された管理者チェックが成功したように見せます。トークン フィルタリングによって削除された実際の管理者グループまたは特権を復元しません。

## SandMan 構成

このページの設定のうち、現在の専用 SandMan コントロールを持つのは *NoUntrustedToken* のみです。

**Sandbox Options > Security Options > Advanced Security > Use LOW integrity token instead of UNTRUSTED (reduces isolation)**

残りの設定は、高度な手動 [`Sandboxie.ini`](SandboxieIni.md) オプションです。*CopyDeviceGroups* には **Sandbox Options > Edit ini Section > Edit ini** を使用してください。専用チェックボックスはありません。

## Sandboxie Plus と Classic

トークン処理は共有 Sandboxie コンポーネントに実装されています。SandMan は *NoUntrustedToken* コントロールを公開し、このページの他の設定は手動構成を使用します。現在のソースには、同等の専用 Sandboxie Control Classic コントロールが含まれていませんが、互換性のある手動 INI 設定は、該当する場合は共有ランタイムで利用できます。Classic は **Configure > Edit Configuration** を通じて手動編集を提供します。

## 構成変更の適用

これらの設定は主に、Sandboxie がプロセス トークンを準備、フィルタリング、または作成するときに参照されます。それらを変更しても、すでに割り当てられたプライマリ トークンが遡って再構築されることはありません。設定を変更した後は影響を受けるサンドボックス化されたプロセスを再起動してください。サンドボックス化されたプロセス ツリーを再作成すると、一貫した動作が得られます。SandMan、サービス、またはドライバーの再起動は通常は必要ありません。

*UnfilteredToken* は、関連する後の偽装トークン処理中にも参照されますが、これはプライマリ トークン ポリシーを変更するときにプロセスを再起動する必要をなくすものではありません。

*CopyDeviceGroups* の決定は、最新のトークン構築に到達したときに評価されます。これには関連する後の偽装トークン処理が含まれます。プロセス開始時のみの別個のキャッシュではありません。後の構成読み取りは既存のプライマリ トークンを再構築しません。

## 失敗時の動作

本質的なトークン フィルタリング、構築、または割り当ての失敗は、意図的に制限の少ないホスト トークンにフォールバックするのではなく、プロセスの初期化を失敗させます。正確なエラーは失敗した操作に依存します。

オプションの *CopyDeviceGroups* 取得の失敗は異なります。使用できないソース トークン ハンドル、失敗した情報クエリ、または割り当ての失敗により、オプションのデバイス グループ情報なしで構築を続行できます。これはトークンの作成または割り当てが成功することを保証せず、コンストラクターの失敗はデバイス グループなしでの再試行を自動的にトリガーしません。

オプションの *CopyTokenAttributes* ステップは異なります。`TokenSecurityAttributes` のコピーの失敗は、それ以外は正常に作成されたトークンを無効にしません。

## バージョン履歴

- *UnfilteredToken* と *UnrestrictedToken* は Sandboxie Plus 0.2.1 / Classic 5.41.1 にさかのぼります。
- *KeepTokenIntegrity* は Sandboxie Plus 0.3.0 / Classic 5.42 にさかのぼります。
- *KeepUserGroup* と *UnstrippedToken* は Sandboxie Plus 1.0.6 / Classic 5.55.6 にさかのぼります。
- 設定メタデータは、*NoUntrustedToken*、*ReplicateToken*、および *CopyTokenAttributes* を Sandboxie Plus 1.14.1 で追加されたものとして記録しています。
- *CopyDeviceGroups* は Sandboxie Plus 1.17.0 / Classic 5.72.0 で導入されました。
- 専用の *NoUntrustedToken* SandMan コントロールは、Sandboxie Plus 1.17.0 / Classic 5.72.0 時代の変更で文書化されました。

## 関連ページ

- [分離メカニズム](IsolationMechanism.md)
- [セキュリティ分離なし](NoSecurityIsolation.md)
- [管理者権限の破棄](DropAdminRights.md)
- [偽の管理者権限](FakeAdminRights.md)
- [Sandboxie Ini](SandboxieIni.md)
