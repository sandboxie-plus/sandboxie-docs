# Protect Host Images

_ProtectHostImages_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。メイン実行可能イメージがホストから来ている特定のサンドボックス化されたプロセスを、サンドボックス内から発信される実行可能コンテンツから保護します。

```ini
[DefaultBox]
ProtectHostImages=y
```

この設定は既定では無効で、現在適用可能な Support Certificate が必要です。

## 動作

この設定が有効な場合、ドライバーは実行可能ファイルがサンドボックスからではなくホストから読み込まれたサンドボックス化されたプロセスを識別します。それらのプロセスについて、通常のイメージ読み込み中にボックス化されたパスからの実行可能イメージ マッピングをブロックします。これは、サンドボックス内に配置された DLL または他の実行可能イメージが、サンドボックス化されて実行されているホストにインストールされたプログラムに読み込まれるのを防ぐことを目的としています。

現在のドライバーはまた、自身の実行可能ファイルがサンドボックスから来ているプロセスが、同じボックス内であっても保護されたホスト イメージ プロセスへの書き込みアクセスを取得することを防ぎ、そのボックス化されたイメージのプロセスが保護されたパスを通じてホスト イメージの子を開始することを防ぎます。

この設定は、すべての DLL またはイメージの読み込み、あらゆる形式のコード インジェクション、またはホスト プロセスとのあらゆる対話を防ぐものではありません。実行可能イメージ マッピングのチェックには、プロセス作成中に必要なマッピングに対する限定的な例外があります。別個の `ProtectHostImages` プロセス作成チェックは依然として適用されます。アプリケーションの互換性のためにファイル移行の例外が必要になることもあります。

`ProtectHostImages` は [Application Compartment](../PlusContent/compartment-mode.md) ボックス (`NoSecurityIsolation=y`) では無効になります。これは [ConfidentialBox](ConfidentialBox.md) とは独立しています。一方はサンドボックス内のイメージおよび関連するプロセス操作を制限し、他方はホストから開かれるプロセス/スレッド ハンドルを制限します。

## 互換性

ボックス化された実行可能イメージをブロックすると、インストールされたモジュールがサンドボックスにコピーされて読み込まれることを期待するアプリケーションが影響を受ける可能性があります。現在の既定のテンプレートには、Firefox ファミリ ブラウザーの一般的なインストール場所に対する移行例外が含まれています。カスタム インストール パスは、影響を受ける場合、同等の `DontCopy` ルールを必要とすることがあります。

通知が有効な場合、Sandboxie はブロックされた実行可能イメージ読み込みに対してメッセージ 1305 を発行します。関連する `NotifyImageLoadDenied` 設定は、その SandMan コントロールが利用可能な間、既定で有効です。

## SandMan 構成

コントロールは次にあります:

**Sandbox Options > Advanced Options > Dlls & Extensions > Image Protection**

その現在のラベルは次のとおりです:

**Prevent sandboxed programs installed on the host from loading DLLs from the sandbox**

隣接する **Issue message 1305 when a program tries to load a sandboxed dll** チェックボックスは `NotifyImageLoadDenied` を制御します。SandMan はグローバルな `ProtectHostImages` の既定とボックスごとの上書きをサポートします。

ドライバーはサンドボックス化されたプロセスが初期化されるときに `ProtectHostImages` を記録します。変更した後は影響を受けるサンドボックス化されたプロセス ツリーを再起動してください。

## バージョン履歴

`ProtectHostImages` と `NotifyImageLoadDenied` は Sandboxie Plus 1.9.0 / Classic 5.64.0 で導入されました。Firefox ファミリ ブラウザーの互換性修正は Sandboxie Plus 1.15.4 / Classic 5.70.4 で続きました。

## 関連ページ

- [Confidential Box](ConfidentialBox.md)
- [Box Encryption](../PlusContent/BoxEncryption.md)
