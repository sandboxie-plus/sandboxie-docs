# AllowCoverTaskbar

_AllowCoverTaskbar_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 1.14.2 以降で利用できます。既定では無効です。

```ini
[DefaultBox]
BlockInterferenceControl=y
AllowCoverTaskbar=y
```

この設定は `BlockInterferenceControl=y` の場合にのみ効果があります。干渉制御が無効な場合、_AllowCoverTaskbar_ は実質的に無効です。

## 動作

_AllowCoverTaskbar_ は、_BlockInterferenceControl_ によって課される選択された制限のための互換性オプションです。独立したタスクバー アクセス機能ではなく、Windows タスクバーと対話する一般的な許可を与えるものでもありません。

`BlockInterferenceControl=y` かつ `AllowCoverTaskbar=n` の場合、Sandboxie はタスクバーの被覆に関連する選択されたウィンドウ位置、サイズ、および Z オーダーの要求を調整することがあります。_AllowCoverTaskbar_ を有効にすると、`CreateWindowExW`、`MoveWindow`、および `SetWindowPos` を含む関連する傍受操作に対して、これらの特定の調整をスキップします。

この設定は _BlockInterferenceControl_ の残りを無効にしません。フォアグラウンド アクティブ化、`BringWindowToTop` API、直接的なカーソル再配置、カーソルの閉じ込め、およびカーソルの非表示に関する制限は引き続き有効です。また、_BlockInterferenceControl_ によって傍受されたウィンドウ作成から削除された初期の `WS_EX_TOPMOST` スタイルを復元するものでもありません。

現在のアプリケーション ウィンドウ制限ロジックは、完全なモニターごとのタスクバー モデルではなく、Windows のプライマリ ディスプレイ作業領域を使用します。セカンダリ モニターのタスクバー、複数のモニターにまたがるウィンドウ、または特殊なシェルやアプリバーの配置を正確にモデル化するために依存しないでください。

## 実行時の動作

_AllowCoverTaskbar_ は、サンドボックス化されたプロセスが初期化されるときに読み取られます。設定を変更した後は、すでに実行中のサンドボックス化されたプロセスを再起動してください。新しく開始されたプロセスが新しい値を受け取ります。この設定には文書化されたプログラムごとの構文はありません。

## Sandboxie Plus インターフェイス

このオプションは、**Sandbox Options > General Options > Restrictions > Other restrictions** の **Allow sandboxed windows to cover the taskbar** というラベルの下で利用できます。

このチェックボックスは既定ではオフで、**Prevent interference with the user interface (Experimental)** が有効な場合にのみ有効になります。専用のツールヒントはありません。

## バージョン履歴

_AllowCoverTaskbar_ は、_BlockInterferenceControl_ の互換性オプションとして Sandboxie Plus 1.14.2 で導入されました。その既定値は引き続き無効です。

## 関連する設定

* [Sandboxie Ini](SandboxieIni.md)
* `BlockInterferenceControl` はこの設定の直接の依存関係です。
* [Border Exclude Taskbar](BorderExcludeTaskbar.md) は Sandboxie Plus の視覚的な境界オーバーレイを独立して制御します。アプリケーション ウィンドウの制限を変更するものではありません。
