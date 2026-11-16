# AppContainer トークン互換性

Sandboxie は、AppContainer 関連の要求をいくつかの異なる段階で処理します。プロファイルおよびトークン API 呼び出し、プロセス作成属性、呼び出し元が供給する子トークン、および後のサンドボックス プライマリ トークン パスです。Windows が子を作成する前にトークン引数を変更することは、Sandboxie のその後のプライマリ トークン置換を無効にすることとは異なります。これらの高度な設定は特定の互換性パスに対処します。1 つの AppContainer オン/オフ スイッチを構成するものではありません。

標準サンドボックスでは、Sandboxie はネイティブの Windows AppContainer モデルを変更せずに保持するのではなく、互換性のために選択された AppContainer 作成動作を置き換えます。実際の Windows AppContainer トークン、Sandboxie の代替互換性トークン、およびプロファイル API によって返される AppContainer のような SID は異なるものです。

## 標準サンドボックスとアプリケーション コンパートメント

以下の動作は Sandboxie Plus 1.18.8 / Classic 5.73.8 以降に適用されます。

| 動作 | 標準サンドボックス | アプリケーション コンパートメント |
| --- | --- | --- |
| 通常の Sandboxie 制限付きプライマリ トークン置換 | 通常はアクティブ | バイパス |
| `CreateAppContainerToken` 互換性フック | Windows 8.1 以降でインストールされます | インストールされません |
| 直接の `NtCreateLowBoxToken` 互換性フック | Windows 8.1 以降でインストールされます | インストールされません |
| AppContainer 関連のプロセス作成属性 | 既定で抑制されます。`FakeAppContainerToken=n` はそれらを通過させます | 常にこの分岐を通じて通過します |
| `CreateAppContainerProfile` 互換性 SID フック | Windows 8 以降でインストールされます | インストールされません |
| `DropAppContainerToken` ランタイム既定 | `y` | `n` |
| `UnRestrictAppContainerToken` 代替パス | インストールされたフックを通じて適用可能 | そのフックを通じて使用されません |

アプリケーション コンパートメントは、ネイティブの Windows AppContainer 処理がより直接的に参加できるようにし、同時に Sandboxie の通常の制限付きプライマリ トークン置換をバイパスします。他のサンドボックス ポリシーは別個のままです。[アプリケーション コンパートメント](../PlusContent/compartment-mode.md)、[セキュリティ分離なし](NoSecurityIsolation.md)、および[アクセス トークンの分離](AccessTokenIsolation.md)を参照してください。

## AppContainer API 互換性

Windows 8.1 以降の標準サンドボックスでは、Sandboxie は `CreateAppContainerToken` をフックします。通常、現在のプロセス トークンを開き、`DISABLE_MAX_PRIVILEGE` を使用し、`CreateRestrictedToken` を通じて選択されたグループを無効にして、制限付き互換性代替を返します。1.18.8 以降、既定では 4 つの広範なグループがその無効化リストから除外されます。[KeepBroadGroupsInAppContainerToken](#keepbroadgroupsinappcontainertoken)を参照してください。結果は、要求された AppContainer SID と機能を含む実際の AppContainer トークンではありません。

標準ボックスのプロセス作成互換性フックは、`PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES` と `PROC_THREAD_ATTRIBUTE_ALL_APPLICATION_PACKAGES_POLICY` を転送せずに成功を報告することにより、それらを抑制できます。1.18.8 以降、[FakeAppContainerToken](#fakeappcontainertoken)がこの動作を制御します。直接の `NtCreateLowBoxToken` 呼び出しには、別個の [NeutralizeLowBoxToken](#neutralizelowboxtoken) コントロールがあります。

Sandboxie の標準ボックス `CreateAppContainerProfile` フックは、`S-1-15-2-...` の形をしたローカルに割り当てられた SID を返します。元の Windows プロファイル作成関数を呼び出したり、通常の AppContainer プロファイルを作成したりしません。現在の固定互換性 SID は、要求されたプロファイル名または機能から構築されていません。

Sandboxie は、`TokenAppContainerSid` を通じて、実際に AppContainer トークンであるプロセス トークンを別途検出できます。その検出は、標準ボックスの代替トークンまたはプロファイル フックの合成 SID がネイティブの AppContainer 分離セマンティクスを持っていることを意味しません。

<div id="fakeappcontainertoken-historical-setting"></div>

### FakeAppContainerToken {#fakeappcontainertoken}

```ini
FakeAppContainerToken=program.exe,n
```

1.18.8 以降、このイメージ認識設定は標準ボックスのプロセス属性パスで再び評価されます。そのランタイム既定は `y` で、上記の 2 つの属性を抑制します。`n` の場合、Sandboxie はそれらを Windows に転送し、ネイティブの AppContainer プロセス属性が子の作成に参加できるようにします。アプリケーション コンパートメントは常にこの分岐を通じてそれらを転送し、この設定を参照しません。

これはプロセス作成属性を制御し、別個のプロファイル SID フック、`CreateAppContainerToken` 代替、または直接の LowBox トークン フックを制御しません。`n` に設定しても、すべての AppContainer 互換性処理が無効になったり、すべての子がネイティブ AppContainer トークンで実行されることが保証されたりするわけではありません。

1.18.6 および 1.18.7 では、このパスの構成テストがコメント アウトされていたため、値を変更しても属性抑制に影響しませんでした。メタデータにおけるこの設定の歴史的な導入バージョンは 1.8.2 です。それは 1.18.8 でのその再開された効果とは別個です。

## 子作成中に呼び出し元が供給するトークン

`DropAppContainerToken` と [子プロセス トークンの破棄](DropChildProcessToken.md)は、呼び出し元プロセスが子を作成するときに供給するトークンに作用します。どちらも既存のトークンから AppContainer SID を削除したり、Sandboxie の後のプライマリ トークン置換を直接無効にしたりしません。

### DropAppContainerToken

```ini
DropAppContainerToken=browser.exe,n
```

この設定が有効で、`CreateProcessInternalW` に供給された `hToken` が AppContainer トークンである場合、Sandboxie はそのトークン引数をクリアし (`hToken = NULL`)、そのトレース パスに **Dropped AppContainer Token** を発行します。子はその後、その呼び出し元が供給するトークン引数なしで作成されます。既存のトークン オブジェクトは書き換えられません。

ランタイム既定は標準サンドボックスでは `y`、アプリケーション コンパートメントでは `n` です。この設定はイメージ認識です。例の `browser.exe` は、子実行可能ファイルではなく、子作成要求を行うサンドボックス化された**呼び出し元**を選択します。`n` の場合、この特定の設定は `browser.exe` が供給する AppContainer トークンを破棄しません。

標準サンドボックスでは、ドライバーは通常、作成後に子に `Token_ReplacePrimary()` を依然として適用します。呼び出し元が供給する AppContainer トークンを破棄することと、Sandboxie の通常の制限付きプライマリ トークンを適用することは別個の段階です。

アプリケーション コンパートメントでは、ネイティブの AppContainer 処理がそれ以外ではより直接的に許可され、通常の制限付きプライマリ トークン置換がバイパスされます。したがって、明示的に `DropAppContainerToken=program.exe,y` を設定すると、子に適用されるはずの Windows トークン制限を削除する可能性があります。これはトークン分離を減少させます。昇格を自動的に付与するものではありません。

### UnRestrictAppContainerToken

```ini
UnRestrictAppContainerToken=program.exe,y
```

このイメージ認識設定は、標準ボックスの `CreateAppContainerToken` 代替パスを制御します。1.18.8 以降、そのランタイム既定は `msedge.exe` を含むすべてのイメージで `n` であるため、Sandboxie は制限付き互換性代替を作成します。`y` の場合、Sandboxie は代わりに `NtDuplicateToken` を呼び出し、そのフックに供給された `TokenHandle` のプライマリ トークン複製を返します。供給されたトークンはすでに制限されている可能性があります。`y` は完全または無制限のユーザー トークンを保証しません。Sandboxie の制限付き代替パスよりも、その供給されたトークンをより多く保持します。

1.18.6 および 1.18.7 では、互換性のために `msedge.exe` のランタイム既定が `y` でした。1.18.8 の広範なグループの変更により、制限付き代替が Edge に対して再び使用可能になり、この既定の例外が削除されました。明示的な `UnRestrictAppContainerToken=msedge.exe,y` は依然として複製パスを選択します。アプリケーション コンパートメントは代替フックをインストールしないため、この設定はそのモードの通常のコントロールではありません。

### KeepBroadGroupsInAppContainerToken {#keepbroadgroupsinappcontainertoken}

```ini
KeepBroadGroupsInAppContainerToken=program.exe,n
```

1.18.8 で導入されたこのイメージ認識設定は既定で `y` です。これは、標準ボックスの `CreateAppContainerToken` フックがその制限付き代替を構築するとき (`UnRestrictAppContainerToken=n`) に適用されます。Sandboxie は Everyone、Users、Authenticated Users、および INTERACTIVE を無効にするグループのリストから除外します。ソース トークン内のそれらの既存の状態は保持されます。この設定はそこで既に無効にされていたグループを再有効化しません。他のグループは制限操作に渡され、`DISABLE_MAX_PRIVILEGE` は依然として適用されます。

これを `n` に設定すると、照会されたすべてのグループを無効化のために `CreateRestrictedToken` に渡す以前の動作が復元されます。その動作は、子が `\KnownDlls` などのリソースを開くのを妨げる可能性がありました。これは互換性/デバッグの選択であり、既定を変更する一般的な推奨ではありません。`UnRestrictAppContainerToken=y` によって選択される複製パスまたは別個の直接 LowBox トークン フックを制御しません。

### NeutralizeLowBoxToken {#neutralizelowboxtoken}

```ini
NeutralizeLowBoxToken=program.exe,n
```

1.18.8 以降、Sandboxie は Windows 8.1 以降の標準サンドボックスで直接の `NtCreateLowBoxToken` 呼び出しもフックします。このイメージ認識設定は既定で `y` です。フックは、要求されたネイティブ LowBox トークンをそのパッケージ SID と機能で作成する代わりに、`ExistingTokenHandle` のプライマリ トークン複製を返します。供給されたトークンはすでに制限されている可能性があります。

`n` の場合、フックは元の呼び出しとその引数を Windows に転送します。Windows のアクセス チェックと失敗は依然として適用されます。アプリケーション コンパートメントはこのフックをインストールしません。この設定は `UnRestrictAppContainerToken`、`KeepBroadGroupsInAppContainerToken`、およびプロセス属性抑制とは別個です。1 つを変更しても他のものが構成されることはありません。

### その他の子トークン互換性パス {#other-child-token-compatibility-paths}

`DropChildProcessToken` は既定で `n` で、選択された呼び出しイメージのために呼び出し元が供給する任意の子トークンをクリアできます。同じクリア動作は、Acrobat Reader またはプラグイン コンテナーとして分類されたイメージに対してハードコードされています。別個の Firefox 分岐は、`-sandboxingKind` を含む子コマンド ラインのためにトークンをクリアできます。これらは別個のパスです。古い Flash 固有の条件はコメント アウトされています。この設定のスコープについては、[子プロセス トークンの破棄](DropChildProcessToken.md)を参照してください。

`DeprecatedTokenHacks` は、従来の Chromium/Edge 互換性分岐のために依然として照会されますが、アプリケーション コンパートメント モードの外で、かつ `OriginalToken` が無効な場合に限られます。有効な場合、この分岐は、呼び出しプロセスが Chrome として分類され、子コマンド ラインが `--service-sandbox-type` を含む場合に、子プロセスのために呼び出し元が供給するトークンをクリアできます。`FakeAppContainerToken` を制御したり、すべての歴史的なトークン回避策のための包括的なスイッチとして機能したりしません。

## 既存のボックスと AppContainer 権限 {#existing-boxes-and-appcontainer-permissions}

バージョン 1.18.8 は、サンドボックス ルートおよびボックス化されたオブジェクトに使用されるセキュリティ記述子に AppContainer アクセス制御エントリ (ACE) を追加します。これらは、ネイティブの AppContainer の子が必要とするボックス化されたリソースにアクセスするのに役立ちます。既存のボックスは古いファイルシステム随意アクセス制御リスト (DACL) を保持している可能性があるため、新しいオブジェクトに使用される記述子を更新しても、それ自体ですべての既存のボックスが修復されるわけではありません。

影響を受ける既存のボックスのために、1.18.8 は次のコマンドを追加します。ボックス フォルダーの DACL を変更する権限で Sandboxie インストール ディレクトリから実行してください。管理者はこの修復を実行できます。

```cmd
KmdUtil.exe fixboxdacls
```

このツールは、呼び出し元のアカウントとセッションに対して有効なボックスを列挙し、既存のファイル ルート ディレクトリを解決し、そのチェックでそれらの付与が欠落していることが判明した場合、`ALL APPLICATION PACKAGES` (`S-1-15-2-1`) と `ALL RESTRICTED APPLICATION PACKAGES` (`S-1-15-2-2`) の継承可能なフル アクセス エントリを追加します。無効なボックスおよびそのアカウントに利用できないボックスは処理されません。このコマンドは選択されたボックスに限定されません。既存の `fixdacls` コマンドも 1.18.8 でこのボックス フォルダー修復を呼び出します。

これは保存されたファイルシステム権限を変更します。読み取り専用の診断ではありません。ボックスの列挙とパス クエリのためにドライバーが利用可能でなければなりません。未解決または存在しないルートはスキップされ、カスタム権限または継承が結果に影響を与える可能性があります。コマンドを実行すると、すべての既存の子オブジェクトへの AppContainer アクセスが保証されたり、利用できないイメージ バッキング ルートが修復されたりすると仮定しないでください。使用する前にカスタム ACL 要件を確認してください。この修復は上記のトークン設定とは別個です。

## セキュリティと構成

これらの設定は特定の Windows トークンの選択を変更し、アクセス チェックを実質的に変更する可能性があります。それ自体ではファイルまたはレジストリの仮想化、ネットワーク制限、IPC ポリシー、またはサンドボックス メンバーシップを無効にせず、管理者権限を付与しません。[元のトークン](OriginalToken.md)と[詳細なトークン設定](AdvancedTokenSettings.md)は、トークン パイプラインの後の方の別個の選択を説明しています。

このページのトークン設定のために特定された専用の現在の SandMan コントロールはありません。特定の互換性またはデバッグの必要性のために [Sandboxie.ini](SandboxieIni.md) を通じて構成してください。オプションの[プログラム名プレフィックス](ProgramNamePrefix.md)は、関連する API 呼び出しを行うサンドボックス化されたプロセスを選択し、その子実行可能ファイルではありません。

これらのパスは、SbieDll の初期化、AppContainer API フッキング、または子プロセスの作成中に選択されます。変更は、すでに実行中のプロセスに割り当てられたトークンを再構築しません。設定を変更した後は影響を受けるサンドボックス化されたプロセス ツリーを再起動してください。Windows の再起動または定期的なサービス/ドライバーの再起動は通常は必要ありません。

現在の設定メタデータは、`DropAppContainerToken` を 1.7.2、`FakeAppContainerToken` を 1.8.2、`UnRestrictAppContainerToken` を 1.8.4、および `DropChildProcessToken` を 1.15.6 で追加されたものとしてリストしています。再開された `FakeAppContainerToken` チェック、統一された `UnRestrictAppContainerToken=n` 既定、`KeepBroadGroupsInAppContainerToken`、`NeutralizeLowBoxToken`、および `fixboxdacls` コマンドは 1.18.8 の変更です。

## 関連ページ

- [子プロセス トークンの破棄](DropChildProcessToken.md)
- [元のトークン](OriginalToken.md)
- [詳細なトークン設定](AdvancedTokenSettings.md)
- [セキュリティ分離なし](NoSecurityIsolation.md)
- [アプリケーション コンパートメント](../PlusContent/compartment-mode.md)
- [Sandboxie Ini](SandboxieIni.md)
