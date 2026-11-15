# サンドボックス デスクトップとウィンドウ ステーション

## 概要

Sandboxie は通常、すべてのサンドボックスに独自の永続的な Windows ウィンドウ ステーションとデスクトップを与えません。代わりに、GUI の初期化と互換性処理の間に一時的なダミー GUI オブジェクトと制御されたハンドル置換を使用します。通常のサンドボックス化された GUI プロセスは、専用のサンドボックスごとの Win32 デスクトップにとどまるのではなく、最終的に対話型ウィンドウ ステーションとデスクトップに接続します。

このページでは、そのアーキテクチャとそれに影響する 3 つの設定について説明します。

| 設定 | 既定 | スコープ | 現在の役割 |
| --- | --- | --- | --- |
| `OpenWndStation` | `n` | ボックス全体 | デスクトップ/ウィンドウ ステーション分離パスの広範な互換性緩和 |
| `UseSbieWndStation` | `y` | ボックス全体またはイメージ認識 | `CreateWindowStation` 失敗後のダミー ウィンドウ ステーション フォールバック |
| `UseSbieDeskHack` | `y` | ボックス全体またはイメージ認識 | ウィンドウ オブジェクト セキュリティと `CreateDesktop` 互換性の回避策 |

`OpenWndStation` はトークン構築、GUI 初期化、フック インストール、および Job Object UI 制限を変更します。2 つの `UseSbie*` 設定は代わりに、通常のモデル内でより狭い互換性フォールバックを提供します。

## Windows オブジェクト モデル

これらの設定に関連する Windows GUI オブジェクト階層は次のとおりです。

```text
セッション
  |
  +-- ウィンドウ ステーション
        |
        +-- デスクトップ
              |
              +-- ウィンドウ / GUI オブジェクト
```

プロセスはウィンドウ ステーションに関連付けられ、各 GUI スレッドはデスクトップに関連付けられます。対話型ウィンドウ ステーションは通常 `WinSta0` という名前で、そのステーションに属するデスクトップは対話型ユーザー インターフェイス要素を表示し、ユーザー入力を受け取ることができます。

## 通常の Sandboxie GUI 初期化

既定の設定:

```ini
OpenWndStation=n
```

Sandboxie は、この高レベルの流れを通じて GUI プロセスを初期化します。

```text
制限付きサンドボックス化されたプロセス
        |
        v
Sandboxie が SbieSvc を通じて GUI オブジェクトとハンドルを取得
        |
        v
一時的なダミー ウィンドウ ステーションとデスクトップのブートストラップ
        |
        v
最初の GUI 変換
        |
        v
Sandboxie が実際の対話型ウィンドウ ステーションと
デスクトップのハンドルを適用
        |
        v
通常のサンドボックス化された GUI 実行
```

主要なコンポーネントは異なる責任を持っています。

- SbieDll は GUI および API フックをインストールし、ブートストラップを調整し、選択されたハンドルを置換し、互換性フォールバックを実装します。
- SbieSvc とその GuiServer はダミー GUI オブジェクトを作成または取得し、プロセスのために適切なハンドルを複製し、関連する Job Object UI 制限を適用します。
- ドライバーはトークン構築と、このモデルに必要なトークン動作に参加します。
- 別個の Win32k フックおよびフィルター メカニズムが存在しますが、それらはこのページの 3 つの設定の主要な実装ではありません。

## ダミー ウィンドウ ステーション

Sandboxie のダミー ウィンドウ ステーションは、発明された疑似ハンドルではなく、実際の非対話型 Win32 ウィンドウ ステーション オブジェクトです。実際のデスクトップを含み、GUI ブートストラップと互換性フォールバックの間に制限付きプロセスからアクセスできます。

ダミー ステーションは、各サンドボックスに割り当てられた永続的で一意のウィンドウ ステーションではなく、そのデスクトップはアプリケーションの最終的な対話型デスクトップではありません。Sandboxie は、アプリケーションが制限付きトークンの下で GUI オブジェクトを通常作成またはクエリできないときにダミー オブジェクトを再利用できます。

## `OpenWndStation`

```ini
OpenWndStation=y
```

`OpenWndStation` はボックス全体の Boolean 設定です。その既定は `n` です。

これを有効にすると、通常の GUI 分離とブートストラップ パスが変更され、Windows がプロセスを対話型ウィンドウ ステーションとデスクトップにより直接接続できるようになります。現在の効果には次が含まれます。

- 通常の一時的な `DesktopName` とダミー オブジェクト ブートストラップ動作をスキップします。
- Sandboxie のデスクトップとウィンドウ ステーション エミュレーション フックのサブセットをバイパスします。
- 関連するトークン パスのために、通常の Untrusted 整合性レベルの代わりに Low 整合性を使用します。
- `SE_GROUP_LOGON_ID` でマークされたトークン グループに通常のグループ制限を適用するのではなく保持します。
- このパスを通じて通常適用される Job Object UI 制限のセットを省略します。

これは 3 つの設定の中で広範な互換性緩和です。プロセスに変更されていないホスト トークンや、すべての GUI オブジェクトへの無制限のアクセスを与えるものではありません。

### トークンと整合性の動作

この GUI モデルの通常のトークン パスは Untrusted 整合性を使用します。`OpenWndStation=y` の場合、Low 整合性を使用し、ログオン SID グループを保持します。

2 つの関連するトークン設定がこの区別に影響します。

- `NoUntrustedToken=y` は独立して Untrusted ではなく Low 整合性を選択します。
- `KeepTokenIntegrity=y` はソース整合性レベルを保持し、その側面について Low 対 Untrusted の選択に取って代わります。

これらの効果は、管理者グループ、特権、またはソース トークンの他のすべてのプロパティを自動的に保持しません。これらの特定の変更以外のトークン フィルタリングは独立したままです。

### Job Object UI 制限

`OpenWndStation=y` の場合、Sandboxie はこのパスを通じて通常の基本的な Job Object UI 制限セットを適用しません。省略される制限は現在、次をカバーしています。

- `JOB_OBJECT_UILIMIT_EXITWINDOWS`
- `JOB_OBJECT_UILIMIT_HANDLES`
- `JOB_OBJECT_UILIMIT_SYSTEMPARAMETERS`
- `JOB_OBJECT_UILIMIT_READCLIPBOARD`

プロセスは依然として Sandboxie Job Object に配置される場合があります。この設定はそのパスを通じて適用される GUI 関連の制限を変更します。

### GUI フックの境界

通常の分離では、Sandboxie は選択されたデスクトップおよびウィンドウ ステーション API のための互換性フックをインストールします。`OpenWndStation=y` の場合、デスクトップおよびウィンドウ ステーション フックの `Gui_InitEnum` グループはインストールされません。他の GUI フックとウィンドウ ポリシー メカニズムは独立したままです。

特に、`OpenWndStation` は次を直接無効にしません。

- ファイルシステムまたはレジストリの分離
- IPC 分離
- ネットワーク制限
- すべての Sandboxie GUI フック
- ウィンドウ クラス ポリシー
- すべてのクリップボード処理
- すべてのトークン制限

これは対象を絞った互換性緩和であり、一般的なサンドボックス バイパスではありません。

## `UseSbieWndStation`

```ini
UseSbieWndStation=y
```

この設定は既定で有効です。ボックス全体の構成とイメージ認識オーバーライドの両方をサポートします。例:

```ini
UseSbieWndStation=program.exe,n
```

現在のランタイムは、`CreateWindowStationA` と `CreateWindowStationW` の Sandboxie ラッパーで `UseSbieWndStation` を使用します。

```text
アプリケーションが CreateWindowStation を呼び出す
        |
        v
Sandboxie が実際の API を呼び出す
        |
        +-- 成功 -> 新しく作成されたウィンドウ ステーションを返す
        |
        v
作成失敗
        |
        v
UseSbieWndStation が有効でダミー ステーションが利用可能な場合
        |
        v
ダミー ウィンドウ ステーション ハンドルを返す
```

したがって、`UseSbieWndStation` は、アプリケーションのウィンドウ ステーション作成の試みが失敗したときに、Sandboxie がダミー ウィンドウ ステーションを互換性フォールバックとして使用できるようにします。すべてのプロセスをダミー ステーションに強制したり、各サンドボックスに一意のステーションを作成したり、メインの `CreateDesktop` 再試行パスを制御したり、プロセス トークンを変更したり、Job Object UI 制限を変更したりしません。

SandMan のラベルと一部の歴史的な記述は、この現在の動作よりも広範です。この設定は古いデスクトップおよびウィンドウ ステーション互換性作業で生まれましたが、現在の実行可能パスは主に `CreateWindowStation` 失敗後にそれを使用します。

`UseSbieWndStation=n` であっても、現在の組み込み互換性処理は、内部的に Chrome または Firefox イメージ タイプとして分類されたプロセスのためにダミー ステーション フォールバックを保持できます。したがって、この設定を無効にしてもすべての特別なイメージ フォールバックが削除されるわけではありません。

## `UseSbieDeskHack`

```ini
UseSbieDeskHack=y
```

この設定は既定で有効で、イメージ認識オーバーライドをサポートします。

```ini
UseSbieDeskHack=program.exe,n
```

`UseSbieDeskHack` は、制限付きトークンの動作がアプリケーションのそれらの操作の通常の完了を妨げるときに、ウィンドウ オブジェクト セキュリティ クエリとデスクトップ作成のための互換性再試行を提供します。

### セキュリティ情報クエリ

Sandboxie は、ダミー ウィンドウ ステーションに対して、選択された失敗したウィンドウ オブジェクト DACL セキュリティ クエリを再試行できます。これは特定の `GetSecurityInfo` および関連する NTMARTA 互換性パスに適用されます。すべてのセキュリティ記述子要求をリダイレクトするわけではありません。

いくつかの内部的に分類されたブラウザー イメージのための狭い `SetSecurityInfo` 互換性処理もあります。これは普遍的な偽の成功動作ではありません。

### `CreateDesktop` 互換性

高レベルの `CreateDesktopA/W` の流れは次のとおりです。

```text
通常の Windows CreateDesktop 操作を試行
        |
        v
必要に応じて、Sandboxie のダミー ウィンドウ ステーションを使用して再試行
        |
        v
UseSbieDeskHack が適用される場合、簡略化された
デバイスおよびセキュリティ パラメーターで再試行
        |
        v
結果を返すか、Sandboxie の互換性フォールバックを適用
```

Sandboxie は現在、`CreateDesktopEx` のための同等のフックをインストールしません。

`OpenDesktop` の場合、通常の `Default` デスクトップ パスは実際の対話型デスクトップへの複製ハンドルを返すことができます。他の失敗は Sandboxie の互換性パスを使用します。

`OpenWndStation=y` の場合、通常の `Gui_InitEnum` `CreateDesktop` および `OpenDesktop` フックはインストールされません。アプリケーションは、そのトークンと利用可能なウィンドウ ステーション権限に従って、パスのその部分についてネイティブの Windows API 動作を観察します。他のデスクトップ関連 GUI フックは依然としてアクティブな場合があります。

`UseSbieDeskHack=n` であっても、現在のソースは、内部的に Chrome、Firefox、または Acrobat Reader イメージ タイプとして分類されたプロセスのために組み込み互換性の動作を保持します。ボックスごとまたはイメージごとの `n` 値は、それらのイメージ タイプのすべての関連フォールバックを無効にしません。

## 相互作用と境界

### `NoSecurityIsolation`

`NoSecurityIsolation=y` の場合、プライマリ トークン置換、通常の Sandboxie GUI ブートストラップ、関連するデスクトップおよびウィンドウ ステーション フック セット、および同じ Job UI 制限パスを含む重要な通常のパスがすでにバイパスされています。したがって、`OpenWndStation` はそれらの特定のメカニズムにとって大部分が冗長です。

アプリケーション コンパートメント モードは、独立した GUI、ウィンドウ メッセージ、およびウィンドウ クラス ポリシーを依然として保持できます。GUI 分離がないものとして記述すべきではありません。

### ウィンドウ クラス ポリシー

`OpenWinClass`、`ClosedWinClass`、および `NoRenameWinClass` は、関連するが独立したウィンドウ ポリシー メカニズムを制御します。`OpenWndStation` はそれらの設定を一般に冗長にするものではありません。[Open Win Class](OpenWinClass.md) および [No Rename Win Class](NoRenameWinClass.md) を参照してください。

### クリップボード

クリップボードはウィンドウ ステーションに関連付けられていますが、Sandboxie は別個のクリップボード フックとプロキシ動作も実装しています。`OpenWndStation` は `JOB_OBJECT_UILIMIT_READCLIPBOARD` を省略しますが、すべての Sandboxie クリップボード処理を置き換えたり無効にしたりするものではありません。

### Win32k とその他のデスクトップ オプション {#win32k-and-other-desktop-options}

このページの設定は、主に SbieDll の USER32、ADVAPI、および NTMARTA フック、SbieSvc/GuiServer の動作、およびドライバーのトークン調整を通じて実装されています。別個の Win32k フックおよびフィルター メカニズムはこのページの範囲外です。

`NoSandboxieDesktop` は、Sandboxie の通常のデスクトップ プロキシとブートストラップをバイパスできる、別個のより広範なデバッグおよび互換性オプションです。

セキュア デスクトップと UAC の動作は別個の流れを使用します。[Prompt On Secure Desktop](PromptOnSecureDesktop.md) および [Use Sandboxie UAC](UseSandboxieUAC.md) を参照してください。

## SandMan 構成

### `OpenWndStation`

パス: **Sandbox Options > Security Options > Security Isolation > Desktop Isolation**

ラベル: **Open Window Station (improves compatibility by reducing desktop isolation)**

チェックボックスは既定でチェックされていません。チェックすると `OpenWndStation=y` が書き込まれます。クリアすると明示的な値が削除され、無効の既定が使用されます。デスクトップ分離の低下は、上記で説明したブートストラップ動作、選択されたフック、トークン整合性とログオン SID 処理、および Job Object UI 制限への複合的な変更です。

### `UseSbieWndStation`

パス: **Sandbox Options > Various Options > Compatibility**

ラベル: **Emulate sandboxed window station for all processes**

チェックボックスは既定でチェックされています。既定の状態は通常、明示的なキーを必要としません。クリアすると `UseSbieWndStation=n` が書き込まれます。ラベルは現在の実行可能ファイルの動作よりも広範で、主に `CreateWindowStation` 失敗後のフォールバックとしてこの設定を使用します。

### `UseSbieDeskHack`

パス: **Sandbox Options > Various Options > Compatibility**

ラベル: **Use desktop object workaround for all processes**

チェックボックスは既定でチェックされています。既定の状態は通常、明示的なキーを必要としません。クリアすると `UseSbieDeskHack=n` が書き込まれます。

これらの 3 つの設定のために専用の New Box Wizard コントロールまたは証明書制限は確認されませんでした。SandMan は、現在の設定メタデータがそれらをより単純に記述しているにもかかわらず、2 つの `UseSbie*` オプションのためのイメージ認識編集もサポートします。

## 構成変更の適用

`OpenWndStation` はトークン構築、GUI 初期化、フック インストール、および Job Object セットアップに影響します。変更した後は影響を受けるサンドボックス化されたプロセス ツリーを再作成または再起動してください。既存のプロセスはそのトークン、Job Object、またはデスクトップ ブートストラップが再構築されません。

`UseSbieWndStation` は `CreateWindowStation` 互換性処理中に参照されますが、ダミー オブジェクトとフックが予測可能な初期化状態になるように、影響を受けるアプリケーションを再起動することをお勧めします。`UseSbieDeskHack` はフック インストールとランタイム互換性再試行の両方に影響するため、変更後は影響を受けるアプリケーションまたはプロセス ツリーも再起動すべきです。

SandMan、SbieSvc、またはドライバーの再起動は通常は必要ありません。

## 失敗時の動作

失敗は、ダミー GUI オブジェクトの作成中、実際のウィンドウ ステーションとデスクトップ ハンドルの取得または複製中、GUI ブートストラップの完了中、または `CreateWindowStation`、`CreateDesktop`、および `OpenDesktop` へのネイティブおよび互換性呼び出しの処理中に発生する可能性があります。

Sandboxie は一部の失敗に対して再試行または互換性フォールバックを適用しますが、他の失敗は個々の API 呼び出しまたは GUI 初期化を失敗させる可能性があります。アプリケーションは、1 つの普遍的なエラー コードまたは互換性ハンドルの内部形式に依存すべきではありません。

## Sandboxie Plus と Classic

これらの設定のランタイム サポートは共有 Sandboxie コンポーネントに実装されています。SandMan は現在のコントロールを提供し、互換性のある INI 設定を共有ランタイムで利用できます。Sandboxie Control Classic インターフェイスで同等の現在のコントロールは確認されていないため、UI の同等性を前提とすべきではありません。

## バージョン履歴

- Sandboxie Plus 0.7.3 / Classic 5.49.5 より前は、Chrome および Firefox イメージ タイプはすでに特定の互換性動作を受け取っていました。
- Sandboxie Plus 0.7.3 / Classic 5.49.5 は `UseSbieWndStation` を導入しました。
- Sandboxie Plus 1.0.6 / Classic 5.55.6 は `UseSbieWndStation=y` を既定にしました。
- Sandboxie Plus 1.1.2 / Classic 5.56.2 は、より広範なプロセス使用のために `UseSbieDeskHack` を追加しました。
- Sandboxie Plus 1.8.2 / Classic 5.63.2 は `UseSbieDeskHack` を既定で有効にしました。
- `OpenWndStation` メタデータは Sandboxie Plus 1.14.9 / Classic 5.69.9 で導入されましたが、主要な現在の GUI ブートストラップ動作は 1.15.0 / 5.70.0 の開発で現れました。
- Sandboxie Plus 1.15.6 / Classic 5.70.6 は、`OpenWndStation=y` と `CreateDesktopA/W` を呼び出すアプリケーションを含む Windows 10 BSoD シナリオを修正しました。現在の実装は、このモードで通常の Job Object UI 制限を省略することにより、関連する条件を回避します。これは歴史的なものであり、現在再現可能な制限ではありません。
- Sandboxie Plus 1.16.7 / Classic 5.71.7 は、`OpenWndStation=y` と `SandboxieAllGroup=y` の間の相互作用を修正しました。現在のトークン処理は、Sandboxie グループを追加する前にログオン SID を保持します。

## 関連ページ

- [Sandboxie Ini](SandboxieIni.md)
- [Use SbieDesk Hack](UseSbieDeskHack.md)
- [Open Win Class](OpenWinClass.md)
- [No Rename Win Class](NoRenameWinClass.md)
- [Prompt On Secure Desktop](PromptOnSecureDesktop.md)
- [Use Sandboxie UAC](UseSandboxieUAC.md)
- [特別なイメージ](SpecialImage.md)
