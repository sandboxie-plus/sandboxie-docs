# Drop Child Process Token

`DropChildProcessToken` は Sandboxie Plus 1.15.6 / Classic 5.70.6 で導入された高度なデバッグ設定です。歴史的に「グリーン ボックス」互換性問題と呼ばれていた問題を含む、子プロセス作成の問題のトラブルシューティングに役立ちます。トークン処理を緩和する一般的な推奨事項ではありません。

この設定が一致する場合、Sandboxie は呼び出し元プロセスが子プロセス作成パスに提供した明示的な `hToken` をクリアします。Sandboxie のトークン パイプライン全体を無効にしたり、既存のトークン オブジェクトを書き換えたりするものではありません。

## 構成と呼び出し元のスコープ

```ini
[DefaultBox]
DropChildProcessToken=parent.exe,y
```

ランタイムの既定は `n` です。これはイメージ対応の設定です。`parent.exe` は、起動する実行可能ファイルではなく、**子プロセス作成呼び出しを行う** サンドボックス化されたプロセスを選択します。このルールは、一致する呼び出し元が子プロセスを作成する方法を変更しますが、`parent.exe` 自体のトークンを変更するものではありません。

Sandboxie は、Acrobat Reader またはプラグイン コンテナとして分類されたイメージに対して、呼び出し元が提供した子トークンも自動的にクリアします。それらのハードコードされたケースには `DropChildProcessToken` ルールは必要ありません。歴史的な Flash 固有のコードはコメント アウトされており、アクティブな自動ケースではありません。

## 子プロセスに何が起こるか

この設定は、この作成要求から呼び出し元が提供した子トークンを削除します (`hToken = NULL`)。子プロセスが最終的にどのトークンで実行されるかは、後のサンドボックス モードとトークン処理パスに依存します:

- **標準サンドボックス:** ドライバーは通常、依然として `Token_ReplacePrimary()` に到達し、Sandboxie の制限されたプライマリ トークンを割り当てます。呼び出し元のトークンをクリアすることと、その後の置き換えを実行することは別個の段階です。
- **[Application Compartment](../PlusContent/compartment-mode.md) または [OriginalToken](OriginalToken.md):** 通常の制限されたプライマリ トークンの置き換えはバイパスされます。したがって、提供されたトークンをクリアすると、子プロセスに選択される Windows トークンに対して異なる、潜在的に大きな影響を与える可能性があります。

この設定は、子プロセスが親の完全なトークンを継承することや、Sandboxie の残りの分離メカニズムが無効になることを保証するものではありません。特定の子プロセス作成の互換性問題を調査するために使用し、構成に残す前にトークンへの影響を確認してください。

## 関連ページ

- [AppContainer Token Compatibility](AppContainerTokens.md)
- [Original Token](OriginalToken.md)
- [Application Compartment](../PlusContent/compartment-mode.md)
- [Sandboxie Ini](SandboxieIni.md)
