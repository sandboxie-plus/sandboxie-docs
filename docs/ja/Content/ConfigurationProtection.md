# Configuration Protection

当初、[Sandboxie Control](SandboxieControl.md) または [Sandman](PlusMigrationGuide.md) UI を使用する誰もが、[Sandboxie Ini](SandboxieIni.md) 構成ファイルに保存されている Sandboxie 構成のあらゆる側面を変更できます。さらに、構成テキスト ファイルにアクセスできる誰もが、構成を操作して Sandboxie に再読み込みできます。

[Sandboxie Ini](SandboxieIni.md) 構成ファイルを不正な変更から保護することを有効にできます。Sandboxie は 4 つの保護モードを提供します:

* 管理者ユーザー アカウントのみが変更できる (参照: [EditAdminOnly](EditAdminOnly.md)。)
* 変更するにはパスワードを入力する必要がある (参照: [EditPassword](EditPassword.md)。)
* 管理者ユーザー アカウントのみが Pause Forcing Programs コマンドを使用できる (参照: [ForceDisableAdminOnly](ForceDisableAdminOnly.md)。)
* メイン ウィンドウが非表示になったときにパスワードをクリアする (参照: ForgetPassword。)

すべてのモードを同時にアクティブにできます。

この保護は、[Sandboxie Ini](SandboxieIni.md) 構成ファイルの **Global Settings**、**Sandbox Settings**、および **Template Settings** セクションに適用されます。ユーザーごとの設定を保存する **User Settings** セクションには適用されません。

[Sandboxie Control](SandboxieControl.md) で保護をアクティブにするには、[Configure menu > Lock Configuration](ConfigureMenu.md#lock-configuration) コマンドを使用します。

[Sandman](PlusMigrationGuide.md) で保護をアクティブにするには、Options menu > Global Settings > Advanced Config > Sandboxie.ini Presets > Config Protection コマンドを使用します。

* * *

保護の回避を防ぐために、次の点を考慮してください:

**構成ファイルの配置:** [Sandboxie Ini](SandboxieIni.md) ページで説明されているように、Sandboxie は構成ファイルを最初に Windows フォルダーで、次に Sandboxie インストール フォルダーで探します。保護は Windows フォルダーにある構成ファイルに適用する必要があります。

保護が Sandboxie インストール フォルダーの構成ファイルに適用されている場合、攻撃者が Windows フォルダーに空の構成ファイルを作成する可能性があります。これにより、次に Sandboxie が構成を読み取るときに保護が事実上無効になります。これは、Sandboxie が新しい空の構成ファイルの使用に切り替わり、そのファイルに対して保護がアクティブになっていないために発生します。

**構成ファイルへのアクセス:** [Sandboxie Ini](SandboxieIni.md) 構成ファイルのアクセス許可を調整し、SYSTEM アカウントのみに書き込みアクセスを許可します。他のユーザー アカウントは引き続き構成を読み取れる必要があるため、読み取りアクセスはユーザー グループ **Authenticated Users** または **Everyone** に許可する必要があります。
