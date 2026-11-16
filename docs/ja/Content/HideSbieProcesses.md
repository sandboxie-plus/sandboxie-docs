# Hide Sandboxie Processes

_HideSbieProcesses_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。そのランタイム フォールバックは `n` です。

```
   .
   .
   .
   [DefaultBox]
   HideSbieProcesses=y
```

`HideSbieProcesses=y` の場合、Sandboxie はフィルター処理されたネイティブ プロセス リストの結果から、提示されるプロセス名が `Sandboxie` または `Sbie` (大文字と小文字を区別せず) で始まるエントリを削除します。`SbieSvc.exe` および `SandboxieRpcSs.exe` は例であり、完全なリストではありません。名前プレフィックスのテストは製品の同一性を検証しません。一致するプレフィックスを持つ別の実行可能ファイルが該当することがあり、それらのプレフィックスを持たない名前はこの設定によって削除されません。

このボックス設定は、SandMan のグローバルな **Hide Sandboxie's own processes from the task list** 設定 (`Options/HideSbieProcesses`) とは異なります。グローバル設定は SandMan 自身のタスク ツリーに影響し、独立して構成できます。これはこのサンドボックス設定のチェックボックスではありません。この設定専用のボックス オプションのチェックボックスは現在の SandMan インターフェイスにはありませんが、INI ファイルで構成できます。

値は以降の列挙時に読み取られるため、`NtQuerySystemInformation` フックがそのプロセスにインストールされていれば、構成の再読み込みが既に実行中のプロセスに影響を与えることがあります。フックと WMI の制限については [Hide Non System Processes](HideNonSystemProcesses.md) を参照してください。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [Hide Host Process](HideHostProcess.md) および [Hide Non System Processes](HideNonSystemProcesses.md)。
