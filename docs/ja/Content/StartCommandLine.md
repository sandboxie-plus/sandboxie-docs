# コマンド ラインの開始

Sandboxie の Start プログラムは、指定されたコマンド ライン パラメーターに応じて、次のいずれかを実行できます。

*   [開始](#start-programs) — Sandboxie の監督下でプログラムを開始します
*   [停止](#stop-programs) — サンドボックス化されたプログラムを停止します
*   [アンマウント](#unmount-box-images) — ボックス イメージまたは RAM ディスクをアンマウントします
*   [マウント](#mount-box-images) — 暗号化されたボックス イメージをマウントします
*   [一覧表示](#list-programs) — サンドボックス化されたプログラムを一覧表示します
*   [削除](#delete-contents-of-sandbox) — サンドボックスの内容を削除します
*   [再読み込み](#reload-configuration) — Sandboxie 構成を再読み込みします
*   [強制プログラムの無効化](#disable-forced-programs)モードを開始します
*   [関連資料](#related-reading-material)

* * *

<div id="start-programs"></div>

### プログラムの開始

これは既定の動作です。プログラムの実行可能ファイルへの完全パスまたは部分パスを指定すると、Sandboxie Start はそのプログラムを Sandboxie の監督下で起動します。
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  c:\windows\system32\notepad.exe
  "C:\Program Files\Sandboxie\Start.exe"  notepad.exe
```

2 つの特別なプログラム名が許可されています。
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  default_browser
  "C:\Program Files\Sandboxie\Start.exe"  mail_agent
```

Sandboxie Start は、指定されたパラメーターに応じて、Run Any Program ダイアログ ウィンドウまたは Sandboxie スタート メニューを表示することもできます。
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  run_dialog
  "C:\Program Files\Sandboxie\Start.exe"  start_menu
```

サンドボックス外からの通常の起動では、パラメーター _/box:SandboxName_ が対象のサンドボックスを選択し、プログラムまたは起動ヘルパーの前に置く必要があります。省略した場合、Start.exe は最初に `[GlobalSettings]` の `DefaultBox` 値を選択し、その値が利用できないか空の場合は `DefaultBox` という名前のサンドボックスにフォールバックします。例:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  run_dialog
```

/box パラメーターの特別な形式は _/box:\_\_ask\_\__ で、Start.exe にサンドボックス選択ダイアログ ボックスを表示させます。

`/box:current` は同じ選択ワークフローに従います。これは呼び出し元の現在のサンドボックスを対象にする一般的な指示ではありません。高度なホスト側起動形式 `/box:-PID` は既存のサンドボックス化されたプロセスをモデルとして使用できますが、制御操作のための汎用セレクターではありません。

すでにサンドボックス化された Start.exe がプログラムを起動する場合、その実際のサンドボックス内に留まります。`/box:` はその起動を別のボックスに移動しません。全ボックス操作は独自の対象を列挙し、`/reload` はボックス スコープではなく、削除フェーズ 2 は保留ディレクトリをより広くスキャンします。

パラメーター _/silent_ を使用すると、一部のポップアップ エラー メッセージを排除できます。例:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /silent  no_such_program.exe
```

終了コードはコマンドによって異なります。[終了ステータス](#exit-status)を参照してください。_IF ERRORLEVEL_ 条件はバッチ ファイルでランチャーの結果を調べることができますが、ゼロは要求された操作が成功したことの普遍的な確認ではありません。`/silent` は失敗を成功に変えることなく、また [Alert Before Start](AlertBeforeStart.md) の確認を含むすべてのプロンプトやダイアログを抑制するわけでもありません。

パラメーター _/elevate_ は、適用される Windows UAC および Sandboxie の制限の下で昇格を要求しますが、管理者権限を保証するものではありません。例:
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /elevate cmd.exe
```

パラメーター _/env_ は、子ワークフローの前にランチャーで環境変数を設定します。
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /env:VariableName=VariableValueWithoutSpace cmd.exe
  "C:\Program Files\Sandboxie\Start.exe"  /env:VariableName="Variable Value With Spaces" cmd.exe
```

パラメーター _/hide_window_ は、起動するプログラムがウィンドウを表示しないように通知しますが、アプリケーションが UI を表示することは可能です。
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /hide_window cmd.exe /c automated_script.bat
```

パラメーター _/wait_ は、起動したプロセスを待機することを要求し、起動パスがプロセス ハンドルを提供し、待機とステータス取得が成功した場合にその終了ステータスを返すことができます。子孫プロセス ツリー全体を待機するわけではありません。
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /wait cmd.exe
```

Start.exe は Win32 アプリケーションでありコンソール アプリケーションではないため、システムの "start" コマンドがここで役立ち、システムに Start.exe の終了を強制的に待機させられることに注意してください。
```cmd
  start "" /wait "C:\Program Files\Sandboxie\Start.exe" /wait cmd /c exit 9
  echo %ERRORLEVEL%
  9
```

この通常の成功した起動では、CMD の `start /wait` が Sandboxie Start.exe を待機し、その `/wait` が `cmd /c exit 9` を待機してステータス 9 を伝播します。2 つの `/wait` オプションは異なるランチャーに属します。

シェル実行は、プロセス ハンドルを返さずに成功することがあります。プログラムは別のプロセスに作業を委任して先に終了することもあり、一部の内部起動パスは通常の待機を迂回します。そのような場合、または待機やステータス取得が失敗した場合は、子のステータス伝播を仮定しないでください。

該当する修飾子は、影響する操作またはプログラムの前に置いてください。`/reload`、`/terminate`、`/terminate:*`、`/terminate_all`、`/unmount`、`/unmount_all`、`/mount`、`/mount_protected`、`/listpids` は解析中に即座に実行され、以降のオプションは処理されません。プログラム トークンは通常のスラッシュ オプション解析を終了するため、以降の引数はそのプログラムに属します。例:
```cmd
   "C:\Program Files\Sandboxie\Start.exe"  /box:CustomBox /silent MyProgram.exe
```

同様に、`Start.exe /box:ExampleBox /mount` はマウント前にボックスを選択しますが、`Start.exe /mount /box:ExampleBox` は同等ではありません。内部ヘルパー `run_sbie_ctrl` と `open_agent` は別の早期ディスパッチを持つため、以下のセクションを参照してください。

<div id="exit-status"></div>

#### 終了ステータス

自動化は、すべてのゼロ終了コードを成功として扱うのではなく、意図した結果を検証する必要があります。

| 操作 | 意味と制限 |
| --- | --- |
| 通常の起動 | 通常、起動が成功したかどうかを報告し、プログラムの最終的な結果ではありません。 |
| `/wait`、`/keep_alive` | 該当するプロセス ハンドル パスが成功した場合に、待機した結果または最終的な監督結果を報告できます。 |
| `/mount`、`/mount_protected` | マウント要求の結果を報告し、完全なサンドボックスの準備完了、再利用時のパスワード検証、または検証済みの保護ではありません。 |
| 終了コマンドとアンマウント コマンド | 個々の操作結果を破棄します。ゼロは終了またはデタッチを証明しません。 |
| `/reload`、`/listpids` | ゼロは再読み込みの成功や完全な列挙の成功を証明しません。 |
| `delete_sandbox` | 最初のランチャー完了は、非同期のフェーズ 2 削除が完了したことを証明しません。 |

<div id="stop-programs"></div>

### プログラムの停止

呼び出し元のセッションで特定のサンドボックス内のプログラムの終了を要求します。要求は SbieSvc に送信され、SbieSvc が終了と再列挙を試みます。即時の終了や成功は保証されません。
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /terminate
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /terminate
  "C:\Program Files\Sandboxie\Start.exe"  /terminate_all
```

_/box:SandboxName_ を省略した場合、要求は選択された既定のサンドボックスを使用します。

形式 _/terminate_all_ と `/terminate:*` は、呼び出し元に対して有効なサンドボックスを列挙し、呼び出し元のセッションで終了を要求します。すべてのセッションのすべてのサンドボックス化されたプロセスを自動的に終了するわけではありません。Start.exe はサービスの終了結果を破棄するため、ゼロは対象のすべてのプロセスが停止したことを確認しません。

* * *

<div id="unmount-box-images"></div>

### ボックス イメージのアンマウント

これらのコマンドは、Sandboxie Plus によって作成されたボックス イメージまたは RAM ディスクのアンマウントを要求します。これらのパラメーターは v1.11.0 / 5.66.0 以降で利用可能です。
```cmd
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /unmount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /unmount_all
```

`/unmount` はまず呼び出し元のセッション内の関連するサンドボックス化されたプロセスの終了を試み、次に選択されたボックスのサービス側アンマウントを要求します。_/box:SandboxName_ を省略した場合、選択された既定のサンドボックスを使用します。終了の成功を確実に確認することなく続行します。

`/unmount_all` は終了対象の適格なサンドボックスを列挙し、次にアンマウント対象としてそれらを再度列挙します。列挙は暗号化されたボックスに限定されず、共有 RAM バッキングを使用するボックスを含む場合があります。マシン上のすべてのマウントされたデバイスまたはすべてのボックスの完全な一覧ではありません。

プロセスの終了は呼び出し元のセッションにスコープされますが、サービス管理のストレージは共有リソースを含む場合があるため、デタッチがセッション ローカルであることは保証されません。Start.exe は個々のアンマウント失敗を集約しないため、ゼロはデタッチの成功を証明しません。失敗した試行でもマウント ルートの状態が変わる可能性があるため、ロールバックを仮定しないでください。

<div id="mount-box-images"></div>

### ボックス イメージのマウント

> [!WARNING]
> `Start.exe` で `/key:password` を使用すると、パスワードがコマンド ライン履歴、プロセス リスト、および場合によってはイベント ログを通じて露出する可能性があります。実際のパスワードをバッチ ファイルやログに保存しないでください。代わりに [SandMan の対話型イメージ マウント ワークフロー](UseFileImage.md)を検討してください。

これらのコマンドは、イメージ管理サービスを通じてボックス イメージのマウントを要求します。これらのパラメーターは v1.11.0 / 5.66.0 以降で利用可能です。
```cmd
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /key:"example password" /mount_protected
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /key:"example password" /mount
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /key:"example password" /mount_protected
  "C:\Program Files\Sandboxie-Plus\Start.exe"  /box:EncryptedBox  /key:"example password" /mount
```

`/box:` と `/key:` はマウント操作の前に置く必要があります。引用符で囲むとパスワードにスペースを含めることができ、引用符なしの値はスペースで終了します。一般的な埋め込み引用符のエスケープ機構はありません。明示的な空の値は拒否され、`/key:` を省略しても対話型パスワード プロンプトは呼び出されません。

_/box:SandboxName_ を省略した場合、要求は選択された既定のサンドボックスを使用します。すでにマウントされたイメージは、新しく指定されたパスワードを認証せずに再利用できるため、成功した結果が常にパスワードが検証された証拠とは限りません。

明示的なイメージ マウント ハンドラーは、`UseFileImage=y` を独立して要求することなく、そのイメージ パスを試みます。これはすべてのストレージ構成を有効な対象にするわけではありません。ImBox/ImDisk の可用性、機能の可用性、および実際のイメージ/バックエンドの状態は依然として重要です。この操作は完全なサンドボックス起動、レジストリ ハイブの初期化、または RAM ディスク バッキングの取得ではありません。[ファイル イメージの使用](UseFileImage.md)を参照してください。

`/mount_protected` は、イメージのマウントに加えてマウント ルートの保護を要求します。マウントの成功は、保護が登録されたことを独立して検証しません。マウント ルートのファイルシステム保護は、イメージ暗号化および `ConfidentialBox` プロセス保護とは別のものであり、考えられるすべてのホスト アクセスに対する保証ではありません。保護の境界については、[マウント時の保護の強制](ForceProtectionOnMount.md)と[管理者のみの保護](ProtectAdminOnly.md)を参照してください。

Start.exe のマウント コマンドは `ForceProtectionOnMount` を消費しません。この設定は SandMan のマウント ダイアログ ワークフローを制御します。`/mount_protected` は明示的な保護要求を行います。

* * *

<div id="list-programs"></div>

### プログラムの一覧表示

呼び出し元のセッションで特定のサンドボックス内のプログラムのプロセス ID 番号を一覧表示します。
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /listpids
  "C:\Program Files\Sandboxie\Start.exe"  /box:TestBox  /listpids
```

_/box:SandboxName_ を省略した場合、選択された既定のサンドボックスが使用されます。すでにサンドボックス化された呼び出し元による列挙は、別の `/box` ターゲットではなく、その実際のサンドボックスを使用します。

出力は 1 行に 1 つの番号としてフォーマットされます。最初の行にはプログラムの数が含まれ、続いて 1 行に 1 つのプロセス ID が続きます。出力例:
```cmd
    "C:\Program Files\Sandboxie\Start.exe"  /listpids | more
    3
    3036
    2136
    384
```

Start.exe はコンソール アプリケーションではないため、`| more` などの構成体を使用して出力をパイプしない限り、出力はコマンド プロンプト ウィンドウに表示されません。終了コード ゼロは、完全な列挙または出力の成功を証明しません。

* * *

<div id="delete-contents-of-sandbox"></div>

### サンドボックスの内容の削除
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent
```

_/box:SandboxName_ パラメーターは、Start.exe と削除コマンドの間に指定できます。

`_silent` サフィックスは削除エラー メッセージを抑制しますが、検出されたエラーが操作を失敗で終了させることはあります。

これらのコマンドは、サンドボックスのファイルシステムの内容を削除するものであり、`Sandboxie.ini` のボックスの構成セクションではありません。これらは Classic 互換の Start.exe 削除パスであり、SandMan の別個のクリーンアップまたはトリガー ワークフローではありません。

削除操作は 2 つのフェーズで行われます。

*   フェーズ 1 は、選択されたサンドボックスのファイルシステム ルートを、`__Delete_(sandbox name)_(timestamp-derived suffix)` の形式の削除保留ディレクトリに名前変更します。たとえば、サンドボックスが DefaultBox の場合、`__Delete_DefaultBox_01C4012345678912` に名前変更されることがあります。サフィックスは乱数ではなく、現在の FILETIME 値から取得されます。

*   フェーズ 2 は、適格なボックスを列挙し、上記のように名前変更された削除保留ディレクトリを検索します。削除コマンドを実行する前に、それらの内容を準備します。
    *   ジャンクションなどのディレクトリ リパース ポイントの削除を試みます。
    *   選択された読み取り専用、隠し、およびシステム属性のクリアを試みますが、これは ACL を普遍的に書き換えたり、すべてのファイルにアクセス可能にしたりするものではありません。
    *   削除を容易にするために、問題のある名前や長いパスを名前変更します。
    *   複数のボックスの保留ディレクトリが処理される場合があります。`/box:` はこのフェーズをそのボックスだけに制限しません。
    *   既定では、名前変更されたサンドボックス フォルダーを削除するために標準システム コマンド RMDIR が使用されます。
    *   あるいは、[DeleteCommand](DeleteCommand.md) を介してサードパーティ製ユーティリティを選択できます。[サンドボックスの安全な削除](SecureDeleteSandbox.md)を参照してください。

_delete_sandbox_ コマンドはフェーズ 1 を実行し、フェーズ 2 を非同期で起動します。最初の Start.exe プロセスはすべての物理的な削除が完了するのを待機しないため、その成功した終了はすべての内容が削除された証拠ではありません。Start.exe は、特定のフェーズを呼び出すために次のコマンドも受け付けます。
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase1
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_phase2
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase1
  "C:\Program Files\Sandboxie\Start.exe"  delete_sandbox_silent_phase2
```

* * *

<div id="reload-configuration"></div>

### 構成の再読み込み

このコマンドは、Sandboxie.ini から共有ドライバー構成を再読み込みします。通常、ファイルを手動で編集した後に役立ち、`/box:` によるスコープはありません。
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /reload
```

Start.exe は `/reload` をディスパッチした後に終了コード 0 を返しますが、基になる再読み込み操作が失敗を報告した場合でも同様です。これは再読み込み成功の確認ではありません。このコマンドは省略可能なドライバー コンポーネントの再構成を要求しません。

再読み込みは共有構成を更新しますが、すでに実行中のプロセスが変更された設定を認識するかどうかは、その設定のコンシューマーとキャッシュのライフサイクルによって異なります。プロセス初期化設定は、通常、影響を受けるプロセスの再起動が必要です。普遍的なライブ更新、アトミックな再読み込み、またはすべての失敗時に以前の構成が保持されることを仮定しないでください。

* * *

<div id="disable-forced-programs"></div>

### 強制プログラムの無効化

ホスト側の起動では、次の修飾子は強制ルールにもかかわらずプログラムをサンドボックス外で実行することを要求します。それらは [Run Sandboxed] 選択ウィンドウから [Run Outside Sandbox] を使用するのと似ています。すでにサンドボックス化されたプロセスがサンドボックスから脱出する方法ではありません。
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  /dfp            c:\path\to\program.exe
  "C:\Program Files\Sandboxie\Start.exe"  /disable_force  c:\path\to\program.exe
```

/dfp と /disable_force は同一であることに注意してください。[Run Sandboxed] コマンドをクリックするときに Ctrl キーと Shift キーを押し下げることでも、このオプションを選択できます。

古いベア コマンドは、呼び出し元のセッションに対して一時的な [Disable Forced Programs] モードを要求します。これは、Sandboxie Control の[通知領域アイコン メニュー](TrayIconMenu.md#disable-forced-programs)（[ファイル メニュー](FileMenu.md#disable-forced-programs)ではない）からコマンドを使用するのと機能的に似ています。
```cmd
  "C:\Program Files\Sandboxie\Start.exe"  disable_force
```

スラッシュがないことに注意してください。このコマンドはモードを有効にしてカウントダウンを再開することを要求するものであり、トグルではありません。キャンセルを要求するには:

```cmd
  "C:\Program Files\Sandboxie\Start.exe"  disable_force_off
```

どちらのベア コマンドも、ドライバーの承認とセッション ルールの対象です。それらのゼロ終了ステータスは、要求された変更が適用されたことを証明しません。

* * *

### 詳細 / 内部スイッチ

以下のスイッチとベア コマンドは、主に高度な使用、自動化、または内部/デバッグ シナリオを対象としています。これらのオプションはバージョン間で変更される可能性があり、通常はエンド ユーザーには必要ありません。

#### /keep_alive

サンドボックス化された Start.exe インスタンスは、起動されたプロセスを監督し、ゼロ以外の結果の後にそれを再起動できます。これはクラッシュ検出器ではありません。意図的なゼロ以外の終了も再起動をトリガーする可能性があります。

> [!Note]
> 再起動ループはサンドボックス化されたインスタンスで実行されます。通常のホストからボックスへの起動は、消費された `/keep_alive` 修飾子を転送しません。一部の直接ホスト起動パスは、その再起動ループを実行せずに待機するためにこれを使用できます。

- 該当する起動パスがプロセス ハンドルを提供する場合、Start.exe は待機し、そのプロセスの終了コードを読み取ります。上記の単一プロセス待機の制限は依然として適用されます。
- ゼロの結果は監督を停止します。
- 連続する短時間のゼロ以外の試行は、最初の試行に続いて最大 5 回の再試行を許可します。
- 少なくとも 5 秒間続くゼロ以外の試行は、別の再試行が許可されている間だけカウンターをリセットします。カウンターが使い果たされると、最後の試行が長かった場合でも監督を停止します。5 回の再試行は普遍的なライフタイム最大値ではありません。
- 5 秒の測定には、分離された子の実行時間だけでなく、ランチャーの起動と待機の作業も含まれます。
- 許可された再試行の間に明示的な遅延やバックオフはありません。
- プログラムを作成できない場合、Start は作成を再試行するのではなく、その呼び出しに対してキープアライブを無効にします。

`/wait` とは異なり、サンドボックス化された監督パスは、ゼロ以外の結果の後にプログラムを再度起動できます。継続的な可用性を保証したり、プロセス ツリー全体を監督したりするものではありません。監督が終了すると、最終的な監督結果を返します。再試行が使い果たされた場合、これが最後のゼロ以外の結果です。

監督する Start.exe がすでにサンドボックス内で実行されている場合は、最初の例を使用します。通常のホスト起動では、2 番目の例はボックス内で監督できる内部の Start.exe を起動します。
```cmd
"Start.exe" /keep_alive notepad.exe
"Start.exe" Start.exe /keep_alive notepad.exe
```
内部の `Start.exe` は解決可能でなければなりません。これらの例は単一プロセスの監督を要求するものであり、すべての失敗からの回復を保証するものではありません。

#### /fake_admin

ホスト側のサンドボックス エントリ起動では、サンドボックス内で偽装された Administrator コンテキストを要求します。これは、管理者状態を検出して異なる動作をする一部のインストーラーやレガシー プログラムに役立ちます。これは互換性対策であり、実際の UAC 昇格ではありません。すでにサンドボックス化された呼び出しが同じフラグを適用するとは限りません。[偽の管理者権限](FakeAdminRights.md)を参照してください。

例:
```cmd
"Start.exe" /fake_admin setup.exe
```

#### /force_children（または /fcp） {#force_children-or-fcp}

ホスト側の直接起動では、起動されたプロセスを登録してその子を選択したサンドボックスに強制しようと試みます。これはそれ自体では最初に起動されたプログラムをサンドボックス化せず、すでにサンドボックス化された呼び出し元をサンドボックス外に移動する方法でもありません。登録は起動後に発生し、`/wait` や `/keep_alive` との一部の組み合わせを含め、競合がなく成功することは保証されません。[子プロセスの強制](ForceChildren.md)を参照してください。

例:
```cmd
"Start.exe" /fcp myinstaller.exe
"Start.exe" /force_children myinstaller.exe
```

#### /env:=Refresh

プログラムを起動する前に、現在サンドボックス化されている Start.exe プロセスの環境を更新します。更新アクションはホスト解析インスタンスでは実行されず、任意のすでに実行中のプロセスを変更しません。個々の値を設定するには `/env:Name=Value` を使用します。この修飾子だけでは完全な起動コマンドではありません。

例:
```cmd
"Start.exe" /env:=Refresh cmd.exe
```

#### uac_prompt

このベア内部ヘルパーは、他のコンポーネントによって生成されたパラメーターを使用して Sandboxie の UAC プロンプトを表示します。セキュア デスクトップの使用は、適用される Windows および Sandboxie の設定によって異なります。これは通常の `/uac_prompt` スイッチでも、任意の呼び出し元向けの安定した公開 API でもありません。

例:
```cmd
"Start.exe" uac_prompt <internal-pkt-params>
```

#### mount_hive

内部のサンドボックス初期化ヘルパーです。ホスト実行はそれをボックスに転送し、サンドボックス化された実行はヘルパー プロセスを一時的に存在させ続けます。レジストリ ハイブのマウントは、このコマンドのパーサーでの直接マウント呼び出しではなく、サンドボックス化されたプロセスの初期化を通じて行われます。ヘルパーの終了は、完全なレジストリの準備完了を証明しません。

例:
```cmd
"Start.exe" mount_hive
```

#### run_sbie_ctrl と open_agent[:param]

これらの内部コマンドは、サービスを通じて制御エージェントの起動を要求します。`run_sbie_ctrl` は構成済み/既定のエージェントを使用し、`open_agent:` は適格なホスト呼び出し元に対してエージェント コマンド テキストを指定できます。それらは無制限の任意のエージェント タスク実行ではなく、起動はエージェントがすでに実行されているかどうかを含むサービス/セッションの状態に依存します。

これらは通常のスラッシュ オプション パーサーの前に処理されます。`/box:` や `/silent` を前に付けても同じヘルパー動作が保持されると仮定しないでください。

例:
```cmd
"Start.exe" run_sbie_ctrl
"Start.exe" open_agent:SandMan.exe
"Start.exe" open_agent:"SandMan.exe -autorun"
```

#### auto_run

このスタートアップ ヘルパーは、サポートされているコピーされたサンドボックスの `Run`/`RunOnce` エントリとスタートアップの場所を処理します。これは `StartProgram`、`StartService`、および `AutoExec` とは別のものであり、ホストから見えるすべての Run キーの実行を約束するものではありません。サービス開始ワークフローについては、[システム ボックスの開始](StartSystemBox.md)を参照してください。

```cmd
"Start.exe" /box:ExampleBox auto_run
```

* * *

<div id="related-reading-material"></div>

### 関連資料

以下も参照してください: [InjectDll](InjectDll.md) と [SBIE DLL API](SBIEDLLAPI.md)

[ヘルプ トピック](HelpTopics.md)に進みます。
