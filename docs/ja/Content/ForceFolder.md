# Force Folder

_ForceFolder_ は [Sandboxie.ini](SandboxieIni.md) のサンドボックス設定で、一致するプログラムを特定のサンドボックスで自動的に開始します。通常のフォルダー エントリはそのフォルダーおよびそのサブフォルダー内のプログラムに適用されます。例:

```ini
[DefaultBox]
ForceFolder=C:\Download
ForceFolder=E:\
```

最初のエントリは `C:\Download` またはそのサブフォルダーの 1 つから開始されたプログラムを `DefaultBox` に強制します。2 番目はドライブ `E:` から開始されたプログラムに適用されます。フォルダーの照合は大文字と小文字を区別しません。

## 何が照合されるか

通常の強制ルール評価中、Sandboxie は最初に実行可能ファイルのディレクトリを _ForceFolder_ に対してチェックします。それでサンドボックスが選択されない場合、[ForceProcess](ForceProcess.md) をチェックします。どちらのチェックでもサンドボックスが選択されない場合、有効な作業ディレクトリとドキュメント引数も _ForceFolder_ に対してチェックされます。後者のチェックは、評価されるプロセスが Sandboxie 自身の `Start.exe` である場合にスキップされます。

通常のフォルダー エントリは再帰的なパス プレフィックスとして照合されます。`*` を含むエントリは代わりに、正規化されたディレクトリ パスに対するワイルドカード パターンとして扱われます。`?` 文字だけでは _ForceFolder_ エントリをワイルドカード マッチングに切り替えません。同じエントリに `*` も含まれている場合にのみワイルドカードとして機能します。実行可能ファイル名による選択が必要な場合は [ForceProcess](ForceProcess.md) を使用してください。

## ショートカット

強制フォルダーにショートカットを保存するだけでは、そのフォルダーの外にあるターゲット プログラムは強制されません。ターゲットは、その実行可能ファイル ディレクトリ、有効な作業ディレクトリ、またはドキュメント引数が _ForceFolder_ ルールに一致する場合に依然として強制されることがあります。

## イマーシブ アプリケーション {#immersive-applications}

既定では、通常の _ForceFolder_ または _ForceProcess_ ルールがサンドボックスを選択した後、Sandboxie は結果のプロセスをイマーシブ/AppContainer アプリケーションとして識別すると、その選択を破棄します。通常のサンドボックス化されていない親の場合、このチェックはプロセスを終了させません。プロセスはこのパスによって選択されたサンドボックスに強制されることなく続行されます。他の独立した起動ポリシーが結果に影響を与えることは依然としてあります。

高度なグローバル設定 `AllowForceImmersive` は、そのようなプロセスに対してこれらの強制ルールを有効にします:

```ini
[GlobalSettings]
AllowForceImmersive=y
```

既定は `n` です。この設定はサンドボックスごとではなくグローバルであり、SandMan は現在のところ専用のコントロールを提供していません。この設定を有効にしても、すべての AppContainer、UWP、またはその他のイマーシブ アプリケーションとの互換性が保証されるわけではありません。

## ルールの順序

実行可能ファイル パスについて、一致する _ForceFolder_ ルールは _ForceProcess_ より前にチェックされます。作業ディレクトリおよびドキュメント引数の _ForceFolder_ チェックは、_ForceProcess_ の後に実行されるため、_ForceFolder_ がすべてのケースで無条件に優先されるわけではありません。

## ユーザー インターフェイス

SandMan で **Sandbox Options > Program Control > Force Programs** を開き、**Force Folder** を使用してリストを維持します。同じページには **Force Program**、**Force Children**、**Remove**、**Show Templates** コントロールもあります。

Sandboxie Control Classic は、関連する [Sandbox Settings > Program Start > Forced Folders](ProgramStartSettings.md#forced-folders) ページを提供します。

## バージョン履歴

`AllowForceImmersive` は Sandboxie Plus 1.16.0 / Classic 5.71.0 で追加されました。_ForceFolder_ は現在のバージョン メタデータより前から存在し、そこに導入バージョンは記録されていません。

## 関連ページ

- [Force Process](ForceProcess.md)
- [Sandboxie Ini](SandboxieIni.md)
