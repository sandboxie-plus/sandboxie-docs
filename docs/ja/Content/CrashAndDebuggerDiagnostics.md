# クラッシュおよびデバッガー診断

Sandboxie のクラッシュ ダンプおよびデバッガー待機オプションは、[トレース ログ監視](SandboxieTrace.md)とは別個です。ミニダンプ設定は、対象となる未処理のクラッシュ後にファイルを作成し、デバッガー待機設定は、デバッガーがアタッチできるように Sandboxie DLL の初期化中に一致するプロセスを早期に一時停止します。

## ミニダンプ クラッシュ診断

### EnableMiniDump

`EnableMiniDump` はイメージ認識であり、既定で無効です。

```ini
EnableMiniDump=y
EnableMiniDump=program.exe,y
```

一致するサンドボックス化されたプロセスの場合、Sandboxie は Windows DbgHelp の `MiniDumpWriteDump` サポートを使用するプロセス ローカルの未処理例外ダンプ ハンドラーをインストールします。ダンプは、このトップレベルの未処理例外パスに到達したクラッシュに対してのみ生成されます。この設定は、すべてのクラッシュまたは終了方法に対してダンプを保証するものではなく、サンドボックス化されていない SandMan、SbieSvc、SbieDrv、またはすべての Sandboxie コンポーネントを自動的にカバーするものでもありません。

ダンプ ファイルはサンドボックス内に次のように書き込まれます。

```text
<sandbox root>\<image-name>.<unique counter>.dmp
```

サフィックスは実行時に生成される一意の値です。クラッシュしたサンドボックス化されたプロセスは、その現在のアクセス許可を使用してファイルを書き込みます。

`EnableMiniDump` を変更した後は、一致するプロセスを再起動してください。`EnableMiniDump` と `MiniDumpFlags` は、Sandboxie Plus 1.0.5 および Sandboxie Classic 5.55.5 で導入されました。

### MiniDumpFlags

`MiniDumpFlags` は要求されるダンプのタイプを制御します。

```ini
MiniDumpFlags=Extended
MiniDumpFlags=0xAABBCCDD
```

設定が存在しない場合、または認識されない通常のテキストが含まれている場合、Sandboxie は組み込みの既定フラグを使用します。`Extended` ははるかに包括的なダンプを要求します。上級ユーザーは 16 進数の Windows `MINIDUMP_TYPE` ビットマスクを指定できます。

拡張またはフル メモリ スタイルのダンプは大きく、アプリケーション データ、ドキュメントの内容、資格情報、またはプロセス内に存在するその他のシークレットを含む機密メモリを含む場合があります。共有する前にダンプを確認し、トラブルシューティングの必要がない限り `Extended` を日常的な既定として使用しないでください。

## デバッガーの待機

### WaitForDebugger

`WaitForDebugger` を使用して、正確なイメージ名で実行可能ファイルを選択します。

```ini
WaitForDebugger=program.exe
```

複数のエントリがサポートされています。一致は大文字と小文字を区別せず、ワイルドカード構文を使用しません。一致するプロセスは、デバッガーがアタッチするまで、Sandboxie DLL の初期化中に非常に早い段階で一時停止します。

タイムアウトはありません。デバッガーがアタッチしない場合、プロセスは無期限に一時停止したままになる可能性があります。

### WaitForDebuggerAll

```ini
WaitForDebuggerAll=y
```

これは、影響を受けるすべてのサンドボックス化されたプロセスをデバッガー待機にします。既定で無効であり、意図的な開発者またはトラブルシューティング作業にのみ使用すべきです。誤って有効にすると、サンドボックス化されたアプリケーションが正常に開始できなくなる可能性があります。

### WaitForDebuggerCmdLine

```ini
WaitForDebuggerCmdLine=some argument
```

複数のエントリがサポートされています。各エントリは、プロセス コマンド ラインの大文字と小文字を区別しない部分文字列として一致させられます。この値をパターンとして説明する歴史的なメタデータにもかかわらず、ワイルドカードまたは正規表現構文を実装していません。

`WaitForDebugger`、`WaitForDebuggerAll`、および `WaitForDebuggerCmdLine` は代替セレクターです。それらのいずれかからの一致が待機をトリガーできます。

### WaitForDebuggerSilent

デバッガーがアタッチした後の現在の動作は `WaitForDebuggerSilent` に依存します。

* サイレント モードが有効な場合、Sandboxie が意図的にブレークポイントを発生させることなく、プロセスが続行されます。
* サイレント モードが無効な場合、Sandboxie はデバッグ ブレークポイントを発生させ、アタッチされたデバッガーがそこで停止します。

`WaitForDebuggerSilent` が存在しない場合、現在のランタイムはサイレント続行を使用します。アタッチ後にブレークポイントを要求するには、次を構成します。

```ini
WaitForDebuggerSilent=n
```

SandMan の **Resume** アクションはありません。デバッガーをアタッチすると最初の待機が解放されます。ブレークポイント モードが使用される場合は、デバッガーから実行を続行してください。

## SandMan 構成

SandMan の **Sandbox Options > Advanced Options > Debug > Debug Options** 汎用設定エディターは、少なくとも `EnableMiniDump` と `WaitForDebugger` を公開します。`MiniDumpFlags`、`WaitForDebuggerAll`、`WaitForDebuggerCmdLine`、または `WaitForDebuggerSilent` の専用チェックボックスは提供していません。

これらのオプションに対して、同等の専用の Sandboxie Control Classic 設定パネルは特定されていません。互換性のある手動 INI 設定は共有ランタイムによって消費されます。

## 変更の適用

これらのオプションはプロセスの初期化中に評価されます。変更した後は一致するサンドボックス化されたプロセスを再起動してください。影響を受けるサンドボックス プロセス ツリーを再作成するのが最も信頼できる方法です。SandMan、サービス、またはドライバーの再起動は、通常は必要ありません。

## 関連ページ

* [WinDbg の使用方法](HowToUseWinDbg.md)
* [Sandboxie Trace](SandboxieTrace.md)
* [Sandboxie Ini](SandboxieIni.md)
