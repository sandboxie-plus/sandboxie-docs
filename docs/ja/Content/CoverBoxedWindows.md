# Cover Boxed Windows

_CoverBoxedWindows_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、互換性のあるキャプチャ パスから対象となるサンドボックス化されたアプリケーション ウィンドウを除外するよう Windows に要求します。すべてのサンドボックス化されたウィンドウを普遍的にキャプチャ不能にするものではありません。

```ini
[DefaultBox]
CoverBoxedWindows=y
```

既定は `n` です。

## 動作の仕組み

Sandboxie は、サンドボックス化されたプロセス内の ANSI および Unicode の `CreateWindowEx` パスを傍受します。親/所有者引数が null の状態でウィンドウが正常に作成された後、Sandboxie は Windows の `SetWindowDisplayAffinity` API を `WDA_EXCLUDEFROMCAPTURE` (`0x00000011`) で呼び出します。

これは、これらの傍受された作成パスを通じて到達した対象の親なしウィンドウに適用されます。Sandboxie は、子ウィンドウや、null 以外の親/所有者引数で作成された所有ウィンドウにアフィニティを再帰的に適用しません。現在の実装は `SetWindowDisplayAffinity` が成功するかどうかをチェックせず、呼び出しが失敗した場合に再試行したりフォールバックを適用したりしません。

## Windows の動作と制限

Microsoft は、`SetWindowDisplayAffinity` が呼び出し元プロセスが所有するトップレベル ウィンドウを必要とし、デスクトップ ウィンドウ マネージャーがデスクトップを合成している間のみ機能することを文書化しています。これはすべてのキャプチャ手法ではなく、特定のパブリック オペレーティング システムのキャプチャ機能セットに影響します。

`WDA_EXCLUDEFROMCAPTURE` は Windows 10 バージョン 2004 以降でその除外動作を提供します。それ以前のサポートされている Windows バージョンでは、Microsoft はこの値を `WDA_MONITOR` のように動作すると文書化しています。これはモニター上にウィンドウを表示しますが、他の場所では内容なしで表示します。

Windows の表示アフィニティはセキュリティ機能でも DRM 保証でもありません。キャプチャ結果は、使用されている Windows とキャプチャ パスに依存します。Microsoft の [`SetWindowDisplayAffinity` ドキュメント](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowdisplayaffinity)を参照してください。

プロジェクト固有の制限も適用されます:

- _CoverBoxedWindows_ は現在、Chromium ベースのブラウザー バージョン 128 以降では動作しません。[issue #4302](https://github.com/sandboxie-plus/Sandboxie/issues/4302) はオープンのままです。
- `cmd.exe` などのコンソール アプリケーションはサポートされていません。
- 子、所有、またはその他の未処理のウィンドウが表示アフィニティを受け取ると想定してはなりません。

## 構成と実行時の変更

_CoverBoxedWindows_ はボックス設定です。ボックスが上書きする値を提供しない場合、通常のテンプレートおよびグローバル フォールバックがその有効な値に寄与できます。

この値は、サンドボックス化されたプロセスがその GUI フックを初期化するときにキャッシュされ、アフィニティは対象となる各ウィンドウが作成されるときに要求されます。設定を変更しても、既に実行中のプロセスが更新されたり、既存のウィンドウが後から適用されたりすることはありません。変更後は影響を受けるサンドボックス化されたアプリケーションを再起動してください。SandMan、サービス、またはドライバーの再起動は通常必要ありません。

## SandMan

**Sandbox Options > Security Options > Box Protection** を開き、次を使用します:

> Prevent processes from capturing window images from sandboxed windows

プロジェクト メタデータは、この設定を実験的として分類しています。

## 関連する設定

- [Block Screen Capture](BlockScreenCapture.md) は、サンドボックス化されたプロセスがサンドボックスの外側のデスクトップまたはウィンドウに対して開始する選択されたキャプチャ試行を制限します。
- [Hide Borders From Capture](HideBordersFromCapture.md) は SandMan の境界およびラベル オーバーレイに別個に適用されます。

## バージョン履歴

この機能は Sandboxie Plus 1.13.2 / Classic 5.68.2 で `IsProtectScreen` として導入され、1.13.3 / 5.68.3 で修正されました。1.13.6 / 5.68.6 で `CoverBoxedWindows` に改名されました。
