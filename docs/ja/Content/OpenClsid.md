# Open Clsid

_OpenClsid_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie の COM 処理が、仲介パスを通じて指定されたホスト COM クラスにアクセスを試みることを可能にします。コンポーネントは依然としてインストールされている必要があり、Windows COM のアクセス許可、サーバーの動作、および他の Sandboxie の制限がアクティブ化を妨げることがあります。

例:

```ini
[DefaultBox]
OpenClsid={D713F357-7920-4B91-9EB6-49054709EC7A}
```

この例は HP Universal Printer Status Monitor のポップアップ コンポーネントを識別します。その CLSID をサンドボックスに対して開いているものとして扱いますが、すべてのシステムでそのコンポーネントをアクティブ化できることを保証するものではありません。

## プログラム修飾ルール

オプションのプログラム名または [Process Group](ProcessGroup.md) を CLSID の前に置くことができます:

```ini
OpenClsid=program.exe,{CLSID}
OpenClsid=<GroupName>,{CLSID}
```

`{CLSID}` は有効なクラス識別子のプレースホルダーです。通常のクライアント側 COM 処理では、プレフィックスは COM サーバーではなくサンドボックス化された**呼び出しプロセス**を選択します。実行可能ファイル名は正確に、大文字と小文字を区別せずに一致します。この設定はワイルドカードまたは否定のプログラム セレクターをサポートしません。特定の呼び出し元に制限されないルールにはプレフィックスを省略してください。ここでは `*` は全プログラム セレクターではありません。プロセス グループは他のグループを含むことができます。

プログラム プレフィックスはクライアント側のアクティブ化処理をフィルター処理しますが、Sandboxie の COM ブローカーは開いている CLSID をボックス スコープで評価します。したがって、プログラム修飾された `OpenClsid` ルールは、完全な実行可能ファイルごとの承認境界では**ありません**。無関係なサンドボックス化されたプログラムが自動的にアクティブ化に成功するわけではありません。通常のインターセプトされたクライアント パスは、ブローカーを選択する前に、通常は一致しない呼び出し元をフィルター処理し、他のアクセス条件も依然として適用されます。

## 構成と変更

有効な `OpenClsid` 値は、ボックス、該当する有効なテンプレート、または `[GlobalSettings]` フォールバックから取得できます。SandMan の無効な行はアクティブなルールではありません。サンドボックス化されたプロセスはそのクライアント側 CLSID リストをキャッシュします。設定を変更した後は、影響を受けるサンドボックス化されたアプリケーションを再起動してください。ブローカーは通常の構成の再読み込み後に後続の要求のためにそのボックス レベルの開いているリストを再構築しますが、これは実行中のサンドボックス化されたプロセスで既にキャッシュされているリストを更新するものではありません。

インターセプトされた `CoGetClassObject`、`CoCreateInstance`、および `CoCreateInstanceEx` パスでは、一致する [Closed Clsid](ClosedClsid.md) ルールが開いているルールの前にチェックされます。この優先順位はすべての COM アクティブ化ルートに一般化すべきではありません。

Sandboxie Plus では、**Sandbox Options > Resource Access > COM > Add COM Object** を使用し、Access 列で **Open** を選択し、オプションで Program を選択します。別個の **Don't use virtualized COM, Open access to hosts COM infrastructure (not recommended)** チェックボックスは COM ルーティングをより広範に変更します。1 つの `OpenClsid` エントリを追加することとは同等ではありません。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Resource Access > COM Access](ResourceAccessSettings.md#com-access)。
