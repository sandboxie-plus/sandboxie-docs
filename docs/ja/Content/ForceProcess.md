# Force Process

_ForceProcess_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、一致するプログラムを特定のサンドボックスで自動的に開始します。例:

```ini
[DefaultBox]
ForceProcess=iexplore.exe
ForceProcess=firefox.exe

[MailBox]
ForceProcess=outlook.exe
ForceProcess=cl?cke?.exe
```

最初の 2 つのエントリは Internet Explorer と Firefox を `DefaultBox` に強制します。他のエントリは Outlook および `clicker.exe` や `clicked.exe` などの実行可能ファイル名を `MailBox` に強制します。

`*` を含まないエントリは実行可能ファイル名に対して大文字と小文字を区別せずに照合され、`?` を使用して 1 文字に一致させることができます。現在のランタイムでは、`*` を含むエントリは代わりに、完全な正規化された実行可能ファイル パスに対する大文字と小文字を区別しないパターンとして照合されます。したがって、`App*.exe` のような名前のみのパターンは、古い名前のみのマッチングと同じセマンティクスを持ちません。十分な場合は、正確な実行可能ファイル名が好ましいです。

_ForceProcess_ は、プログラムがサンドボックスの外で開始された場合にのみ適用されます。プログラムがサンドボックスで明示的に開始された場合、または既にサンドボックス化されたプログラムによって起動された場合は再適用されません。

## イマーシブ アプリケーション

既定では、通常の _ForceProcess_ または [ForceFolder](ForceFolder.md) ルールがサンドボックスを選択した後、Sandboxie は結果のプロセスをイマーシブ/AppContainer アプリケーションとして識別すると、その選択を破棄します。以下のグローバル設定は、そのようなプロセスに対してこれらの強制ルールを有効にします:

```ini
[GlobalSettings]
AllowForceImmersive=y
```

`AllowForceImmersive` は既定で `n` であり、サンドボックスごとの設定ではなく、専用の SandMan コントロールもありません。これを有効にしても、すべての AppContainer、UWP、またはその他のイマーシブ アプリケーションとの互換性が保証されるわけではありません。結果として得られる起動動作と制限については [Force Folder](ForceFolder.md#immersive-applications) を参照してください。

## ルールの順序

Sandboxie は _ForceProcess_ をチェックする前に、実行可能ファイルのディレクトリを _ForceFolder_ に対してチェックします。作業ディレクトリおよびドキュメント引数の _ForceFolder_ チェックは、_ForceProcess_ の後に実行されるため、_ForceFolder_ がすべてのケースで無条件に優先されるわけではありません。

## ユーザー インターフェイス

SandMan で **Sandbox Options > Program Control > Force Programs** を開き、**Force Program** を使用してリストを維持します。同じページには **Force Children**、**Force Folder**、**Remove**、**Show Templates** コントロールもあります。

Sandboxie Control Classic は、関連する [Sandbox Settings > Program Start > Forced Programs](ProgramStartSettings.md#forced-programs) ページを提供します。

## バージョン履歴

`AllowForceImmersive` は Sandboxie Plus 1.16.0 / Classic 5.71.0 で追加されました。_ForceProcess_ は現在のバージョン メタデータより前から存在し、そこに導入バージョンは記録されていません。

## 関連ページ

- [Force Folder](ForceFolder.md)
- [Program Settings](ProgramSettings.md#page-1)
- [Sandboxie Ini](SandboxieIni.md)
