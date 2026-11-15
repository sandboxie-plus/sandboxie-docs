# BlockInterferePower

_BlockInterferePower_ は Sandboxie Plus 1.13.2 以降で使用可能な [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。既定では無効で、現在は Experimental としてマークされています。

例:

```ini
[DefaultBox]
BlockInterferePower=y
```

有効な場合、この設定はサンドボックス化されたプロセスが使用する選択されたメカニズムがホストの電源およびセッション動作に干渉することを防ぎます。完全な電源管理の分離ではありません。

## SetThreadExecutionState

この設定が有効な間、Sandboxie は `SetThreadExecutionState` への呼び出しをブロックします。実装は個々の実行状態フラグを選択的に許可しません。

その結果、`ES_SYSTEM_REQUIRED`、`ES_DISPLAY_REQUIRED`、または `ES_AWAYMODE_REQUIRED` などのフラグを使用する要求は、この API を通じてホスト システムまたはディスプレイをアクティブに保ちません。

この動作は `SetThreadExecutionState` に限定されます。`PowerSetRequest` などの最新の電源要求メカニズムは対象外です。

## シャットダウン動作

この設定は 2 つのシャットダウン関連パスを対象とします:

- `ShutdownBlockReasonCreate` がブロックされるため、アプリケーションはその API を通じてシャットダウン ブロック理由を登録できません。
- 傍受された `WM_QUERYENDSESSION` メッセージについて、Sandboxie はアプリケーションの元のハンドラーを呼び出さずに成功を返します。これにより、アプリケーションはそのパスを通じてシャットダウンを拒否できなくなります。

_BlockInterferePower_ は Windows のシャットダウンをブロックしません。これらのケースでは、サンドボックス化されたアプリケーションがシャットダウンを防ぐ能力を低減します。一般的にシャットダウン、再起動、またはサスペンド API をブロックするものではありません。

## 制限事項

この設定はすべての電源管理メカニズムを対象としません。現在の実装は次のものにこの設定を適用しません:

- `PowerCreateRequest`
- `PowerSetRequest`
- `PowerClearRequest`
- `SetSuspendState`
- 電源プラン API

その他のシャットダウンおよびセッション管理 API が対象であると仮定すべきではありません。

## 互換性

影響を受ける API を使用するアプリケーションは、この設定が有効な場合に異なる動作をすることがあります。例:

- `SetThreadExecutionState` を使用するメディア プレーヤーは、ディスプレイまたはシステムをスリープ状態に保てなくなることがあります。
- その API を使用するゲームやプレゼンテーション ソフトウェアも同じ動作を失うことがあります。
- それに依存する長時間実行アプリケーションは、スリープを抑制できなくなることがあります。
- アプリケーションは `ShutdownBlockReasonCreate` を通じてシャットダウン ブロック理由を登録できません。
- アプリケーションは傍受された `WM_QUERYENDSESSION` パスを通じてセッション終了を拒否できません。

これらの影響は、対象となるメカニズムを使用するアプリケーションにのみ適用されます。

## コンパートメント モード

この設定は通常のセキュリティ分離ボックスを対象としており、コンパートメント モードで完全な機能としてサポートされていません。

## ランタイムとスコープ

主要な制限はサンドボックス化されたプロセスが初期化されるときにインストールされます。プロセスが既に開始された後に設定を有効にしても、遡ってインストールされません。したがって、オプションを変更した後は既存のサンドボックス化されたアプリケーションを再起動する必要があります。

一部の個々のパスは現在の構成を動的に参照することがありますが、影響を受けるサンドボックス化されたアプリケーションを再起動することが変更を適用する確実な方法です。

これらの制限は主にサンドボックス化されたプロセス内のユーザー モード API 傍受を通じて実装されています。カーネル強制の保護として、または代替のフックされていない API を対象とするものとして説明すべきではありません。

## Sandboxie Plus インターフェイス

オプションは次にあります:

**Sandbox Options > General Options > Restrictions > Prevent sandboxed processes from interfering with power operations (Experimental)**

既定ではチェックされていません。セキュリティ分離が無効な場合、インターフェイスはこのオプションを無効にします。

## バージョン履歴

_BlockInterferePower_ は Sandboxie Plus 1.13.2 で導入され、後にインターフェイスと構成の永続化のメンテナンスを受けました。その既定は無効のままです。

## 関連設定

- [Sandboxie Ini](SandboxieIni.md)
- [BlockInterferenceControl](BlockInterferenceControl.md)
