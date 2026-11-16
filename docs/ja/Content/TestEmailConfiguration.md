# Test Email Configuration

### 構成のテストと確認

Sandboxie はほとんどのメール プログラム向けに簡単な構成を提供しています。詳細については [Sandbox Settings > Applications > Email Reader](ApplicationsSettings.md#email-reader) を参照してください。

メール構成を完了した後、サンドボックスを削除したときに新しいメールが失われないことを確認するためにテストすることをお勧めします。そのためには、次の手順に従います:

*   サンドボックス内でインターネット アクセスを無効にします。これは、構成が正しいことを確認する前に、サンドボックス化されたメール プログラムが新しいメール メッセージを取得できないようにするための予防措置です:<br>
    [Sandbox Settings > Restrictions > Internet Access](RestrictionsSettings.md#internet-access) を開き、_Block All Programs_ をクリックし、最後に _OK_ をクリックします。
*   メール プログラムを Sandboxie の下で_サンドボックス化して_実行します。([Sandboxie Control](SandboxieControl.md) の [Tray Icon Menu](TrayIconMenu.md) から _Run Email Reader_ コマンドを使用できます。)
*   自分宛てのテスト用下書きメッセージを作成します。送信しないでください。
*   メール プログラムを終了します。メール プログラムがテスト メッセージを送信するよう提案する場合は、その提案を無視してください。
*   サンドボックスを削除します。([Delete Sandbox](DeleteSandbox.md) を参照してください。)
*   メール プログラムを通常どおり、つまり Sandboxie の_監督外で_実行します。
*   通常の (サンドボックス化されていない) メール プログラムのインスタンスを使用して、作成したテスト メッセージを表示および編集できることを確認します。

サンドボックス化されたメール プログラムのインスタンスで作成したメール メッセージが、サンドボックスが削除された後でも通常の (サンドボックス化されていない) インスタンスでアクセスできる場合、構成は正しいです。

*   完了したら、サンドボックス内でインターネット アクセスを再度有効にします:<br>
    [Sandbox Settings > Restrictions > Internet Access](RestrictionsSettings.md#internet-access) を開き、_Remove_ をクリックして (制限を削除し)、最後に _OK_ をクリックします。

詳細については、[Email Protection](EmailProtection.md) および [FAQ Email](FAQEmail.md) を参照してください。
