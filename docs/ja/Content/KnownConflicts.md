# 既知の競合

* * *
既知の競合は、サンドボックス設定 > アプリケーション、またはサンドボックス オプション > アプリ テンプレート（Plus エディション）でアプリケーション構成を有効にすることで解決できます。
* * *

### すべてのプログラムが Sandboxie 内でインストールまたは実行できるわけではありません

問題: サービスやドライバーを呼び出す一部のアプリケーションは、Sandboxie 内でインストール/実行できない場合があります。

解決策 #1: システムにインストールされているサードパーティのセキュリティ ソフトウェアと競合している可能性があります（問題 [#647](https://github.com/sandboxie-plus/Sandboxie/issues/647) と [#293](https://github.com/sandboxie-plus/Sandboxie/issues/293) を参照）。どのセキュリティ スイートが関係している可能性があるかを詳しく知りたい場合は、[アーカイブされたフォーラム](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica726a726.html?f=11&t=21539)を参照してください。

解決策 #2: アプリケーションを新しい空のサンドボックスにインストールしようとすでに試した場合は、ホストにインストールしてからサンドボックス内で実行してください。

問題が解決しない場合、特に以前の Sandboxie バージョンで動作していたアプリケーションで問題が発生する場合は、[GitHub リポジトリ](https://github.com/sandboxie-plus/Sandboxie/issues)に投稿して詳細をお知らせください。

### Microsoft Store アプリ

問題: Microsoft Store アプリは Sandboxie Classic および Sandboxie Plus では動作しません。

解決策: 現時点ではありません。これに関する変更の可能性を追跡するには、問題 [#19](https://github.com/sandboxie-plus/Sandboxie/issues/19) を参照してください。

### Office 2013/2016/2019 & Office 365（C2R バージョンのみ）

問題: Microsoft Office 2013、2016、2019、および Office 365 の Click to Run バージョンは、サンドボックス化するとクラッシュします。これには Outlook 2013 以降が含まれます。

解決策: 修正は [v0.9.7 / 5.52.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.7) に含まれています。

### Office 2021

問題: Office 2021 はサンドボックス内にインストールできません。

解決策: 現時点ではありません。これに関する変更の可能性を追跡するには、問題 [#1675](https://github.com/sandboxie-plus/Sandboxie/issues/1675) または [#1900](https://github.com/sandboxie-plus/Sandboxie/issues/1900) を参照してください。

### Tor Browser

問題: Tor Browser はサンドボックス内で非常に遅くなったり、クラッシュしたり、一定時間後にクラッシュしたりします。

解決策: 修正は [v1.0.21 / 5.55.21](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.21) に含まれています。

### HP Universal Print Driver

問題: HP Universal Printer Status Monitor のポップアップ コンポーネントが、サンドボックス化された Web ブラウザーから印刷するときに失敗します。

解決策: サンドボックス設定 > リソース アクセス > COM アクセスを開き、追加をクリックして次のリソース名を入力します:
`{D713F357-7920-4B91-9EB6-49054709EC7A}`

### Microsoft Edge の自動削除機能

問題: 自動削除機能が Microsoft Edge で動作しなくなりました。

解決策: Microsoft Edge は（システム内の）「スタートアップ ブースト」と呼ばれる新しい設定で更新され、既定で有効になっています。これにより Edge が完全にシャットダウンされないため、このオプションを無効にするか、修正を含む [v1.1.2 / 5.56.2](https://github.com/sandboxie-plus/Sandboxie/releases/tag/v1.1.2) 以降をインストールすることをお勧めします。

### Steam ゲーム

問題: すべての Steam ゲームがサンドボックス内で機能するわけではありません。

解決策: ゲームはサンドボックスではなくコンピューターにインストールしてください。ほとんどのゲームは動作します。ただし、一部は単純に動作しない可能性があるという[既知の報告](https://github.com/sandboxie-plus/Sandboxie/labels/game%20issue)があります。Steam ゲームで問題が発生した場合は、ホスト マシンで Steam クライアントが更新されていることを確認してください。Steam をサンドボックス化せずに実行し、ゲームをホスト コンピューターにダウンロードしてインストールし、回避策としてゲームのショートカットを「右クリック」して「Run Sandboxed」を選択します。問題が解決しない場合は、[GitHub リポジトリ](https://github.com/sandboxie-plus/Sandboxie/issues)に投稿して詳細をお知らせください。

### GOG ゲームと Galaxy ベータ

問題: GOG Galaxy のゲームはサンドボックス化すると実行されない場合があります。

解決策: 部分的な回避策が [#1246](https://github.com/sandboxie-plus/Sandboxie/issues/1246) で利用できます。GOG プログラム フォルダーを「強制」して、サンドボックス内で正しく動作させることができます。[ForceFolder](ForceFolder.md)も参照してください。

### Windows 11 のどのサンドボックスでもマイクやカメラにアクセスできない

問題: Windows 11 システムでは、どのサンドボックスでもマイク/カメラにアクセスできません。

解決策: 回避策が [#1669](https://github.com/sandboxie-plus/Sandboxie/issues/1669) で利用できますが、恒久的な修正はありません。

### Chromium 系ブラウザーのタブ セッションが Sandboxie で正しく復元されないことがある

問題: Chromium 系ブラウザーがサンドボックス外で実行されていると、タブ セッションが失われます。

解決策: まだ修正はありませんが、いくつかの回避策が [#558](https://github.com/sandboxie-plus/Sandboxie/issues/558) で利用できます。

### Windows エクスプローラーでフォルダー、ドライブ、またはコンテキスト メニューを開くのに時間がかかる

問題: Windows 10 および 11 でサンドボックス化すると、Windows エクスプローラーを開くのに時間がかかることがあります。

解決策: まだ修正はありません。[#69](https://github.com/sandboxie-plus/Sandboxie/issues/69) を参照してください。

### サンドボックス化されたファイル エクスプローラー インスタンスで「プログラムから開く」ダイアログが動作しない

問題: 「プログラムから開く」機能が Sandboxie で動作しません。

解決策: 修正は [v1.0.6 / 5.55.6](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.6) に含まれています。

### ファイル エクスプローラーで検索ボックスを使用できない

問題: サンドボックス化するとファイル エクスプローラーの検索ボックスにフォーカスが当たらず、何も入力できません。

解決策: 修正は [v0.9.8c / 5.53.2](https://github.com/sandboxie-plus/Sandboxie/releases/tag/0.9.8c) に含まれています。

### プログラムをサンドボックス化しているときに「Sandboxed service failed to start: BITS」または「Request to start service bits was denied」が表示されることがある

問題: BITS サービスは、Sandboxie でブロックされる WMI の一部を使用しているため、いくつかの Windows 10 リリース以降壊れているようです。

解決策: 回避策は [v1.0.1 / 5.55.1](https://github.com/sandboxie-plus/Sandboxie/releases/tag/1.0.1) に直接含まれています。

### このリストに自分の問題が見つからない

さらに問題を検索したい場合は、[GitHub リポジトリ](https://github.com/sandboxie-plus/Sandboxie)を参照してください。
