# Secure Delete Sandbox

一般的なファイル削除は、データをオペレーティング システムとプログラムからアクセスできなくしますが、データはハード ドライブの記憶媒体から物理的に消去されるわけではなく、データ復旧技術者によって回復される可能性があります。この回復をより困難にするため、_安全な削除_を実行できるサードパーティ製ソフトウェアが存在します。これは通常、削除前にデータを複数回上書きすることによって実現されます。

詳細については、[Wikipedia のデータ残留 (Data remanence)](https://en.wikipedia.org/wiki/Data_remanence) を参照してください。

既定では、Sandboxie Control Classic/`Start.exe` の削除パスは、標準の Windows _RMDIR_ コマンドを使用してフォルダーを削除します。これにより、サンドボックスの内容 (悪意のあるソフトウェアを含む) がオペレーティング システムから適切に削除されることが保証されます。ただし、上記のように、データはフォレンジックの専門家による検査と回復に対して脆弱なままになります。

機密データのプライバシーを懸念する人は、サードパーティ製の安全な削除ユーティリティを Classic/`Start.exe` の削除パスに組み込み、標準コマンドの代わりに使用させることができます。

Classic/`Start.exe` の削除パスの場合、Sandboxie Control を通じて、または [Sandboxie Ini](SandboxieIni.md) 構成ファイルを手動で編集することによって、カスタム削除コマンドを構成できます。

代わりに SandMan は [`OnBoxDelete`](SandManTriggers.md#onboxdelete) を提供します。これは、SandMan が独自のクリーンアップを実行する前に構成された自動化を実行するホスト側のトリガーです。`DeleteCommand` と同じメカニズムではなく、トリガーを有効にしてもそれ自体で SandMan の削除方法が変わったり、安全な消去が保証されたりするわけではありません。

**Sandboxie Control で**

[Sandbox Settings > Delete > Command](DeleteSettings.md#command) を使用します。Delete Command のいくつかの例:

*   [Eraser by Heidi Computers](https://eraser.heidi.ie/) を呼び出して内容を安全に削除します:
```
    %SystemRoot%\System32\eraserl.exe -folder "%SANDBOX%" -subfolders -method DoD_E -resultsonerror -queue
```

*   [SDelete by SysInternals/Microsoft](https://technet.microsoft.com/en-us/sysinternals/bb897443.aspx) を呼び出して内容を安全に削除します。
```
    "C:\Program Files\Sysinternals\SDelete\sdelete.exe" -p 3 -s -q "%SANDBOX%"
```

**Sandboxie.ini 構成ファイルで**

特定のサンドボックスのカスタム削除コマンドを構成するには、[Sandboxie Ini](SandboxieIni.md) のサンドボックス セクションで [DeleteCommand](DeleteCommand.md) 設定を編集または挿入します。

グローバルのカスタム削除コマンドを構成するには、[Sandboxie Ini](SandboxieIni.md) の [GlobalSettings] セクションで [DeleteCommand](DeleteCommand.md) 設定を編集または挿入します。


この設定を指定するときは、コマンドに **"%SANDBOX%"** (引用符付き) を含めるようにしてください。

削除コマンドを起動する前に、[Delete Contents of Sandbox](StartCommandLine.md#delete-contents-of-sandbox) で説明されているように、Sandboxie はサンドボックスをスキャンしてすべてのファイルが適切に削除できることを確認します。

* * *

[Help Topics](HelpTopics.md) に移動します。
