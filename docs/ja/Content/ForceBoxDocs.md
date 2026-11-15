# Force Box Docs

_ForceBoxDocs_ は [Sandboxie Ini](SandboxieIni.md) のグローバル設定です (v1.17.0 / 5.72.0 で導入)。有効な場合、ファイル パス引数を伴って Sandboxie の外でプログラムが起動され、そのファイルがサンドボックス内にあるとき、Sandboxie はその同じサンドボックスでプログラムを自動的に開始します。

使用法:

```ini
   [GlobalSettings]
   ForceBoxDocs=y
```

この設定がどのように評価されるか:

- プロセスがサンドボックス化されずに開始された場合にのみ適用されます。プロセスが既にサンドボックス化されて開始されている場合、この設定は使用されません。
- コマンド ラインから解析されたファイル パス/ドキュメント引数をチェックします。
- Sandboxie は、ターゲット ファイル パスを正しく識別するために、先頭のコマンド ライン スイッチ (`-` または `/` で始まるオプション、たとえば `/n` や `-Embedding`) を無視します。
- 評価されるプロセスが Sandboxie 自身の `Start.exe` である場合、ファイル パス/ドキュメント引数のチェックはスキップされます。
- 現在のユーザー/セッションに対して有効なボックスのみが考慮されます。
- [DisableForceRules](DisableForceRules.md) を持つボックスはスキップされます。

この設定は、ユーザーがボックス化されたパスから直接ドキュメントを開き、関連付けられたアプリケーションを正しいサンドボックスで自動的に開始したい場合に便利です。

コマンド ラインの例:

```text
"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE" /n /dde "C:\Sandbox\Alice\DefaultBox\drive\C\Docs\Report.docx"
```

結果: ファイル パスが `DefaultBox` を指しているため、プロセスは `DefaultBox` に強制されます。

```text
"C:\Windows\System32\notepad.exe" "C:\Users\Alice\Desktop\Notes.txt"
```

結果: ファイル パスがサンドボックス パス内にないため、`ForceBoxDocs` はプロセスを強制しません。

参照:

- [ForceFolder](ForceFolder.md)
- [ForceProcess](ForceProcess.md)
