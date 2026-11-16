# System Event Log

System Event Log は、Windows 自体およびその他のサードパーティ製ソフトウェアによって発行された情報メッセージとエラー メッセージを収集する Windows コンポーネントです。Sandboxie は一部のメッセージを System Event Log に発行します。メッセージは Source 値 SbieDrv でリストされます。ログにアクセスしてメッセージを表示するには、Event Viewer ツールを使用します:

Windows Start Menu > Control Panel > Administrative Tools > Event Viewer

System Event Log の詳細については、[Wikipedia の Event Viewer](https://en.wikipedia.org/wiki/Event_Viewer) を参照してください。

初期化の成功を妨げるエラーにより Sandboxie メッセージが発行された場合、[Sandboxie Control](SandboxieControl.md) は点滅する感嘆符アイコンを表示します。点滅するアイコンを右クリックして _Show Errors_ を選択し、関連するメッセージを表示します。

_Messages From Sandboxie_ は _Windows Event Log_ に保存されません。[ログをフラット ファイルに保存する](MessagesFromSandboxie.md#log-messages-to-a-file)ための回避策が利用可能です。

参照: [SBIE Messages](SBIEMessages.md)。
