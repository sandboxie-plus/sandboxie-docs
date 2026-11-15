Sandboxie Plus は 6 つの基本ボックス タイプと、省略可能な暗号化/機密の組み合わせを提供します。

サンドボックスは通常、ホスト システムをボックス内で実行されているプロセスから分離し、コンピューター内の他のプログラムやデータに永続的な変更を加えるのを防ぎます。分離のレベルは、[セキュリティ](../PlusContent/security-mode.md)とアプリケーションとの[互換性](../PlusContent/compartment-mode.md)の両方に影響します。
Sandboxie Plus は、その監督下で実行されているプロセスによって[個人データがアクセスされるのを保護](../PlusContent/privacy-mode.md)できます。

Sandboxie Plus は、[暗号化サンドボックス ストレージ](../PlusContent/BoxEncryption.md)と[機密ボックス](../Content/ConfidentialBox.md)保護を組み合わせることもできます。後者は、関連するサンドボックス外のホスト プロセスによるサンドボックス化されたプロセスおよびスレッド ハンドルへのアクセスを制限します。[マウント ルート保護](BoxEncryption.md#root-protection-while-mounted)は別のファイルシステム保護オプションです。組み合わせたウィザード オプションについては、[ブラック ボックス](../PlusContent/black-box.md)を参照してください。

この表は、6 つの基本タイプの通常の構成を示しています。**アプリケーション コンパートメント**はそのモードを識別するものであり、一般的な互換性評価ではありません。色とアイコンは表示上の補助であり、ボックスの有効な設定を保証するものではありません。

| ボックスの種類 | [セキュリティ強化](../PlusContent/security-mode.md) | [データ保護](../PlusContent/privacy-mode.md) | [アプリケーション コンパートメント](../PlusContent/compartment-mode.md) |
|-|-|-|-|
|![](../Media/sandbox-r-full.png) レッド ボックス — データ保護付きセキュリティ強化サンドボックス|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES| ![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|
|![](../Media/sandbox-o-full.png) オレンジ ボックス — セキュリティ強化サンドボックス|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO| ![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|
|![](../Media/sandbox-b-full.png) ブルー ボックス — データ保護付きサンドボックス|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES| ![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|
|![](../Media/sandbox-y-full-e1684328804872.png) イエロー ボックス — 標準サンドボックス|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO| ![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|
|![](../Media/sandbox-c-full.png) シアン ボックス — データ保護付きアプリケーション コンパートメント ボックス|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES|
|![](../Media/sandbox-g-full.png) グリーン ボックス — アプリケーション コンパートメント ボックス|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|![Red Color](https://placeholder.antonshell.me/img?width=15&color_bg=FF0000&text=+) NO|![Green Color](https://placeholder.antonshell.me/img?width=15&color_bg=green&text=+) YES|

## 暗号化および機密オプション

新しいボックス ウィザードの **Encrypt Box content and set Confidential** オプションは、6 つの基本タイプのいずれかと組み合わせることができます。通常のウィザード ワークフローでは、選択した基本構成を保持したまま `UseFileImage=y` と `ConfidentialBox=y` を追加します。

| 機能 | ブラック ボックス オプション |
|-|-|
| [暗号化ストレージ](BoxEncryption.md) | はい |
| [機密プロセス保護](../Content/ConfidentialBox.md) | はい |
| セキュリティ / データ保護 / アプリケーション コンパートメント モード | 選択した基本タイプから保持 |

![Black Box type icon](../Media/sandbox-k-full.png) SandMan は、組み合わせた暗号化/機密の表示のためにこの暗いアイコンを表示できます。これは 1 つの固定された基本モードを識別したり、黒い枠を意味したりするものではありません。表示設定については、[ボックスの表示](../Content/BoxPresentation.md)を参照してください。
