# Sandboxie Trace

Sandboxie は、互換性と分離ルールのトラブルシューティングのためにいくつかの独立したトレース メカニズムを提供します。その出力は共有のセッションごとのモニター バッファーに収集され、次を通じて表示できます:

* Sandboxie Plus の [Trace logging](../PlusContent/TraceLog.md)。
* Sandboxie Control Classic の [Resource Access Monitor](ResourceAccessMonitor.md)。

いずれかのビューアーを開くとモニター コンシューマーがアクティブになります。以下で説明するすべての詳細トレース オプションが自動的に有効になるわけではありません。一部のベースライン リソース アクティビティは追加設定なしで利用できますが、`ApiTrace`、`HookTrace`、`DebugTrace`、および `ErrorTrace` などのオプションは、特殊化されたまたは大量の診断情報を追加します。

モニター コンシューマーがアクティブでない場合、共有モニター バッファーは維持されず、そのメッセージは後で表示するために保持されません。明示的に有効にされたトレース オプションは、ビューアーが閉じている間もフックをインストールしたり、プロセス側の診断作業を実行したりできます。

モニターは、選択された Sandboxie メッセージを Windows イベント ログに送信する [Log Message Events](LogMessageEvents.md) とは別個です。クラッシュ ダンプとプロセス起動の一時停止は [Crash and Debugger Diagnostics](CrashAndDebuggerDiagnostics.md) で扱います。

## リソース アクセスのトレース

リソース トレース設定は、サンドボックス化されたアプリケーションが失敗する理由を説明する可能性のあるファイル、レジストリ、IPC、および関連する操作を特定するのに役立ちます。ドライバー リソース フィルターは、特定の設定がサポートする場合に次の実用的な値を使用します:

| 値 | 意味 |
| ----- | ------- |
| `A` | 成功または許可された操作 |
| `D` | 失敗または拒否された操作 |
| `I` | サポートされている場合の無視されたデバイス操作 |
| `*` | 広範なトレース |

`AD` などの組み合わせがサポートされ、`ad` などの小文字の組み合わせはこのフィルターを使用する設定で受け入れられます。これらの文字はすべてのトレース オプションによって一様に実装されているわけではありません。

### FileTrace

リソース モードでは、`FileTrace` はファイル、ディレクトリ、ボリューム、およびデバイスのアクティビティを記録します:

```ini
FileTrace=A
FileTrace=D
FileTrace=AD
FileTrace=I
FileTrace=*
```

`A` は成功または許可されたアクティビティを選択し、`D` は失敗または拒否されたアクティビティを選択し、`I` は無視されたデバイス クラスを選択します。`*` は広範なファイル リソース トレースを要求します。

同じレガシー設定名には、別個の高度な SbieDll ファイル API トレースの用途もあります:

```ini
FileTrace=y
FileTrace=program.exe,y
```

この形式は詳細なファイル API 呼び出しレコードを追加し、実行可能ファイルに限定できます。リソース フィルター形式とイメージ修飾ブール形式は、1 つの統合された構文としてではなく、同じレガシー名の別個の診断用途として扱ってください。

### KeyTrace、PipeTrace、および IpcTrace {#keytrace-pipetrace-and-ipctrace}

これらの設定は、許可/成功および拒否/失敗のリソース フィルターをサポートします:

```ini
KeyTrace=AD
PipeTrace=AD
IpcTrace=AD
```

* `KeyTrace` はレジストリ キー操作を記録します。
* `PipeTrace` は名前付きパイプおよびメールスロット操作を記録します。
* `IpcTrace` は他の IPC オブジェクトおよびプロセス間操作へのアクセスを記録します。

`I` は現在これらの設定に対して意味のある役割を持ちません。

### GuiTrace

`GuiTrace` はレガシー設定です。その直接の GUI トレース実装は古い Windows XP 時代の Win32k フック パスに属します。現在サポートされている Windows バージョンは、このオプションを通じて同等の実装を提供しません。GUI およびウィンドウ クラス関連のイベントは他のモニター メカニズムを通じて依然として現れることがありますが、Windows 10 または Windows 11 で `GuiTrace` を有効にしても歴史的な GUI トレースが再現されることは期待すべきではありません。

### ClsidTrace

`ClsidTrace` は詳細な COM 操作レコードを追加します。現在のランタイムは、`A`、`D`、および `I` をリソース フィルターとして解釈するのではなく、明示的な空でないレガシー値を有効として扱います。利用可能な場合は SandMan のチェックボックスを使用するか、手動で構成したトレースを無効にするには明示的なエントリを削除してください。

### NetFwTrace

`NetFwTrace` は現在の設定メタデータで無効としてマークされています。限られたユーザー モード ネットワーク診断の残骸が残っていますが、古い WFP/ファイアウォール ログ パスは機能的な完全なファイアウォール トレースではありません。**Network Firewall** トレース チェックボックスが引き続き SandMan に表示されることがありますが、一般的な WFP パケットまたはファイアウォール決定ロガーとして扱うべきではありません。手動無効化形式として `NetFwTrace=n` に依存するのではなく、明示的なエントリを削除してください。

## 拒否されたリソースのトラブルシューティング

拒否されたトレース レコードは、それ自体でアクセスが許可されるべきであることを意味しません。多くの拒否された操作は予期されたものであり無害です。構成の変更は、イベントがアプリケーションの失敗と妥当に関連している場合にのみテストし、可能な限り最も狭いリソース固有のルールを優先してください。ホスト リソースを開くとサンドボックスの分離が低下することがあります。

リソース タイプを使用して関連する構成ファミリを特定します:

| トレース リソース | 関連するアクセス設定 |
| -------------- | ----------------------- |
| ファイル、ディレクトリ、ボリューム、およびデバイス | [Open File Path](OpenFilePath.md)、[Closed File Path](ClosedFilePath.md)、[Read File Path](ReadFilePath.md) |
| レジストリ キー | [Open Key Path](OpenKeyPath.md)、[Closed Key Path](ClosedKeyPath.md)、[Read Key Path](ReadKeyPath.md) |
| 名前付きパイプおよびメールスロット | [Open Pipe Path](OpenPipePath.md) |
| IPC およびプロセス間オブジェクト | [Open Ipc Path](OpenIpcPath.md)、[Closed Ipc Path](ClosedIpcPath.md) |
| GUI およびウィンドウ アクセス | [Open Win Class](OpenWinClass.md) |
| COM クラス | [Open Clsid](OpenClsid.md)、[Closed Clsid Path](ClosedClsid.md) |

たとえば、`\BaseNamedObjects\Xyzzy` に対する拒否された IPC イベントが再現可能な失敗の時点で繰り返し現れ、そのオブジェクトへのアクセスをテストする明確な理由がある場合:

```ini
[DefaultBox]
OpenIpcPath=\BaseNamedObjects\Xyzzy
```

実用的なテストは次のとおりです:

1. Trace Logging がアクティブな間に問題を再現します。
2. 失敗付近の拒否されたイベントを見つけ、そのリソース タイプを特定します。
3. その特定のイベントが失敗を妥当に説明するかどうかを判断します。
4. 説明する場合は、最も狭い適切なルールを一時的に追加します。
5. 必要に応じて構成を再読み込みまたは適用し、影響を受けるアプリケーションを再起動して、テストを再現します。
6. 動作を比較し、問題を解決しない場合はルールを削除します。

一般的なトラブルシューティング方法として広範な `Open*` ワイルドカードを使用しないでください。トレース カテゴリは、特定の 1 つのアクセス ルールが必要であることを機械的に決定するものではありません。

## API 呼び出しのトレース

### ApiTrace

`ApiTrace` は、Sandboxie の共通 SbieDll フック メカニズムを通過する呼び出しを記録します:

```ini
ApiTrace=y
ApiTrace=program.exe,y
```

これはイメージ対応ですが、アプリケーションが使用するすべての Windows API をトレースするわけではありません。出力はモニターに API 呼び出しレコードとして表示されます。このオプションは大量で負荷が高い可能性があるため、トラブルシューティング中にのみ有効にし、変更後は影響を受けるプロセスを再起動してください。

### ApiTraceDll

`ApiTraceDll` は、選択されたモジュール内の名前付きエクスポートに対するトレース専用フックを追加することにより、`ApiTrace` を拡張します。複数のエントリがサポートされます:

```ini
ApiTraceDll=kernel32.dll
ApiTraceDll=user32.dll
```

完全なパスではなくモジュールのベース名を使用してください。モジュールの照合は大文字小文字を区別しません。すべてのエクスポートがトレース可能であることは保証されません。

### ApiSkipTrace

`ApiSkipTrace` は一致する関数名プレフィックスを除外します。主に `ApiTraceDll` で要求された追加のエクスポート カバレッジから除外します:

```ini
ApiSkipTrace=Nt
```

複数のエントリがサポートされます。プレフィックスの照合は大文字小文字を区別します。これは Sandboxie の通常のフックに対する普遍的な抑制ルールではありません。

呼び出しレコードではなくインストールの診断については [Hook Trace](HookTrace.md) を参照してください。

## システムコールと内部トレース

### CallTrace

`CallTrace` はドライバーのシステムコール トレースであり、一般的な Windows API トレースではありません:

```ini
CallTrace=A
CallTrace=D
CallTrace=AD
CallTrace=*
```

`A` はトレース パスに到達する傍受された呼び出しを広範に記録します。`D` は成功以外の NTSTATUS を返す呼び出しを追加します。これらの文字は、普遍的な許可対拒否の分類として解釈すべきではありません。SandMan の **Syscall Trace** チェックボックスは `CallTrace=*` を書き込みます。

### CallTraceEx

`CallTraceEx` は、Windows プロセス インストルメンテーション コールバックに基づく別個の高度なシステムコール トレース メカニズムを要求します。現在、構成された空でない値はそれを要求します。最新の Windows を対象としており、すべてのアーキテクチャまたは構成でサポートされているわけではなく、専用の SandMan チェックボックスはありません。

### SbieTrace

`SbieTrace` は、SbieDll と他の Sandboxie コア コンポーネント間の相互作用のための選択された診断を有効にします。その出力は Debug タイプのレコードとして表示されます。完全な内部実行トレースではありません。

### DebugTrace

`DebugTrace` は、アプリケーションの通常のデバッグ出力呼び出しを保持しつつ、アプリケーションの `OutputDebugString` 出力をモニターにキャプチャします。任意の長さの文字列のロスレス キャプチャとして扱うべきではありません。

### ErrorTrace

`ErrorTrace` は、現在フックされているパスを通じて観測されたゼロ以外の Win32 の最後のエラーの割り当てを記録します。非常にノイズが多くなることがあり、すべての Windows エラーまたはすべての NTSTATUS を対象とするわけではありません。

## DNS トレース {#dns-tracing}

`DnsTrace` は、Sandboxie の DNS 互換性およびフィルタリング レイヤーが使用する傍受された Winsock サービス検索パスを記録します。要求名、IPv4 および IPv6 の結果、検索エラーまたは完了、およびその機能が構成されている場合に `NetworkDnsFilter` によって影響を受ける応答を表示できます。

すべての DNS API をトレースしたり、DNS パケットをキャプチャしたり、独自の直接リゾルバーを使用するアプリケーションを対象としたりするものではありません。照会されたホスト名と返されたアドレスが Trace Log に表示されることがあるため、共有する前にトレース出力を確認してください。`DnsTrace` は `NetworkDnsFilter` を有効にしません。

現在のランタイムは明示的な空でないレガシー値を有効として扱います。利用可能な場合は SandMan のコントロールを使用するか、`DnsTrace=n` に依存するのではなく手動で無効にするにはエントリを削除してください。

`DnsTrace` は Sandboxie Plus 1.14.0 および Sandboxie Classic 5.69.0 で導入されました。

## スタック トレース {#stack-traces}

`MonitorStackTrace` は事実上グローバルなモニター オプションであり、既定では無効です。モニター バッファーが作成される前に有効にすると、共通モニター パスを通過するレコードにスタック アドレスが添付されます:

```ini
[GlobalSettings]
MonitorStackTrace=y
```

すべての診断ソースがスタックを含むことは保証されず、スタックは不完全であったり、シンボル化できないフレームを含んでいたりすることがあります。SandMan はシンボルを非同期で解決し、DbgHelp およびシンボル サポートを使用またはインストールすることがあります。スタック キャプチャとシンボル解決は診断コストを追加し、シンボルのダウンロードはネットワーク アクセスを伴うことがあります。

SandMan はこの設定を Trace Log の **Show Stack Trace** を通じて公開します。変更してもアクティブなモニター バッファーは再構築されません。確実に有効化または無効化するには:

1. **Show Stack Trace** を変更します。
2. Trace Logging を停止します。
3. Trace Logging を再度開始します。

サービスまたはドライバーの再起動は通常必要ありません。`MonitorStackTrace` は Sandboxie Plus 1.9.6 および Sandboxie Classic 5.64.6 で導入されました。

## モニター バッファー サイズ {#monitor-buffer-size}

`TraceBufferPages` は共有トレース/モニター バッファーの割り当てサイズを制御します。現在の構成された既定は `256` で、値は監視の開始時に読み取られます:

```ini
[GlobalSettings]
TraceBufferPages=2560
```

この例はより大きなバッファーを要求します。文書化されたバイトまたは MiB 換算を表すものではありません。より大きな値は追加のメモリを犠牲にしてオーバーフローを低減できます。バッファーがこれ以上レコードを受け入れられない場合、イベントがドロップされ、Sandboxie がモニター バッファーのオーバーフローを報告することがあります。

監視がアクティブな間に設定を変更しても現在のバッファーはサイズ変更されません。変更後は Trace Logging または Resource Access Monitor を停止して再起動してください。

## 関連するモニター コントロール {#related-monitor-controls}

`DisableResourceMonitor=y` は、影響を受けるサンドボックスまたはプロセスの多くの通常のユーザー モードおよびリソース モニターの送信を抑制します。明示的に有効にされたすべてのドライバー トレースが抑制されることを保証するものではありません。

`MonitorAdminOnly` は共有モニターのアクティブ化を管理者に制限し、モニター制御チェックに対して事実上グローバルです。[Monitor Admin Only](MonitorAdminOnly.md) を参照してください。

## SandMan 構成

**View > Trace Logging** を通じてライブ ビューアーを開きます。ボックスごとのトレース コントロールは **Sandbox Options > Advanced Options > Tracing** にあり、現在次を含みます:

* Disable Resource Monitor。
* Syscall、File、Pipe、Registry Key、IPC、GUI、COM Class、Network Firewall、および DNS のトレース。
* Hook、API、Debug Output、および Error のトレース。

専用のコントロールがない高度な設定には、`ApiTraceDll`、`ApiSkipTrace`、`CallTraceEx`、`SbieTrace`、および `TraceBufferPages` が含まれます。`MonitorStackTrace` は、ボックスごとのトレース チェックボックス グループではなく、Trace Log の **Show Stack Trace** によって制御されます。

## 変更の適用

多くのトレース設定は各サンドボックス化されたプロセスによって初期化またはキャッシュされます。変更後は影響を受けるプロセスを再起動してください。`MonitorStackTrace` および `TraceBufferPages` を含む共有モニター バッファーに影響するオプションは、新しいバッファーが作成されるように監視を停止して再起動する必要があります。

明示的に有効にされたトレース設定は、ビューアーが開いていない間もフックをインストールしたり、プロセス側の作業を実行したりすることがあります。アクティブな監視のオーバーヘッドは、有効な診断とイベント量によって異なります。

## バージョン履歴

* `ApiTrace`、`ApiTraceDll`、および `ApiSkipTrace` はバージョン 1.13.0 で設定メタデータに追加されました。
* `DnsTrace` は Sandboxie Plus 1.14.0 および Sandboxie Classic 5.69.0 で導入されました。
* `CallTraceEx` はバージョン 1.14.3 で追加されました。
* `HookTrace` は Sandboxie Plus 1.15.5 および Sandboxie Classic 5.70.5 で導入されました。

## 関連ページ

* [Trace logging](../PlusContent/TraceLog.md)
* [Resource Access Monitor](ResourceAccessMonitor.md)
* [Hook Trace](HookTrace.md)
* [Crash and Debugger Diagnostics](CrashAndDebuggerDiagnostics.md)
* [Sandboxie Ini](SandboxieIni.md)
