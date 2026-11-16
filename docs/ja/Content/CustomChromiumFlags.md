# Custom Chromium Flags

_CustomChromiumFlags_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、v1.14.2 / 5.69.2 以降で利用できます。この設定により、サンドボックス内で起動されたときに Chromium ベースのブラウザーに追加のコマンド ライン フラグを渡すことができます。Sandboxie はこれらのフラグをブラウザーの起動コマンド ラインに自動的に挿入し、サンドボックス化された環境内での互換性と機能を強化するためにブラウザーの動作をきめ細かく制御できるようにします。

## 使用法

```ini
[DefaultBox]

CustomChromiumFlags=--disable-features=PrintCompositorLPAC --disable-gpu
```

## 構文

```ini
CustomChromiumFlags=--disable-features=PrintCompositorLPAC [<flag 1> <flag 2> ...]
```

## 技術的な詳細

`CustomChromiumFlags` が構成されている場合、Sandboxie はプロセスの初期化中に、Chromium ベースのブラウザーとして識別されたアプリケーションのコマンド ラインを変更します:

1. **ブラウザーの検出**: この設定は、[`SpecialImage`](SpecialImage.md) 構成または自動検出[^1]を通じて Chrome として分類されたアプリケーションにのみ適用されます。

2. **コマンド ラインの挿入**: カーネルの初期化中に、Sandboxie はプロセス パラメーターを傍受し、実行可能ファイルのパスと既存の引数の間にカスタム フラグ[^7]を挿入してコマンド ラインを再構築します[^2]。

3. **子プロセスのフィルタリング**: フラグはメインのブラウザー プロセスにのみ追加され、`--type=` パラメーターを含む子プロセスには追加されません。これにより、重複や潜在的な競合を防ぎます[^3]。

## 既定の構成

Sandboxie には、ブラウザーの互換性を確保するための既定値が含まれています:

```ini
CustomChromiumFlags=--disable-features=PrintCompositorLPAC
```

この既定のフラグは、サンドボックス化された環境で互換性の問題を引き起こす可能性がある Print Compositor LPAC (Low Privilege App Container) 機能を無効にします[^4]。

## 使用例

- **基本的な GPU アクセラレーションの無効化**:
  ```ini
  CustomChromiumFlags=--disable-features=PrintCompositorLPAC --disable-gpu
  ```

- **複数のパフォーマンス フラグ**:
  ```ini
  CustomChromiumFlags=--disable-features=PrintCompositorLPAC --no-sandbox --disable-web-security
  ```

- **デバッグ オプション**:
  ```ini
  CustomChromiumFlags=--disable-features=PrintCompositorLPAC --enable-logging --log-level=0
  ```

## セキュリティへの影響

- **ブラウザーの互換性**: 既定の `PrintCompositorLPAC` フラグは、印刷関連のクラッシュを防ぎ、サンドボックス内での安定したブラウザー動作を確保します
- **フラグの検証**: 一部のフラグはサンドボックスのセキュリティやブラウザーの安定性を損なう可能性があるため、ユーザーはカスタム フラグを慎重に検証する必要があります
- **自動適用**: この設定は、手動で構成されたか自動的に検出されたかに関係なく、Chrome ブラウザーとして定義されたすべてのアプリケーションに自動的に適用されます

## 実装に関する注意

この設定は、Sandboxie が Chromium ベースのブラウザーを検出したときに DLL の初期化中に処理されます。システムは次のことを行います:

- `CustomChromiumFlags` キーを使用して `SbieApi_QueryConfAsIs` で構成を照会します[^5]
- カスタム フラグに対応するために、展開されたコマンド ライン用の追加メモリを割り当てます
- 実行可能ファイルのパスをコピーし、カスタム フラグを挿入し、残りの引数を追加してコマンド ラインを再構築します[^6]
- 変更されたコマンド ラインをアプリケーションに返すために `GetCommandLineW` および `GetCommandLineA` 関数をフックします

## ブラウザーのサポート

この設定は、次のものを含むすべての Chromium ベースのブラウザーで動作します:
- Google Chrome
- Microsoft Edge (Chromium)
- Brave Browser
- Opera
- Vivaldi
- Chromium エンジン上に構築されたその他のブラウザー

## 関連する設定

- [SpecialImage](SpecialImage.md) - アプリケーションを Chromium ブラウザーとして分類するために使用されます

関連する Sandboxie Plus 設定: UI で直接公開されていません (既定値を自動的に使用します)

[^1]: `dllmain.c` でのブラウザー検出: アプリケーションは `SpecialImage` 構成システムを通じて `DLL_IMAGE_GOOGLE_CHROME` として分類され、ブラウザーの実行可能ファイルを専用の処理のために Chrome イメージ タイプにマップします。

[^2]: `kernel.c` でのコマンド ライン再構築: システムは `SbieDll_FindArgumentEnd` を呼び出して実行可能ファイルのパスと引数の境界を特定し、展開されたメモリを割り当て、挿入されたフラグでコマンド ラインを再構築します。

[^3]: `kernel.c` での子プロセス フィルタリング: 条件 `!wcsstr(ProcessParms->CommandLine.Buffer, L" --type=")` は、メインのブラウザー プロセスのみがカスタム フラグを受け取り、レンダラーおよびユーティリティ プロセスを除外することを保証します。

[^4]: `Templates.ini` での既定の構成: 既定の `--disable-features=PrintCompositorLPAC` フラグは、サンドボックス化された環境でブラウザーの不安定性を引き起こす可能性がある Low Privilege App Container の印刷問題を防ぎます。

[^5]: `kernel.c` での構成の照会: `SbieApi_QueryConfAsIs(NULL, L"CustomChromiumFlags", 0, CustomChromiumFlags, ARRAYSIZE(CustomChromiumFlags))` はカーネルの初期化中に設定値を取得します。

[^6]: `kernel.c` でのコマンド ラインの変更: システムは元の実行可能ファイルのパスをコピーし、カスタム フラグを適切な間隔で追加し、残りの引数を連結して変更されたコマンド ラインを作成します。

[^7]: Chromium コマンド ライン スイッチのリスト - `https://peter.sh/experiments/chromium-command-line-switches/`
