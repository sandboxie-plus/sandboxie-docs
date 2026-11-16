Sandboxie-Live は、最新の修正を試し、最新のバグを発見したいプロジェクト サポーター（サポーター証明書を持つユーザー）および/または冒険心のある人々（プレビュー チャネル）向けの高速更新サービス（安定版チャネル）です。

「Global Options」の「Support & Updates」タブで、ユーザーは次のリリース チャネルから選択できるようになりました。

![grafik](https://user-images.githubusercontent.com/3890945/208420986-d28373f1-8584-4455-ae39-83d2e9eec78d.png)

1. Stable - GitHub Releases
2. Preview - GitHub Pre-Releases

そこでは、「New Version」（インストーラーが利用可能）または「Version Update」（既存のインストールの個々のファイルのみが更新される）が見つかったときの動作も選択できます。

「New Version」の場合、次のオプションが利用可能です。

- Notify
- Download & Notify
- Download & Install

「Version Update」の場合、次のオプションが利用可能です。

- Ignore
- Notify
- Download & Notify
- Download & Install

「New Version」には「Ignore」オプションはありません。これは更新チェックを無効にすることでカバーされるためです。

「Stable」チャネルでは、「Version Update」のチェックは有効な証明書を持つサポーターのみが利用できます。このチャネルでは、すべての更新が署名されており、最新の互換性テンプレートと緊急のバグ修正および翻訳で構成されています。

「Preview」チャネルでは、「Version Update」は数日ごとにリリースされる未署名のテスト ビルド（署名されたドライバーを除く）で構成されています（1.6.0、1.6.1a、1.6.1b など）。ここでは更新に半分しかテストされていない修正だけでなく、まだバグがないとは限らない新機能も含まれるためです。
