# Separate User Folders

_SeparateUserFolders_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 0.2.2 / Classic 5.41.2 以降で使用できます。[FileRootPath](FileRootPath.md) の下でリダイレクトされたユーザー プロファイル ファイルがどのように編成されるかを選択します。ランタイムの既定は `y` です。

```ini
   [DefaultBox]
   SeparateUserFolders=n
```

`y` の場合、Sandboxie は認識されたプロファイルの場所を `user\current`、`user\all`、および利用可能な場合は `user\public` などのポータブル フォルダーにマップします。`n` の場合、それらの特別なマッピングを設定しません。通常のローカル プロファイル パスはその後ドライブ レイアウトを使用します。たとえば `drive\C\Users\...` です。この設定は Windows ユーザー プロファイルまたはアカウントのアクセス許可を変更しません。

SandMan のチェックボックスは **Sandbox Options > File Options > Separate user folders** です。ボックスが空でない場合は使用できません。この設定を変更しても `user\...` と `drive\...` の間でファイルは移行されません。空のボックスで使用してください。既存のデータを保持する必要がある場合は、設定がそれを移行すると仮定するのではなく、別途処理してください。

Sandboxie は各サンドボックス化されたプロセスでファイル処理を初期化するときにこのオプションを読み取ります。変更後は影響を受けるプロセスを再起動してください。既存のプロセスはプロファイル マッピングを自動的に再構築しません。[Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md) および [Sandbox Hierarchy](SandboxHierarchy.md) を参照してください。
