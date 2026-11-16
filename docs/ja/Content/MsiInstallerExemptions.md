# Msi Installer Exemptions

_MsiInstallerExemptions_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、v0.7.2 / 5.49.0 以降で使用できます。

ランタイム フォールバックは `n` です。この設定を有効にする有効な値がない場合、サンドボックス化された MSIServer は通常、LocalSystem トークンではなく Sandboxie のシステムレスなユーザー トークン互換パスを使用します。Sandboxie はそのパスで他の MSI 互換処理を提供するため、この設定はすべての MSI インストーラーに必要なわけではありません。

```ini
[DefaultBox]
MsiInstallerExemptions=y
```

`MsiInstallerExemptions=y` は、サンドボックス化された MSIServer に対して Sandboxie の SYSTEM トークン サービス パスを選択します。これは既定のトークン モデルを緩和し、この互換パスを必要とする MSI パッケージに役立つことがありますが、分離を弱める可能性があり、すべてのインストーラーが動作することを保証するものではありません。ホストの MSIServer をサンドボックスの外で実行したり、無制限のホスト SYSTEM アクセスを付与したりするものではありません。より広範な [Run Services As System](RunServicesAsSystem.md) 設定とは異なります。

[Application Compartment](NoSecurityIsolation.md) または `OriginalToken=y` の場合、この設定はサンドボックス化された RpcSs プロセスの SYSTEM トークン ソースも選択できます。この追加の効果は条件的であり、他の MSI 固有の互換回避策はこの設定によって有効になりません。関連するサービス トークン パスについては [Sandboxed Services](SandboxedServices.md) を参照してください。

この設定は、開いている COM インフラストラクチャに対する MSI 起動チェックを上書きしません。Sandboxie がその状態を検出した場合、`MsiInstallerExemptions` に関係なく SBIE2196 を報告し、MSI プロセスを終了させます。そのチェックの後、MSI として分類されたプロセスは、例外が有効でなく [NotifyMsiInstaller](NotifyMsiInstaller.md) が有効な場合 (そのランタイム フォールバックは `y`)、代わりに SBIE2194 警告を生成することがあります。SBIE2194 自体はインストーラーをブロックしません。`NotifyMsiInstaller=n` は、例外を有効にしたり SBIE2196 をバイパスしたりすることなく、警告を抑制します。

MSIServer トークンはサンドボックス化されたサービスが開始されるときに選択され、RpcSs トークンはサンドボックス化された RpcSs が開始されるときに選択されます。設定を変更してもどちらのトークンも遡って変更されません。一貫した新しい構成を使用するには、影響を受けるサンドボックス化されたインストーラーおよびサービス プロセスを再起動してください。

SandMan は、**Sandbox Options > Security Options > Security Hardening** の下で **Allow MSIServer to run with a sandboxed system token and apply other exceptions if required** としてこの設定を公開しています。チェックボックスはボックスの直接の値を読み取り、これはテンプレートまたは `GlobalSettings` を通じて継承された有効な値と異なることがあります。SandMan は **Drop Admin Rights** が有効な間はこれを無効にします。手動で構成された組み合わせは、サービス開始の承認の対象のままです。Sandboxie Control Classic には、特定された同等の専用コントロールはありません。この設定は Sandboxie Ini で構成できます。
