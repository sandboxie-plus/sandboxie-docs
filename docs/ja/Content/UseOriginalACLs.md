# Use Original ACLs

_UseOriginalACLs_ は v1.15.0 / 5.70.0 以降で使用可能な [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。選択されたサンドボックス化されたファイルおよびディレクトリの作成と移行パスのセキュリティ記述子の処理を変更します。操作に応じて、Sandboxie はアプリケーションによって提供されたセキュリティ属性を再利用するか、既存のソース オブジェクトからセキュリティ情報を取得しようとすることができます。

このオプションは、特定のファイルシステム セキュリティ属性に依存するアプリケーションとの互換性を目的としています。適切な記述子が利用可能な場合、Sandboxie はプロセス ユーザーの許可アクセス制御エントリ (ACE) の追加を試みます。これは最終的な記述子または有効なアクセスが元のものと一致することを保証するものではありません。

## 使用方法

```ini
[DefaultBox]

UseOriginalACLs=y
```

ランタイム フォールバックは `n` です。有効な値が構成されていない場合、オプションは無効です。サンドボックス化されたプロセスの有効な構成には、直接のボックス設定、適用可能な有効なテンプレート、および `GlobalSettings` フォールバックを含めることができます。直接のボックス値は継承された有効化値を上書きできます:

```ini
[DefaultBox]

UseOriginalACLs=n
```

## SandMan UI

**Sandbox Options > Security Options > Security Hardening > File ACLs** では、チェックボックスは **Use original Access Control Entries for boxed Files and Folders (for MSIServer enable exemptions)** です。

チェックボックスは直接のボックス設定を読み取り、必ずしもテンプレートまたは `GlobalSettings` から継承された有効な値ではありません。通常、チェックすると `UseOriginalACLs=y` が書き込まれます。チェックを外すと `n` を書き込むのではなく通常の直接値が削除されるため、継承された `y` がアクティブなままになることがあります。

手動で構成された直接の `UseOriginalACLs=n` は継承を上書きできますが、その後チェックボックスを外した状態で設定を保存すると、その直接値が削除されることがあります。継承された構成を使用する場合、チェックボックスの直接設定と有効なランタイム値を区別してください。

## 技術的な詳細

有効なオプションは 1 つの普遍的な記述子コピー メカニズムを選択しません:

1. **新規ファイルおよび明示的な新規ディレクトリ**: 通常のサンドボックス コピー作成パスは、アプリケーションの作成要求を通じて提供された記述子を複製し、その後プロセス ユーザー ACE 調整を試みます。対応するホスト ファイルまたはディレクトリを自動的に照会しません。記述子が提供されない場合、または複製が記述子を生成しない場合、この有効なブランチは `Secure_NormalSD` を代替するのではなく `NULL` を渡します。ネイティブの Windows の既定および継承処理が適用されることがあります。オプションが無効な場合、検査されたブランチは `Secure_NormalSD` を選択します。開かれたパス、デバイス、および特殊なケースは異なる処理に従うことがあります[^1]。

2. **中間ディレクトリ**: サンドボックス コピー パスを構築する間、Sandboxie は対応するソース ディレクトリを開き、そのセキュリティ情報を照会しようとします。照会が成功した後、プロセス ユーザー ACE 調整を試み、結果の記述子を宛先操作に提供します。ソースを開けない場合、または使用可能な照会済み記述子が得られない場合、これらのブランチは `Secure_NormalSD` を使用することがあります。このフォールバックは中間ディレクトリの作成に固有であり、すべての ACL 処理パスではありません[^2]。

3. **移行されたファイルおよびディレクトリ**: 既存のソース オブジェクトは、独立した新規オブジェクト記述子パスではなくソース セキュリティ クエリを使用します。照会された記述子は可能な場合に調整され、宛先作成中に提供されます。ファイルの内容とセキュリティ処理は別個の決定です。移行ポリシーは空のコピーを生成することがあり、このヘルパーを通じたディレクトリ移行はすべての子の再帰的なコピーではありません。有効なセキュリティ クエリの失敗は、`Secure_NormalSD` にフォールバックするのではなく移行ヘルパーを中止することがあります。外側のファイル操作ラッパーは追加の再試行動作を適用できるため、これは 1 つの最終的なアプリケーション可視エラーを確立しません[^3]。

4. **再解析ポイント**: 別個の移行パスが再解析データとセキュリティ情報を別々の操作で処理します。そのセキュリティ クエリは再度開かれた真のパス ハンドルを使用できるため、再解析データをコピーしてもリンク オブジェクト自体のアクセス許可の保持は保証されません。完全な記述子の保持、およびすべてのシンボリック リンク、ジャンクション、または他の再解析タイプの同一の処理は保証されません[^3]。

検査されたソース オブジェクト クエリは DACL、SACL、およびグループ情報を要求しますが、元の所有者は要求しません。SACL の取得は条件付きです。セキュリティ クエリ フックは、選択されたアクセス拒否失敗の後で SACL 情報なしで再試行できますが、すべての失敗またはパスに対してではありません。アプリケーション提供の記述子は異なるパスに従い、所有者情報を含むことができます。記述子を提供しても、Windows のセキュリティ記述子の割り当ておよび継承ルールが依然として適用されるため、同一の永続化されたアクセス許可を保証するものではありません[^1][^2][^3]。

## セキュリティへの影響

- **互換性**: このオプションは、特定のファイルシステム ACL またはセキュリティ記述子に依存するアプリケーションに役立つことがありますが、作成またはアクセスの成功を保証するものではありません。
- **MSI インストーラーのサポート**: UI は MSIServer 互換性のために [Msi Installer Exemptions](MsiInstallerExemptions.md) を検討することを推奨しています。設定には独立したコンシューマーがあり、どちらも他方の機能的前提条件ではなく、どちらもすべてのインストーラーが機能することを保証しません。
- **プロセス ユーザーのアクセス**: Sandboxie は `GENERIC_ALL` を要求する許可 ACE を追加しようとします。既存の拒否エントリは意図的に削除されません。有効なアクセスは依然としてそれらのエントリ、アクセス トークン制限、整合性ポリシー、特権、および Windows オブジェクト セキュリティと継承ルールに依存することがあります[^4]。
- **分離境界**: このオプションは選択されたファイルシステム セキュリティ記述子を変更します。Sandboxie の分離メカニズムを置き換えるものではなく、分離強化の保証として扱うべきではありません。

## 実装上の注意

`Secure_Init` は初期化中に有効な設定をプロセス ローカルの SbieDll 状態である `Secure_CopyACLs` に読み取ります。これはライブのグローバル トグルではなく、すべてのファイルシステム操作に対して再評価されるものではありません[^5]。

- `Secure_NormalSD` は Sandboxie が構築した通常の記述子であり、ソース オブジェクトから照会された記述子ではありません。
- `File_DuplicateSecurityDescriptor` は提供された記述子を検証および複製し、必要に応じて自己相対形式に変換します。複製自体は ACE を追加しません[^1]。
- `File_CreatePath` は `File_CreateBoxedPath` を通じても到達され、その両方のディレクトリ作成ループでソース ディレクトリ クエリを試みます。`File_MigrateFile` と `File_MigrateJunction` には別個の移行契約があります[^2][^3]。
- これらのソース クエリは `DACL_SECURITY_INFORMATION | SACL_SECURITY_INFORMATION | GROUP_SECURITY_INFORMATION` を要求します。`OWNER_SECURITY_INFORMATION` は含まれません[^2][^3]。
- `File_AddCurrentUserToSD` は、Sandboxie が記録したプロセス ユーザー SID に対して `GENERIC_ALL` およびフラグ `CONTAINER_INHERIT_ACE | OBJECT_INHERIT_ACE | INHERITED_ACE` を持つ許可 ACE を追加しようとします。使用可能な DACL と SID が必要で、失敗することがあり、検査された呼び出し元は戻りステータスをチェックしません。ヘルパーは可能な場合に既存の ACE をコピーし、明示的な正規の並べ替えや重複 ACE の抑制は行いません。調整の成功も、正確な永続化された ACE の順序も保証されません[^4]。

構成を保存して再読み込みしても、既に初期化されたサンドボックス化されたプロセスではこのキャッシュされた値は更新されません。有効な設定を変更した後は、影響を受けるサンドボックス化されたプロセスを再起動してください。この設定は本質的に Windows の再起動や Sandboxie サービスの再起動を必要としません[^5]。

オプションを変更しても、既存のサンドボックス ファイルまたはディレクトリを遡って書き換えたり、以前にコピーされた記述子を変更したり、内容を自動的に再移行したりすることはありません。プロセスを再起動しても過去の ACL は修復されません。

## 関連設定

- [MsiInstallerExemptions](MsiInstallerExemptions.md) - MSI インストーラー用の別個のサービス トークン互換性ガイダンス。

[^1]: [file.c](https://github.com/sandboxie-plus/Sandboxie/blob/05becaf9a58116dbb427476f5e3120ae77e65e78/Sandboxie/core/dll/file.c) の通常の作成: `File_NtCreateFileImpl` は呼び出し元によって提供された `ObjectAttributes->SecurityDescriptor` を使用します。`File_DuplicateSecurityDescriptor` はファイルシステム パスを照会するのではなくその記述子を複製します。

[^2]: [file.c](https://github.com/sandboxie-plus/Sandboxie/blob/05becaf9a58116dbb427476f5e3120ae77e65e78/Sandboxie/core/dll/file.c) の中間ディレクトリ: `File_CreatePath` の両方のループがソース ディレクトリ セキュリティ クエリを試み、記述子が残らない場合に `Secure_NormalSD` を選択します。クエリは [secure.c](https://github.com/sandboxie-plus/Sandboxie/blob/05becaf9a58116dbb427476f5e3120ae77e65e78/Sandboxie/core/dll/secure.c) の `Secure_NtQuerySecurityObject` を使用し、選択されたクエリを SACL 情報なしで再試行できます。

[^3]: [file_copy.c](https://github.com/sandboxie-plus/Sandboxie/blob/05becaf9a58116dbb427476f5e3120ae77e65e78/Sandboxie/core/dll/file_copy.c) の移行: `File_MigrateFile` はファイルとディレクトリを処理し、`File_MigrateJunction` は再解析データを別途処理します。どちらも有効な場合に選択されたソース セキュリティ情報を照会し、所有者情報を省略し、通常の記述子を代替するのではなくセキュリティ クエリの失敗を返すことがあります。

[^4]: [file.c](https://github.com/sandboxie-plus/Sandboxie/blob/05becaf9a58116dbb427476f5e3120ae77e65e78/Sandboxie/core/dll/file.c) の ACL 調整: `File_AddCurrentUserToSD` が許可 ACE の追加を試み、そのステータスは検査された作成および移行の呼び出し元によって無視されます。許可エントリは[有効な Windows アクセス](https://learn.microsoft.com/en-us/windows/win32/secauthz/how-dacls-control-access-to-an-object)を保証せず、[作成時の記述子処理](https://learn.microsoft.com/en-us/windows/win32/secauthz/security-descriptors-for-new-objects)が最終的な ACL に影響を与えることがあります。

[^5]: [secure.c](https://github.com/sandboxie-plus/Sandboxie/blob/05becaf9a58116dbb427476f5e3120ae77e65e78/Sandboxie/core/dll/secure.c) の初期化: `Secure_Init` は `SbieApi_QueryConfBool(NULL, L"UseOriginalACLs", FALSE)` を通じて `Secure_CopyACLs` を初期化します。構成 API はこの NULL セクションをサンドボックス化されたプロセスのボックス コンテキストを通じて解決します。キャッシュされたフラグはプロセス ローカルです。
