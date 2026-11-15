# Special Image Classification

_SpecialImage_ は、サンドボックス化されたプロセスの初期互換性分類を選択する [Sandboxie Ini](SandboxieIni.md) 設定です。結果として得られるイメージ タイプは、選択されたプロセス作成、ファイル処理、および GUI 互換性パスによって参照されます。これはサンドボックスのセキュリティ レベル、トークン タイプ、または分離モードではなく、カテゴリを割り当てても、そのカテゴリ内のすべてのアプリケーションに対して均一な動作のセットが保証されるわけではありません。

## 構文

```ini
[DefaultBox]
SpecialImage=chrome,mybrowser.exe
SpecialImage=firefox,anotherbrowser.exe
SpecialImage=mail,myclient.exe
```

形式は `SpecialImage=category,program.exe` です。サポートされるカテゴリは `chrome`、`firefox`、`thunderbird`、`browser`、`mail`、`plugin`、および `none` です。

Sandboxie は `program.exe` を実行可能ファイルのベース名と正確に、大文字と小文字を区別せずに比較します。有効な構成内で最初に一致する _SpecialImage_ エントリが優先されます。この専用形式は汎用のプログラム名プレフィックス ルールを使用しません。ワイルドカード実行可能ファイル名、ProcessGroup セレクター、および否定セレクターはここではサポートされません。

エントリはボックスに直接構成することも、適用可能なテンプレートによって提供することもできます。Sandboxie の既定の `SpecialImages` テンプレートは、既知のブラウザーおよびメール アプリケーションのマッピングを提供します。

アプリケーションがカテゴリに関連付けられた互換性処理を必要とするが、既存のマッピングまたは自動検出で認識されない場合、手動分類が役立つことがあります。最初に一致するエントリが優先されるため、まず既存のマッピングを確認してください。

## サポートされるカテゴリ

- `chrome` は Chrome/Chromium 互換性イメージ タイプを選択します。これは一部の Electron ベースのアプリケーションにも使用されます。
- `firefox` は Firefox 互換性イメージ タイプを選択します。
- `thunderbird` は Thunderbird メール イメージ タイプを選択します。
- `browser` はその他の Web ブラウザー イメージ タイプを選択します。
- `mail` はその他のメール クライアント イメージ タイプを選択します。
- `plugin` はプラグイン コンテナ イメージ タイプを選択します。
- `none` は初期フォールバック分類を抑制します。ただし[以下](#the-none-category)で説明する後続の検出が対象となります。

これらの名前は互換性カテゴリを識別するものであり、カテゴリに割り当てられたすべてのアプリケーションが同一のファイル、GUI、またはトークンの扱いを受けることを約束するものではありません。

## 分類順序

プロセスの初期化中、Sandboxie は次の順序で初期イメージ分類を決定します:

1. 最初に一致する _SpecialImage_ エントリ (存在する場合)。
2. エントリが一致しなかった場合、既知の実行可能ファイル名の組み込み分類。
3. イメージがまだ未分類で、[Use Electron Detection](UseElectronDetection.md) が有効な場合の、初期の Electron/Chromium ファイル レイアウト ヒューリスティック。

_UseElectronDetection_ は既定で有効です。これらはフォールバック段階であり、すべてのプロセスに対して必ず実行されるチェックではありません。分類は主にそのサンドボックス化されたプロセスの互換性固有の動作を選択します。

## 分類の使用方法

イメージ タイプは特定の互換性パスによってチェックされます。それらの他の条件と設定も依然として重要です。例:

- Chromium 分類は、該当するコマンド ラインに構成された `CustomChromiumFlags` を適用する前にチェックされます。また、条件付きの Chrome Secure Preferences ファイル処理パス、および選択されたウィンドウ ステーションまたはデスクトップ互換性フォールバックによってもチェックされます。
- Firefox 分類は、選択されたウィンドウ ステーションおよびデスクトップ フォールバック、プロセス作成の互換性ケース、および実行可能ファイルのファイル オープン ワークアラウンドによってチェックされます。これらは特定のケースであり、Firefox 分類されたすべてのプロセスに対する一般的なアクセス許可の変更ではありません。
- メール分類は、選択されたメール プログラム チェックが `OpenFilePath` 構成を参照するようにすることができますが、Chrome、Firefox、およびその他のブラウザー分類はそのメール プログラム パスから明示的に除外されます。これはカテゴリ全体のファイルシステム アクセス許可を確立するものではありません。
- プラグイン分類は、子プロセスを作成するときに使用されるトークン引数に影響を与えることがあります。現在のプラグイン プロセスのトークンを削除したり、そのプロセスをトークンなしにしたりするものではありません。

## 既定のマッピング

既定の `Template_SpecialImages` 構成は、既知の Chromium ファミリおよび Firefox ファミリのブラウザー、その他のブラウザー、メール クライアント、および一部の Electron/Chromium ベースのアプリケーションのマッピングを提供します。維持されているリストはリリース間で変更されることがあります。上記の例は例示的なもので、テンプレート マッピングの完全なリストではありません。プログラムのカテゴリは、単にその製品名によってではなく、実際に一致するエントリによって決定されます。

## `none` カテゴリ {#the-none-category}

```ini
[DefaultBox]
SpecialImage=none,example.exe
```

`none` はその実行可能ファイルに対する初期の組み込みおよび早期 Electron/Chromium フォールバック分類を抑制します。永続的な「決して分類しない」状態を確立するものではありません。後続の動的検出がプロセスを分類する可能性があります。

## 動的検出

`DynamicImageDetection` は既定で有効で、早期の _UseElectronDetection_ ヒューリスティックとは別個です。プロセスが未分類のままの場合、Sandboxie のローダーは後で特徴的なモジュールが読み込まれたときに分類を割り当てることができます。これは初期の _SpecialImage=none_ 一致の後でも発生する可能性があります。

## 変更の適用

初期分類と動的検出設定は、各サンドボックス化されたプロセスに対して初期化されます。_SpecialImage_、_UseElectronDetection_、または `DynamicImageDetection` を変更した後は、影響を受けるアプリケーションとその関連する子プロセスの新しいインスタンスを開始して、新しい構成を使用するようにしてください。Windows の再起動や Sandboxie サービスの再起動は通常必要ありません。

_SpecialImage_ エントリは主にテンプレートまたは手動の INI 構成を通じて管理されます。SandMan はそれらの専用チェックボックスを提供しません。SandMan は **Sandbox Options > Various Options > Compatibility** の下に _UseElectronDetection_ チェックボックスを提供します。

_SpecialImage_ は Sandboxie Plus 0.5.3a / Classic 5.45.2 で導入されました。

## 関連設定

- [Use Electron Detection](UseElectronDetection.md) は、プロセスがまだ未分類のときに使用される早期の Electron/Chromium ヒューリスティックを制御します。
- [Custom Chromium Flags](CustomChromiumFlags.md) は Chromium 分類されたプロセスに関連します。
- [Drop Child Process Token](DropChildProcessToken.md) は別個の子プロセス トークン コントロールです。`SpecialImage=plugin` は現在のプロセスのトークンをドロップしません。
