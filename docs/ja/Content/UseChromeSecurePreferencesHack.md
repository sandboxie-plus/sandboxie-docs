# Use Chrome Secure Preferences Hack

_UseChromeSecurePreferencesHack_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Chrome および一部の関連アプリケーションで使用される Secure Preferences ファイルに対する Sandboxie の互換性ワークアラウンドを有効にします。

```ini
[DefaultBox]
UseChromeSecurePreferencesHack=y
```

この設定はグローバルに、または特定の実行可能ファイルに対して無効にできます:

```ini
UseChromeSecurePreferencesHack=n
UseChromeSecurePreferencesHack=browser.exe,n
```

## スコープと既定

ワークアラウンドは、Sandboxie が内部的に Chrome または Chromium アプリケーションとして分類するプロセスに対してのみ既定で有効です。その分類は [`SpecialImage=chrome`](SpecialImage.md)、バンドルされたアプリケーション マッピング、または互換性のある [Electron/Chromium 検出](UseElectronDetection.md) から得られます。正確な `chrome.exe` ファイル名に限定されません。

対象となるプロセスの場合:

- 設定が存在しない場合、ワークアラウンドは有効です。
- `UseChromeSecurePreferencesHack=n` はそれを無効にします。
- `UseChromeSecurePreferencesHack=y` はそれを明示的に有効にします。

この設定は無関係なプロセス分類では非アクティブです。分類だけでは、アプリケーションが Chrome の Secure Preferences 形式を使用すること、またはこのワークアラウンドの恩恵を受けることも保証されません。

## 互換性動作

現在のワークアラウンドは、対象となるプロセスに対して 3 つの動作を組み合わせます。

### Secure Preferences の移行

プロセスが `Secure Preferences` という名前のホスト ファイルにアクセスするとき、Sandboxie は要求をそのコピーオンライト [ファイル移行](FileMigrationSettings.md)パスに送ることができます。その後、互換性の変更は、意図的にホスト ファイルを上書きするのではなく、サンドボックス コピーに適用されます。

通常の Sandboxie のファイルおよびパスのルールは依然として適用されます。直接または通常パスのルールは、このワークアラウンドで使用される移行パスを変更またはバイパスすることがあります。

### 暗号化ハッシュ エントリ

サンドボックス コピーを作成するとき、Sandboxie は名前が `_encrypted_hash` で終わる JSON メンバーを削除できます。これは復号ではなく、保護された値を回復するものでもありません。

現在の実装では、この変換されたコピーのパスは 16 MiB 未満の空でない一致ファイルに適用されます。より大きなファイル、または変換できないファイルは、代わりに通常の移行動作を使用することがあります。ワークアラウンドは、将来のすべての Chromium 設定形式に対する保証として扱うべきではありません。

### ドメイン メンバー互換性クエリ

対象となるプロセスの場合、ワークアラウンドは関連する `IsOS(OS_DOMAINMEMBER)` 互換性クエリも true を報告させます。これはそのクエリに対するアプリケーションの見え方に影響しますが、コンピューターの Windows ドメイン メンバーシップを変更するものではありません。

Sandboxie プロジェクトの根拠は、移行および調整されたサンドボックス コピーと組み合わせて、Chrome の Secure Preferences 検証動作に影響を与えることです。Sandboxie 分離を無効にするものではありません。

## 制限事項

プロジェクトで文書化されている利点は、ブラウザー設定および拡張機能の互換性に限定されています。このワークアラウンドは、次のような保護されたホスト データへのアクセスを提供しません:

- 資格情報。
- Cookie。
- 保存されたパスワード。
- Application-Bound Encryption のシークレットまたはキー。

Chrome または Chromium として分類されるアプリケーションは、ファイル形式とセキュリティ ポリシーが異なることがあります。Chrome で確認された動作が Edge、Brave、すべての Chromium 派生製品、またはすべての Electron アプリケーションに同一に適用されると仮定すべきではありません。

## テンプレートとの相互作用

バンドルされた `Chromium_Elevation` テンプレートは明示的に次を設定します:

```ini
UseChromeSecurePreferencesHack=n
```

そのテンプレートは、別個の Chromium 昇格互換性メカニズムが使用される場所でこのワークアラウンドを無効にします。昇格メカニズムは独立しており、この設定によって有効になるものではありません。

バンドルされた `Edge_Fix` テンプレートには、Edge の `Secure Preferences` ファイル用の `NormalFilePath` ルールが含まれています。そのような直接または通常パスのルールは、通常のサンドボックス移行および変換パスに到達するかどうかを変更することがあります。_UseChromeSecurePreferencesHack_ を直接無効にするものではありません。

## 変更の適用

設定とアプリケーション分類はプロセスの初期化中に確立されます。構成を変更した後は、影響を受けるブラウザーまたはアプリケーションとその関連する子プロセスを再起動してください。

この設定には SandMan または Sandboxie Control Classic に専用のコントロールはありません。`Sandboxie.ini` で、INI エディターを通じて、または適用可能なテンプレートを通じて手動で構成してください。

## バージョン履歴

_UseChromeSecurePreferencesHack_ は Sandboxie Plus 1.18.0 / Classic 5.73.0 で公に導入されました。現在の実装は同じ全体的な互換性アプローチを保持しています。

## 関連構成

- [Special Image Classification](SpecialImage.md)
- [Use Electron Detection](UseElectronDetection.md)
- [File Migration Settings](FileMigrationSettings.md)
- [Sandboxie Ini](SandboxieIni.md)
