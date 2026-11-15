# No Security Isolation

_NoSecurityIsolation_ は Sandboxie の **Application Compartment** モードを選択します。このモードは、標準のサンドボックスで使用されるいくつかのセキュリティ分離メカニズムをバイパスすることで互換性を優先しますが、すべての Sandboxie の分離または仮想化メカニズムを無効にするわけではありません。

> [!WARNING]
> Application Compartment は分離を実質的に低減し、互換性要件を持つ信頼できるアプリケーションを対象としています。ファイルとレジストリの仮想化はアクティブなままにできますが、仮想化だけをセキュリティ境界として扱うべきではありません。

## 使用法

```ini
[DefaultBox]
NoSecurityIsolation=y
```

既定は `n` です。これはボックス全体の設定です。

## トークンの動作

Application Compartment は、Sandboxie の通常の制限付きプライマリ トークン置換、および通常の偽装トークンの検証とフィルター処理のパスをバイパスします。

これはそれ自体でプロセスを昇格させるものではありません。代わりに、プロセスは起動されたときのセキュリティ コンテキストを保持できます:

- 昇格されていないプロセスは昇格されないままです。
- 昇格されたトークンで起動されたプロセスは、その昇格されたコンテキストを保持できます。
- この設定は管理者または SYSTEM 特権を付与しません。

この動作は、別個の `OriginalToken` 設定の一部と重複しますが、Application Compartment はサンドボックス構成で `OriginalToken=y` を自動的に追加または有効にしません。

## Job オブジェクトの動作

Application Compartment プロセスは、Sandboxie の通常のルート Job オブジェクトの割り当てから除外されます。その結果、その Job オブジェクトを通じて実装されるボックス レベルのプロセス、メモリ、および CPU 制限は通常どおりには適用されません。

これは、プロセスが別のコンポーネントによって作成または割り当てられた Job オブジェクトに属することを妨げません。完全な Job オブジェクト モデルについては、[Job Objects](JobObjects.md) を参照してください。

## パス ポリシーの既定

Application Compartment は、3 つの特定の Sandboxie パス ポリシーの既定を緩和します:

- 通常の `AlwaysCloseForBoxed` 動作は適用されません。
- 通常の `DontOpenForBoxed` 動作は適用されません。
- `ProtectHostImages` は適用されません。

これらの変更は、すべてのリソース ルールが無視されることを意味しません。他の構成されたアクセス ルール、組み込みテンプレート ルール、およびアクティブなフィルター レイヤーが依然としてアクセスに影響を与えることがあります。

Sandboxie はまた、Application Compartment プロセス用の組み込み `TemplateAppCPaths` ルールを読み込みます。これらはこのボックスの種類用のテンプレート パス ポリシーであり、すべてのリソース分離を無効にするわけではありません。

## アクティブのままにできる分離

通常の Application Compartment 構成では:

- ファイルシステムとレジストリの仮想化はアクティブなままにできます。
- Sandboxie のファイル、レジストリ キー、およびカーネル オブジェクト ドライバー フィルターは、別途無効にしない限りアクティブなままです。
- 構成されたファイル、レジストリ、IPC、ネットワーク、および GUI ルールは依然として適用されることがあります。
- 名前付きオブジェクトの名前空間処理は、[Nt Namespace Isolation](NtNamespaceIsolation.md) などの設定の対象のままです。

`NoSecurityIsolation=y` だけでは、Sandboxie のファイル、キー、またはオブジェクト フィルターの無効化状態を設定しません。別個の [No Security Filtering](NoSecurityFiltering.md) 設定は、Application Compartment がアクティブな間にこれら 3 つのドライバー フィルターを無効にできます。

## 名前付きオブジェクトの名前空間オプション

Application Compartment は通常、Sandboxie の名前付きカーネル オブジェクト リダイレクションと NT ディレクトリ オブジェクト名前空間の処理を引き続き使用します。高度な構成では `UseAlternateIpcNaming=y` を使用して、通常の別個のディレクトリ オブジェクト名前空間を使用する代わりに、Sandboxie がリダイレクトする名前付きオブジェクトの命名戦略を変更できます。

`UseAlternateIpcNaming` は特に Application Compartment ボックスを対象としています。すべての IPC プロトコルの名前を変更したり、すべての IPC 制御を無効にしたりするものではありません。詳細については [Nt Namespace Isolation](NtNamespaceIsolation.md#alternate-ipc-naming) を参照してください。

## サポートされていない DynData フォールバック {#unsupported-dyndata-fallback}

互換性のある DynData が利用できない場合、現在のドライバー コードは影響を受けるプロセスを低減された分離の Application Compartment 状態に強制し、警告 `MSG_1207` を発行することがあります。これはドライバーのプロセス状態を変更しますが、サンドボックス構成に `NoSecurityIsolation=y` を書き込むことはありません。

## SandMan の構成

Application Compartment は SandMan でボックスの種類として選択できます。対応する高度な設定は次の場所にあります:

**Sandbox Options > Security Options > Security Isolation**

チェックボックスのラベルは **Disable Security Isolation** です。現在の SandMan のボックスの種類のセレクターはこのプリセットを **Application Compartment** と呼び、New Box Wizard はこれを **Application Compartment Box** と呼びます。SandMan はこのモードをサポーター機能として扱います。

## バージョン履歴

Application Compartment と `NoSecurityIsolation` は Sandboxie Plus 1.0.0 / Classic 5.55.0 で導入されました。Sandboxie Plus 1.8.0 は組み込みの Application Compartment アクセス ルールを `TemplateAppCPaths` に移動しました。

## 関連ページ

- [Application Compartment](../PlusContent/compartment-mode.md)
- [No Security Filtering](NoSecurityFiltering.md)
- [Nt Namespace Isolation](NtNamespaceIsolation.md)
- [Job Objects](JobObjects.md)
- [Sandboxie Ini](SandboxieIni.md)
