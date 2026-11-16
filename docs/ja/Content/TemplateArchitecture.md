# テンプレート アーキテクチャ

Sandboxie テンプレートは、主に [Sandboxie 構成](SandboxieIni.md)エントリの再利用可能なコレクションです。テンプレートを選択すると、その通常の設定が有効な構成の一部になります。選択によってそれらのエントリがサンドボックスの明示的な構成に恒久的にコピーされることはありません。テンプレートの表示と検出データは、Sandboxie が実行時に適用するルールとは別個です。

例:

```ini
[Template_Example]
Tmpl.Title=Example
Tmpl.Class=Misc
OpenFilePath=C:\Example\*
OpenIpcPath=\RPC Control\Example

[DefaultBox]
Template=Example
```

ここで `OpenFilePath` と `OpenIpcPath` は `DefaultBox` に構成を提供します。`Tmpl.*` エントリはテンプレートを説明するものであり、サンドボックス アクセス ルールではありません。

## 公式およびローカル テンプレート

公式テンプレートは Sandboxie インストールの `Templates.ini` に同梱されています。既存の定義の参照としてそのファイルを使用しますが、カスタム テンプレートはストック ファイルを編集するのではなく [`Sandboxie.ini`](SandboxieIni.md) に配置してください。

公式テンプレート セクションは通常 `[Template_Name]` を使用します。ユーザー作成のテンプレートは慣例的に `[Template_Local_Name]` を使用し、UI で区別され、将来の公式名との衝突を回避します。

```ini
[Template_Local_ExampleSoft]
Tmpl.Title=ExampleSoft
Tmpl.Class=Local
OpenWinClass=ExampleSoft_WindowClass
OpenIpcPath=*\BaseNamedObjects*\ExampleSoft_*
```

ローカル テンプレートは公式テンプレートと同様に手動で有効にできます。`Template_Local_` は命名と表示の慣例であり、別個のランタイム継承メカニズムではありません。[アプリケーション設定](ApplicationsSettings.md#local)ページは、従来のローカル テンプレート UI についても説明しています。

## テンプレートの選択 {#selecting-templates}

サンドボックスのテンプレートを有効にするには、`Template=` の後にその名前を指定します。

```ini
[DefaultBox]
Template=Example
```

セクションには複数の `Template=` エントリを含めることができます。Sandboxie は選択された各テンプレートを処理し、その設定をそのセクションの有効な構成にマージします。テンプレートはグローバルに選択することもできます。

```ini
[GlobalSettings]
Template=Example
```

グローバル選択は、グローバルな有効構成に設定を提供します。すべてのサンドボックス セクションにテンプレート定義の別個の恒久的なコピーを作成するわけではありません。

`TemplateReject=Name` は `[GlobalSettings]` に属します。検出されたテンプレートが保留中の推奨として残るのではなく、拒否済み/構成済みとして扱われるように、互換性テンプレートの選択状態を記録します。この目的のために個々のサンドボックス セクション内の値は参照されません。明示的に選択された `Template=Name` から設定を差し引くものではありません。通常のテンプレート マージはその選択に依然として適用されます。

## テンプレートのマージ方法

構成の読み込み時に、Sandboxie は最初に `GlobalSettings` で選択されたテンプレートを処理し、次に `[DefaultTemplates]` をグローバルな有効構成に適用し、次に各サンドボックスによって選択されたテンプレートを処理します。選択されたテンプレート内の通常の設定は、宛先の有効な構成にマージされます。`Tmpl.*` メタデータはこのランタイム マージによってスキップされます。

明示的なエントリとテンプレート由来のエントリは、有効な構成内で共存できます。Sandboxie はどのエントリがテンプレートから来たかを記録し、通常、直接エントリが後でマージされたエントリより前に来ます。競合するエントリの効果は依然としてそれらを消費するサブシステムに依存します。構成ソースの順序は普遍的な優先順位ルールではありません。リソース ルールの競合については、[ルールの特異性](../PlusContent/RuleSpecificity.md)を参照してください。

## 既定のテンプレート

同梱の `Templates.ini` の `[DefaultTemplates]` は、グローバルな有効構成に自動的にマージされる組み込みテンプレートをリストします。これらは、ユーザーがボックスのために個別に選択することなく、ベースライン設定を提供します。現在のリストには `RpcPortBindings`、`SpecialImages`、`COM`、`WindowsExplorer`、`ThirdPartyIsolation`、`BlockSoftwareUpdaters`、`BlockWinRM`、`OpenWinInetCache`、`CredentialUIBroker`、および `MSI_Lite` が含まれます。同梱のリストはリリース間で変更される可能性があります。既定のテンプレートは不変のポリシーではありません。

この自動マージは、特定のサンドボックスのためにオプションのアプリケーション互換性テンプレートを有効にすることとは異なります。

## テンプレート変数と内部セクション

`[TemplateSettings]` は、共有 `%Tmpl.*%` 変数定義と関連するメタデータ インフラストラクチャを提供します。テンプレートは、[展開可能な変数](ExpandableVariables.md#template-variables)で説明されているように、これらの変数を使用できます。`[TemplateSettings]` は `Template=TemplateSettings` で選択される互換性テンプレートではありません。カスタム テンプレートはそれをコピーまたは編集する必要はありません。

名前が `Template` で始まる他のセクションも通常のアプリ テンプレートではありません。`TemplateDefaultPaths`、`TemplateSModPaths`、`TemplatePModPaths`、および `TemplateAppCPaths` は、別個の読み込みパスを通じてランタイム サブシステムに組み込みパス ルールを提供します。アプリ テンプレート リストを通じてそれらを有効にしたり、`Template=Name` がそれらを制御すると仮定したりしないでください。

## テンプレート メタデータ {#template-metadata}

`Tmpl.` で始まるエントリは、テンプレートを説明したり、いつ役立つかを検出するのに役立ちます。テンプレート ルールがランタイム構成にマージされるときにスキップされます。

| エントリ | 目的 |
| --- | --- |
| `Tmpl.Title` | 表示タイトル |
| `Tmpl.Class` | UI カテゴリ |
| `Tmpl.Url` | 関連ソフトウェアまたはベンダーの URL |
| `Tmpl.Comment` | 説明またはコメント |
| `Tmpl.Hide` | 通常の表示からテンプレートを隠します |
| `Tmpl.Entry` | 特殊な互換性または既知の競合エントリ メタデータ |
| `Tmpl.Version` | テンプレート/構成メタデータ バージョン |
| `Tmpl.Scan` | 互換性検出モード |
| `Tmpl.Scan*` | テンプレートが適用される可能性があるかどうかを検出するために使用される証拠 |
| `Tmpl.ScanScript` | SandMan の最新チェッカーにおけるスクリプト化された検出 |

これらのフィールドのほとんどは、アクセス ルールとしてドライバーによってではなく、テンプレートの表示または互換性検出コードによって使用されます。

## テンプレート検出 {#template-discovery}

テンプレート検出は、Sandboxie または SandMan が互換性テンプレートを提案すべきかどうかを決定します。それ自体はテンプレートのサンドボックス ルールを強制しません。それらのルールは、テンプレートが既定テンプレート メカニズムを通じて選択または適用されたときにのみ、有効な構成に入ります。

`Tmpl.Scan` は 1 つ以上の証拠モードを選択します。

- `i` は `OpenIpcPath` と `Tmpl.ScanIpc` 証拠を使用して IPC オブジェクトをチェックします。`i` が選択されていない限り、`OpenIpcPath` エントリだけではスキャンを意味しません。
- `w` は `OpenWinClass` と `Tmpl.ScanWinClass` 証拠を使用して既知のウィンドウ クラスをチェックします。
- `s` は `Tmpl.ScanService`、`Tmpl.ScanProduct`、`Tmpl.ScanKey`、および `Tmpl.ScanFile` などのソフトウェア存在証拠をチェックします。これらはサービス、インストール済み製品、レジストリ キー、またはファイルを示すことができます。`s` はサービスに限定されません。

SandMan の最新互換性チェッカーは、スキャン スクリプトが存在する場合、最初に `Tmpl.ScanScript` を評価します。古い C++ フォールバック スキャナーは代わりに `Tmpl.Scan` 証拠フィールドを使用し、そのスクリプト パスを実行しません。最新チェッカーによる自動スキャンは `Local_` テンプレートをスキップします。ローカル テンプレートは手動選択のために引き続き利用できます。

## ソフトウェア アップデーターのブロック {#software-updater-blocking}

同梱の `[DefaultTemplates]` リストには `Template=BlockSoftwareUpdaters` が含まれます。その `[Template_BlockSoftwareUpdaters]` セクションは、維持された `SoftwareUpdater` パターンを有効な構成に提供します。この既定のテンプレートはすでに含まれています。ユーザーはそれらの定義を取得するためにオプションのアプリ テンプレートとしてそれを選択する必要はありません。

維持されたルールは、発信元のアプリケーション イメージの後にアップデーターの実行可能ファイルまたはパス パターンを使用します。

```ini
SoftwareUpdater=starting_image.exe,updater_path\updater_image.exe

SoftwareUpdater=firefox.exe,*\mozilla firefox\updater.exe
SoftwareUpdater=msedge.exe,*\Microsoft\EdgeUpdate\MicrosoftEdgeUpdate.exe
```

`BlockSoftwareUpdaters` は別個のランタイム ゲートで、既定 `y` で照会されます。ゲートが有効で、子プロセスが `SoftwareUpdater` ルールに一致する場合、Sandboxie は `ERROR_ACCESS_DENIED` でその作成をブロックし、モニター パスに **Blocked start of an updater** を報告します。`BlockSoftwareUpdaters=n` の場合、既定のテンプレートとそのパターンは依然として有効な構成に存在する場合がありますが、このプロセス作成ブロッカーはそれらを強制しません。

`BlockSoftwareUpdaters` は 0.5.5 で導入され、1.0.11 で削除され、1.14.4 で再導入されました。現在のランタイムでアクティブです。このメカニズムは一致するアップデーター プロセスの作成をカバーします。すべてのソフトウェア更新、インストーラー、またはネットワーク ベースの更新パスがブロックされることを保証するものではありません。

## SandMan と変更の適用

SandMan では、テンプレートは **Sandbox Options > App Templates** の下にタイトルとカテゴリ別に表示されます。サンドボックスのためにいずれかを有効にすることは、手動の `Template=` 編集を必要とせずにその構成を選択することに対応します。

テンプレートを有効化、無効化、または編集した後は、プロセス初期化中にキャッシュされた設定が一貫して再構築されるように、影響を受けるサンドボックス化されたプロセスを再起動してください。テンプレート由来の設定はそれぞれ寿命が異なります。テンプレートの変更がすべての実行中プロセスを即座に更新すると仮定すべきではありません。Windows の再起動、ドライバーの再起動、またはサービスの再起動は、通常は必要ありません。

## 関連ページ

- [Sandboxie Ini](SandboxieIni.md)
- [アプリケーション設定](ApplicationsSettings.md)
- [展開可能な変数](ExpandableVariables.md)
- [ルールの特異性](../PlusContent/RuleSpecificity.md)
