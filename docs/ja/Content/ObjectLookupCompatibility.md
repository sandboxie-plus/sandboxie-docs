# オブジェクト ルックアップ互換性

`UseDriverObjLookup` と `UseObjectNameForKeys` は、Sandboxie が既存のオブジェクトおよびレジストリ キーのハンドルから名前を取得する方法に関する高度な互換性設定です。どちらも既定で無効です。ファイル、レジストリ キー、または名前付きオブジェクトへのアクセスを許可または拒否するルールではなく、Sandboxie 内部の名前解決を変更します。

## Sandboxie でのオブジェクト名ルックアップ

一部の Sandboxie パス処理操作は、開かれたハンドルに関連付けられた名前を必要とします。Sandboxie の内部 `Obj_GetObjectName` ヘルパーは通常、`NtQueryObject` を通じて Windows に `ObjectNameInformation` を要求します。他の内部ファイル、IPC、および選択されたセキュリティ オブジェクト パスもこのヘルパーを使用します。これは、アプリケーション自身の `NtQueryObject` 呼び出しに対する Sandboxie のフックとは別個です。`UseDriverObjLookup` を有効にしても、そのようなすべての呼び出しがドライバーを通じてルーティングされるわけではありません。

## UseDriverObjLookup

標準サンドボックスでは、`UseDriverObjLookup=y` は Sandboxie の内部オブジェクト名ヘルパーに、通常のユーザー モード `NtQueryObject` ルックアップを使用する代わりに、Sandboxie ドライバーにハンドルの名前を解決するよう要求させます。

```ini
[DefaultBox]
UseDriverObjLookup=y
```

これは、オブジェクト名クエリがハングする可能性がある特定のハンドルおよび I/O 条件（特に保留中の読み取りを伴う同期パイプ ハンドル）に対するオプトインの回避策です。一般的なパフォーマンス オプションでも、すべてのオブジェクト ルックアップ問題に対する保証でもありません。ドライバーは独自のオブジェクト名パスを使用して供給されたハンドルの名前を解決し、一部のファイル オブジェクトに対して特別な処理を行います。そのルックアップが失敗した場合、ヘルパーは失敗を返します。ネイティブの `NtQueryObject` パスを再試行しません。

アプリケーション コンパートメントは、`UseDriverObjLookup=y` が構成されていても、このドライバー支援ヘルパー パスを有効にしません。その `Obj_GetObjectName` 呼び出しはネイティブ パスを引き続き使用します。

## UseObjectNameForKeys

レジストリ操作が `RootDirectory` キー ハンドルと相対名を供給する場合、Sandboxie は相対部分を追加する前にルート キーの完全な名前を取得します。既定では、`Key_GetName` は `NtQueryKey(KeyNameInformation)` を通じてそのルート名を取得します。`UseObjectNameForKeys=y` は代わりに、このルート ハンドル ルックアップを `Obj_GetObjectName` 経由で送信します。

```ini
[DefaultBox]
UseObjectNameForKeys=y
```

このオプションは、すべての `NtQueryKey` 呼び出しを置き換えたり、レジストリ アクセス ルールを変更したりしません。操作にルート ハンドルがない場合、この選択はそのパスの構築に関与しません。

この代替は、以前の `NtQueryObject` ベースのルート ルックアップが元に戻された後、互換性のために保持されました。それは、一部のキーで `NtQueryKey` が失敗する可能性があるケースに対処しましたが、Windows 10 バージョン 1803 以前で問題を引き起こしました。それは歴史的な文脈であり、今日特定の Windows バージョンでそれを有効にすることを推奨するものではありません。

## 設定の相互作用

| `UseObjectNameForKeys` | `UseDriverObjLookup` | レジストリ ルート ハンドル名ルックアップ |
| --- | --- | --- |
| `n` | どちらの値でも | `NtQueryKey(KeyNameInformation)`。ドライバー設定は他の内部 `Obj_GetObjectName` 呼び出し元に依然として影響を与える場合があります。 |
| `y` | `n` | `Obj_GetObjectName`。ネイティブ `NtQueryObject(ObjectNameInformation)` を使用します。 |
| `y` | `y`、標準サンドボックス | `Obj_GetObjectName`。ドライバー支援ルックアップを使用します。 |
| `y` | `y`、アプリケーション コンパートメント | `Obj_GetObjectName`。ネイティブ `NtQueryObject` を使用します。ドライバー支援ヘルパー パスはこのモードでは無効のままです。 |

どちらの設定も、もう一方を有効にする必要はありません。選択されたルックアップが失敗した場合は、自動的に他のルックアップ方法に切り替えるのではなく、呼び出し元に失敗として返されます。

## 変更の適用

これらはボックス全体の yes/no 設定であり、実行可能ファイル修飾またはプロセス グループ ルールではありません。有効な値は、ボックス、`[GlobalSettings]`、または該当する有効なテンプレートから取得できます。Sandboxie はサンドボックス化されたプロセスで DLL を初期化しながら各値を読み取るため、変更した後は影響を受けるサンドボックス化されたプロセスを再起動してください。新しいプロセスが変更された構成を読み取るために、ドライバー、サービス、または Windows の再起動は通常は必要ありません。

SandMan にはどちらの設定にも専用チェックボックスがなく、組み込みの詳細オプション候補の中にもそれらをリストしていません。**Sandbox Options > Advanced Options > Miscellaneous > Add Option** フィールドは手動で入力されたオプション名を受け入れます。上記の例は直接の `Sandboxie.ini` 形式も示しています。

## バージョン履歴

- `UseObjectNameForKeys` は、Sandboxie Plus 0.8.8 / Classic 5.50.8 でオプトイン互換性設定として追加されました。
- `UseDriverObjLookup` は、まれなオブジェクト名クエリ ハング シナリオのために Sandboxie Plus 1.10.3 / Classic 5.65.3 で追加されました。

## 関連ページ

- [Sandboxie Ini](SandboxieIni.md)はボックス構成と継承を説明しています。
- [キー ルート パス](KeyRootPath.md)は、サンドボックス レジストリ ハイブがどこにマウントされるかを説明しています。ルート ハンドル ルックアップ方法を選択するものではありません。
- [NT 名前空間の分離](NtNamespaceIsolation.md)は、既存のハンドルの名前のルックアップではなく、名前付きオブジェクト ディレクトリの分離に関するものです。
