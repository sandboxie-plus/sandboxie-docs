# Open Credentials

`OpenCredentials` は、Sandboxie のユーザー モード Windows Credential API (WinCred) 互換レイヤー用の [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。既定では無効 (`n`) です。これはボックス/有効なブール設定であり、実行可能ファイル修飾ルールではありません。

Windows Credential API を使用すると、アプリケーションはユーザー名、パスワード、および関連するサインイン情報 (ネットワーク リソースの資格情報を含む) を保存および取得できます。この設定は、Sandboxie のインターセプトされた WinCred 呼び出しの処理に関するものであり、すべての Windows 資格情報メカニズムに関するものではありません。

```ini
[DefaultBox]
OpenCredentials=y
```

有効にすると、Sandboxie は影響を受けるサンドボックス化されたプロセスに対して WinCred フックをインストールしないため、そのフック セット内の呼び出しはネイティブ Windows 実装を使用します。これはそれ自体で Sandboxie の別個のレガシ [Protected Storage](ProtectedStorage.md) (PStore) フックを無効にするものでは**ありません**。すべての Windows 資格情報、認証、またはパスワード ストレージ メカニズムを記述するものではありません。

## 標準サンドボックスで無効な場合の動作

有効な IPC ポリシーが `\RPC Control\protected_storage` を開いていない限り (たとえば [Open Protected Storage](OpenProtectedStorage.md) テンプレートを通じて)、Sandboxie は `CredWriteA/W`、`CredReadA/W`、`CredWriteDomainCredentialsA/W`、`CredReadDomainCredentialsA/W`、`CredDeleteA/W`、および `CredEnumerateA/W` をインターセプトします。これは実装されている WinCred フック セットであり、すべての資格情報関連 API のカバレッジを保証するものではありません。

既定の互換レイヤーは、主に変更を仮想化しつつ、読み取り透過動作を保持します:

- インターセプトされた資格情報およびドメイン資格情報の書き込みは、それらのフックされた呼び出しを通じてネイティブ資格情報を直接更新するのではなく、Sandboxie の PStore バッキング ストレージにシリアル化されます。
- `CredReadW` はまずサンドボックス化された表現をチェックし、有効なサンドボックス化された項目が見つからない場合はネイティブの `CredReadW` にフォールバックできます。`CredReadDomainCredentialsW` も同様に、一致するサンドボックス化された項目が見つからない場合はネイティブのドメイン資格情報読み取りにフォールバックします。
- `CredEnumerateW` は、サンドボックス化されたエントリとネイティブ資格情報列挙の結果を組み合わせることができます。したがって、サンドボックス化されたプロセスはこの API を通じてホスト資格情報エントリを参照することがあります。
- インターセプトされた削除は、そのパスを通じてネイティブの資格情報削除 API を呼び出す代わりに、ローカルの削除マーカーを書き込みます。

Application Compartment は PStore レイヤーで異なります。そのモードでは、Sandboxie は置換の `PStoreCreateInstance` フックをインストールしませんが、保護されたストレージ エンドポイントも `OpenCredentials=y` もそれらをバイパスしない場合は WinCred フックがインストールされることがあります。その場合、それらのバッキング ストアの初期化は Sandboxie の `IPStoreImpl` ではなくネイティブ PStore プロバイダーに到達するため、上記の標準サンドボックスのストレージの説明を Application Compartment に一般化すべきではありません。

これらの動作は、ホスト資格情報の完全な機密性境界ではありません。また、Sandboxie のフック セット外の API を通じて何が起こるかを確立するものでもありません。

## Open Protected Storage との相互作用

`Template=OpenProtectedStorage` テンプレートは、保護されたストレージ IPC エンドポイントを開くルールを追加します。有効な IPC ポリシーがそのエンドポイントを開くと、Sandboxie は PStore フックと WinCred フックの両方をスキップします。したがって、このテンプレートは `OpenCredentials=y` だけよりも広範な効果を持ちます。このテンプレートは、内部的に古い `OpenProtectedStorage` ブールを設定するだけではありません。

SandMan では、現在のコントロールは **Sandbox Options > General Options > Restrictions > Other restrictions > Open Windows Credentials Store (user mode)** です。**Open System Protected Storage** を選択すると、この資格情報コントロールがチェック済みおよび無効として表示されます。`OpenCredentials=y` を自動的に保存することはありません。PStore コントロールの選択を解除すると、保存された資格情報設定の状態が復元されます。

フックのインストールは、サンドボックス化されたプロセスで関連するモジュールが初期化されるときに決定されます。この設定またはテンプレートを変更した後は、影響を受けるサンドボックス化されたアプリケーションとその子プロセスを再起動してください。これらのフックのためだけに Windows の再起動または定期的な Sandboxie ドライバー/サービスの再起動が必要になることは通常ありません。

[Protected Storage](ProtectedStorage.md)、[Open Protected Storage](OpenProtectedStorage.md)、および [SBIE2213](SBIE2213.md) を参照してください。
