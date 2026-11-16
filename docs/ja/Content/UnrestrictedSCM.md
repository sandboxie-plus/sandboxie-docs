# Unrestricted SCM

_UnrestrictedSCM_ は、Sandboxie のサービス開始承認パスにおける 1 つの Service Control Manager (SCM) アクセス許可チェックをバイパスする高度なサンドボックス設定です:

```ini
[DefaultBox]
UnrestrictedSCM=y
```

既定は `n` です。

> [!WARNING]
> この設定を有効にすると分離が弱まります。サービスの互換性要件が確認された場合にのみ使用してください。

## 設定が変更する内容

広範な `RunServicesAsSystem=y` パスがサンドボックス化されたサービスの SYSTEM ソース トークンを選択する場合、SbieSvc は通常、呼び出し元が実際の Windows SCM に対して `SC_MANAGER_ALL_ACCESS` を持つかどうかをチェックします。SCM セキュリティ記述子を取得し、ボックス モードに適した呼び出し元トークンを使用して Windows アクセス チェックを実行します。そのチェックが失敗した場合、Sandboxie は SYSTEM サービスの起動を拒否します。

_UnrestrictedSCM_ はその特定のアクセス許可チェックをバイパスします。すべてのサンドボックス化されたプロセスに無制限の SCM アクセスを付与したり、Sandboxie の一般的な SCM 傍受とエミュレーションを無効にしたりするものではありません。

## 関連するサービス コントロール

_UnrestrictedSCM_ は次を行いません:

- `RunServicesAsSystem` を有効にする。
- `RunServiceAsSystem` にサービスを追加する。
- サービスをサンドボックス化済みとして分類する。
- 既存のホスト サービスをサンドボックスに移動する。
- 結果として得られるサービス プロセスをサンドボックス外にする。

`RunServicesAsSystem` および `RunServiceAsSystem` は、別個の広範およびサービスごとのパスを通じて SYSTEM ソース ID を選択します。これらの設定については [Sandboxed Services](SandboxedServices.md) を参照してください。

Sandboxie は _UnrestrictedSCM_ チェックの前に [Drop Admin Rights](DropAdminRights.md) を評価します。drop-rights ポリシーが既に昇格パスを拒否している場合、_UnrestrictedSCM_ を有効にしてもその拒否は上書きされません。

`SandboxieDcomLaunch.exe` には別個の組み込み承認例外があり、_UnrestrictedSCM_ を必要としません。

## 構成スコープ

_UnrestrictedSCM_ はボックス全体のブール設定です。ボックスが上書き値を提供しない場合、通常のテンプレートおよびグローバル フォールバックがその有効な値に寄与することがあります。関連するサービス開始承認が実行されるときに照会されるため、構成の再読み込みは以降の要求に影響を与えることがあります。既に実行中のサービス プロセスを変更するものではありません。

## SandMan

**Sandbox Options > Security Options > Advanced Security** を開き、次を使用します:

> Allow only privileged processes to access the Service Control Manager

チェックボックスは _UnrestrictedSCM_ に対して反転しています:

- チェック済み: 通常の保護が有効で、これが既定です。
- 未チェック: SandMan は `UnrestrictedSCM=y` を書き込むことができます。

SandMan は `UnrestrictedSCM=y` のボックスを **Reduced Isolation** を持つものとして識別します。

## バージョン履歴

_UnrestrictedSCM_ は、セキュリティ問題 ID-3 のために追加された SCM アクセス チェックを無効にするためのデバッグ オプションとして Sandboxie Plus 0.3 / Classic 5.42 で導入されました。

## 関連ページ

- [Sandboxed Services](SandboxedServices.md)
- [Drop Admin Rights](DropAdminRights.md)
- [Sandboxie Ini](SandboxieIni.md)
