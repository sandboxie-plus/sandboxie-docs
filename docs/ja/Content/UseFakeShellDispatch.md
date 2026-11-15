# Use Fake Shell Dispatch

_UseFakeShellDispatch_ は Sandboxie Plus 1.17.3 以降で使用可能な [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Shell オートメーションの互換性フォールバックを提供し、既定で有効です。

```ini
[DefaultBox]
UseFakeShellDispatch=y
```

この設定はすべての COM アクティベーションを置き換えるものではなく、完全な Windows Shell をエミュレートするものでもなく、Electron または WebView2 アプリケーションに限定されるものでもありません。

## Shell ディスパッチの動作

`IShellWindows::FindWindowSW` を通じて行われた対象となるデスクトップ ディスパッチ要求に対して、Sandboxie は使用可能なサンドボックス ローカルのディスパッチ オブジェクトを保持するか、部分的な合成 Shell ディスパッチ チェーンにフォールバックできます。

通常のセキュリティ分離ボックスでは、Sandboxie はまずサンドボックスに関連付けられた使用可能な実 Shell ディスパッチを保持しようとします。それが使用できない場合、合成実装にフォールバックする前に他の使用可能な実 Shell ディスパッチ パスを試すことがあります。

コンパートメント モードでは、対象となるデスクトップ ディスパッチ要求は、元のホスト デスクトップ ディスパッチの代わりに合成 Shell ディスパッチ チェーンを使用します。この動作は対象となる Shell ディスパッチ要求に適用され、すべての COM トラフィックの一般的な置き換えではありません。

フォールバックは、この互換性パスに必要なコア `IShellDispatch` および `IShellDispatch2` インターフェイスをサポートします。以降の `IShellDispatch3` から `IShellDispatch6` インターフェイスのサポートを約束するものではありません。

## サポートされる操作

合成オブジェクトは、次を含む限定されたプロパティとアクションのセットを提供します:

- `Application`
- `Parent`
- `Windows`
- `Open`
- `Explore`
- `ControlPanelItem`
- `ShellExecute`

`Open`、`Explore`、`ControlPanelItem`、および `ShellExecute` は、Sandboxie の既存の shell 実行パスを通じて実際の Shell アクションを実行できます。単に偽造された成功結果を返すわけではありません。

フォールバックは意図的に部分的であり、完全な `IShellDispatch` または `IShellDispatch2` サーフェスを実装していません。`BrowseForFolder`、`MinimizeAll`、`ShutdownWindows`、`FindFiles`、および `ServiceStart` などの操作は、実装されていない代表的な例です。サポートされていない操作は、暗黙的に成功として扱われるのではなく、not-implemented または member-not-found スタイルの COM 失敗を返すことがあります。

したがって、対象となる要求の可能な結果には、使用可能な実ディスパッチの使用、合成ディスパッチの使用、サポートされていない合成操作のエラー、または必要なインターフェイスやオブジェクトを作成できない場合の COM 失敗が含まれます。

## プロセスごとの構成

_UseFakeShellDispatch_ はイメージ修飾値をサポートします:

```ini
[DefaultBox]
UseFakeShellDispatch=y
UseFakeShellDispatch=problem.exe,n
UseFakeShellDispatch=another.exe,y
```

非修飾値は通常のボックス レベルの既定を提供します。プロセス修飾エントリは特定の実行可能ファイルに対して動作を無効または有効にでき、正確なイメージ固有の設定は Sandboxie の通常のイメージ対応構成動作に従って優先されます。

## Electron と WebView2

この機能は、WebView2 関連ソフトウェアで見られる Shell ディスパッチ互換性のケースに対処するために部分的に導入されましたが、実装自体は一般的です。これは Shell オートメーションの互換性フォールバックであり、一部の WebView2 ベースのアプリケーションにも役立つことがあります。

_UseFakeShellDispatch_ と [UseElectronDetection](UseElectronDetection.md) は独立した互換性コントロールです:

- _UseFakeShellDispatch_ は Chrome または Electron プロセス分類に依存しません。
- _UseElectronDetection_ は偽の Shell ディスパッチを有効または無効にしません。
- _UseFakeShellDispatch_ は対象となる Shell ディスパッチ呼び出しに対して評価され、_UseElectronDetection_ は起動中にプロセスを分類します。

## COM と分離に関する考慮事項

通常の Sandboxie COM および CLSID 制限は依然として適用されます。フォールバック自体は `OpenClsid` アクセスを付与したり、`ClosedClsid` 処理をバイパスしたりしません。`IShellWindows` 互換性フックが適用される前に、初期 COM アクティベーションが Sandboxie の通常のパスを通じて成功する必要があります。`BoxedCOM` は、このフォールバックの前提条件ではなく、より広範な関連 COM 分離設定です。

この設定は、サポートされている Shell アクションを Sandboxie の既存の shell 実行パスを通じてルーティングしつつ、ホスト Explorer ディスパッチ オブジェクトへの依存を減らします。これは互換性メカニズムであり、単独のセキュリティ境界ではありません。結果として得られる起動は、別途構成された [Breakout Process](BreakoutProcess.md) または [Breakout Document](BreakoutDocument.md) ルールの影響を依然として受ける可能性があります。この設定自体がブレイクアウト動作を作成するものではありません。

## 変更の適用

この設定は、対象となる `FindWindowSW` 要求が発生したときに現在のイメージに対して評価されます。構成の変更は、既に実行中のプロセス内の以降の対象となる呼び出しに影響を与えることがありますが、既に返された COM オブジェクトまたは結果を遡って置き換えるものではありません。将来の対象となる呼び出しが新しい値を使用するためだけにアプリケーションを再起動することは通常必要ありません。

## Sandboxie Plus インターフェイス

現在 _UseFakeShellDispatch_ 用の専用 SandMan チェックボックスはありません。Sandboxie の INI 構成を通じて構成してください。チェックボックスがないことは、機能が無効であることを意味しません。そのランタイム既定は有効です。

## バージョン履歴

_UseFakeShellDispatch_ は Sandboxie Plus 1.17.3 で導入されました。既定で有効で、プロセスごとの無効化をサポートし、現在専用の SandMan チェックボックスはありません。

## 関連構成

- [Sandboxie Ini](SandboxieIni.md)
- [Breakout Process](BreakoutProcess.md)
- [Breakout Document](BreakoutDocument.md)
- `OpenClsid`
- `ClosedClsid`
- `BoxedCOM`
