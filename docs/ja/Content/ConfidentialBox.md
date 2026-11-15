# Confidential Box

_ConfidentialBox_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。サンドボックスで実行されているプロセスとスレッドに対する追加の保護を有効にします。

```ini
[DefaultBox]
ConfidentialBox=y
```

この設定は既定では無効で、現在適用可能な Support Certificate が必要です。

## 保護する内容

`ConfidentialBox=y` の場合、ドライバーは、サンドボックス化されたプロセスまたはスレッドへのハンドルを作成または複製するときに、サンドボックス化されていないホスト プロセスによって要求されるアクセス権をチェックします。これには、ターゲットを変更または制御できる権限だけでなく、読み取り専用およびクエリ アクセスも含まれます。

この保護はプロセスおよびスレッド ハンドルを対象とします。ファイルを暗号化したり、マウントされたボックス ルートを保護したり、ネットワーク、クリップボード、GUI、IPC、およびその他の許可されたデータ転送パスを自動的に制限したりするものではありません。暗号化されたバッキング ストレージが必要な場合は [Box Encryption](../PlusContent/BoxEncryption.md) を使用してください。

Sandboxie は、サンドボックスの管理または実行に必要なコンポーネントおよび Windows プロセスのための運用上の例外を保持します。これには SbieSvc と Start、選択されたコアまたは保護された Windows プロセス、初期化中にターゲットを開始しているプロセス、および該当する SandMan または Sandboxie Control のセッション リーダーが含まれます。[ProtectAdminOnly](ProtectAdminOnly.md) は、そのセッション リーダー例外に管理者アクセスが必要かどうかを決定します。

## DenyHostAccess

`DenyHostAccess` は、同じプロセス/スレッド保護パスのためにプログラム固有のルールを提供します。`ConfidentialBox` とは独立して使用できます。

```ini
[DefaultBox]
DenyHostAccess=monitor.exe,y
DenyHostAccess=audiodg.exe,n
```

一般的な構文は次のとおりです:

```ini
DenyHostAccess=[host-program-or-group,]y|n
```

- `y` は一致するサンドボックス化されていないホスト プログラムを拒否します。
- `y` は、上記の運用上の例外を条件として、一致するサンドボックス化されていないホスト プログラムにアクセス制限を適用します。
- `n` は一致するプログラムをこの特定の保護チェックから除外します。Windows または他のチェックが拒否するはずの権限を付与するものではありません。
- プログラム プレフィックスがない場合、その値はボックス全体の既定を提供します。したがって `DenyHostAccess=y` は既定の拒否ルールと同等です。
- プログラム セレクターはワイルドカードを含む Sandboxie の[プログラム名マッチング](ProgramNamePrefix.md)を使用し、構成されたプロセス グループを参照できます。

`ConfidentialBox` がない場合、`DenyHostAccess` は、ホスト プロセスが Sandboxie の通常許可されるアクセス サブセット外の権限を要求するときに評価されます。このサブセットはプロセス ハンドルとスレッド ハンドルで異なります。該当するサブセット内の権限のみを含む要求は、この特定の制限をトリガーしません。

オブジェクト フィルター パスでは、一致する拒否ルールは操作を直接拒否するのではなく、ハンドル作成または複製のために要求されたアクセス マスクを制限します。操作が成功した場合、結果のハンドルに使用可能なアクセス権がないことがあります。独立した Windows アクセス チェックまたは保護されたプロセスの制限により、操作が依然として失敗することがあります。

`ConfidentialBox` の場合、同じチェックが読み取り専用およびクエリ要求も対象とし、ホスト プログラムの既定は拒否になります。明示的な `DenyHostAccess=program.exe,n` エントリは互換性の例外を作成できます。組み込みの **Less Confidential Box** テンプレートは現在、`audiodg.exe` に対してそのような例外を使用しています。

上記の運用上の例外は依然として適用されます。`DenyHostAccess` は一般的なファイルシステム ルールではなく、指定された実行可能ファイルがサンドボックスとのあらゆる形式の相互作用を行うことをブロックするものではありません。

## 関連設定

- [Box Encryption](../PlusContent/BoxEncryption.md) はサンドボックスのバッキング ストレージを保護し、マウントされたルート保護を追加できます。`ConfidentialBox` とは独立しています。
- [ProtectAdminOnly](ProtectAdminOnly.md) は、保護されたプロセス、およびルート保護付きでマウントされた暗号化ルートのためのセッション リーダー例外を制御します。
- [ProtectHostImages](ProtectHostImages.md) は、特定のサンドボックス化されたプロセスによって読み込まれる実行可能イメージを制限します。別個の保護パスです。

## SandMan 構成

コントロールは次にあります:

**Sandbox Options > Security Options > Box Protection**

- **Protect processes within this box from host processes** は、選択すると `ConfidentialBox=y` を書き込みます。
- **Allow useful Windows processes access to protected processes** は **Less Confidential Box** 互換性テンプレートを有効にします。
- ホスト プロセス リストとその **Allow Process** および **Deny Process** アクションは `DenyHostAccess` エントリを書き込みます。
- **When box root is protected require SandMan to run as Administrator in order to access the files** は `ProtectAdminOnly` を制御します。

UI のホスト プロセス エディターはプログラム名を受け入れます。より高度なプログラム グループまたはワイルドカード ルールは手動で構成できます。

## 変更の適用

`ConfidentialBox` は各サンドボックス化されたプロセスが初期化されるときに記録されるため、変更後は影響を受けるサンドボックス化されたプロセス ツリーを再起動してください。`DenyHostAccess` および `ProtectAdminOnly` のプロセス アクセス部分は、構成の再読み込み後にホスト アクセス チェック中に参照されます。

## バージョン履歴

`ConfidentialBox` と `DenyHostAccess` は Sandboxie Plus 1.3.3 / Classic 5.58.3 で導入されました。暗号化されたサンドボックス イメージは後に Sandboxie Plus 1.11.0 / Classic 5.66.0 で追加されました。

## 関連ページ

- [Black Box](../PlusContent/black-box.md)
- [Box Encryption](../PlusContent/BoxEncryption.md)
- [Protect Admin Only](ProtectAdminOnly.md)
- [Protect Host Images](ProtectHostImages.md)
