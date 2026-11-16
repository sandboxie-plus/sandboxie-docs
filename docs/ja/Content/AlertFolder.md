# Alert Folder

`AlertFolder` は、Sandboxie Plus 0.5.0 / Classic 5.45.0 で導入されたグローバルな [Sandboxie Ini](SandboxieIni.md) 設定です。プログラムがサンドボックスの外で開始されるときに、**実行可能ファイル自身のパス/ディレクトリ**を評価します。一部の [Force Folder](ForceFolder.md) チェックとは異なり、アラートの照合に現在の作業ディレクトリやドキュメント引数を検査しません。任意のファイル アクセスを監視するものでもありません。

```ini
[GlobalSettings]
AlertFolder=C:\Example
```

通常のフォルダー エントリは、そのフォルダー配下の実行可能ファイルを再帰的に照合します。ワイルドカードを含むエントリはパターンとして処理されます。通常の強制でサンドボックスの選択に失敗した後、`AlertFolder` は [Alert Process](AlertProcess.md) より前にチェックされます。以前の強制選択が成功している場合は、この通常のアラート リスト チェックを通りません。アラートは宛先サンドボックスを選択しません。

既定の `StartRunAlertDenied=n` では、一致によって [SBIE1301](SBIE1301.md) が発行されることがありますが、このメカニズム自体が起動をブロックすることはありません。グローバルな `StartRunAlertDenied=y` では、通常のアラート リスト一致は代わりに拒否されます。`AlertStartRunAccessDenied` は既定で `y` であり、その拒否に対する [SBIE1308](SBIE1308.md) 通知を制御します。ブロックの決定を制御するものではありません。

SandMan では、**Global Settings > Program Control > Program Alerts > Add Folder** を使用します。**Prevent the listed programs from starting on this system** コントロールがブロック モードを有効にします。評価順序、一時停止の動作、およびサンドボックスの Start/Run 制限との違いについては、[Program Forcing Controls](ProgramForcingControls.md) を参照してください。
