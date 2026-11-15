# ネットワーク アクセス

`NetworkAccess` は、Sandboxie のネットワーク ルール エンジンのためのプログラム、アドレス、ポート、およびプロトコル ルールを定義します。同じルール パーサーと比較ロジックが、ユーザー モード Winsock パスと、有効な場合は [Windows Filtering Platform (WFP) パス](../PlusContent/WFPSupport.md)で使用されます。それらの強制カバレッジは異なります。

## 構文と例

```ini
NetworkAccess=[process,]Allow|Block[;Port=...][;Address=...][;Protocol=...]
```

例:

```ini
[DefaultBox]
NetworkAccess=*,Block;Port=80,443
NetworkAccess=chrome.exe,Allow;Port=443;Address=192.0.2.10;Protocol=TCP
NetworkAccess=<Browsers>,Allow;Port=80,443;Protocol=TCP
```

省略可能なプロセス セレクターは、実行可能ファイル、一致する実行可能パターン、または[プロセス グループ](ProcessGroup.md)を識別できます。Sandboxie の通常の[プログラム名マッチング](ProgramNamePrefix.md)は否定セレクターもサポートします。プロセス セレクターのないルールは、以下で説明するルール比較において、一致する明示的な `*` セレクターよりも広く適用されます。

`NetworkAccess` ルールが一致しない場合、ルール エンジンはトラフィックを許可します。既定で拒否するルール セットを構築するには、広い適用可能なブロックを追加し、必要な場合はより狭い許可を追加します。

```ini
NetworkAccess=*,Block
NetworkAccess=chrome.exe,Allow;Port=443
```

このルール エンジンの既定は、[WFP サポート](../PlusContent/WFPSupport.md#allownetworkaccess)で説明されている `AllowNetworkAccess` ゲートとは別個です。

## 一致するルールの選択方法

候補プログラムとエンドポイントについて、Sandboxie はこの順序で最初の 4 つの基準を厳密に比較します。後続の候補は、異なるこれらの基準の最初のもので優れている場合、現在の勝者を置き換えます。

| 順序 | 基準 | より特異なまたは優先される一致 |
| --- | --- | --- |
| 1 | プロセス セレクター | 一致する正のセレクター、次に一致する否定セレクター、次に明示的な `*`、次にセレクターなし |
| 2 | 結合エンドポイント | アドレスとポートの両方が制約されているものが、いずれか一方のみまたはどちらも制約しないものより優先 |
| 3 | ポート | 正確なポート、次に範囲、次に制約なし |
| 4 | アドレス | 正確なアドレス、次に範囲、次に制約なし |

一致する正のセレクターには、実行可能ファイル名、ワイルドカード イメージ パターン、または `ProcessGroup` が含まれます。最上位カテゴリは正確な実行可能ファイル名に限定されません。以下の最初の 3 つの例は正のセレクターです。残りの行は否定セレクター、明示的な `*`、およびセレクターなしを示しています。

```ini
NetworkAccess=chrome.exe,Allow;Port=443
NetworkAccess=chr*.exe,Allow;Port=443
NetworkAccess=<Browsers>,Allow;Port=443
NetworkAccess=!chrome.exe,Block
NetworkAccess=*,Block
NetworkAccess=Block
```

プロセスの一致が最初に比較されるため、より強いプロセス セレクターが、より正確なアドレスまたはポートの制約を持つルールよりも上位にランクされる場合があります。同等のプロセスの一致では、`Address` と `Port` の両方を指定するルールが、いずれか一方のみを指定するものより上位にランクされます。その結合比較の後、ポートの特異性がアドレスの特異性より前にチェックされます。

最初の 4 つの基準が同点の場合、現在のコンパレーターはアクションとプロトコルを非対称に処理します。`Block` 候補は `Allow` の勝者を即座に置き換えます。そうでなければ、比較はプロトコルの特異性に続行でき、指定されたプロトコルが `Any` より上位にランクされます。したがって、それ以外で同点の 1 つのルールが `Block` を優先し、もう 1 つがより特異なプロトコルを優先する場合、ルールの順序が結果に影響を与える可能性があります。

コンパレーターが現在の勝者を置き換える理由を見つけられない場合、既存の勝者が残ります。互換性のあるルールは内部的にマージされる場合もあります。`NetworkAccess` は最後のルールが優先されるエンジンではありません。

## アドレス、ポート、およびプロトコル

`Address` は、単一の IPv4 または IPv6 アドレス、アドレス範囲、およびコンマ区切りのエントリを受け入れます。例:

```ini
Address=192.0.2.10
Address=192.0.2.10-192.0.2.50
Address=2001:db8::10
```

`Port` は、単一の数値ポート、範囲、およびコンマ区切りのセットを受け入れます。

```ini
Port=80,443,49152-65535
```

現在のルール言語は `Protocol=Any`、`TCP`、`UDP`、および `ICMP` を認識します。修飾されていないルールは既定で `Any` になります。`ICMPv6` キーワードは定義されていません。サポートされているアドレス構文はアドレスと範囲を使用し、CIDR 表記は使用しません。`http` のようなポート名は数値ポート値ではありません。

## 強制パス

WFP 強制なしでは、SbieDll は傍受されたユーザー モード Winsock パスを通じて `NetworkAccess` を適用します。これには、`connect`、`WSAConnect`、`sendto`、および `WSASendTo` などの重要な送信 TCP および UDP 操作が含まれます。関連する受信フックもこの実装に関与します。これは主に送信ルールの強制であり、すべての Windows ネットワーク パスをカバーするわけではありません。ユーザー モード フックを迂回または削除するコードは、このレイヤーをバイパスできます。

`NetworkEnableWFP=y` の場合、Sandboxie はカーネル WFP コールアウトを使用して、追跡されたサンドボックス化されたプロセスの共有ルールを送信接続および受信 receive/accept 認可レイヤーで評価します。グローバル スイッチ、プロセス マッピング、およびライフサイクルについては、[WFP サポート](../PlusContent/WFPSupport.md)を参照してください。

パーサーと SandMan エディターは `ICMP` を認識しますが、ユーザー モード フックは Winsock TCP 接続と UDP 送受信に焦点を当てています。ICMP カバレッジは強制パスとトラフィック タイプに依存します。この設定も WFP も、すべての raw または ICMPv6 パスの保証として読むべきではありません。

`AllowNetworkAccess=n` は、別個のイメージ認識アクセス ゲートです。WFP 下では、通常の `NetworkAccess` ルール評価の前に包括的なインターネット ブロックを選択できます。`NetworkAccess=...,Allow` ルールが必ずしもそのゲートを上書きするわけではありません。[Prompt For Internet Access](PromptForInternetAccess.md)からの実行時の承認は、プロセス インスタンスのゲートに影響を与える場合がありますが、永続的な `NetworkAccess` ルールではありません。[Block Local Loop](BlockLocalLoop.md)も WFP 下で別途評価されます。

## SandMan とバージョンの文脈

ルール エディターは **Sandbox Options > Network Options > Network Firewall** にあります。そのフィールドは Program、Action、Protocol、IP/Address、および Port に対応します。**Test Rules** コントロールは、入力されたプログラム、アドレス、ポート、およびプロトコルの部分的なプレビューを提供します。ネットワーク接続は行いません。プレビューはワイルドカードまたはプロセス グループ セレクターを処理せず、テンプレート ルールをスキップし、無効なルールを考慮する場合があります。したがって、その強調表示された結果は、ランタイムで適用されるルールと異なる場合があります。

`NetworkAccess` は Sandboxie Plus 0.9.0 で導入されました。ルール カバレッジと更新動作は強制パスに依存するため、ポリシーを変更した後は影響を受けるサンドボックス化されたアプリケーションを再起動して、プロセス ローカル状態が一貫して再構築されるようにしてください。WFP ルールは、Sandboxie の構成更新パスを通じて既存の追跡されたプロセスのために更新することもできます。

## 関連ページ

- [WFP サポート](../PlusContent/WFPSupport.md)
- [Block Local Loop](BlockLocalLoop.md)
- [Prompt For Internet Access](PromptForInternetAccess.md)
- [プロセス グループ](ProcessGroup.md)
