# プライバシーに関する懸念

これは高度なトピックであり、Sandboxie の下でプログラムを実行した後でも、コンピューターが_どの_プログラムが実行されたか、またはそれらが何をしたかを記録する可能性があることを説明します。これはセキュリティ侵害ではなく、サンドボックス化されたプログラムがコンピューターに感染したり、その他の方法で悪用したりすることを決して許可しないことを強調することが重要です。ただし、Sandboxie の使用のプライバシー面に関心のある方にとって興味深い読み物になるかもしれません。

**概要**

Sandboxie の指針となる原則は、コンピューターとオペレーティング システムをクリーンで健全な状態に保つ目的で、Sandboxie が監督するプログラムによって行われるあらゆるアクションを分離して封じ込めることです。

Sandboxie の下でプログラムを実行することによる副作用のほとんどは、実際には Sandboxie の下で実行されているそのプログラム自体によって引き起こされ、サンドボックスが削除されると消えます。たとえば、Sandboxie の下で実行されている Web ブラウザーは、閲覧履歴をサンドボックスに記録し、この履歴はサンドボックスを削除すると完全に消去されます。

したがって、上記の指針となる原則から小さな論理的な飛躍を行い、Sandboxie の原則がプライバシーを保護し、その監督下で実行されているプログラムによって直接的または間接的に引き起こされたすべての痕跡をクリーンアップすることであると仮定するのは簡単です。しかし、この仮定は正しくありません。

Sandboxie は、監督するプログラムによって行われるアクションを封じ込めることに多大な労力を費やしていますが、Sandboxie は、あなた自身の Windows オペレーティング システムがコンピューターで行ったことの記録を保持するのを防ぐためにまったく効果を発揮しません。

Sandboxie 側の極端なプライバシーへの配慮という誤った仮定をする人は、サンドボックス内でさえ、どのプログラムが実行されているかを記録するいくつかの種類のトレースとログを Windows で見つけて驚くかもしれません。

このページでは、Sandboxie の監督下かどうかに関係なく、実行するプログラムに関する情報を記録するさまざまな既知のメカニズムについて説明します。

**Prefetch と SuperFetch**

Windows XP で導入された Prefetch と、Windows Vista で導入された SuperFetch は、Windows の [prefetcher](https://en.wikipedia.org/wiki/Prefetcher) コンポーネントを構成します。

このコンポーネントは、プログラム ファイルのコピーをすばやくアクセスできる場所に保持することで、アプリケーションの起動時間を改善するように設計されています。コピーは、メインの Windows フォルダー内にある _Prefetch_ というフォルダーに保持されます。通常は _C:\Windows\Prefetch_ です。

Windows は、プログラムが Sandboxie の下で実行された場合でも、プログラム ファイルのコピーをこの Prefetch フォルダーに保存する場合があります。

Prefetch の動作は、起動シーケンス中に使用されるプログラムのみをキャッシュするように、またはまったく何もキャッシュしないように減らすことができます。詳細については、次のリンクを参照してください。

* [https://www.ghacks.net/2008/01/13/enableprefetcher-in-prefetchparameters](https://www.ghacks.net/2008/01/13/enableprefetcher-in-prefetchparameters)
* [https://www.howtogeek.com/998/change-superfetch-to-only-cache-system-boot-files-in-vista](https://www.howtogeek.com/998/change-superfetch-to-only-cache-system-boot-files-in-vista)
* [https://www.howtogeek.com/989/how-to-disable-superfetch-on-windows-vista](https://www.howtogeek.com/989/how-to-disable-superfetch-on-windows-vista)

**MUI キャッシュ**

Windows エクスプローラーは、それを通じて直接起動されたプログラムの名前をレジストリに記録します。これには、スタート メニュー、デスクトップ、クイック起動領域、または任意のフォルダー ビューを通じたプログラムの起動が含まれます。右クリックの「Run Sandboxed」アクションを使用して Sandboxie の下でプログラムを起動した場合でも同様です。

記録された情報は、このレジストリ キーに保持されます。
```
   HKEY_CURRENT_USER\Software\Microsoft\Windows\ShellNoRoam\MUICache
```

Sandboxie の機能（Sandboxie スタート メニューなど）を通じて、またはすでに Sandboxie の下で実行されているプログラムを通じてプログラムを起動する場合、この情報はサンドボックス内のレジストリに保持されます。

この情報を消去できるさまざまなサードパーティ製レジストリ クリーニング ツールがあります。

**Windows タスクバー**

Windows 7 以降では、Windows エクスプローラーはタスクバー上のアイコンに関連付けられた情報を保存します。この情報には、プログラムのアイコンとそれを起動するために使用されたコマンドが含まれます。情報は、ユーザー プロファイル フォルダー内の次のフォルダーのファイルに保存されます。
```
   %Appdata%\Microsoft\Internet Explorer\Quick Launch\User Pinned\ImplicitAppShortcuts
```

[サンドボックス設定 > アプリケーション > その他](ApplicationsSettings.md#miscellaneous)設定ページには、「Windows タスクバーのジャンプ リストをプログラムが更新することを許可する」という設定が含まれています。この設定が有効な場合、ユーザー プロファイル フォルダー内の次のフォルダーに追加のファイルが作成されます。
```
   %Appdata%\Microsoft\Windows\Recent\CustomDestinations
   %Appdata%\Microsoft\Windows\Recent\AutomaticDestinations
```

**Windows ページ ファイル**

通常の操作の過程で、Windows は、別のプログラムのためのスペースを確保するために、あるプログラムが使用するメモリの内容を退避させる必要がある場合があります。メモリの内容は Windows の[ページ ファイル](https://www.howtogeek.com/126430/what-is-the-windows-page-file)に保存されます。

Sandboxie の下で実行されるプログラムは、コンピューター内の他のプログラムと同じ Windows オペレーティング システムで実行されているため、サンドボックス化されたプログラムと通常のプログラムの一部が同じページ ファイル内に並んで存在することになる場合があります。

シャットダウン時にページ ファイルの内容をクリアするように Windows を構成することが可能です。詳細は[こちら](https://winaero.com/clear-pagefile-shutdown-windows-10)と[こちら](https://www.vistax64.com/threads/virtual-memory-paging-file-clear-at-shutdown.157323)を参照してください。

ページ ファイルの内容を暗号化するように Windows を構成することが可能です。

* _secpol.msc_ を実行して _ローカル セキュリティ ポリシー_ エディターを開きます
* _公開キーのポリシー_ というラベルのグループを展開します
* _暗号化ファイル システム_ というラベルの項目を右クリックして _プロパティ_ を選択します
* _許可_ を選択して暗号化ファイル システム (EFS) を有効にします
* _適用_ をクリックし、次に _OK_ をクリックします
* 再起動して新しい設定を有効にします

**Windows 休止状態ファイル**

Windows ページ ファイルと同様に、休止状態ファイルは、休止状態プロセスの一環としてコンピューターの電源を切る前のメモリとシステムの状態のコピーを保存します。したがって、休止状態ファイルには、サンドボックス化されたプログラムによって使用されたメモリの断片が含まれる場合があります。

**システムの復元**

復元ポイントは、ある時点でのオペレーティング システムの状態のスナップショットです。Windows XP 以降のシステムの復元コンポーネントは、これらのスナップショットを記録して復元します。

スナップショットは（通常はアクセスできない）_System Volume Information_ というフォルダーに記録され、サンドボックスのフォルダー内を含め、システム全体に見られる[多くの種類のファイル](https://docs.microsoft.com/en-us/windows/win32/sr/monitored-file-extensions)を含む場合があります。

したがって、システムの復元が、サンドボックス内にのみ存在するファイルまたはプログラムのバックアップ コピーをそのフォルダーに作成する可能性があります。

システムの復元コンポーネントは、一時フォルダー内のファイルとフォルダーを無視するように設定できるため、[サンドボックスを _%TEMP%\SANDBOX_ に移動](FileRootPath.md)し（既定の _C:\SANDBOX_ の代わりに）、レジストリ キー [FilesNotToSnapshot](https://learn.microsoft.com/en-us/windows/win32/vss/excluding-files-from-shadow-copies#using-the-filesnottosnapshot-registry-key) 内にそのパスを追加すれば、システムの復元はシャドウ コピー スナップショットを作成するときにサンドボックスを無視するはずです。詳細は[こちら](https://learn.microsoft.com/en-us/windows/win32/backup/registry-keys-for-backup-and-restore)を参照してください。

**システム、監査、およびその他のイベント ログ**

Windows は、実行中のプログラムに関する情報の断片をさまざまな[イベント ログ](https://en.wikipedia.org/wiki/Event_Viewer)に記録する場合があります。通常、プログラムについてログに記録される情報はごくわずかです。ただし、システムの一部の側面に対してセキュリティ監査が有効になっている場合、Windows は Sandboxie の下で実行されているプログラムによって行われたアクションの詳細を問題なくログに記録します。

Windows には Event Viewer プログラムがあり、イベント ログを表示および削除するために使用できます。詳細は[こちら](https://www.howtogeek.com/123646/htg-explains-what-the-windows-event-viewer-is-and-how-you-can-use-it)を参照してください。

**Windows システムトレイ アイコン**

Sandboxie の下で実行されているプログラムが[システムトレイ領域](https://www.computerhope.com/issues/chsys.htm)にアイコンを配置するよう要求すると、Sandboxie はそのプログラムが実際のシステムトレイ（通常はディスプレイの右下隅にあります）にアイコンを配置できるようにします。

これには、サンドボックス化されたプログラムのトレイ アイコンとの対話が他のトレイ アイコンとの対話と同じくらい簡単であるという利点があります。ただし、Windows がこのアイコンとその説明を、これまでに表示したすべてのトレイ アイコンの履歴に記録することを意味します。

[Windows](https://www.howtogeek.com/739/clean-up-past-notification-icons-in-windows-vista) でこの履歴を手動でクリアすることが可能です。この情報を消去できるサードパーティ製レジストリ クリーニング ツールも存在する場合があります。

**ディスクの最適化**

ディスク デフラグ ソフトウェアを使用して、データ ブロックのレベルでハード ディスクの内容を整理し、オペレーティング システムがファイルにすばやくアクセスできるようにすることができます。

これはプライバシーの懸念ではありませんが、サンドボックス化されたプログラムがディスクをデフラグできるという問題が提起されており、対処する必要があります。

Sandboxie の分離は、データ ブロックのより低いレベルではなく、より高いファイル レベルで発生します。ディスク上でデータ ブロックを移動してもサンドボックスの分離に影響はなく、悪意のあるプログラムが何らかの方法でそのデータをサンドボックスから「移動」するために使用することはできません。

**IP プライバシー**

Sandboxie の分離と保護は完全にローカル コンピューター内で発生し、他のリモート コンピューターからは見えません。したがって、サンドボックス化されたプログラムを使用してインターネットにアクセスすることは、Sandboxie の下で実行されていないプログラムを使用してインターネットにアクセスすることと同じに見えます。どちらの場合も、リモート コンピューターは IP アドレスによってアクセス元のコンピューターを識別します。

匿名 Web アクセスのためのさまざまなサードパーティ製ソリューションがあります。詳細は[こちら](https://en.wikipedia.org/wiki/Anonymous_web_browsing)を参照してください。

**Windows DNS ホスト キャッシュ**

Sandboxie は、Windows マシン上の _hosts_ ファイル (DNS キャッシュ) のログ記録と保存を防ぎません。これは _C:\Windows\System32\drivers\etc_ に書き込まれます。
