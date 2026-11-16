# AlertBeforeStart

*AlertBeforeStart* は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 1.14.1 および Sandboxie Classic 5.69.1 以降で利用できます。既定では無効です。

```ini
[DefaultBox]
AlertBeforeStart=y
```

有効にすると、*AlertBeforeStart* は、サンドボックス化されていない Start.exe インスタンスが選択されたサンドボックス内で自身を再起動する前に確認を求めます。対象となるホスト側の Start.exe 起動にユーザー同意の手順を追加するものであり、すべてのサンドボックス化されたプロセスに対する確認プロンプトではなく、セキュリティ境界でもありません。

## 対象となる起動パス

確認は、ホスト側の Start.exe サンドボックス進入パスに適用されます。対象となる例は次のとおりです:

- Start.exe /box:<box> program.exe、および選択されたサンドボックスまたは既定のサンドボックスを使用する通常のホスト側 Start.exe 起動。
- **Run Program**、**Run Web Browser**、**Run Email Reader**、**Start Menu** を含む、Start.exe を通じて起動する SandMan アクション。
- 現在の Sandboxie Plus の **Run Sandboxed** シェル統合。これは最終的に SandMan と Start.exe を通じて起動します。
- SandMan によって生成されたショートカット、および Start.exe を直接呼び出すショートカット。

これは、すべての SandMan アクションが対象になるという意味ではありません。アクションは、対象となる Start.exe サンドボックス進入パスを使用する必要があります。終了、再読み込み、削除操作など、そのパスの前に完了する制御専用の操作は、この設定の対象外です。より広範なコマンド リファレンスについては [Start Command Line](StartCommandLine.md) を参照してください。

現在の強制無効化や強制子プロセスのバイパス パスなど、意図的に初期プログラムをサンドボックス外で開始する起動パスは、その初期プロセスに対してこの確認に到達しません。

## サンドボックス内および強制起動

すでにサンドボックス化されている Start.exe インスタンスは、通常のサンドボックス内起動に対してこの確認を繰り返しません。したがって、この設定は、サンドボックス内ですでに行われている通常のプロセス作成を対象としません。これには次が含まれます:

- CreateProcess の子プロセス。
- 通常の ShellExecute 子起動。
- ブラウザーのレンダラーまたは GPU プロセス。
- ゲームを開始するゲーム ランチャー。
- サンドボックス化されたアプリケーションのその他の通常の子孫プロセス。

直接の [ForceProcess](ForceProcess.md) および [ForceFolder](ForceFolder.md) による起動も、この Start.exe 確認パスを使用しません。*AlertBeforeStart* を有効にしても、すべての強制プログラムに確認が必要になるわけではありません。別個の強制プログラムおよび強制フォルダーの動作については [Program Start Settings](ProgramStartSettings.md) を参照してください。

## 確認プロンプト

設定が有効な場合:

1. Start.exe はまず、選択されたサンドボックスで新しいプログラムを開始するかどうかを尋ねます。
2. 見かけ上の親プロセスが、Sandboxie のインストール ディレクトリ配下の実行可能パスに基づいて Sandboxie コンポーネントらしく見えない場合、2 番目の警告が表示されることがあります。

最初のプロンプトは対象のサンドボックスを識別します。開始される実行可能ファイル、完全なコマンド ライン、呼び出し元の実行可能ファイル、または呼び出し元のプロセス ID は表示しません。どちらのプロンプトも **Yes** と **No** の選択肢を使用し、「記憶する」オプションはありません。

- **Yes** は、該当する場合は 2 番目の警告に進むか、サンドボックスの起動に進みます。
- **No** は起動をキャンセルします。Start.exe は、要求されたサンドボックス化されたプロセスを起動する代わりに失敗して終了するため、スクリプトの呼び出し元は失敗したプロセスの結果を確認できます。

ユーザーが **No** を選択したという理由だけで、専用の SBIE 拒否メッセージは生成されません。

2 番目の警告は、見かけ上の親パスのチェックを使用します。これは、署名検証、信頼された発行元の検証、Sandboxie バイナリの認証、または呼び出し元のサンドボックス状態の検証ではありません。

## サイレントおよび非対話型の使用

/silent スイッチは *AlertBeforeStart* 確認ダイアログを抑制しません。/hide_window も同様に抑制しません。これらのスイッチは他の Start.exe UI の動作に影響しますが、これらの確認プロンプトをバイパスするものではありません。

この機能は対話型の確認ダイアログを想定しており、タイムアウトを提供しません。非対話型またはサービス形式の起動のための確定的な拒否メカニズムとして扱うべきではなく、Sandboxie はダイアログに応答できない場合の別個のログ記録や拒否のフォールバックを提供しません。

## 昇格

確認は、サンドボックス化された Start.exe インスタンスが作成される前、および最終的なターゲット プログラムの UAC または昇格要求の前に発生します。*AlertBeforeStart* は昇格を制御せず、UAC や特権の境界でもありません。

## セキュリティとポリシーの制限

このオプションは、対象となるサンドボックス起動が進む前にユーザー確認を要求することで、気付かれないホスト側の Start.exe の使用を減らすことができます。ただし、次のことは行いません:

- サンドボックス エスケープを防ぐ。
- Sandboxie コンポーネントを認証する。
- サンドボックス化されたプロセスが開始できるすべての方法を対象とする。
- StartRunAccess やその他の起動制限を置き換える。

アラートを確認しても、通常のサンドボックス ポリシーは上書きされません。別のポリシーが要求された起動を拒否する場合、**Yes** を選択しても許可は与えられません。[BreakoutProcess](BreakoutProcess.md) および [BreakoutFolder](BreakoutFolder.md) も別個のメカニズムです。

## サンドボックス オプション

Sandboxie Plus では、**Sandbox Options > Program Control > Start Restrictions** を開き、次を使用します:

**Display a pop-up warning before starting a process in the sandbox from an external source**

このチェックボックスは既定ではオフです。そのツールヒントには次のように表示されます:

> This setting can be used to prevent programs from running in the sandbox without the user's knowledge or consent.

ここで「外部ソース」とは、対象となるホスト側の Start.exe 起動パスを指します。正式に認証された呼び出し元のカテゴリではありません。

## スコープと変更の適用

この設定は、サンドボックスごとに構成することも、通常のテンプレートを通じて継承することも、GlobalSettings フォールバックを通じて指定することもできます。文書化されたプログラムごとまたはイメージごとの構文はありません。

Start.exe は、対象となるサンドボックス進入の試行ごとに設定を読み取ります。変更が保存されると、次回の対象となる呼び出しに適用されます。短命なランチャーは起動間でそれをキャッシュしません。このオプションが変更されたというだけで、SandMan、SbieSvc、および既存のサンドボックス化されたプログラムを再起動する必要はありません。Sandboxie.ini を手動で編集する場合は、通常の構成再読み込みの要件が引き続き適用されます。

## Sandboxie Plus と Classic

起動時の動作は共有の Start.exe に実装されています。Sandboxie Plus は SandMan でチェックボックスを公開しますが、Sandboxie Classic の Start.exe は SandMan インターフェイスを提供せずに INI 設定を尊重できます。

この設定を [Alert Process](AlertProcess.md) と混同しないでください。*AlertBeforeStart* は対象となる Start.exe サンドボックス進入の前に確認を要求しますが、*AlertProcess* は方向とスコープが異なる別個のアラート機能です。

## バージョン履歴

*AlertBeforeStart* は Sandboxie Plus 1.14.1 および Sandboxie Classic 5.69.1 で導入され、既定では無効です。SandMan のチェックボックスは同じリリース開発サイクル中に追加されました。現在の動作は引き続きホスト側の Start.exe 確認モデルを使用します。

## 関連する構成

- [Sandboxie Ini](SandboxieIni.md)
- [Start Command Line](StartCommandLine.md)
- [Program Start Settings](ProgramStartSettings.md)
- [Alert Process](AlertProcess.md)
- [ForceProcess](ForceProcess.md)
- [ForceFolder](ForceFolder.md)
