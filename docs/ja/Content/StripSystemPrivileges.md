# Strip System Privileges

_StripSystemPrivileges_ は、特定の SbieSvc サービスおよび RpcSs パスを通じて作成された SYSTEM ソース トークンからの特権の削除を制御します:

```ini
[DefaultBox]
StripSystemPrivileges=y
```

既定は `y` で、これが保護的な動作です。

> [!WARNING]
> `StripSystemPrivileges=n` は、影響を受ける SYSTEM トークン パスに対して古い、制限の少ない動作を復元し、推奨されません。

## 削除される特権

影響を受けるパスで有効な場合、Sandboxie は新しく複製されたトークンから次の特権を削除します:

- `SeTcbPrivilege`
- `SeCreateTokenPrivilege`

Sandboxie は Windows の `SE_PRIVILEGE_REMOVED` 操作を使用します。特権は単に無効化されるのではなくそのトークンから削除されるため、同じトークン上で単純に再度有効にすることはできません。`SeAssignPrimaryTokenPrivilege` は現在のヘルパーでは削除されません。

## ランタイム スコープ

現在の実装は、SbieSvc が次を作成するときにこの設定を適用します:

- SYSTEM として実行するように選択されたサンドボックス化されたサービスのための SYSTEM ソース トークン。
- 関連するサンドボックス化された RpcSs プロセス サーバー パスのための SYSTEM ソース トークン。

通常のユーザー トークン サービス起動には適用されず、すべてのサンドボックス化されたプロセスまたはすべての SYSTEM プロセスのためのグローバル特権フィルターとして説明すべきではありません。

トークンの複製、調整、または必要な特権削除操作が失敗した場合、影響を受ける起動またはトークン要求は、意図的に未削除の SYSTEM トークンで続行するのではなく失敗します。

## 構成スコープ

_StripSystemPrivileges_ はボックス全体のブール設定です。ボックスが上書き値を提供しない場合、通常のテンプレートおよびグローバル フォールバックがその有効な値に寄与することがあります。影響を受けるトークンが作成されるときに参照されるため、変更しても実行中のプロセスに既に割り当てられたトークンは変更されません。変更後は影響を受けるサンドボックス化されたサービスまたはプロセスを再起動してください。

## SandMan

**Sandbox Options > Security Options > Advanced Security** を開き、次を使用します:

> Drop critical privileges from processes running with a SYSTEM token

チェックボックスは保護設定を直接表します:

- チェック済み: 特権削除が有効で、これが既定です。
- 未チェック: SandMan は `StripSystemPrivileges=n` を書き込みます。

## セッション 0 の起動との関係

[Start System Box](StartSystemBox.md) は別の起動パスを使用します。SYSTEM ID でセッション 0 で開始されるボックスは、それ自体ではそのトークンがここに文書化されている _StripSystemPrivileges_ ヘルパーを通過する原因になりません。

## バージョン履歴

_StripSystemPrivileges_ は、セキュリティ問題 ID-4 の修正の一部として Sandboxie Plus 0.5.4 / Classic 5.46.0 で導入されました。

## 関連ページ

- [Sandboxed Services](SandboxedServices.md)
- [Start System Box](StartSystemBox.md)
- [Drop Admin Rights](DropAdminRights.md)
- [Sandboxie Ini](SandboxieIni.md)
