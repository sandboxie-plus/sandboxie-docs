# HideBordersFromCapture

_HideBordersFromCapture_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 1.17.3 以降で使用できます。

```ini
[DefaultBox]
HideBordersFromCapture=y
```

この設定は、サンドボックス化されたアプリケーションの内容ではなく、Sandboxie Plus の視覚的な境界線オーバーレイに適用されます。これを有効にしても、アプリケーション自身のウィンドウがキャプチャ不能になるわけではありません。

## キャプチャの動作

Sandboxie Plus (SandMan) は、色付きの境界線とサンドボックス名またはエイリアス ラベルに使用される別個のウィンドウに Windows の表示アフィニティを適用します。_HideBordersFromCapture_ が有効な場合、SandMan は最初に `WDA_EXCLUDEFROMCAPTURE` を要求します。Windows がその要求を拒否した場合、`WDA_MONITOR` にフォールバックします。設定が無効な場合、オーバーレイは `WDA_NONE` を使用します。

`WDA_EXCLUDEFROMCAPTURE` は互換性のある Windows のキャプチャ パスにオーバーレイ ウィンドウを省略するよう要求し、Windows 10 バージョン 2004 以降でサポートされています。それ以前の Windows バージョンでは、Microsoft はこの値が `WDA_MONITOR` と同様に動作すると文書化しています。`WDA_MONITOR` フォールバックはモニター上でオーバーレイを表示したままにしますが、他の場所では空白として表示されることがあります。一方 `WDA_NONE` は表示アフィニティ制限を適用しません。互換性のある OS 管理のキャプチャ パスは通常 Sandboxie の境界線オーバーレイを省略または空白にしますが、すべてのキャプチャまたは録画ツールとの互換性は保証されません。

色付きの枠とラベルは同じオーバーレイを共有するため、表示アフィニティ設定は両方に適用されます。サンドボックス化されたアプリケーションの内容は、別の独立した設定が影響しない限りキャプチャ可能なままです。

Windows の表示アフィニティは DRM メカニズムでもセキュリティ境界でもありません。このオプションは、互換性のあるスクリーンショットや画面録画から Sandboxie の視覚的な境界線とラベルを除外することを目的としており、サンドボックス化されたアプリケーションのスクリーンショット保護を提供するものではありません。

Windows API のセマンティクスと制限については、Microsoft の [`SetWindowDisplayAffinity` のドキュメント](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowdisplayaffinity) を参照してください。

## 既定値と構成スコープ

_HideBordersFromCapture_ のメタデータ上の既定値は無効です。明示的なボックスごとの値が優先され、次に明示的なグローバル値が続きます。どちらの値も存在しない場合、SandMan はボックス ローカルの _CoverBoxedWindows_ 値をフォールバックとして使用します。ボックス内でどちらの設定も有効でない場合、有効な動作はオフです。

このフォールバックは特にボックス ローカルの _CoverBoxedWindows_ 値に対するものであり、その設定のテンプレートまたはグローバル継承は使用しません。_HideBordersFromCapture_ には、文書化されたプログラムごとの構文はありません。

## ランタイム動作

既存の SandMan 境界線オーバーレイは、その表示アフィニティ状態を動的に更新でき、境界線サブシステムは既存のオーバーレイを更新します。サンドボックス化されたアプリケーションを再起動する必要は通常ありません。

通常の Sandbox Options インターフェイスには、_HideBordersFromCapture_ 専用のチェックボックスは現在ありません。INI 構成を通じて構成します。

## 関連設定

* [Sandboxie Ini](SandboxieIni.md)
* [Border Color](BorderColor.md) は視覚的な境界線を表示するかどうか、およびその方法を制御します。
* [Cover Boxed Windows](CoverBoxedWindows.md) はサンドボックス化されたアプリケーション ウィンドウのキャプチャと表示アフィニティの動作に関係し、_HideBordersFromCapture_ は SandMan の境界線とラベルのオーバーレイに関係します。2 つの設定は同一のフォールバックまたは継承セマンティクスを持ちません。
* [Block Screen Capture](BlockScreenCapture.md) はサンドボックス化されたプロセスによって開始されるキャプチャ操作を独立して制御します。SandMan のオーバーレイが互換性のあるホスト側のキャプチャ パスに表示されるかどうかは制御しません。

## バージョン履歴

_HideBordersFromCapture_ は、境界線オーバーレイのキャプチャ動作をより広範な _CoverBoxedWindows_ 動作から分離するために Sandboxie Plus 1.17.3 で導入されました。その明示的なメタデータ上の既定値は無効のままであり、上記のランタイム フォールバックの対象です。
