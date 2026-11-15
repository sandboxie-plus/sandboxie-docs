# サンドボックス階層

### 概要

サンドボックス化されたプログラムがオブジェクト（たとえばファイル）を作成（または変更）するとき、実際には何らかのデータが作成される必要があります。Sandboxie は、有害な変更からシステムを保護するために、これらのオブジェクトを邪魔にならない場所に作成します。しかし、これらのオブジェクトはシステムのどこかに存在する必要があります。このページでは、さまざまな種類のサンドボックス化されたオブジェクトがどこに配置されるかを説明します。

Sandboxie バージョン 2.80 以降、サンドボックスのレイアウトはコンピューター固有のデバイス名とアカウント名に結び付けられていません。詳細については、[ポータブル サンドボックス](PortableSandbox.md)を参照してください。

### ファイル {#files}

既定のファイル レイアウト オプションでは、リダイレクトされたファイルは [FileRootPath](FileRootPath.md) の下に概ね次のように整理されます。
```
  . FileRootPath
  . . drive
  . . . C
  . . . D
  . . . Q
  . . user
  . . . all
  . . . current
  . . . public
  . . share
  . . . server
  . . . . share
  . RegHive
```

`user\public` ブランチは、Public プロファイルが利用可能な場合に適用されます。[SeparateUserFolders](SeparateUserFolders.md) とボリューム レイアウト オプションは、これらのフォルダー名を変更できます。[サンドボックス ルートとボリューム レイアウト](SandboxRootsVolumeLayout.md)を参照してください。

[FileRootPath](FileRootPath.md) 設定は、特定のサンドボックスのルートへのパスを指定します。言い換えると、[FileRootPath](FileRootPath.md) がフォルダー _C:\MySandbox_ を指定する場合、サブフォルダー _drive_ と _user_ はそれぞれ _C:\MySandbox\drive_ と _C:\MySandbox\user_ として作成されます。

有効な [FileRootPath](FileRootPath.md) が利用できない場合、存在すれば非推奨の [BoxRootFolder](BoxRootFolder.md) が使用されます。これはベース フォルダーを提供します。DefaultBox という名前のボックスと `BoxRootFolder=C:\MySandbox` の場合、導出されるファイル ルートは `C:\MySandbox\Sandbox\DefaultBox` で、その下に `drive` と、既定のプロファイル レイアウトでは `user` が置かれます。どちらの設定も利用できない場合、Sandboxie は組み込みのファイル ルート既定値を使用します。

サンドボックス化されたプログラムが新しいファイルを作成したり既存のファイルを変更したりすると、Sandboxie はこれらの操作をサンドボックス内に通じるパスに対して作用するようにリダイレクトします。サンドボックス化されたプログラムがファイル _C:\NEW.TXT_ を作成しようとした場合、代わりに _([FileRootPath](FileRootPath.md))\drive\C\NEW.TXT_ を作成するようにリダイレクトされます。

サンドボックス化されたプログラムがファイル _C:\Users\joe\Documents\NEW.TXT_ を作成しようとした場合、_([FileRootPath](FileRootPath.md))\user\current\Documents\NEW.TXT_ を作成するようにリダイレクトされます。

`SeparateUserFolders=y`（既定）では、現在のユーザーの _profile_（または _home_）フォルダー（たとえば Windows Vista 以降の _C:\Users\joe_）内またはその下で作成または変更されたファイルは、サンドボックス化された _user\current_ フォルダーにリダイレクトされます。

同じオプションの下で、汎用（または _All Users_）プロファイル内のファイルは _user\all_ を使用し、認識された Public プロファイルは _user\public_ を使用できます。`SeparateUserFolders=n` の場合、通常のローカル プロファイル パスは代わりにドライブ レイアウトに従います（例: _drive\C\Users\joe_）。既存の内容はこれらのレイアウト間で自動的に移動されません。

他のローカル ファイルは通常、サンドボックス化された _drive\X_ フォルダーを使用します。ここで _X_ はホスト ボリュームのドライブ文字です。`UseVolumeSerialNumbers=y` と読み取り可能なファイルシステム ボリューム シリアルの場合、コンポーネントはたとえば _drive\C~1234-ABCD_ になります。ドライブ文字なしでマウントされたボリュームの場合、既定のマッピングはマウントされたディレクトリに従います。`UseVolumeGuidWhenNoLetter=y` は代わりに _drive\{volume-guid}_ を使用できます。

リモート ネットワーク共有上で作成または変更されたファイルは、サンドボックス化された _share\\servername\\sharename_ フォルダーにリダイレクトされます。

プログラムが、サンドボックス内にコピーがすでに存在するファイルを開こうとした場合、Sandboxie は、以前にサンドボックスに保存されたそのファイルのコピーにプログラムをリダイレクトします。逆に、そのファイルのコピーがサンドボックス内に存在せず、プログラムがファイルを変更しようとしない場合、Sandboxie はサンドボックスの外側の元のファイルに対して読み取り専用アクセスを許可します。この動作は、ファイル関連の設定 [OpenFilePath](OpenFilePath.md)、[ReadFilePath](ReadFilePath.md)、および [ClosedFilePath](ClosedFilePath.md) で影響を受ける場合があります。

通常のディレクトリ バッキング ボックスの場合、ファイル ルートは 1 つのストレージ ボリューム上に存在します。サンドボックス化されたプログラムは、複数のホスト ドライブ上にあるように見えるファイルを作成または変更できますが、リダイレクトされたコピーはそのボックスのファイル ルートの下に保存されます。

ファイル レイアウト フォルダーと並んで、サンドボックス ルートには _RegHive_ と、関連するレジストリ ハイブ ログ ファイルが含まれる場合があります。これらはサンドボックス化されたレジストリを保持します。以下を参照してください。

### レジストリ

レジストリ キーは、サンドボックス化されたレジストリ ハイブ内に作成されます。_レジストリ ハイブ_は、単一の_ハイブ ファイル_に保存された関連するレジストリ キーのグループに対する Microsoft Windows の用語です。

ハイブのバッキング ファイルは [FileRootPath](FileRootPath.md) の下の _RegHive_ です。Windows が維持するサポート ハイブ ファイルも存在する場合があります。ハイブは、サンドボックス化されたプロセスの初期化中にマウント（レジストリに読み込み）されます。複数のプロセスがマウントを共有でき、ハイブが対象となったときにアンロードが調整されます。すべてのサンドボックス化されたプログラムの終了後すぐには完了しない場合があります。

既定のレジストリ ルートでは、サンドボックス化されたハイブは Windows レジストリのグローバル構造内で次の位置と構造を持ちます。
```
 . HKEY_USERS
 . . KeyRootPath
 . . . machine
 . . . user
 . . . . current
```

[KeyRootPath](KeyRootPath.md) 設定は、ハイブがマウントされるレジストリの場所を指定し、そのバッキング ファイル名ではありません。有効な値が構成されていない場合、既定で _HKEY_USERS\Sandbox_(user name)_(sandbox name)_ になります。たとえば、ユーザー joe がサンドボックス DefaultBox を使用している場合、既定の [KeyRootPath](KeyRootPath.md) は _HKEY_USERS\Sandbox_joe_DefaultBox_ です。

サンドボックス化されたプログラムが新しいレジストリ キーを作成したり既存のキーを変更したりすると、Sandboxie はこれらの操作をサンドボックス内に通じるパスに対して作用するようにリダイレクトします。サンドボックス化されたプログラムがキー _HKEY_LOCAL_MACHINE\Software\NewKey_ を作成しようとした場合、代わりに _([KeyRootPath](KeyRootPath.md))\machine\Software\NewKey_ を作成するようにリダイレクトされます。

サンドボックス化されたプログラムがキー _HKEY_CURRENT_USER\Software\NewKey_ を作成しようとした場合、_([KeyRootPath](KeyRootPath.md))\user\current\Software\NewKey_ を作成するようにリダイレクトされます。

通常のレジストリ仮想化では、主なマッピングは次のとおりです。

- HKEY_LOCAL_MACHINE ツリーの下で作成または変更されたレジストリ キーは、サンドボックス化された _machine_ キーの下にリダイレクトされます。

- HKEY_CURRENT_USER ツリーの下で作成または変更されたレジストリ キーは、サンドボックス化された _user\current_ キーの下にリダイレクトされます。

- HKEY_CLASSES_ROOT は Windows の Classes ビューであり、1 つの独立した均一な Sandboxie ルートではありません。そのマシン/ユーザーごとのマージと、Sandboxie のサンドボックス側 Classes マッピングは別個の関係です。

サンドボックスのカスタマイズは、_user\current\software\classes_ から _user\current_classes_ へのシンボリック リンクを作成できます。そのリンクが作成される場所では、2 つの名前は同じサンドボックス側の内容を参照します。

既存のホストのみのキーの通常の読み取り専用オープンは、最初にサンドボックス カウンターパートを作成せずにホスト キーを使用できます。サンドボックス状態が存在する場合、選択されたキー/値のクエリと列挙は、それを対象となるホスト状態とマージできます。サンドボックス キーは、必ずしもホスト キーを完全に覆い隠す完全なコピーではありません。この動作は、レジストリ関連の設定 [OpenKeyPath](OpenKeyPath.md)、[ReadKeyPath](ReadKeyPath.md)、および [ClosedKeyPath](ClosedKeyPath.md) で影響を受ける場合があります。マージ、削除、アクセス モード、およびライフサイクルの境界については、[レジストリ仮想化](RegistryVirtualization.md)を参照してください。

### プロセス間オブジェクト

これらのオブジェクトは、プログラムが情報を共有し、処理を同期し、サービスを提供するために使用されます。これらのオブジェクトはディスクに書き込まれることがなく、システムのシャットダウン時に消えます。

Sandboxie は、同じプログラムをサンドボックス化してサイド バイ サイドで非サンドボックス化して実行できるようにするために、これらのオブジェクトを分離します。また、サンドボックス化されたプログラムがサンドボックス化されていないものに干渉するのを防ぎます。

これらのオブジェクトは NT オブジェクト名前空間に作成されます。その名前空間内での位置と構造は次のとおりです。
```
 . IpcRootPath
 . . BaseNamedObjects
 . . . Global
 . . . Local
 . . . Session
 . . RPC Control
```

[IpcRootPath](IpcRootPath.md) 設定は、特定のサンドボックスのルートへのパスを指定します。省略した場合、既定で _\Sandbox\(user name)\(sandbox name)\Session_(session number)_ になります。たとえば、ユーザー joe がセッション 0 で実行されていて、サンドボックス DefaultBox を使用している場合、既定の [IpcRootPath](IpcRootPath.md) は _\Sandbox\joe\DefaultBox\Session_0_ です。

[IpcRootPath](IpcRootPath.md) の下には、NT 名前空間を構成する_オブジェクト ディレクトリ_があり、サンドボックス領域外の既存のオブジェクト ディレクトリのレイアウトに一致します。ディレクトリは_永続_属性で作成されます。これは、システム シャットダウン時にのみ消えることを意味します。

サンドボックス化されたプログラムによって作成されたオブジェクトは、サンドボックス オブジェクト ディレクトリ内に作成されます。プログラムが Sandboxie の監督外で実行されている場合、通常はそのようなオブジェクトを \BaseNamedObjects オブジェクト ディレクトリに作成します。

オブジェクトは名前なしで作成される場合があり、その場合、オブジェクトは実質的にそれを作成した特定のプログラムに分離されます。ただし、プログラムは別のプログラムの内部にアクセスして、そのような名前のないオブジェクトを特定して使用できます。これを軽減するために、Sandboxie はサンドボックス内のプログラムがこの方法でサンドボックス外のプログラムにアクセスするのを防ぎます。

Sysinternals（現在は Microsoft の一部）による無料ユーティリティ [WinObj](https://docs.microsoft.com/en-us/sysinternals/downloads/winobj) を使用して、NT オブジェクト名前空間を表示できます。

ファイルやレジストリ キーの場合とは異なり、サンドボックス化されたプログラムは、読み取り専用アクセスであっても、サンドボックス名前空間外の IPC オブジェクトにアクセスすることを決して許可されません。この動作は、レジストリ関連の設定 [OpenIpcPath](OpenIpcPath.md) および [ClosedIpcPath](ClosedIpcPath.md) で影響を受ける場合があります。

Sandboxie には、プログラムが正しく機能できるようにするための多数の組み込み [OpenIpcPath](OpenIpcPath.md) 設定が含まれており、一般的なシステムでは、サードパーティ製ソフトウェアの互換性設定を通じてより多くの [OpenIpcPath](OpenIpcPath.md) 設定が適用されることに注意してください。
