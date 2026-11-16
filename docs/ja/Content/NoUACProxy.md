# No UAC Proxy

## 概要

**NoUACProxy** は、Sandboxie が Windows Application Information (AppInfo) サービスへのサポート対象の非同期 RPC 要求をインターセプトし、認識された昇格要求を自身の UAC プロキシを通じてルーティングするかどうかを制御します。既定では無効であるため、Sandboxie のプロキシ処理は通常アクティブです。

```ini
[DefaultBox]
NoUACProxy=y
```

`NoUACProxy=y` の場合、Sandboxie の RPC ラッパーはこれらの呼び出しに対する昇格の認識とプロキシ ロジックをスキップします。その後、元のネイティブ RPC 呼び出しが続行を許可されます。

## 何を意味しないか

この設定は Windows ユーザー アカウント制御を無効にせず、それ自体で昇格要求をブロックしません。ネイティブ UAC パスが成功するかどうかは、Windows とサンドボックスの RPC およびリソース アクセス構成に依存します。

逆に、`NoUACProxy=n` は、Sandboxie が可能なすべての昇格メカニズムをインターセプトすることを意味しません。現在のプロキシは、プロセスの昇格および管理者トークン要求に対するサポート対象の非同期 AppInfo/UAC RPC 要求を認識します。

## ブール設定と互換性テンプレート

ブールと組み込みテンプレートは異なるスコープを持ちます:

```ini
NoUACProxy=y
```

は Sandboxie の昇格 RPC インターセプトを無効にします。RPC アクセス ルールを追加しません。

```ini
Template=NoUACProxy
```

はブールを有効にし、さらにテンプレートの互換性シナリオでネイティブ ルートが機能することを意図した UAC 関連の RPC ポート バインドを提供します。これらの追加のバインドはブール自体からではなく `Template_NoUACProxy` から取得されます。

SandMan には専用の **NoUACProxy** チェックボックスはありません。組み込みテンプレートは **Sandbox Options > App Templates > Templates** の下で **Open RPC Port Bindings for UAC** として、**Miscellaneous** カテゴリにあります。`Template=NoUACProxy` で手動で選択することもできます。

## Application Compartment の履歴

Sandboxie Plus 1.0.4 / Classic 5.55.4 の変更履歴は、Application Compartment ボックスが既定でテンプレートを有効にすることを記していました。現在の SandMan コードは、Application Compartment プリセットを作成または選択するときにそれを自動有効にしなくなりました。以前の呼び出しはコメントアウトされています。そのボックスの種類を選択すると現在 **NoUACProxy** またはそのテンプレートが有効になると想定しないでください。

## 他の昇格設定との関係

* [Use Sandboxie UAC](UseSandboxieUAC.md) は Sandboxie のプロキシ内の強化されたプロンプトを制御します。`NoUACProxy=y` がプロキシ インターセプトをスキップする場合、そのプロンプトにはスキップされたパスを通じて到達しません。
* [Apply ElevateCreateProcess Fix](ApplyElevateCreateProcessFix.md) は、`CreateProcess` が昇格が必要であると報告した後で Windows の `runas` 要求を開始できます。**NoUACProxy** は、Sandboxie のサポート対象の RPC インターセプトが結果の昇格パスに関与するかどうかを決定します。

`UseSandboxieUAC=n` は `NoUACProxy=y` の代替ではありません。前者は強化されたプロンプトのみをスキップし、後者は Sandboxie のサポート対象の RPC 昇格インターセプトをスキップします。

## 変更の適用

RPC フックは関連する要求ごとに **NoUACProxy** を読み取ります。構成が保存および再読み込みされた後、既に実行中のプロセスにおける後続の要求は新しい有効な値を使用します。通常、プロセス、SandMan、SbieSvc、またはドライバーを再起動する必要はありません。進行中の要求は遡って変更されません。

## バージョン履歴

`NoUACProxy` とそれに付随するテンプレートは Sandboxie Plus 1.0.4 / Classic 5.55.4 で導入されました。

## 関連ページ

* [Apply ElevateCreateProcess Fix](ApplyElevateCreateProcessFix.md)
* [No Security Isolation](NoSecurityIsolation.md)
* [Sandboxie Ini](SandboxieIni.md)
* [Use Sandboxie UAC](UseSandboxieUAC.md)
