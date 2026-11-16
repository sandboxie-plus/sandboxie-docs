# Drop ConHost Integrity

_DropConHostIntegrity_ はコンソール互換性設定です。Sandboxie のコンソール プロキシを通じて作成されたコンソールに関連付けられた外部 `conhost.exe` の整合性レベルを下げるよう Sandboxie に試みさせます。

```ini
[DefaultBox]
DropConHostIntegrity=y
```

既定は `n` です。これはボックス全体の Boolean 設定であり、通常のテンプレートおよび `GlobalSettings` の継承がその有効な値に寄与できます。

## ランタイムの動作

Sandboxie のコンソール プロキシが使用されると、SbieSvc ヘルパーがコンソールを作成し、Windows は関連付けられた `conhost.exe` をサンドボックスの外で開始します。その後、サンドボックス化されたプロセスがそのコンソールに接続し、ヘルパーは終了します。

`DropConHostIntegrity=y` の場合、ヘルパーは関連付けられたコンソール ホスト プロセスを識別し、そのプロセス トークンを開き、その必須整合性レベルを **Untrusted** に設定しようと試みます。これは、そのプロキシによって作成されたコンソール ホストの整合性ラベルを変更します。`conhost.exe` をサンドボックス化したり、サンドボックス化されたアプリケーションのトークンを変更したりするものではありません。

調整はベスト エフォートです。Sandboxie がコンソール ホストを識別できない場合、プロセスまたはそのトークンを開けない場合、または新しい整合性ラベルを適用できない場合、コンソールの作成はその調整の失敗を致命的なものとして扱わずに続行されます。

## 存在する理由

この設定は、Untrusted のサンドボックス化されたプロセスがより高い整合性レベルでコンソール ホストに接続されたときに一部のコンソール バッファ操作を実行できなかったコンソール アプリケーションのために導入されました。報告された症状には、PowerShell のエラーや Node.js の対話型コンソールの失敗が含まれていました。関連付けられたコンソール ホストを Untrusted に下げることで、報告された不一致が解決されましたが、すべてのコンソール障害がこの原因を持つわけではなく、動作は Windows のバージョン間で異なることがあります。元の報告については [Sandboxie issue #678](https://github.com/sandboxie-plus/Sandboxie/issues/678) を参照してください。

## スコープと制限

`DropConHostIntegrity` は、すべての `conhost.exe` プロセスに対するグローバル ポリシーではありません。Sandboxie コンソール ヘルパーがプロキシ コンソールの作成に成功したときに参照され、そのヘルパーが作成したコンソールに関連付けられたコンソール ホストのみを対象とします。

この設定はすべてのターミナル アーキテクチャを制御するものではありません。特に、その実装は Windows Terminal、擬似コンソール (ConPTY)、または Sandboxie のプロキシ パスの外で作成されたコンソール ホストに対する一般的なカバレッジを確立しません。

## NoSandboxieConsole との関係

[No Sandboxie Console](NoSandboxieConsole.md) は Sandboxie のカスタム コンソール リダイレクトおよびプロキシ パスをバイパスします。`DropConHostIntegrity` はそのプロキシ パス内で適用されるため、`NoSandboxieConsole` パスを通じて作成されたコンソール ホストを変更することは期待できません。

## SandMan 構成

SandMan で次を開きます:

**Sandbox Options > Security Options > Advanced Security**

チェックボックスは **Drop ConHost.exe Process Integrity Level** とラベル付けされています。これを選択すると `DropConHostIntegrity=y` が書き込まれ、オフにするとサンドボックスの明示的な値が削除されます。その後、この設定は継承されたテンプレートまたは `[GlobalSettings]` の値にフォールバックし、構成されていない場合は既定の `n` にフォールバックします。

## 変更の適用

この値は、新しいプロキシ コンソールが作成されるときに参照されます。変更しても既存のコンソール ホストのラベルは変更されません。影響を受けるサンドボックス化されたコンソール アプリケーションを再起動して、新しい設定で該当するコンソールを作成できるようにしてください。SandMan、サービス、またはドライバーの再起動は通常必要ありません。

## バージョン履歴

`DropConHostIntegrity` は Sandboxie Plus 0.7.3 / Classic 5.49.5 で導入されました。専用の SandMan チェックボックスは Sandboxie Plus 1.14.7 / Classic 5.69.7 で追加されました。

## 関連ページ

- [No Sandboxie Console](NoSandboxieConsole.md)
- [Sandboxie Ini](SandboxieIni.md)
