# File Root Path

_FileRootPath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。特定のサンドボックスのファイル コンテナ ルートを指定します。これは保存場所の設定であり、ホスト ファイルへのアクセスを許可するルールではありません。

ボックスに対して設定するか、有効なグローバルまたは有効なテンプレート構成を通じて提供できます。有効な `FileRootPath` は、たとえ `FileRootPath` が `[GlobalSettings]` から来ていて `BoxRootFolder` がボックスに対して設定されていても、レガシーの [BoxRootFolder](BoxRootFolder.md) よりも優先されます。

このルートの下の内容については [Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md) および [Sandbox Hierarchy](SandboxHierarchy.md) を参照してください。

使用法:

```
   .
   .
   .
   [DefaultBox]
   FileRootPath=C:\Sandbox\MySandbox
```

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox menu > Set Container Folder](SandboxMenu.md#set-container-folder)

SandMan では、グローバル既定は **Global Settings > Advanced Config > Sandboxie Config > Sandbox file system root** にあります。New Box ウィザードはコンテナの場所を提供し、ボックスごとの `FileRootPath` は **Sandbox Options > Advanced Options > Miscellaneous > Add Option** で入力できます。上記の Sandboxie Control リンクは Classic/レガシー インターフェイスを記述しています。

**技術的な詳細**

次の置換変数がこのパスで役立つことがあります。

*   %Personal% などの[シェル フォルダー](ShellFolders.md)変数。ユーザーの Documents フォルダーに展開されます
*   変数 %SBIEHOME%。Sandboxie インストールのルートに展開されます
*   変数 %SystemDrive%。Windows のシステム ドライブ文字に展開されます
*   変数 %SANDBOX%。サンドボックスの名前に展開されます
*   変数 %USER% (または %USERNAME%)。ユーザー名に展開されます
*   変数 %SID%。ユーザー セキュリティ ID (SID) に展開されます
*   変数 %SESSION%。ターミナル サービス セッション番号に展開されます

有効な _FileRootPath_ が利用できない場合、Sandboxie は非推奨の [BoxRootFolder](BoxRootFolder.md) をチェックします。存在する場合、その値の後に旧式のサフィックスが続きます:

*   `BoxRootFolder\Sandbox\<box name>`

どちらの設定も利用できない場合、組み込みのランタイム既定は次のとおりです:

*   `\??\%SystemDrive%\Sandbox\%USER%\%SANDBOX%`

一般的な Windows インストールでは、これは `C:\Sandbox\alice\DefaultBox` のような場所に解決されます。`%BOXNAME%` はサポートされているルート展開エイリアスではありません。`%SANDBOX%` を使用してください。

構成で `FileRootPath` を変更しても、既存のコンテナは移動しません。パスを変更する前に影響を受けるサンドボックス化されたプロセスを停止し、既存の内容が自動的に再配置されると想定しないでください。パスだけを変更すると古い内容が残ることがあります。
