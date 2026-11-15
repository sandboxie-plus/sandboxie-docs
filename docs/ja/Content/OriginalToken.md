# Original Token

*OriginalToken* は、高度で安全でない互換性およびデバッグ設定です。Sandboxie が通常の制限付きトークン パスを通じてサンドボックス化されたプロセスのプライマリ Windows アクセス トークンを置き換えることを防ぎます。また、他の場所で選択されたトークンおよび偽装の処理を緩和します。プロセスをサンドボックスの外で実行するものでは**ありません**。

> [!WARNING]
> `OriginalToken=y` は Sandboxie のトークン ベースの分離を実質的に弱めます。Sandboxie が通常低減するグループ、特権、および整合性の特性が、受信トークンから利用可能なままになることがあります。昇格されたトークンで開始されたアプリケーションはその昇格を保持することがあります。この設定は標準ユーザーに管理者特権を付与しません。より強力なトークンは、他のサンドボックス メカニズムがアクティブなままであっても、ホスト リソースへのアクセスを増加させることがあります。Sandboxie はこれを安全でないデバッグ オプションとして分類しています。

## 構成

```ini
[DefaultBox]
OriginalToken=y
```

ランタイムの既定は `n` (無効) です。これはボックス レベルのブール設定です。通常の構成解決は、該当するテンプレートまたはグローバル設定を通じてそれを提供することもできます。現在のコンシューマーは実行可能ファイル名で *OriginalToken* を選択しません。この動作を構成するために `OriginalToken=program.exe,y` などの実行可能ファイル修飾形式を使用しないでください。

SandMan には専用の *OriginalToken* チェックボックスまたは通常の Advanced Options リストのエントリはありません。特定の互換性またはデバッグのニーズがそれを正当化する場合、[Sandboxie Ini](SandboxieIni.md) を通じて構成してください。現在出荷されているテンプレートはそれを自動的に有効にしません。

## プライマリ トークンの動作

通常のサンドボックス化されたプロセスの場合、Sandboxie は初期プライマリ トークンを取得し、構成されている場合は予備フィルター処理を適用し、次にサンドボックス管理のプライマリ トークンを構築または制限して割り当てます。構成に応じて、これらの手順は特権を低減し、グループ アクセスを変更し、整合性を下げることがあります。

`OriginalToken=y` の場合、ドライバーはその通常のプライマリ トークンのフィルター処理、制限、および割り当てパスの前に戻ります。プロセスは Sandboxie の通常制限された置換を受け取るのではなく、そのパスに提供された Windows トークンを保持します。これは、すべての元の特権が常に存在することを意味しません。受信トークンは既に制限されている可能性があり、他の Windows または Sandboxie のパスが依然として特定のトークン操作に影響を与えることがあります。通常のトークン モデルについては [Access Token Isolation](AccessTokenIsolation.md) を参照してください。

### 他のトークン設定との区別

| 構成 | 通常のプライマリ トークン パスにおける予備フィルター処理 | その後の制限付きトークンの構築と割り当て |
| --- | --- | --- |
| 既定 | 適用 | 適用 |
| `UnfilteredToken=y` | スキップ | 依然として適用 |
| `UnrestrictedToken=y` | 依然として関与 | より制限の少ないトークンが Sandboxie のトークン パスを通じて複製および割り当てられる |
| `OriginalToken=y` | 通常のプライマリ トークン置換パスをスキップ | そのパスを通じて制限付きプライマリ トークンが割り当てられない |

したがって、*UnfilteredToken* と *UnrestrictedToken* は *OriginalToken* のエイリアスではありません。プライマリ トークン置換パスでは、*OriginalToken* は *ReplicateToken*、*CopyTokenAttributes*、*UnstrippedToken*、*KeepTokenIntegrity*、および予備の *DropAdminRights* フィルター処理などのオプションの分岐の前に戻ります。これは、それらの設定のすべての別個のコンシューマーが無関係になるわけではありません。[Advanced Token Settings](AdvancedTokenSettings.md) はそれらの個々の段階を説明しています。*FakeAdminRights* も子プロセス作成中に別個の互換性動作を持ちます。

## サンドボックス化されたままのもの

プロセスはそのサンドボックスに登録されたままであり、Sandboxie の通常のプロセス初期化は独立して構成されたファイル、レジストリ、IPC、GUI、およびネットワーク処理を依然として設定します。SbieDll インジェクションとサンドボックス ID は *OriginalToken* だけでは無効になりません。したがって、ファイルとレジストリの仮想化、該当するフィルター、および他のサンドボックス ルールはアクティブなままにできます。

アクティブなフィルターは、通常制限付きトークンのプロセスと同じホスト アクセス結果を約束するものではありません。Windows のアクセス チェックは *OriginalToken* によって保持されたより強力なトークンを観察することがあります。この設定はトークン ベースの保護の実質的な低減として扱い、サンドボックスの完全な除去としても、他のすべての保護を同一の強度で維持するものとしても扱わ**ない**でください。

## Application Compartment

[Application Compartment](NoSecurityIsolation.md) と *OriginalToken* は、制限付きプライマリ トークン置換をバイパスし、より直接的な子プロセス作成パスを使用するいくつかのランタイム分岐を共有します。Application Compartment は `OriginalToken=y` を自動的に書き込んだり有効にしたりせず、2 つの構成は同等ではありません。Application Compartment には、*OriginalToken* だけでは選択されない追加のパス ポリシー、フィルター処理、および Job オブジェクト動作があります。

## 子プロセスと AppContainer トークン

子の作成では、*OriginalToken* は Sandboxie のその後の中断された作成およびトークン置換シーケンスをスキップし、結果のトークン選択を Windows に渡します。すべての子が親のトークンの正確なコピーを受け取ることを保証するものでは**ありません**。特に、[Drop Child Process Token](DropChildProcessToken.md) は、*OriginalToken* 分岐が実行される**前に**呼び出し元提供のトークンをクリアできます。*DropAppContainerToken* もその分岐の前に評価され、他の特殊なケース処理が Windows に渡されるトークンに影響を与えることがあります。

*OriginalToken* はすべての AppContainer 互換処理を無効にするわけではありません。[AppContainer Token Compatibility](AppContainerTokens.md) はそれらの別個の API、プロセス属性、および呼び出し元提供トークンの段階を説明しています。

## 偽装と関連する効果

この設定はプライマリ トークン置換よりも広範です。ドライバーは Sandboxie 固有の偽装トークン検証パスを緩和し、SbieDll は選択された偽装フックとトークン互換処理を省略します。他の IPC 名前空間およびセキュリティ フックはインストールされたままです。これは偽装が常に成功すること、またはすべての IPC 分離が無効になることを意味しません。Windows のチェックと他の Sandboxie コントロールが依然として適用されます。

*OriginalToken* は、Sandboxie のサービスによって行われる選択されたトークン選択とチェックも変更します。それ自体では、サンドボックス化された RpcSs を SYSTEM として実行させる**ことはありません**。現在の自動 SYSTEM ソース パスには、*MsiInstallerExemptions* や *RunServicesAsSystem* などの設定も必要です。それらの別個の動作については [Sandboxed Services](SandboxedServices.md) および [RPC Compatibility](RpcCompatibility.md) を参照してください。

この設定は、プロセスをその Job オブジェクトから削除したり、そのリソース制限を自動的に無効にしたりすることなく、Sandboxie のルート Job オブジェクトに対する基本的な UI 制限を省略することがあります。[Job Objects](JobObjects.md) を参照してください。

## 変更の適用

プライマリ トークン置換およびいくつかのフック インストールの決定は、サンドボックス化されたプロセスが開始されるときに行われます。*OriginalToken* を変更しても、既存のプロセスのトークンが再構築されたり、そのプロセスにフックが再インストールされたりすることはありません。変更後は影響を受けるサンドボックス化されたプロセスを再起動してください。サンドボックス化されたプロセス ツリーを再起動すると一貫したテストが得られます。Windows の再起動または定期的な SandMan、サービス、またはドライバーの再起動は通常必要ありません。

## バージョン履歴

現在の設定メタデータは `AddedVersion=0.2.1` をリストしていますが、変更履歴は *OriginalToken* を Sandboxie Plus 0.4.5 / Classic 5.44.1 の実験的なテスト/デバッグ オプションとして説明しています。これらのソースは単一の明確な導入バージョンを確立しません。変更履歴は後にそれを安全でないデバッグ オプションと呼んでいます。

## 関連ページ

- [Access Token Isolation](AccessTokenIsolation.md)
- [Advanced Token Settings](AdvancedTokenSettings.md)
- [Drop Child Process Token](DropChildProcessToken.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Sandboxie Ini](SandboxieIni.md)
