# BlockInterferenceControl

_BlockInterferenceControl_ は Sandboxie Plus 1.13.6 以降で使用可能な [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。既定では無効で、現在は Experimental としてマークされています。

例:

```ini
[DefaultBox]
BlockInterferenceControl=y
```

有効な場合、この設定はサンドボックス化されたプロセスによって実行される選択されたカーソル、フォアグラウンド、アクティベーション、および最前面ウィンドウ操作を制限します。すべての可能なユーザー インターフェイスまたは入力の相互作用をブロックするものではなく、完全なデスクトップ分離として扱うべきではありません。

## 影響を受ける動作

この設定は、次の Windows API に関連する選択された動作を制限します:

- `SetCursorPos`
- `ClipCursor`
- `ShowCursor`
- `SetForegroundWindow`
- `SetActiveWindow`
- `BringWindowToTop`
- `SwitchToThisWindow`
- `CreateWindowEx`、`MoveWindow`、および `SetWindowPos` を通じて実行される選択された操作

これらの API はすべて同じ方法で処理されるわけではありません。一部の呼び出しはブロックされ、選択されたウィンドウ作成、位置指定、および最前面要求は Windows に渡される前に変更されます。

## カーソルの動作

_BlockInterferenceControl_ は `SetCursorPos` を通じた直接のカーソル再配置をブロックします。

`ClipCursor(rect)` によるカーソル制限の作成または変更もブロックされます。既存の制限を解放できるように `ClipCursor(NULL)` は引き続き許可されます。

`ShowCursor(FALSE)` を通じたカーソルを隠す要求は抑制されますが、カーソルを表示する要求は引き続き許可されます。

この設定は、`SendInput`、Raw Input、マウス キャプチャ、カーソル形状の変更、またはすべての模擬入力メカニズムを具体的にブロックするものではありません。これらのパスの一部は、別個の Sandboxie 保護の対象となることがあります。

## フォアグラウンドとウィンドウ アクティベーション

この設定は `SetForegroundWindow`、`SetActiveWindow`、`BringWindowToTop`、および `SwitchToThisWindow` を通じた明示的な呼び出しを抑制します。

これらの制限はサンドボックス化されていないターゲット ウィンドウに限定されません。現在の動作は、ターゲットが同じサンドボックスに属する場合にも適用されます。`SetFocus` はこの設定の一部ではありません。

## 最前面ウィンドウと Z オーダー

傍受されたウィンドウ作成パスについて、Sandboxie は `WS_EX_TOPMOST` スタイルを削除します。タスクバーの被覆が許可されていない場合、`SetWindowPos` を通じた選択された `HWND_TOPMOST` 要求も低減されます。

この設定は選択された最前面要求を制限しますが、すべての通常の Z オーダー変更をブロックするものではありません。サンドボックス化されたウィンドウがタスクバーを覆うのを防ぐために、ウィンドウの位置とサイズ変更の要求が調整されることもあります。

## タスクバーの被覆の許可

関連する設定:

```ini
AllowCoverTaskbar=y
```

は、_BlockInterferenceControl_ が `MoveWindow`、`SetWindowPos`、および選択されたウィンドウ作成の位置指定の周囲に適用する一部の位置とサイズの制限を緩和します。

_AllowCoverTaskbar_ はすべての干渉制御動作を無効にするわけではありません。特に、ブロックされたフォアグラウンドおよびアクティベーション API、またはすべての最前面要求を復元するものではありません。

## 互換性

一部のブロックされた操作は、暗黙的に許可されるのではなく、アプリケーションに失敗を報告します。制限された動作に依存するプログラムは、したがってサンドボックス内で異なる動作をすることがあります。

Sandboxie プロジェクトは、このオプションがゲームとの互換性の問題を引き起こす可能性があると警告し、ゲーム用ボックスには推奨していません。ゲームはカーソル制限、直接のカーソル移動、フォアグラウンド アクティベーション、または全画面および最前面ウィンドウの動作に依存することがあります。この警告は、すべてのゲームが互換性がないという意味ではありません。

## ランタイムとスコープ

この設定はサンドボックス化されたプロセスが初期化されるときに読み取られます。既存のプロセスは通常、構成を変更した後に再起動する必要があります。新しく開始されたサンドボックス化されたプロセスは新しい値を受け取ります。

これはサンドボックスおよびプロセス レベルで適用され、文書化されたプログラムごとの構文はありません。制限は主に、カーネル強制の保護としてではなく、サンドボックス化されたプロセス内のユーザー モード API 傍受を通じて実装されています。この設定で対象とされない代替 API がブロックされると仮定すべきではありません。

## Sandboxie Plus インターフェイス

オプションは次にあります:

**Sandbox Options > General Options > Restrictions > Prevent interference with the user interface (Experimental)**

既定ではチェックされていません。そのツールチップは、マウスの移動の防止、ウィンドウを前面に出す操作、および類似の操作がゲームで問題を引き起こす可能性が高いと警告しています。

オプションが有効な場合、**Allow sandboxed windows to cover the taskbar** コントロールが使用可能になります。

## バージョン履歴

_BlockInterferenceControl_ は Sandboxie Plus 1.13.6 で導入されました。_AllowCoverTaskbar_ は後に互換性オプションとして追加されました。_BlockInterferenceControl_ の既定は無効のままです。

## 関連設定

- [Sandboxie Ini](SandboxieIni.md)
- [Block Screen Capture](BlockScreenCapture.md): 別個のスクリーン キャプチャ保護メカニズムを使用します
- [BlockInterferePower](BlockInterferePower.md)
