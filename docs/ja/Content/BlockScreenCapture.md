# Block Screen Capture

_BlockScreenCapture_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、サンドボックス化されたプロセスが同じサンドボックス外のデスクトップまたはウィンドウに対して行う選択されたキャプチャ試行を制限します。選択された一般的な USER32 および GDI キャプチャ パスを対象とします。完全なスクリーン キャプチャ防止メカニズムではありません。

```ini
[DefaultBox]
BlockScreenCapture=y
```

既定は `n` です。

## 傍受する内容

通常の GUI 分離がアクティブな場合、_BlockScreenCapture_ が有効なときに Sandboxie はこれらの USER32 関数を傍受します:

- `GetDC`
- `GetWindowDC`
- `GetDCEx`
- `PrintWindow`
- `ReleaseDC`

`GetDC`、`GetWindowDC`、および `GetDCEx` について、null ウィンドウ ハンドル、デスクトップ ウィンドウ、または同じサンドボックス外のウィンドウを対象とする要求は、実際のディスプレイまたはウィンドウ DC ではなく、ダミー ビットマップに支えられた互換メモリ DC を受け取ります。`ReleaseDC` はこれらの代替 DC を認識して解放します。

同じ外部ターゲットについて、`PrintWindow` は失敗し、ゼロを返し、Windows エラーをアクセス拒否に設定します。同じサンドボックス内のウィンドウを対象とする呼び出しは、通常の API 操作の対象となり得ます。

Sandboxie はまた、特定のデバイスなしで `DISPLAY` ドライバーを要求する ANSI および Unicode の `CreateDC` パスを傍受し、ダミー DC を代替します。現在の実装は `BitBlt` または `StretchBlt` 自体をフックしません。

## スコープと制限事項

この設定は実験的であり、UI の不具合を引き起こす可能性があります。SandMan のツールチップが述べているように、スクリーン キャプチャを取得する一般的な方法の一部のみをブロックします。すべてのキャプチャ API、キャプチャ プログラム、ディスプレイ ドライバー、または記録手法に対する保護として扱うべきではありません。

`OpenWinClass=*` が構成されている場合、SandMan は通常の _BlockScreenCapture_ チェックボックスを無効にし、Sandboxie は上記の主要な USER32 傍受パスをインストールしません。別個の GDI ディスプレイ DC 傍受は、設定が手動で強制された場合に初期化されることがありますが、その部分的な動作を通常または完全なキャプチャ保護として扱うべきではありません。

## 構成とランタイムの変更

_BlockScreenCapture_ はボックス設定です。ボックスが上書き値を提供しない場合、通常のテンプレートおよびグローバル フォールバックがその有効値に寄与することがあります。

値はサンドボックス化されたプロセスが GUI/GDI フックを初期化するときにキャッシュされます。変更後は影響を受けるサンドボックス化されたアプリケーションを再起動してください。SandMan、サービス、またはドライバーの再起動は通常必要ありません。

## SandMan

**Sandbox Options > General Options > Restrictions** を開き、次を使用します:

> Prevent sandboxed processes from capturing window images (Experimental, may cause UI glitches)

ツールチップの記載:

> This feature does not block all means of obtaining a screen capture, only some common ones.

## 関連設定

- [Cover Boxed Windows](CoverBoxedWindows.md) は、該当するサンドボックス化されたアプリケーション ウィンドウを互換性のあるキャプチャ パスから除外するよう Windows に要求します。
- [Hide Borders From Capture](HideBordersFromCapture.md) は SandMan の別個の境界線とラベルのオーバーレイに適用されます。

これらのコントロールは独立しており、異なる方向に作用します。

## バージョン履歴

この機能は Sandboxie Plus 1.13.4 / Classic 5.68.4 で `IsBlockCapture` として導入されました。Windows 7 および KeePass の互換性修正も含まれていた 1.13.6 / 5.68.6 で `BlockScreenCapture` に名前が変更されました。
