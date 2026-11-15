# No Security Filtering

_NoSecurityFiltering_ は [Application Compartment](../PlusContent/compartment-mode.md) ボックス用の高度な互換性設定です。有効な場合、Sandboxie のドライバーはボックス内のプロセスに対してファイル、レジストリ キー、およびカーネル オブジェクト フィルターを無効にします。

> [!WARNING]
> この設定は、既に通常のトークン制限と Sandboxie Job オブジェクトの割り当てをバイパスするモードで、3 つの中核的なドライバー強制レイヤーを削除します。これらのフィルターを無効にする必要がある互換性を持つ信頼できるアプリケーションにのみ使用してください。

## 前提条件と構文

```ini
[DefaultBox]
NoSecurityIsolation=y
NoSecurityFiltering=y
```

両方の設定のコンシューマー フォールバックは `n` です。`NoSecurityFiltering` の複合的な効果には、プロセスがドライバーの Application Compartment 状態にあることが必要で、通常は `NoSecurityIsolation=y` によって選択されます。標準の分離モードのままのプロセスには複合的な効果はありません。ドライバーがその状態に入る例外的な方法については、[unsupported DynData fallback](NoSecurityIsolation.md#unsupported-dyndata-fallback) を参照してください。

## 何を無効にするか

両方の設定が有効な場合、ドライバーは次によって個別に制御される同じ 3 つの内部フィルター無効化状態を設定します:

- [Disable File Filter](DisableFileFilter.md);
- [Disable Key Filter](DisableKeyFilter.md);
- [Disable Object Filter](DisableObjectFilter.md)。

個々の設定は別個の構成キーのままです。`NoSecurityFiltering` はそれらのキーをサンドボックス構成に書き込んだり自動的に追加したりしません。Application Compartment プロセスに対して、実行時に同等の 3 つの状態が有効になるようにします。

影響を受けるレイヤーは、特に Sandboxie のドライバー レベルの次です:

- ファイル フィルター。
- レジストリ キー フィルター。
- カーネル オブジェクト フィルター。

## 何を意味しないか

`NoSecurityFiltering` は、すべての Sandboxie フック、ルール、またはサービスのための万能スイッチではありません。この設定は、すべての Sandboxie セキュリティまたは仮想化動作を無効にするものとして説明すべきではありません。特に、その現在のドライバー実装自体は、すべての SbieDll フック、GUI 制限、ネットワーク コントロール、サービス動作、または構成ルールを無効にしません。

したがって他のメカニズムが関連し続けることがありますが、Application Compartment と無効化されたドライバー フィルターの組み合わせは、標準のサンドボックスよりも大幅に少ない保護しか提供しません。

## SandMan の構成

コントロールは次の場所にあります:

**Sandbox Options > Security Options > Security Isolation**

その正確なラベルは **Disable Security Filtering (not recommended)** です。SandMan は **Disable Security Isolation** が選択されている間のみこのチェックボックスを有効にします。

## バージョン履歴

`NoSecurityFiltering` は Application Compartment とともに Sandboxie Plus 1.0.0 / Classic 5.55.0 で導入されました。

## 関連ページ

- [No Security Isolation](NoSecurityIsolation.md)
- [Application Compartment](../PlusContent/compartment-mode.md)
- [Disable File Filter](DisableFileFilter.md)
- [Disable Key Filter](DisableKeyFilter.md)
- [Disable Object Filter](DisableObjectFilter.md)
- [Sandboxie Ini](SandboxieIni.md)
