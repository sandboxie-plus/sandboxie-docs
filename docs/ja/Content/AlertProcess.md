# Alert Process

`AlertProcess` は、サンドボックスの外で開始されるプログラムのためのグローバルな [Sandboxie Ini](SandboxieIni.md) 設定です。任意のプログラム アクティビティではなく、実行可能ファイル/イメージの識別情報を照合し、宛先サンドボックスを選択しません。

```ini
[GlobalSettings]
AlertProcess=example.exe
```

通常のエントリは実行可能イメージ名を照合します。`*` を含むエントリは、正規化された実行可能パスに対する大文字と小文字を区別しないパターンとして処理されます。他のセレクター構文がこのアラート パスに適用されると想定しないでください。

構成された強制でボックスの選択に失敗した後、Sandboxie は [Alert Folder](AlertFolder.md)、次に `AlertProcess` をチェックします。以前の通常の強制選択が成功している場合は、この分岐を通じて通常のアラート リストの決定を受け取りません。

既定の `StartRunAlertDenied=n` では、一致によって [SBIE1301](SBIE1301.md) が発行されることがありますが、このメカニズム自体が起動を拒否することはありません。グローバルな `StartRunAlertDenied=y` では、通常のアラート リスト一致が起動をブロックします。`AlertStartRunAccessDenied` は既定で `y` であり、拒否された起動が [SBIE1308](SBIE1308.md) を報告するかどうかを制御します。拒否自体を制御するものではありません。

SandMan では、**Global Settings > Program Control > Program Alerts > Add Program** を使用します。**Prevent the listed programs from starting on this system** がブロックを制御します。より広範な強制、アラート、一時停止のアーキテクチャについては、[Program Forcing Controls](ProgramForcingControls.md) を参照してください。

Sandboxie Control Classic については、[Configure Menu > Program Alerts](ConfigureMenu.md#program-alerts) および [Program Settings alert option](ProgramSettings.md#alert) を参照してください。
