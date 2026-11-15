# Use Shell Notify Icon Proxy

_UseShellNotifyIconProxy_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。サポートされている `Shell_NotifyIcon` 操作を Sandboxie の GUI プロキシを通じてルーティングして、通知領域のアイコンを実際のデスクトップ シェルを通じて作成または更新できるようにするかどうかを制御します。

```ini
[DefaultBox]
UseShellNotifyIconProxy=y
```

この設定は無効にするか、1 つのプログラムに限定することもできます:

```ini
UseShellNotifyIconProxy=n
UseShellNotifyIconProxy=program1.exe,y
UseShellNotifyIconProxy=program2.exe,n
```

否定イメージ セレクターを使用して、1 つを除くすべてのプログラムにルールを適用できます:

```ini
UseShellNotifyIconProxy=n
UseShellNotifyIconProxy=!program.exe,y
```

## 既定の動作

既定はサンドボックスのウィンドウ アクセス構成によって異なります:

- [`OpenWinClass=*`](OpenWinClass.md) がアクティブな場合、プロキシは既定で有効です。明示的な `UseShellNotifyIconProxy=n` はそれを無効にします。
- `OpenWinClass=*` がない場合、プロキシは既定で無効です。明示的な `UseShellNotifyIconProxy=y` はそれを有効にします。

プロキシ ルートには、Sandboxie の GUI プロキシ サービスが利用可能であることも必要です。Application Compartment モードおよび `NoSandboxieDesktop=y` はそのサービスを使用しないため、この設定はそれらのモードでプロキシ ルートを強制できません。

## 互換性スコープ

これは通知領域またはトレイ アイコンの互換性設定です。サンドボックス化されたプログラムのトレイ アイコンが表示されない、または直接パスを通じて正しく更新できない場合に役立ちます。

すべての shell API やウィンドウ メッセージをプロキシしたり、ホスト ウィンドウへの一般的なアクセスを付与したり、構成された `OpenWinClass` ルールを変更したりするものではありません。

プロキシ トランスポートを正常に使用できない場合、Sandboxie は直接のネイティブ通知アイコン パスにフォールバックできます。アプリケーションは、すべての失敗ケースに対して特定の Windows エラーに依存すべきではありません。

## 変更の適用

Sandboxie は通知アイコン呼び出しが処理されるときにこの設定をチェックしますが、周囲の GUI モードとプロキシの可用性はプロセスが初期化されるときに確立されます。この設定または関連する GUI 構成を変更した後は、影響を受けるアプリケーションを再起動してください。

この設定には SandMan または Sandboxie Control Classic に専用のコントロールはありません。`Sandboxie.ini` で、または INI エディターを通じて手動で構成してください。

## バージョン履歴

- Sandboxie Plus 1.17.5 / Classic 5.72.5 が `OpenWinClass=*` でのトレイ アイコン互換性のためのプロキシを導入しました。
- Sandboxie Plus 1.18.4 / Classic 5.73.4 が条件付き既定を保持しつつ、`OpenWinClass=*` 外での明示的な有効化を追加しました。

## 関連構成

- [Open Win Class](OpenWinClass.md)
- [Sandboxie Ini](SandboxieIni.md)
