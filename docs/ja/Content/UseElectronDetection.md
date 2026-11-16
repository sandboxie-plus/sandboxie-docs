# Use Electron Detection

_UseElectronDetection_ は Sandboxie Plus 1.17.4 以降で使用可能な [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。一致する Chromium 形式のアプリケーションを Sandboxie の互換性処理のために Chrome として分類できる初期ヒューリスティックを有効にします。

```ini
[DefaultBox]
UseElectronDetection=y
```

この設定は既定で有効です。初期ファイル レイアウト ヒューリスティックを無効にするには _n_ に設定します:

```ini
[DefaultBox]
UseElectronDetection=n
```

## 検出動作

ヒューリスティックは初期プロセス初期化中に評価されます。Electron メタデータを解析せず、WebView2 を直接検出しません。代わりに、アプリケーションの実行可能ファイルの近くに Chromium 形式のファイル レイアウトがあるかどうかをチェックします。

現在の実装は、実行可能ファイル ディレクトリとその `app` および `resources` サブディレクトリで、特徴的なパッケージング ファイルをチェックします。これには次が含まれます:

- `chrome_100_percent.pak`
- `chrome_200_percent.pak`
- `resources.pak`
- `chrome_elf.dll`

現在、いずれか 1 つの候補への一致で十分です。これらのファイル名はヒューリスティックの動作を説明しますが、永続的なアプリケーション検出仕様として扱うべきではありません。

明示的な [SpecialImage](SpecialImage.md) 構成および組み込みイメージ分類は、このヒューリスティックの前に評価されます。自動検出は、プロセスがまだ別の分類を受け取っていない場合にのみ使用されます。明示的な分類を上書きしません。

プロセスが一致すると、Sandboxie はそのプロセスに対して既存の Chrome 指向のプロセス分類を使用します。この分類は、フック選択、コマンド ライン処理、デスクトップまたはウィンドウ ステーション互換性、トークン処理、および [Use Chrome Secure Preferences Hack](UseChromeSecurePreferencesHack.md) など、Chromium 関連の互換性処理に影響を与えることがあります。サンドボックス分離を無効にしたり、広範なホスト アクセスを付与したりするものではありません。

## 検出の制限

これはファイル レイアウト ヒューリスティックであり、正確な Electron 識別ではありません。Electron アプリケーションを見逃すことも、他の Chromium ベースのパッケージに一致することもあります。

特徴的なファイルは Electron に排他的ではないため、偽陽性が発生する可能性があります。CEF、NW.js、WebView2、または他の Chromium ベースのコンポーネントで構築されたアプリケーションは類似のレイアウトを使用することがありますが、特定の製品が一致することは保証されません。

偽陰性は次の場合に発生する可能性があります:

- アプリケーションが異なるパッケージングを使用している。
- 期待されるファイルの名前が変更されている。
- ファイルがチェック対象のディレクトリの外に保存されている。
- 関連する Chromium コンポーネントが実行時にのみ後で現れる。

_UseElectronDetection_ を無効にすると、この初期ファイル レイアウト チェックのみが無効になります。Sandboxie の独立した `DynamicImageDetection` メカニズムは、Chromium 関連のモジュールが読み込まれた場合、後でプロセスを分類することがあります。

分類はプロセスごとに別々に実行されます。子プロセスは、親プロセスのメモリ内分類を単に継承するのではなく、独自の分類ロジックを実行します。

## 変更の適用

この設定は初期プロセス初期化中に読み取られます。変更しても既に実行中のアプリケーションは再分類されません。設定を変更した後は、影響を受けるアプリケーションとその関連する子プロセスを再起動してください。SandMan 自体を再起動する必要はありません。

## Sandboxie Plus インターフェイス

この設定は次で使用できます:

**Sandbox Options > Various Options > Compatibility**

チェックボックスのラベルは **Use heuristics to identify Electron/Chromium based processes** です。既定でチェックされており、専用のツールチップはありません。クリアすると無効の上書きが書き込まれます。通常のチェック済み状態は有効な既定動作に依存します。

## 診断

Sandboxie には別個のコマンド ライン ベースの診断もあり、プロセスが Chromium ベースに見えるが Chrome 分類を持たない場合に `SBIE2189` を報告することがあります。この診断は _UseElectronDetection_ と同じアルゴリズムではなく、この設定がメッセージを直接発行するわけではありません。

ユーザーの確認後、トラブルシューターは影響を受ける実行可能ファイル用のイメージ修飾 `SpecialImage=chrome,<program>` エントリを追加することを提案することがあります。

## バージョン履歴

_UseElectronDetection_ は Sandboxie Plus 1.17.4 で導入され、既定で有効です。構成メタデータでは、同じリリースで削除された古い _UseElectronWorkaround_ 設定を置き換えました。古い設定は異なる互換性メカニズムを使用しており、_UseElectronDetection_ の別名ではありません。

## 関連構成

- [Sandboxie Ini](SandboxieIni.md)
- [Special Image Classification](SpecialImage.md)
- [Custom Chromium Flags](CustomChromiumFlags.md)
- `DynamicImageDetection`
