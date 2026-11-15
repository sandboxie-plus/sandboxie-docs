# NT Namespace Isolation

_NtNamespaceIsolation_ は、名前付きカーネル オブジェクトのコンテナーとして使用される NT ディレクトリ オブジェクトの Sandboxie による分離を制御します。既定で有効です。

この設定は名前付きオブジェクトによって使用されるディレクトリ オブジェクト名前空間に関するものです。すべての形式のプロセス間通信 (IPC) のためのスイッチではありません。

## 使用法

ボックスの通常の名前空間分離動作を無効にするには:

```ini
[DefaultBox]
NtNamespaceIsolation=n
```

## 現在の動作

名前空間分離が有効な場合、Sandboxie は NT ディレクトリ オブジェクトを含む操作を仲介します。これには、名前付きカーネル オブジェクトによって使用されるディレクトリ作成および開くパスが含まれます。Sandboxie は通常、これらのオブジェクトをサンドボックス名前空間にリダイレクトします。

ディレクトリのサンドボックス コピーが利用できない場合、SbieDll の `NtOpenDirectoryObject` フォールバックは対応するホスト ディレクトリを開くことができます。名前空間分離が有効な場合、そのフォールバックは要求されたアクセスをクエリ、トラバーサル、および読み取り制御権限に低減します。これにより、通常のユーザー モード フォールバックがホスト ディレクトリに対して作成または他の変更権限を取得することを防ぎます。

この動作は、サンドボックス化されたプロセスがホスト名前空間で競合する名前を作成することを防ぐのに役立ちます。Sandboxie Plus 1.8.0 / Classic 5.63.0 のリリースは、この保護をセキュリティを改善し、名前の占有 (name squatting) を防ぐものとして説明していました。

## 名前空間分離の無効化

`NtNamespaceIsolation=n` は、ホスト NT ディレクトリ オブジェクトへのより制限の少ないアクセスを許可します。これは、通常とは異なる名前付きオブジェクト名前空間シナリオの互換性を改善できますが、Sandboxie のディレクトリ オブジェクト仮想化と名前占有保護を弱めます。

この設定を無効にしても、すべての IPC 制限またはすべての形式の IPC 分離が無効になるわけではありません。IPC パス ルールおよび他の Sandboxie コントロールは別個のままです。

## 代替 IPC 命名 {#alternate-ipc-naming}

`UseAlternateIpcNaming` は、Application Compartment ボックス用に導入された別個の高度な命名モードです:

```ini
[DefaultBox]
NoSecurityIsolation=y
UseAlternateIpcNaming=y
```

Sandboxie がリダイレクトする名前付きカーネル オブジェクトを、通常の別個の NT ディレクトリ オブジェクト名前空間の下に配置する代わりに、Sandboxie はサンドボックス固有のサフィックスを導出し、それをリダイレクトされたオブジェクト名に追加します。このモードでは、リダイレクトされた名前が既存の名前空間を使用するため、SbieDll は通常のディレクトリ オブジェクト名前空間フックをインストールしません。

この設定は、リダイレクトされた名前付きカーネル オブジェクトの Sandboxie の命名戦略を変更します。すべての IPC プロトコルまたはすべての Sandboxie サービス エンドポイントの名前を変更するものではありません。

`UseAlternateIpcNaming` は Application Compartment ボックスを対象としています。プロジェクトは、標準の分離されたボックスでこれを使用すると、ドライバーがアクセスをブロックする可能性があると警告しています。これは `NtNamespaceIsolation=n` のエイリアスではありませんが、代替命名は通常の別個のディレクトリ オブジェクト名前空間パスを回避します。

## バージョン履歴

| 設定または変更 | バージョン |
| --- | --- |
| NT ディレクトリ オブジェクト名前空間仮想化と `NtNamespaceIsolation` | Sandboxie Plus 1.8.0 / Classic 5.63.0 |
| `UseAlternateIpcNaming` | Sandboxie Plus 1.17.0 / Classic 5.72.0 |

## 関連ページ

- [No Security Isolation](NoSecurityIsolation.md)
- [Application Compartment](../PlusContent/compartment-mode.md)
- [Sandboxie Ini](SandboxieIni.md)
