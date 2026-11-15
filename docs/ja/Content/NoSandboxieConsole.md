# No Sandboxie Console

_NoSandboxieConsole_ は、Sandboxie のカスタム コンソール リダイレクションおよびプロキシ パスをバイパスする高度なデバッグおよび互換性の設定です。

```ini
[DefaultBox]
NoSandboxieConsole=y
```

既定は `n` です。これはボックス全体のブール設定であり、通常のテンプレートと `GlobalSettings` の継承がその有効な値に寄与することがあります。

> [!IMPORTANT]
> この名前は、コンソール アプリケーションが無効になること、またはコンソール ウィンドウが存在できなくなることを意味しません。Sandboxie のカスタム コンソール処理を無効にして、可能な場合は通常の Windows コンソール動作を使用できるようにします。

## 何が変わるか

`NoSandboxieConsole=y` の場合、Sandboxie はプロセスの初期化中にカスタム コンソールなしの分岐を取ります:

- ドライバーは、コンソール アプリケーションを初期コンソールから切断し、後でプロキシ コンソールを作成するためにマークする可能性のある特別な初期化をスキップします。
- 低レベルの初期化は、対応する WOW64 コンソール ハンドル調整をスキップします。
- SbieDll は、プロキシ コンソールの再接続と `AllocConsole` 置換パス、および通常の分岐によってインストールされるコンソール タイトル フックをスキップします。
- Sandboxie の `ConsoleControl` フックはインポートまたはインストールされません。

これらの変更は、SbieDll が SbieSvc GUI プロキシにヘルパー コンソールを作成するよう要求し、その後サンドボックス化されたプロセスをそれにアタッチするパスをバイパスします。この設定は、`cmd.exe`、PowerShell、または他のコンソール アプリケーションの実行を妨げません。

## 何がアクティブのままか

この設定は、コンソールに関連するすべての Sandboxie コード パスを削除するわけではありません。SbieDll は、コンソール ウィンドウが存在する場合、その後の補助 GUI/メッセージ スレッドが動作できるように、現在のコンソール ウィンドウを依然として記録します。これには、デバイス変更通知に使用されるメッセージ処理が含まれます。

他の Sandboxie の分離および仮想化メカニズムも独立したままです。`NoSandboxieConsole` は、ターミナル、デスクトップ、トークン、または GUI 分離のための一般的なスイッチではありません。

## 互換性とデバッグ

このオプションは、Sandboxie のカスタム コンソール リダイレクションで動作しないアプリケーションのためのデバッグおよび互換性のエスケープとして存在します。通常の既定ではなく、Windows Console Host を無効にするものとして説明すべきではありません。

現在のソースは、上記で説明した従来の Sandboxie コンソール パスを実装しています。Windows Terminal または擬似コンソール (ConPTY) セッションに対する包括的な動作を確立するものではありません。

## Application Compartment

[Application Compartment](NoSecurityIsolation.md) プロセスは、ドライバー、低レベル、および SbieDll の初期化中に既に同じカスタム コンソール分岐をバイパスします。`NoSandboxieConsole=y` を追加しても、Application Compartment ボックスでそのコンソール動作が再度有効になることはありません。この等価性は関連するコンソール パスに限定され、2 つの設定はそれ以外の点で交換可能ではありません。

## DropConHostIntegrity との関係

[Drop ConHost Integrity](DropConHostIntegrity.md) は、Sandboxie のプロキシ/ヘルパー パスを通じて作成された外部コンソール ホストに適用されます。`NoSandboxieConsole=y` はそのパスをバイパスするため、`DropConHostIntegrity` が、結果として生じる通常の Windows コンソール パスを通じて作成されたコンソール ホストを変更することは期待すべきではありません。

## SandMan の構成

SandMan は現在、`NoSandboxieConsole` 専用のコントロールを提供していません。`Sandboxie.ini` のサンドボックス セクションで手動で構成するか、該当するテンプレートまたは `GlobalSettings` エントリを通じて構成します。

## 変更の適用

この設定は、初期のプロセスとコンソールの初期化中に使用され、既に実行中のプロセスに別のコンソール パスを後付けすることはできません。変更後は、影響を受けるサンドボックス化されたコンソール アプリケーションを再起動してください。SandMan、サービス、またはドライバーの再起動は通常必要ありません。

## バージョン履歴

`NoSandboxieConsole` は Sandboxie Plus 0.9.8 / Classic 5.53.0 で導入されました。変更履歴は、このコンソール動作が以前は `NoSandboxieDesktop=y` の一部であったことを記しています。現在のソースは `NoSandboxieConsole` と `NoSandboxieDesktop` を別個の設定として読み取ります。

## 関連ページ

- [Drop ConHost Integrity](DropConHostIntegrity.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Sandboxie Ini](SandboxieIni.md)
