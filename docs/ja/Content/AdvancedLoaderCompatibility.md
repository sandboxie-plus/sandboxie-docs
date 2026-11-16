# 高度なローダーおよび SxS 互換性

これらの高度な設定は、特定のプロセス作成、Side-by-Side (SxS) アクティベーション コンテキスト、初期 DLL 読み込み、および Windows バージョンの互換性問題に対処します。これらはトラブルシューティング コントロールであり、一般的なセキュリティ改善でも、別の Windows インストールを再現する方法でもありません。

| 設定 | 現在のスコープ |
| --- | --- |
| `PreferExternalManifest` | 作成される**子実行可能ファイル**によって Sandboxie のダミー マニフェスト回避策を選択します。 |
| `ExternalManifestHack` | 子を作成する**サンドボックス化された親**によってその回避策を選択します。 |
| `DisableBoxedWinSxS` | 一致するプロセスに対して、Sandboxie のボックス化された SxS サービスの代わりに代替アクティベーション コンテキスト パスを使用します。 |
| `DelayLoadDll` | 初期プロセス初期化中に名前付き DLL を利用不可にし、そのパスを記録します。 |
| `OverrideOsBuild` | サンドボックス化されたプロセス内の選択されたバージョン クエリ API からの結果を変更します。 |

## プロセス作成中のマニフェスト互換性 {#manifest-compatibility-during-process-creation}

`PreferExternalManifest` は既定で無効です。その名前にもかかわらず、Windows にアプリケーション自身の外部 `.manifest` ファイルを優先するよう単に指示するものではありません。子実行可能ファイルに対して有効な場合、Sandboxie はプロセス作成中にその子のマニフェストまたは構成ファイルのオープンを傍受し、Sandboxie に同梱されたファイルで置き換えることができます。また、関連する SxS レジストリ アクセスを Sandboxie のサービス側互換性キーにリダイレクトすることもできます。アプリケーションの実際のマニフェストは編集されません。

Sandboxie のプロセス作成パスが子を `asInvoker` としてマークする場合、たとえばアプリケーションのマニフェストが明示的に `asInvoker` を要求する場合、置き換えられるファイルは小さな `asInvoker` マニフェストと最小限の構成ファイルです。それ以外の場合、Sandboxie は空のファイルで置き換え、Windows が UAC 昇格ヒューリスティックを引き続き適用できるようにします。これらの置き換えはプロセス作成互換性パスに固有であり、すべてのアプリケーション マニフェストの一般的な置き換えではありません。

例:

```ini
[DefaultBox]
PreferExternalManifest=legacyapp.exe,y
```

オプションの実行可能セレクターは**作成される子**を指します。ボックス全体の `PreferExternalManifest=y` は回避策を一般的に有効にします。より具体的な `legacyapp.exe,n` はその子に対してそれをオフにできます。通常のボックス、グローバル、および有効なテンプレートの構成ルックアップが適用されます。

`ExternalManifestHack` は、同じ互換性パスを選択する別個の既定で無効な方法です。

```ini
[DefaultBox]
ExternalManifestHack=parent.exe,y
```

ここでセレクターは、子ではなく、子を作成する**すでに実行中のサンドボックス化された親**を指します。親が有効な `ExternalManifestHack` ルールに一致する場合、子指向の `PreferExternalManifest` チェックの前に回避策が選択されます。したがって、これら 2 つの実行可能ファイル修飾設定は互換ではありません。親指向のオプションは、Windows 11 KB5014019 後の Edge 互換性ケースのために追加されました。古い Edge テンプレート エントリは現在コメント アウトされており、アクティブな既定値として扱うべきではありません。

現在のイメージ認識ルックアップは、ワイルドカード パターンと構成されたプロセス グループも受け入れます。回避策を必要とするアプリケーションにのみ実行可能ファイル修飾ルールを使用してください。特定の一致値が一般的な値より優先される場合があります。

## `DisableBoxedWinSxS`

Sandboxie の通常の `CreateActCtxW` 処理は、ボックス化された RpcSs SxS サービスにアクティベーション コンテキスト データを生成するよう要求できます。`DisableBoxedWinSxS=y` はそのルートに対する互換性の代替であり、WinSxS アセンブリをオフにするスイッチでは**ありません**。一致するプロセスに対して、SbieDll は代わりにシステム `CreateActCtxW` パスを呼び出し、必要に応じてサンドボックス化されたソース ファイル パスを変換します。

```ini
[DefaultBox]
DisableBoxedWinSxS=explorer.exe,y
```

設定メタデータがボックス全体の Boolean のみを記述しているにもかかわらず、SbieDll の選択はイメージ認識です。同梱の ARM64 互換性テンプレートは実行可能ファイル修飾値を使用します。この代替パスは、SandboxieRpcSs 自体の内部および AppContainer トークンを持つプロセスに対しても自動的に選択されます。

ボックス化された RpcSs に 2 番目のコンシューマーがあります。起動時に `DisableBoxedWinSxS` の通常の有効な Boolean を読み取ります。ボックス全体の `y` はその `RPCSS_SXS` サービス スレッドが初期化されるのを防ぎます。このルックアップは、SbieDll と同じ実行可能ファイル名マッチングを実行し**ません**。したがって、プロセス修飾エントリは、一致するプロセスのために代替パスを選択するものとして理解されるべきであり、ボックス全体でボックス化された SxS サービスを無効にする信頼できる方法としてではありません。

## `DelayLoadDll`

`DelayLoadDll` は DLL の**ベース名**を取得し、大文字と小文字を区別しない完全一致を使用します。現在のドライバー チェックはパスまたはワイルドカード マッチングを実装していません。

```ini
[DefaultBox]
DelayLoadDll=guard64.dll
```

新しく開始するプロセスで SbieDll が初期化される前に、一致する DLL オープンはファイルが存在しないように見せかけられます。ドライバーは DLL の完全なパスをプロセスごとのキューに記録し、キューに入れられたパスを取得する API が存在します。ただし、その API の現在のツリー内呼び出し元、または意図された後の DLL 読み込みを完了する他の現在のツリー内パスは見つかりませんでした。`DelayLoadDll` を DLL がその後読み込まれる保証として依存しないでください。既存の互換性テンプレートには Comodo、ThreatFire、Logitech Process Monitor などの製品のエントリが依然として含まれていますが、その存在は後の読み込みパスがアクティブであることを立証するものではありません。

## `OverrideOsBuild`

`OverrideOsBuild` は、開始される実行可能ファイルによってオプションで修飾された 10 進数の Windows **ビルド番号**を受け入れます。

```ini
[DefaultBox]
OverrideOsBuild=legacyapp.exe,7601
```

ボックス全体の値には `OverrideOsBuild=7601` を使用します。現在のパーサーは `_wtoi()` を使用します。`10.0.19045.6216` のような完全なバージョン文字列は有効なビルド番号構文では**ありません**。最初の数値 `10` として解析されます。解析されたビルドがゼロでない場合、SbieDll はそのプロセスのために `RtlGetVersion`、`GetVersionExW`、および `GetVersionExA` をフックします。

Sandboxie はそれらのフックを通じて構成されたビルド番号を報告し、対応するメジャー/マイナー バージョンとサービス パック レベルを導出します。たとえば、ビルド `7601` は Windows 7 SP1 (`6.1`)、`9200` は Windows 8 (`6.2`)、`9600` は Windows 8.1 (`6.3`)、`9600` を超えるビルドはメジャー/マイナー `10.0` にマップされます。これは実際の OS、利用可能な API、製品エディション、またはビルド リビジョンを変更しません。また、すべてのバージョン検出方法をカバーするわけでもありません。`VerifyVersionInfoW` はこのメカニズムによってフックされません。

実行可能セレクターは、バージョン クエリ API がフックされるサンドボックス化されたプロセスと照合されます。通常のボックス、グローバル、および有効なテンプレートのルックアップが適用され、一致するイメージ固有の値が一般的な値より優先されます。

## SandMan 構成

ボックス全体の `PreferExternalManifest` チェックボックスは **Sandbox Options > Various Options > Compatibility** の下にあり、**Force usage of custom dummy Manifest files (legacy behaviour)** とラベル付けされています。既定でチェックされていません。

実行可能ファイル修飾 `PreferExternalManifest` エントリ、および一般的または実行可能ファイル修飾 `ExternalManifestHack` エントリは、**Sandbox Options > Advanced Options > Miscellaneous** の詳細 **Add Option** エディターで利用できます。`ExternalManifestHack` には専用チェックボックスがありません。そのエディターはテンプレートから継承されたエントリを別途表示できます。

現在の SandMan 特殊オプション リストには、`DisableBoxedWinSxS`、`DelayLoadDll`、または `OverrideOsBuild` のための専用コントロールがありません。[Sandboxie Ini](SandboxieIni.md)または該当する互換性テンプレートを通じて構成してください。テンプレートの存在は、そのテンプレートが有効でない限り設定が適用されることを意味しません。

## 変更の適用

マニフェスト回避策は子プロセスの作成中に照会されます。構成の再読み込み後、実行中のサンドボックス化された親は、後の子のために変更された `PreferExternalManifest` または `ExternalManifestHack` ルールを使用できます。すでに作成された子は影響を受けません。

`DisableBoxedWinSxS` の代替パス決定は、SbieDll の初期化中に行われます。変更した後は影響を受けるサンドボックス化されたプロセスを再起動してください。ボックス化された RpcSs SxS スレッドを制御するボックス全体の変更の場合、RpcSs が新しい値で開始するようにサンドボックス プロセス ツリーを再作成してください。

`DelayLoadDll` は、SbieDll 初期化前の該当する DLL オープンでのみドライバーによってチェックされるため、変更は主に新しく開始するプロセスにとって重要です。`OverrideOsBuild` はプロセスの初期化中にフックをインストールします。変更した後は影響を受けるプロセスを再起動してください。どちらの設定も、すでに読み込まれた DLL またはすでに初期化されたプロセスを遡って変更しません。

## バージョン履歴

- Sandboxie Plus 0.4.5 / Classic 5.44.1 は、古いアプリケーション マニフェスト ハックを既定で無効にしました。`PreferExternalManifest=y` はその従来の動作を保持しました。
- Plus 0.7.2 / Classic 5.49.0 は `OverrideOsBuild=7601` を追加しました。Plus 0.7.5 / Classic 5.49.8 はプロセスごとの `PreferExternalManifest` 構成を追加しました。
- Plus 1.0.3 / Classic 5.55.3 は `OverrideOsBuild` に影響する `GetVersionExW` の問題を修正しました。
- Plus 1.1.1 / Classic 5.56.1 は `PreferExternalManifest` を改善し、KB5014019 後の Edge の問題を修正しました。現在のメタデータは `ExternalManifestHack` を 1.1.2 で追加されたものとしてリストしています。

現在のメタデータは、`DisableBoxedWinSxS` または `DelayLoadDll` の導入バージョンを確立していません。特に、`PreferExternalManifest` と `DisableBoxedWinSxS` のメタデータ記述は、現在の実行可能ファイルの動作よりも広範です。

## 関連ページ

- [Sandboxie Ini](SandboxieIni.md)
- [RPC 互換性](RpcCompatibility.md)
- [コード インジェクション](CodeInjection.md)
