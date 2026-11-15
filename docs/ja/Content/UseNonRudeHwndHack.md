# Use Non-Rude HWND Hack

_UseNonRudeHwndHack_ は v1.16.0 / 5.71.0 以降で使用可能な [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。この設定は NonRudeHWND プロパティの互換性ハックを有効にして、サンドボックス化されたアプリケーションでの全画面サポートを改善します。

使用方法:

```ini
[DefaultBox]

UseNonRudeHwndHack=y
```

## 目的

NonRudeHWND プロパティは、アプリケーションがその全画面動作とタスクバーとの相互作用をシステムに通知するために設定できる Windows ウィンドウ プロパティです。一部のアプリケーション、特にゲームやメディア プレーヤーは、不要なタスクバーの干渉なしに適切な全画面表示を確実にするためにこのプロパティを設定します。

サンドボックス化されたアプリケーションが `SetProp()` を通じて NonRudeHWND プロパティを設定しようとすると、Sandboxie のセキュリティ モデルは通常、分離を維持するためにこれらのプロパティ変更をブロックまたはフィルター処理します。ただし、これによりこのプロパティに依存するアプリケーションの全画面機能が壊れることがあります。

## 技術的な詳細

この設定は、Sandboxie の GUI プロパティ処理コードの `Gui_NonRudeHWND_Hack` 変数を制御します[^1]。有効な場合、Sandboxie は `SetPropW()` および `SetPropA()` 関数への呼び出しを傍受し、NonRudeHWND プロパティの設定を具体的に成功させ、実際に操作を実行せずに `TRUE` を返します[^2]。

ハックは次のように機能します:

1. プロパティ名「NonRudeHWND」での `SetProp` 呼び出しを傍受します[^3]
2. この特定のプロパティが検出されると、直ちに成功を返します[^4]
3. アプリケーションにプロパティが正しく設定されたと信じさせます
4. これにより、サンドボックスのセキュリティを損なうことなく適切な全画面動作が可能になります

## 既定の動作

既定では、この設定は:
- アプリ コンパートメント モードで実行されて**いない**場合は**有効** (`y`)
- アプリ コンパートメント モードで実行されている場合は**無効** (`n`)

ロジックは `!Dll_CompartmentMode`[^5] です。つまり、コンパートメント モードがアクティブでない限り有効です。

## 重要な注意事項

- この設定は Sandboxie が NonRudeHWND プロパティをどのように処理するかにのみ影響します。Windows の実際のタスクバー動作を変更するものではありません。
- このハックはサンドボックスのセキュリティを維持しつつ、アプリケーションが全画面モードで正しく機能できるようにします。

## 関連する問題

この設定は、特に GitHub イシュー [#4761](https://github.com/sandboxie-plus/Sandboxie/issues/4761) として参照される全画面互換性の問題に対処するために導入されました。

[^1]: **ソース**: guiprop.c: `static BOOLEAN Gui_NonRudeHWND_Hack = FALSE;`

[^2]: **ソース**: guiprop.c: `Gui_SetPropW()` および `Gui_SetPropA()` 関数は NonRudeHWND プロパティをチェックし、ハックが有効な場合は直ちに `TRUE` を返します。

[^3]: **ソース**: guiprop.c: `if (_wcsicmp(lpString, L"NonRudeHWND") == 0)` および 537 行目: `if (strcmp(lpString, "NonRudeHWND") == 0)`

[^4]: **ソース**: guiprop.c: `return TRUE;` - この関数は実際にプロパティを設定せずに成功を返します。

[^5]: **ソース**: guiprop.c: `Gui_NonRudeHWND_Hack = SbieApi_QueryConfBool(NULL, L"UseNonRudeHwndHack", !Dll_CompartmentMode);`
