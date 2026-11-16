# よくある質問


### 概要 {#overview}

*   [Sandboxie とは何で、他のソリューションとどう違うのですか?](#what-is-sandboxie-and-how-is-it-different-than-other-solutions)
*   [Sandboxie を使うとどのくらい安全ですか?](#how-safe-would-i-be-by-using-sandboxie)
*   [Sandboxie を使うなら他のソリューションも必要ですか?](#do-i-need-other-solutions-if-i-use-sandboxie)
*   [Sandboxie ではどのような種類のプログラムを実行できますか?](#what-kinds-of-programs-can-i-run-using-sandboxie)
*   [Sandboxie を実行するための技術要件は何ですか?](#what-are-the-requirements-to-run-sandboxie)

### 技術 {#technical}

*   [Sandboxie は技術的にどのようにして私を保護しますか?](#how-does-sandboxie-protect-me-technically)
*   [Sandboxie は悪意のあるキーロガーから私を保護しますか?](#will-sandboxie-protect-me-from-malicious-key-loggers)
*   [一部の競合製品はサンドボックス化を開始するために再起動が必要なのはなぜですか?](#some-competing-products-require-a-reboot-to-initiate-sandboxing-why)
*   [Sandbox ドライバーからのメッセージが表示されるのはなぜですか?](#why-am-i-getting-some-messages-from-sandbox-driver)
*   [なぜこんなに多くのファイルがサンドボックスにコピーされるのですか?](#why-are-so-many-files-copied-into-the-sandbox)
*   [SandboxieRpcSs と SandboxieDcomLaunch とは何ですか?](#what-are-sandboxierpcss-and-sandboxiedcomlaunch)
*   [Sandboxie を使って電子メール内のウイルスから身を守るにはどうすればよいですか?](#how-can-i-use-sandboxie-to-protect-myself-from-viruses-in-email)
*   [たまにしか使わない場合に Sandboxie を構成するにはどうすればよいですか?](#how-to-configure-sandboxie-for-only-an-occasional-use)

### 問題 {#problems}

*   [保存したお気に入りやダウンロードをクイック復元に表示させるにはどうすればよいですか?](#how-do-i-make-quick-recovery-show-my-saved-favorites-and-downloads)
*   [ダウンロードしたファイル、ドキュメント、またはメールをサンドボックス内に保存してしまいました。どうやって取り出せばよいですか?](#i-saved-a-downloaded-file-a-document-or-an-email-inside-the-sandbox-how-do-i-get-it-out)
*   [既定の Web ブラウザーをサンドボックス内で実行すると、なぜ誤ったプログラムが起動するのですか?](#why-does-the-wrong-program-start-when-i-run-my-default-web-browser-sandboxed)
*   [サンドボックス内で Sysinternals Process Monitor が動作しないのはなぜですか?](#why-does-sysinternals-process-monitor-not-work-inside-the-sandbox)
*   サンドボックス内で正しく動作しないプログラムがある場合は、[問題を報告](https://github.com/sandboxie-plus/Sandboxie/issues/new/choose)する前に[既知の競合](KnownConflicts.md)ページで調べてください。

* * *

[ヘルプ トピック](HelpTopics.md)に戻る

* * *

<div id="what-is-sandboxie-and-how-is-it-different-than-other-solutions"></div>

### Sandboxie とは何で、他のソリューションとどう違うのですか?

PC を 1 枚の紙だと考えてください。実行するすべてのプログラムはその紙に書き込みます。ブラウザーを実行すると、訪問したすべてのサイトについて紙に書き込みます。そして遭遇するマルウェアは通常、自分自身をその紙に書き込もうとします。

従来のプライバシーおよびアンチマルウェア ソフトウェアは、紙に残したくないと思われる書き込みを見つけて消去しようとします。ほとんどの場合、それらは正しく処理します。しかし、まずこれらのソリューションの制作者は、紙の上で何を探すべきか、またそれを安全に消去する方法をソリューションに教えなければなりません。

一方、Sandboxie のサンドボックスは、紙の上に置かれた透明なレイヤーのように機能します。プログラムは透明なレイヤーに書き込み、プログラムからはそれが本物の紙であるかのように見えます。サンドボックスを削除すると、透明なレイヤーを取り除くようなもので、変更されていない本物の紙が現れます。

![](../Media/PaperAnimation.gif)

紙のメタファーを提供してくれた _esalkin_ に感謝します。グラフィックを提供してくれた _warwagon_ に感謝します。

**[目次に戻る](#overview)**

* * *

<div id="how-safe-would-i-be-by-using-sandboxie"></div>

### Sandboxie を使うとどのくらい安全ですか?

Sandboxie を使えばかなり安全です。ただし、時折、人々が Sandboxie の脆弱性、つまり悪意のあるソフトウェアがシステムに侵入できる抜け穴を見つけることができることに注意すべきです。

これは非常にまれであり、攻撃経路である穴を塞ぐことで迅速に解決されます。

したがって、より従来型のアンチマルウェア ソフトウェアを導入することをお勧めします。これが次の質問の主題です。

**[目次に戻る](#overview)**

* * *

<div id="do-i-need-other-solutions-if-i-use-sandboxie"></div>

### Sandboxie を使うなら他のソリューションも必要ですか?

Sandboxie は最初の防御線になるかもしれませんが、より従来型のアンチウイルスおよびアンチマルウェア ソリューションで補完するべきです。これらのソリューションは、システムが何らかの形で感染したかどうかを知らせてくれます。

通常、これらの他のソリューションは、悪意のあるソフトウェアやその他の脅威を発見するためにさまざまな形式のパターン マッチングを採用しています。一方、Sandboxie は、どのソフトウェア コードもサンドボックスから出すほどには信頼しません。

2 つのアプローチを組み合わせることで、他の未知の当事者の利益に奉仕する悪意のあるソフトウェアをコンピューターから締め出すことができます。

**[目次に戻る](#overview)**

* * *

<div id="what-kinds-of-programs-can-i-run-using-sandboxie"></div>

### Sandboxie ではどのような種類のプログラムを実行できますか?

ほとんどのアプリケーションをサンドボックス内で実行できるはずです。

*   主要な Web ブラウザー
*   メールおよびニュース リーダー
*   インスタント メッセンジャーおよびチャット クライアント
*   ピアツーピア ネットワーキング
*   Office スイート（MS Office、LibreOffice、OpenOffice）
*   ほとんどのゲーム
    *   特に、拡張ソフトウェア コードをダウンロードするオンライン ゲーム

このリストのすべての場合において、クライアント側のプログラムはリモートのソフトウェア コードにさらされており、そのコードがプログラムをシステムに侵入するための経路として利用する可能性があります。プログラムをサンドボックス内で実行することで、その経路に対する制御を大幅に強化できます。

さらに、一部のアプリケーションをサンドボックスに_インストール_することもできます。

**[目次に戻る](#overview)**

* * *

<div id="what-are-the-requirements-to-run-sandboxie"></div>

### Sandboxie を実行するための技術要件は何ですか?

Sandboxie は以下で動作します。

*   Windows XP SP3（Sandboxie 5.22 まで、および [v5.40](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v5.40) のみ）
*   Windows Vista SP2（Sandboxie 5.22 まで）
*   Windows 7 32/64
*   Windows 8.1 32/64
*   Windows 10 32/64（[モダン アプリはサポートされていません](https://github.com/sandboxie-plus/Sandboxie/issues/19)）
*   Windows 11 64（[モダン アプリはサポートされていません](https://github.com/sandboxie-plus/Sandboxie/issues/19)）

[ダウンロード ページ](https://github.com/sandboxie-plus/Sandboxie/releases)を参照してください。

サポートされている Web ブラウザー（32 ビットと 64 ビットをサポート）

*   Internet Explorer 8、9、10、11
*   Microsoft Edge (Chromium)
*   Google Chrome
*   Firefox
*   Opera
*   PaleMoon
*   SeaMonkey
*   Vivaldi
*   Waterfox
*   Brave Browser
*   その他多数!

Sandboxie は以下では動作しません...

*   Windows XP x64 ビット
*   Windows 95、98、または ME
*   Mac または Linux オペレーティング システム

Sandboxie は直接サポートされていないため、Microsoft Server オペレーティング システムにはインストールしないでください。ただし、多くのユーザーが正常に展開しています。

Sandboxie は VM 環境（VMWare、VirtualBox、Apple BootCamp など）で実行できます。

Sandboxie を実行するための特別なハードウェア要件はありません。ただし、タッチスクリーン デバイスでのテストは行っていません（多くのユーザーが Surface Pro や同様のデバイスに Sandboxie を正常にインストールしています）。

Sandboxie に必要なメモリはわずかで、パフォーマンスへの影響はごくわずかです。

**[目次に戻る](#overview)**

* * *

<div id="how-does-sandboxie-protect-me-technically"></div>

### Sandboxie は技術的にどのようにして私を保護しますか?

Sandboxie は、オペレーティング システム (OS) に溶け込むことで、サンドボックス化機能を OS に拡張します。アプリケーションはディスク ストレージなどのハードウェアに直接アクセスすることは決してできず、OS に代行を依頼する必要があります。Sandboxie は OS に統合されているため、回避されるリスクなしにその機能を実行できます。

以下のクラスのシステム オブジェクトが Sandboxie によって監視されます: ファイル、ディスク デバイス、レジストリ キー、プロセスおよびスレッド オブジェクト、ドライバー オブジェクト、およびプロセス間通信に使用されるオブジェクト: 名前付きパイプとメールボックス オブジェクト、イベント、ミューテックス（NT 用語ではミュータント）、セマフォ、セクション、LPC ポート。これに関する詳細については、[サンドボックス階層](SandboxHierarchy.md)を参照してください。

Sandboxie はまた、サンドボックス内で実行されているプログラムが非サンドボックス プログラムを乗っ取り、サンドボックス外で動作するための手段として使用することを防ぐ措置を講じています。同じ理由で、Sandboxie はサンドボックス化されたプロセスがサンドボックス化されていないプロセスのメモリを読み取ることを許可せず、選択したホスト プロセスをサンドボックス化されたプロセスから隠す機能を提供します。これに関する詳細については、[#59](https://github.com/sandboxie-plus/Sandboxie/issues/59#issuecomment-653756014) と [0.3 / 5.42 のリリース ノート](https://github.com/sandboxie-plus/Sandboxie/blob/master/CHANGELOG.md#added-35)を参照してください。

Sandboxie はまた、サンドボックス内で実行されているプログラムがドライバーを直接読み込むことを防ぎます。また、プログラムが Service Control Manager と呼ばれる中央システム コンポーネントにドライバーの代行読み込みを依頼することも防ぎます。このようにして、ドライバー、さらに重要なことにルートキットをサンドボックス化されたプログラムによってインストールすることはできません。

ただし、Sandboxie は通常、高度な構成なしでは、その監視下で実行されているプロセスによるユーザー データの持ち出しを防がないことに注意してください。既定のファイルおよびレジストリ アクセス スキームは、ユーザーが特定のパスを閉じるように指定した場合を除き、すべてに対して読み取りを許可するものです。しかし、[ClosedFilePath](ClosedFilePath.md) と [ClosedKeyPath](ClosedKeyPath.md) 設定を慎重に構成することで、この目標も達成できます。

これに関する今後の開発を追いたい場合は、[新しいプライバシー強化されたファイル/レジストリ アクセス スキーム、ホワイト リスト/テンプレート モード、計画と議論](https://github.com/sandboxie-plus/Sandboxie/issues/890)を参照してください。

**[目次に戻る](#technical)**

* * *

<div id="will-sandboxie-protect-me-from-malicious-key-loggers"></div>

### Sandboxie は悪意のあるキーロガーから私を保護しますか?

はい、ある程度は。まず第一に、あなたのシステム（サンドボックス外）が、インストールされたキーロガーによってすでに侵害されていない必要があります。Sandboxie は、すでにサンドボックス外で実行されているキーロガーから保護することはできません。

誤ってキーロガーをシステムに入れないように、常にサンドボックス内でブラウジングすることを検討するとよいでしょう。

キーロガーを確実に検出することは非常に困難です。長い説明については、[キーロガーの検出](DetectingKeyLoggers.md)を参照してください。したがって、Sandboxie がキーロガーに対する保護のために提供する最も重要なツールは、サンドボックスを削除することです。

（すべてのサンドボックスで）すべてのサンドボックス化されたアクティビティを停止し、これから使用するサンドボックスを削除すると、すべてのキーロガーが死んだとかなり確信できます。

**[目次に戻る](#technical)**

* * *

<div id="some-competing-products-require-a-reboot-to-initiate-sandboxing-why"></div>

### 一部の競合製品はサンドボックス化を開始するために再起動が必要なのはなぜですか?

コンピューティング環境への変更は、永続的であるためには、最終的にディスク ストレージに到達する必要があります。これは明らかにファイルに当てはまります。しかし、システム レジストリに保存された設定や環境設定のようなものにも当てはまります。

一部の競合製品は、ディスク ストレージを全体としてサンドボックス化するため、使用するたびに再起動が必要です。それらはオペレーティング システムとその中のすべてに単一の仮想ディスクを提供し、それを永続的な変更を閉じ込めるために使用します。

オペレーティング システムは、一部のタスクに 1 つのディスクを使用し、別のタスクに別のディスクを使用するようには設計されていません。したがって、仮想ディスクとの切り替えには再起動が必要です。

Sandboxie は、ディスク全体ではなくファイルへのアクセスをサンドボックス化するため、再起動を必要としません。また、レジストリ キーへのアクセスもサンドボックス化します。さらに、サンドボックス化されたプログラムに、騙されていないと思い込ませるために、他の多くのクラスのシステム コンポーネントへのアクセスもサンドボックス化します。

一部の競合製品におけるこの低レベル サンドボックス化により、システム ドライバーを含む、より幅広いアプリケーションやシステム ツールをサンドボックスにインストールできます。Sandboxie はほとんどのアプリケーションをサンドボックスにインストールできますが、システム ソフトウェアやドライバーはインストールできません。

明らかなように、他のほとんどのものと同様、各ツールには長所と短所があり、目の前のタスクに最適なツールを選択する必要があります。

**[目次に戻る](#technical)**

* * *

<div id="why-am-i-getting-some-messages-from-sandbox-driver"></div>

### Sandbox ドライバーからのメッセージが表示されるのはなぜですか?

すべてのメッセージがエラーではなく、発生したイベントを単に通知するものもあります。詳細については、[SBIE メッセージ](SBIEMessages.md)と[メッセージをファイルに記録する](MessagesFromSandboxie.md#log-messages-to-a-file)を参照してください。

**[目次に戻る](#technical)**

* * *

<div id="why-are-so-many-files-copied-into-the-sandbox"></div>

### なぜこんなに多くのファイルがサンドボックスにコピーされるのですか?

プログラムがファイルにアクセスするとき、ファイルに対して計画している操作を宣言します: ファイルから読み取るのか、ファイルに書き込むのか、属性を変更するのか、などです。プログラムがファイルへの何らかの書き込みアクセスを宣言するたびに、Sandboxie はそれをサンドボックスにコピーします。場合によっては、プログラムが実際には書き込むつもりがないのに書き込むと宣言することがありますが、それでも Sandboxie はファイルをサンドボックスにコピーしなければなりません。

**[目次に戻る](#technical)**

* * *

<div id="what-are-sandboxierpcss-and-sandboxiedcomlaunch"></div>

### SandboxieRpcSs と SandboxieDcomLaunch とは何ですか?

[サービス プログラム](ServicePrograms.md)を参照してください。

**[目次に戻る](#technical)**

* * *

<div id="how-can-i-use-sandboxie-to-protect-myself-from-viruses-in-email"></div>

### Sandboxie を使って電子メール内のウイルスから身を守るにはどうすればよいですか?

全文記事を参照してください: [メール保護](EmailProtection.md)。

**[目次に戻る](#technical)**

* * *

<div id="how-to-configure-sandboxie-for-only-an-occasional-use"></div>

### たまにしか使わない場合に Sandboxie を構成するにはどうすればよいですか?

既定では、Sandboxie は自動的に読み込まれ、起動するように構成されています。必要なときだけ Sandboxie を読み込むようにするには、次の変更を行います。

*   [Sandboxie Control](SandboxieControl.md) で、_構成 -> Windows シェル統合_ ウィンドウを開き、_When Windows starts_ チェックボックスをオフにして Sandboxie Control の起動を停止します。
*   Sandboxie Plus では、[Sandboxie-Plus 移行ガイド](PlusMigrationGuide.md#shell-integration)を参照してください。
*   Windows のサービス構成ウィンドウを開きます: _スタート メニュー -> コントロール パネル -> 管理ツール -> サービス_。次に Sandboxie サービスを見つけます。ダブルクリックしてプロパティ ウィンドウを表示します。_スタートアップの種類_ を自動ではなく手動に設定します。
*   Sandboxie のドライバー コンポーネントは Sandboxie サービスによって起動されます。したがって、サービスを手動で開始するように設定すると、間接的にドライバーも手動で開始するように設定されます。

Sandboxie Control を起動すると、サービスも起動します。（ただし、サービスを起動するには管理者権限が必要であることに注意してください。）

**[目次に戻る](#technical)**

* * *

<div id="how-do-i-make-quick-recovery-show-my-saved-favorites-and-downloads"></div>

### 保存したお気に入りやダウンロードをクイック復元に表示させるにはどうすればよいですか?

初期インストールでは既定でいくつかのフォルダーしか構成されていないため、クイック復元にすべてのフォルダーが表示されない場合があります。[クイック復元](QuickRecovery.md)も参照してください。

**[目次に戻る](#problems)**

* * *

<div id="i-saved-a-downloaded-file-a-document-or-an-email-inside-the-sandbox-how-do-i-get-it-out"></div>

### ダウンロードしたファイル、ドキュメント、またはメールをサンドボックス内に保存してしまいました。どうやって取り出せばよいですか?

[Sandboxie とは何か](#what-is-sandboxie-and-how-is-it-different-than-other-solutions)を読んだなら、Sandboxie が紙の上に置かれた透明なレイヤーのようなものであることがわかるでしょう。（紙はあなたのコンピューターです。）サンドボックス化されたプログラムを通じてファイル（ダウンロード、ドキュメント、メールなど）を保存すると、これらのファイルはサンドボックスという透明なレイヤーに入ります。

クイック復元を使用してこれらのファイルを取り出すことができます。別途構成しない限り、クイック復元は _Documents_、_Favorites_、_Desktop_、_Downloads_ フォルダーを調べます。これらのフォルダーのいずれかにファイルを保存した場合は、クイック復元を使用して簡単に取り出すことができます。

もう 1 つのアプローチは、1 つ以上のフォルダーを [OpenFilePath](OpenFilePath.md) として構成することです。そのようなフォルダーにファイルを保存すると、サンドボックス メカニズムを迂回し、実際のフォルダーに直接書き込まれます。この設定はより複雑ですが、場合によっては役立つこともあります。

**[目次に戻る](#problems)**

* * *

<div id="why-does-the-wrong-program-start-when-i-run-my-default-web-browser-sandboxed"></div>

### 既定の Web ブラウザーをサンドボックス内で実行すると、なぜ誤ったプログラムが起動するのですか?

これは一部の人に起こります。

Windows 7 では、コントロール パネルをアイコン ビューで開き、既定のプログラム > 既定のプログラムの設定を選択します。その後、既定として設定したいブラウザーを選択できます。

Windows 8/8.1 では、画面の右下隅または右上隅をポイント（クリックはしない）し、設定アイコンをクリックします。右下隅で、PC 設定の変更 > 検索とアプリ > 既定をクリックします。その後、既定として設定したいブラウザーを選択できます。

Windows 10/11 を使用している場合は、Windows の既定の Web ブラウザーが正しく設定されていることを確認してください（スタート メニューをクリックし、「既定のアプリ」と入力して、既定のアプリを選択します）。

**[目次に戻る](#problems)**

<div id="why-does-sysinternals-process-monitor-not-work-inside-the-sandbox"></div>

### サンドボックス内で Sysinternals Process Monitor が動作しないのはなぜですか?

Process Monitor はサンドボックス内では実行できませんが、サンドボックス内のアクティビティを監視することはできます。

**[目次に戻る](#problems)**
