# Protect Admin Only

_ProtectAdminOnly_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie のセッション リーダーが、保護されたルートおよび機密プロセスのチェックから例外を受け取るために管理者アクセスを持たなければならないかどうかを制御します。

```ini
[DefaultBox]
ProtectAdminOnly=y
```

現在のランタイムの既定は `y` です。管理者アクセスを必要とせずにセッション リーダーをこれらのチェックに通すには、`ProtectAdminOnly=n` を設定します。

## 暗号化ルートの動作

暗号化されたボックス イメージが **Protect Box Root from access by unsandboxed processes** でマウントされている場合、ドライバーは通常、無関係なホスト プロセスがマウントされたルートを開くことをブロックします。ルートを所有するサンドボックス、SbieSvc、必要な Windows コンポーネント、および許可された SandMan または Sandboxie Control のセッション リーダーは例外のままです。

`ProtectAdminOnly=y` の場合、そのセッション リーダーの例外は、セッション リーダーが管理者アクセスを持っている場合にのみ付与されます。したがって、非管理者の SandMan または Sandboxie Control インスタンスは保護されたルート チェックによってブロックされます。`ProtectAdminOnly=n` の場合、セッション リーダーは昇格されていなくても例外を受け取ることがあります。

この設定は、通常のサンドボックス化されたアプリケーションを管理者として実行することを要求せず、一般的な Windows 管理者ポリシーまたはファイルシステム ACL でもありません。暗号化ルート アクセスの場合、ルート保護がアクティブな間のみセッション リーダーの例外を制御します。その別個のプロセス/スレッドへの効果は以下で説明します。

## 機密プロセスの動作

[ConfidentialBox](ConfidentialBox.md) または `DenyHostAccess` がそれ以外の点でホスト プロセスによるサンドボックス化されたプロセスまたはスレッドのオープンをブロックする場合、同じ設定が参照されます。`ProtectAdminOnly=y` の場合、非管理者のセッション リーダーはその拒否から免除されません。管理者のセッション リーダーは免除されることがあります。実装上必要な他のシステムおよび Sandboxie の例外は別個のままです。

## SandMan 構成

コントロールは次にあります:

**Sandbox Options > Security Options > Box Protection**

その現在のラベルは次のとおりです:

**When box root is protected require SandMan to run as Administrator in order to access the files**

ランタイムの既定が有効であるため、設定が存在しない場合、チェックボックスは選択されています。

設定を変更すると、構成の再読み込み後に以降のプロセス/スレッド アクセス チェックに影響します。暗号化ルートが既にマウントされている場合、そのルート保護に選択を適用するにはボックスをアンマウントして再マウントしてください。

## バージョン履歴

`ProtectAdminOnly` は、既定で有効として Sandboxie Plus 1.16.4 / Classic 5.71.4 で導入されました。SandMan は Sandboxie Plus 1.16.8 / Classic 5.71.8 で専用のチェックボックスを追加しました。

## 関連ページ

- [Box Encryption](../PlusContent/BoxEncryption.md)
- [Confidential Box](ConfidentialBox.md)
