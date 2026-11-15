# Open Protected Storage

ホストのレガシ Windows [Protected Storage](ProtectedStorage.md) (PStore) エンドポイントを開く現在の方法は、ボックスに対して Sandboxie の **Open Protected Storage** テンプレートを選択することです:

```ini
[DefaultBox]
Template=OpenProtectedStorage
```

古い `OpenProtectedStorage=y` ブールは設定メタデータに残っており、古い構成に現れることがありますが、現在の構成方法では**ありません**。Sandboxie Plus 1.8.0 / Classic 5.63.0 はそれをテンプレートに置き換えました。レガシ構成の移行は古いブールをテンプレート選択に変換できます。現在のソースに表示される古いドライバー コンシューマーはコメントアウトされています。このオプションを有効にするために出荷されたテンプレートを編集しないでください。

## テンプレートが行うこと

出荷されたテンプレートには次のシステム パスを開くルールが含まれています:

```ini
OpenFilePath=|\Device\NamedPipe\protected_storage
OpenIpcPath=*\BaseNamedObjects*\PS_SERVICE_STARTED
OpenIpcPath=\RPC Control\protected_storage
```

通常のサンドボックスでは、Sandboxie は通常 `PStoreCreateInstance` をフックし、独自の `IPStoreImpl` 互換実装を提供します。有効な IPC ポリシーが `\RPC Control\protected_storage` を開くと、Sandboxie の PStore 初期化はそのフックをスキップします。テンプレートの開くルールが有効な場合、このメカニズムを通じて Sandboxie の置換ではなくネイティブ PStore パスを許可します。出荷されたテンプレートの歴史的な `FuncSkipHook=PStoreCreateInstance` 行はコメントアウトされており、アクティブなルールではありません。

同じエンドポイント チェックは、Sandboxie の [Open Credentials](OpenCredentials.md) 設定がチェックされる前に実行されます。そのエンドポイントが有効に開いている場合、Sandboxie はユーザー モード WinCred フックもスキップし、サポート対象のネイティブ資格情報 API 呼び出しが通過できます。対照的に、`OpenCredentials=y` だけでは別個の PStore フックがそのまま残ります。PStore と Windows Credential API はここでは関連していますが、同じ機能ではありません。

## SandMan とスコープ

SandMan はこのテンプレートを **Sandbox Options > General Options > Restrictions > Other restrictions > Open System Protected Storage** で公開しています。選択すると、別個の **Open Windows Credentials Store (user mode)** チェックボックスがチェック済みおよび無効として表示されます。SandMan はテンプレートの選択を保存し、`OpenProtectedStorage=y` または自動の `OpenCredentials=y` 値を保存しません。

[Application Compartment](../PlusContent/compartment-mode.md) では、Sandboxie は既に置換の PStore フックをスキップします。それは、別個の WinCred フックがインストールされているかどうかをそれ自体で確立するものではありません。それら独自のエンドポイントと `OpenCredentials` チェックが依然として重要です。

フックの決定は、サンドボックス化されたプロセスで関連するモジュールが初期化されるときに行われます。テンプレートを変更した後は、影響を受けるサンドボックス化されたアプリケーションとその子プロセスを再起動してください。これらのユーザー モード フックのためだけに Windows の再起動または定期的なドライバー/サービスの再起動は通常必要ありません。
