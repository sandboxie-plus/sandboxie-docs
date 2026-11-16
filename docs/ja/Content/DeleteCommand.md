# Delete Command

DeleteCommand は [Sandboxie Ini](SandboxieIni.md) の従来のサンドボックス設定で、Sandboxie Control Classic および `Start.exe` で引き続き機能します。その削除パスがサンドボックスの内容を物理的に削除するために使用するコマンドを指定します。その主な目的は、サードパーティの安全な削除ユーティリティを Sandboxie に組み込めるようにすることです。[Secure Delete Sandbox](SecureDeleteSandbox.md) を参照してください。

SandMan は、サンドボックスの内容をクリーンアップする前に、構成されたホスト側の自動化のために別個の [`OnBoxDelete`](SandManTriggers.md#onboxdelete) トリガーを使用します。`OnBoxDelete` は名前変更された `DeleteCommand` ではありません。トリガーは SandMan のクリーンアップ前に実行されますが、`DeleteCommand` は従来の Classic/`Start.exe` パスでディレクトリ削除を実行するコマンドを選択します。

使用法:
```
   .
   .
   .
   [DefaultBox]
   DeleteCommand=%SystemRoot%\System32\cmd.exe /c RMDIR /s /q "%SANDBOX%"
```

この例は、DeleteCommand が明示的に指定されていない場合に使用される既定の設定であり、Windows の RMDIR コマンドを呼び出してサンドボックス フォルダーを削除します。

その他の例については、[Secure Delete Sandbox](SecureDeleteSandbox.md) を参照してください。

***

この設定を指定するときは、コマンドに **"%SANDBOX%"** (引用符付き) を含めるようにしてください。

***

注: 安全な削除はプライバシー対策であり、セキュリティ対策ではありません。通常の削除と安全な削除はどちらも、サンドボックスに収集された不要なソフトウェアを効果的に削除します。[Secure Delete Sandbox](SecureDeleteSandbox.md) を参照してください。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Delete > Command](DeleteSettings.md#command)

関連する SandMan ドキュメント: [SandMan Triggers](SandManTriggers.md)
