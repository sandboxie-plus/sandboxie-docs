# Disable Object Filter

_DisableObjectFilter_ は [Sandboxie Ini](SandboxieIni.md) の高度なサンドボックス設定です。影響を受けるサンドボックス化されたプロセスに対して、通常は同じサンドボックス外のターゲットへのプロセスおよびスレッド ハンドル アクセスを制限するカーネル オブジェクト マネージャー コールバック ポリシーを緩和します。

> [!WARNING]
> この設定は、Sandboxie が通常制限するプロセスおよびスレッド ハンドルの権限を公開し、サンドボックス化されたプログラムがサンドボックス外のプロセスを検査、変更、または制御する能力を高める可能性があります。Sandboxie はこのオプションを安全でないものとして分類しています。すべての Sandboxie 分離を無効にするわけではありませんが、特定の互換性要件が保護の低下を正当化する場合にのみ使用してください。

## 構成

```ini
[DefaultBox]
DisableObjectFilter=y
```

構文は次のとおりです:

```ini
DisableObjectFilter=y|n
```

- `y` はプロセスごとのフィルター例外を有効にします。
- `n` (既定) は通常のコールバック ポリシーを維持します。

この設定は有効なサンドボックス構成から解決され、各サンドボックス化されたプロセスが初期化されるときに保存されます。したがって、通常のテンプレートおよびグローバル フォールバックが有効な値に寄与できますが、現在のコンシューマーはこの設定に対して実行可能ファイルで修飾されたマッチングを提供しません。

## 無効にするもの

サンドボックス化された呼び出し元が `DisableObjectFilter=y` でカーネル コールバックのプロセス/スレッド ポリシーを通過する場合、Sandboxie はその呼び出し元に対する通常の送信制限を適用する代わりに、要求されたアクセスを保持します。

影響を受けるコールバックは、プロセスおよびスレッド ハンドルの作成と複製を対象とします。一般的な設定名にもかかわらず、あらゆる種類の Windows オブジェクトに対するスイッチではありません。

## 無効にしないもの

`DisableObjectFilter=y` は次を行いません:

- グローバル オブジェクト マネージャー コールバックの登録を解除する;
- 有効な構成でそれを有効にしていない他のサンドボックス化されたプロセスのコールバック フィルタリングを無効にする;
- ファイルまたはレジストリのフィルタリングを無効にする;
- すべての IPC 名前空間またはリソース アクセス メカニズムを無効にする;
- すべての Sandboxie プロセス/スレッド アクセス チェックを無効にする;
- プロセスを非サンドボックス化する。

現在のドライバーはシステムコール固有のプロセス/スレッド チェックを保持しています。グローバル コールバックが利用できない場合、それらのパスの一部は共有アクセス ポリシーを直接適用し、プロセスごとの `DisableObjectFilter` 状態を一律に参照しません。したがって、この設定は、現在のすべてのプロセス/スレッド アクセス制限に対する万能スイッチとして扱ってはなりません。これは、フォールバックが常にまったく同じ構造になることを保証するものではなく、実装上の境界です。

## グローバル コールバック設定

オブジェクト マネージャー コールバック フィルタリングは既定でグローバルに有効です。ユーザーは通常の現在の動作のために `EnableObjectFiltering=y` を追加する必要はありません。

グローバル コントロールとサンドボックスごとのコントロールは同等ではありません:

| 設定 | スコープ | オブジェクト マネージャー コールバック | 結果 |
| --- | --- | --- | --- |
| `EnableObjectFiltering=n` | グローバル | 登録解除 | すべてのサンドボックスのコールバック レイヤーを削除します。システムコール固有のチェックは残ることがあります |
| `DisableObjectFilter=y` | 影響を受けるサンドボックス化されたプロセス | 引き続きインストール済み | それらのプロセスの送信コールバック フィルタリングを緩和します |

グローバルな既定、コールバック スコープ、およびシステムコール フィルターの区別については [Enable Object Filtering](EnableObjectFiltering.md) を参照してください。

## ホストからサンドボックスへの保護

コールバックには、サンドボックス化されていないホスト プロセスがサンドボックス化されたプロセスまたはスレッドへのハンドルを要求するための別個のパスがあります。このパスは [Confidential Box](ConfidentialBox.md) および `DenyHostAccess` や `ProtectAdminOnly` を含む設定をサポートします。

ホストからサンドボックスへの保護は別個に、送信 `DisableObjectFilter` 例外より前に評価されます。したがって、ターゲット サンドボックスで `DisableObjectFilter` を有効にしても、グローバル コールバック レイヤーがアクティブな間は、それ自体でホスト プロセスがそのサンドボックスのプロセスに無制限にアクセスできるようにはなりません。

## Application Compartment と NoSecurityFiltering

[Application Compartment](NoSecurityIsolation.md) モードは、構成で `DisableObjectFilter=y` を自動的に設定しません。

新しい Application Compartment プロセスに対して、[No Security Filtering](NoSecurityFiltering.md) は対応するファイル、レジストリ キー、およびオブジェクト フィルターの無効状態を実行時に有効にします。これには `DisableObjectFilter` によって直接制御される同じプロセスごとのオブジェクト フィルター状態が含まれますが、グローバル コールバックの登録を解除したり、他のサンドボックスを変更したりはしません。

## IPC プロセス ルール

通常のオブジェクト フィルタリングでは、次のようなプロセス ターゲット形式により、サンドボックス全体でフィルターを無効にすることなく特定のアクセスを許可または拒否できます:

```ini
OpenIpcPath=$:target.exe
ReadIpcPath=$:target.exe
ClosedIpcPath=$:target.exe
```

[Open IPC Path](OpenIpcPath.md)、[Read IPC Path](ReadIpcPath.md)、および [Closed IPC Path](ClosedIpcPath.md) を参照してください。これらのルールは、`DisableObjectFilter=y` よりも狭い互換性例外を提供できます。

## SandMan 構成

SandMan は `DisableObjectFilter` 専用のサンドボックス チェックボックスを提供していません。これは高度な INI/構成オプションです。SandMan の安全でない構成の検出はこの設定を認識しますが、表示される状態では別のボックス状態の警告が優先されることがあります。

## 変更の適用

この設定は、プロセスの初期化中にサンドボックス化された各プロセスのドライバー状態に保存されます。構成の再読み込みは、既に実行中のプロセスのその状態を書き換えません。

`DisableObjectFilter` を変更した後は、影響を受けるサンドボックス化されたプロセスを再起動してください。変更を一貫してテストするときは、サンドボックス化されたプロセス ツリーを再起動するのが適切です。Windows の再起動は通常必要ありません。

## バージョン履歴

設定メタデータには、`DisableObjectFilter` が Sandboxie Plus 0.9.2 で追加されたと記載されています。対応するプロセス状態の割り当てはその古いタグではアクティブではありませんでした。アクティブなプロセスごとのオプトアウトとオブジェクト マネージャー コールバック機能は、Sandboxie Plus 1.0.0 / Classic 5.55.0 で存在し、公開文書化されていました。

コールバック レイヤーは Sandboxie Plus 1.0.16 / Classic 5.55.16 で既定で有効になったため、`EnableObjectFiltering=y` を追加するという歴史的な要件はもはや適用されません。

## 関連ページ

- [Enable Object Filtering](EnableObjectFiltering.md)
- [No Security Filtering](NoSecurityFiltering.md)
- [No Security Isolation](NoSecurityIsolation.md)
- [Confidential Box](ConfidentialBox.md)
- [Disable File Filter](DisableFileFilter.md)
- [Disable Key Filter](DisableKeyFilter.md)
- [Sandboxie Ini](SandboxieIni.md)
