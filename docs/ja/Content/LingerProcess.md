# Linger Process

_LingerProcess_ は [Sandboxie Ini](SandboxieIni.md) の繰り返し可能なボックスごとの設定です。通常の非 linger プログラムが残っていない後に、Sandboxie がクリーンアップ候補として扱うことができるヘルパーまたはバックグラウンドの実行可能ファイルを識別します。

```ini
[DefaultBox]
LingerProcess=helper.exe
LingerProcess=updater.exe
```

名前は正確かつ大文字と小文字を区別せずに照合されます。現在のコンシューマーはワイルドカード マッチングを実行しません。

一致するプロセスはすぐには終了されません。残っている関連するサンドボックス プロセスがすべて lingerer であり、該当する例外が妨げない場合に自動クリーンアップが検討されます。Sandboxie はまた、自身の一部のサービスまたはヘルパー プロセスを内部的に lingerer として扱います。その実装リストは変更されることがあります。

## Linger の寛容性

`LingerLeniency` は既定で有効です。有効な間、次のことを行います:

1. SandboxieRpcSs が初期化されるときに既にアクティブな一致する構成済み lingerer を保持します。
2. 関連する強制パスまたは `Start.exe` パスを通じて明示的に開始された構成済み lingerer を免除します。
3. 自動クリーンアップの前に、最近開始された残りのプロセスに現在の 5 秒の猶予チェックを適用します。

```ini
[DefaultBox]
LingerLeniency=n
```

`n` に設定すると、これらの動作が無効になります。したがってこの設定はタイムアウト スイッチよりも広範であり、5 秒の間隔はこれを通じて構成できません。サンドボックス内の最初のプロセスが常に免除されるという無条件のルールはサポートしていません。

`LingerLeniency` は Sandboxie Plus 1.0.7 / Classic 5.55.7 で導入されました。Sandboxie Plus 1.13.4 / Classic 5.68.4 では `LingerLeniency=n` が拡張され、5 秒の猶予チェックも無効にするようになりました。

## 可視ウィンドウ

[Linger Exempt Wnds](LingerExemptWnds.md) は、可視のトップレベル ウィンドウが、それ以外の場合は対象となる linger クリーンアップを防ぐかどうかを別個に制御します。これはプロセスを lingerer として分類するものではありません。

linger リストは、SandboxieRpcSs がサンドボックス内で初期化されるときに読み込まれます。リストまたは寛容性ポリシーを変更した後に予測可能な動作を得るには、影響を受けるサンドボックス プロセス ツリーを再起動または再作成してください。

Sandboxie Plus では、**Sandbox Options > Program Control > Stop Behaviour > Lingering Programs** を開きます。`LingerLeniency` と可視ウィンドウの例外は **Stop Options** の下にあります。Sandboxie Control Classic は、従来の [Sandbox Settings > Program Stop > Lingering Programs](ProgramStopSettings.md#lingering-programs) ページを公開していますが、すべての新しい SandMan コントロールを提供すると想定すべきではありません。

ライフサイクルの完全な概要については [Program Stop Settings](ProgramStopSettings.md) を参照してください。
