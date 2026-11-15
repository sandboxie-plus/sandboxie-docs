# Sandboxie Logon

Sandboxie は通常、[トークン分離](IsolationMechanism.md)の一部として、サンドボックス化されたプロセスのアクセス トークンによって表される ID を置き換えます。既定のパスは Windows の匿名ログオン ID を使用します。オプションの *SandboxieLogon* 設定は、代わりにサンドボックスに関連付けられた仮想 SID を使用します。

この動作はアクセス トークン分離の一部であり、Windows ユーザー アカウント管理ではありません。ローカルまたはドメイン アカウントを作成したり、ユーザーを Windows にサインインさせたり、別個の対話型ログインを作成したり、サンドボックスに独自のユーザー プロファイルやパスワードを与えたりするものではありません。

## SandboxieLogon

```ini
SandboxieLogon=y
```

```ini
SandboxieLogon=n
```

*SandboxieLogon* はボックス全体のブール設定で、既定は `n` です。ランタイムで実行可能ファイル修飾の一致をサポートしません。他のボックス設定と同様に、通常の Sandboxie 構成とテンプレートを通じて継承できます。

この設定が有効な場合、Sandboxie サービスはサンドボックスに関連付けられた仮想 SID マッピングを作成または解決します。Sandboxie はその SID をトークン構築機構に提供し、サンドボックス トークンの `TokenUser` として使用します。実際には、*SandboxieLogon* は通常の匿名サンドボックス トークン ID を、サンドボックスに関連付けられた仮想 SID に置き換えます。

仮想 SID は、Windows のアクセス チェックのためにサンドボックスに識別可能な ID を与えることができます。ただし、それは分離のために使用されるトークン ID のままです。通常の Windows アカウントでも別個のログオン セッションでもなく、それ自体でユーザー プロファイルを作成しません。

## AnonymousLogon

```ini
AnonymousLogon=y
```

```ini
AnonymousLogon=n
```

*AnonymousLogon* はボックス全体のブール設定で、既定は `y` です。専用の SandMan コントロールはないため、高度な手動構成設定です。ランタイムで実行可能ファイル修飾の一致をサポートしません。

匿名 ID パスがアクティブで、サンドボックス固有の SID が使用されていない場合、Sandboxie は Windows の **ANONYMOUS LOGON** SID (`S-1-5-7`) をトークン ユーザーとして置き換えます。関連する現在の Windows パスでは、Sandboxie はトークン構築の一部として匿名認証 LUID も使用することがあります。

通常の構成は次のとおりです:

```ini
SandboxieLogon=n
AnonymousLogon=y
```

*SandboxieLogon* を有効にすると、通常の匿名ユーザー ID の代わりにボックス固有の Sandboxie SID が使用されます。したがって、これらは通常のトークン構築パスにおける代替の役割であり、2 つの独立したユーザー ID 置換が順番に適用されるものではありません。

*AnonymousLogon* はサンドボックス トークンに表される ID を変更します。それ自体で匿名ネットワーク認証を保証するものではありません。SSPI、保存または明示的に提供された資格情報、SMB、ブラウザー、Windows 資格情報マネージャー、およびその他のアプリケーションまたは Windows の認証メカニズムは、このトークン ユーザー置換を超えた動作を持つことがあります。

## KeepLogonSession

```ini
KeepLogonSession=y
```

```ini
KeepLogonSession=n
```

*KeepLogonSession* はボックス全体のブール設定で、既定は `n` で、専用の SandMan コントロールはありません。ランタイムで実行可能ファイル修飾の一致をサポートしません。

その名前にもかかわらず、この設定は元の Windows ログオン セッションのすべてのプロパティを保持するものではありません。Sandboxie は通常、トークン構築中にトークン グループを制限します。*KeepLogonSession* が有効な場合、Sandboxie は `SE_GROUP_LOGON_ID` でマークされたトークン グループを保持し、そのログオン SID グループに対する通常の無効化または拒否のみの扱いを適用しません。

この実装がトークンの `AuthenticationId`、`TokenOrigin`、`TokenSessionId`、LSA 資格情報、DPAPI 状態、SSPI コンテキスト、またはネットワーク資格情報を保持または復元することは示されていません。

## トークン ユーザーとログオン SID

トークン ユーザーとログオン SID は別個の Windows トークンの概念です:

- *SandboxieLogon* と *AnonymousLogon* は、通常のサンドボックス トークン パスで `TokenUser` によって表される ID を選択します。
- *KeepLogonSession* は、Sandboxie のグループ制限ステップ中にログオン SID としてマークされたトークン グループを保持します。

ログオン SID グループを保持しても、Sandboxie または Anonymous Logon の `TokenUser` 置換は取り消されません。逆に、`TokenUser` の変更は LSA ログオン セッションの作成、保持、または削除とは同じではありません。

## セキュリティ分離と高度なモード

既定の匿名 ID とオプションのサンドボックス固有 SID は、Sandboxie のトークン ID 分離の一部です。*SandboxieLogon* はアクセス チェックで表されるサンドボックス ID を変更し、*KeepLogonSession* は Sandboxie が通常制限する 1 つのグループを保持します。他の Sandboxie 分離メカニズムは別途引き続き適用されます。

[`NoSecurityIsolation=y`](NoSecurityIsolation.md) の場合、Sandboxie は通常、プロセスのプライマリ トークンの置き換えをバイパスします。したがって、このページで説明されている ID 変換は一般にそのプライマリ トークン パスの一部ではありません。SandMan はセキュリティ分離が無効な場合、*SandboxieLogon* コントロールも無効にしてクリアします。

高度な *ReplicateToken* トークン構築モードは、通常の Sandboxie または Anonymous Logon ユーザー置換を実行するのではなく、ソース トークン ユーザーを保持します。他の高度なトークン フィルター処理設定はこのページの範囲外です。

## SandMan 構成

SandMan は *SandboxieLogon* を次で公開しています:

**Sandbox Options > Security Options > Advanced Security**

チェックボックスのラベルは **Use a Sandboxie login instead of an anonymous token** です。New Box Wizard も、該当する場合は Sandboxie ログオンの選択肢を公開します。

*AnonymousLogon* または *KeepLogonSession* 用の専用 SandMan コントロールはありません。必要に応じて [`Sandboxie.ini`](SandboxieIni.md) で手動で構成してください。

## Sandboxie Plus と Classic

ランタイム サポートは共有 Sandboxie コンポーネントに実装されています。SandMan は現在の *SandboxieLogon* インターフェイスを提供します。現在のソースには同等の専用 Sandboxie Control Classic コントロールは含まれていませんが、互換性のある手動 INI 設定は該当する場合に共有ランタイムで使用できます。

## 変更の適用と失敗時の動作

このページの設定は、Sandboxie がプロセス トークンを準備または構築するときに使用されます。既に割り当てられたプライマリ トークンを遡って再構築するものではありません。変更後は影響を受けるサンドボックス化されたプロセスを再起動してください。サンドボックス化されたプロセス ツリーを再作成すると予測可能な結果が得られます。SandMan、サービス、またはドライバーの再起動は通常必要ありません。

必須のトークン構築または割り当ての失敗は、意図的に制限の少ないホスト トークンにフォールバックするのではなく、プロセスの起動を失敗させます。サービスがサンドボックス固有の SID を作成または解決できない場合、その SID なしで続行でき、通常の匿名 ID パスが利用可能なままになります。これは考えられるすべてのトークン作成失敗に対する保証として扱うべきではありません。

## バージョン履歴

- 元の *SandboxieLogon* メカニズムは Sandboxie Plus 0.2.2 / Classic 5.41.2 時代にさかのぼります。
- Sandboxie Plus 1.2.0 / Classic 5.57 が現代のボックスごとの SID 動作を導入し、一時的に既定で有効にしました。
- Sandboxie Plus 1.2.7 / Classic 5.57.7 が既定を無効に戻しました。
- Sandboxie Plus 1.4.0 / Classic 5.59 が SandMan インターフェイスを追加しました。
- *KeepLogonSession* は Sandboxie Plus 1.14.1 で設定メタデータに追加されました。

現在のメタデータは *AnonymousLogon* の信頼できる導入バージョンを特定していません。

## 関連ページ

- [Isolation Mechanism](IsolationMechanism.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Sandboxie Ini](SandboxieIni.md)
