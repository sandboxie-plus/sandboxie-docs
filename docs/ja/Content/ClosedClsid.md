# Closed Clsid

_ClosedClsid_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、v0.5.3a / 5.45.2 以降で利用できます。Sandboxie の傍受されたクライアント側アクティブ化パスで、指定された COM クラス識別子をブロックします。

例:

```ini
[DefaultBox]
ClosedClsid={8BC3F05E-D86B-11D0-A075-00C04FB68820}
```

この WMI クラス ルールは、その CLSID に対する一致する傍受された COM アクティブ化の試行を拒否します。Windows Management Instrumentation を使用するすべての方法がブロックされることを確立するものではありません。

## プログラム修飾ルール

[Open Clsid](OpenClsid.md) と同様に、この設定は単純な `{CLSID}`、または `program.exe,{CLSID}` もしくは `<GroupName>,{CLSID}` の値を受け入れます。省略可能なセレクターは、サンドボックス化された呼び出し元プロセスと照合されます。実行可能ファイル名の照合は完全一致で、大文字と小文字を区別しません。ワイルドカードおよび否定のプログラム セレクターはサポートされていません。ルールを 1 つの呼び出し元に制限しない場合はプレフィックスを省略してください。ここでは `*` は全プログラム セレクターではありません。[Process Groups](ProcessGroup.md) はネストできます。

## スコープと優先順位

Sandboxie は、傍受された `CoGetClassObject`、`CoCreateInstance`、および `CoCreateInstanceEx` パスで `ClosedClsid` をチェックします。一致すると、一致する `OpenClsid` ルールが COM ブローカーを選択する前に `E_ACCESSDENIED` を返します。これはパス固有の優先順位ルールです。傍受された `CoGetObject` 昇格モニカー パスは同じクローズ リスト チェックを実行せず、SbieSvc ブローカーは `ClosedClsid` を参照せずにオープン適格性をチェックします。この設定をすべての COM または RPC 経路に対する万能のブロックとして依存しないでください。

有効な値には、ボックス構成、該当する有効なテンプレート、および `[GlobalSettings]` フォールバックを含めることができます。SandMan の無効な行はアクティブなルールではありません。クライアント側のリストは初期化後にキャッシュされるため、`ClosedClsid` を変更した後は影響を受けるサンドボックス化されたアプリケーションを再起動してください。このクライアント側設定のために、定期的なサービスの再起動や Windows の再起動は必要ありません。

Sandboxie Plus では、**Sandbox Options > Resource Access > COM > Add COM Object** を使用し、Access 列で **Closed** を選択します。エディターには Program 列もあります。
