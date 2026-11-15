# Apply ElevateCreateProcess Fix

## 概要

**ApplyElevateCreateProcessFix** は、昇格が必要なために `CreateProcess` によるプロセス起動が失敗したときに、Sandboxie の従来の ElevateCreateProcess 互換フォールバックを有効にします。既定では無効で、サンドボックス全体に対して、または `CreateProcess` 呼び出しを行うサンドボックス化された実行可能ファイルに対して構成できます。

```ini
[DefaultBox]
ApplyElevateCreateProcessFix=y
```

プロセス固有のルールの場合:

```ini
[DefaultBox]
ApplyElevateCreateProcessFix=legacy-installer.exe,y
```

省略可能な実行可能ファイル セレクターは、要求された子実行可能ファイルではなく、起動を試みたサンドボックス化されたプロセスと照合されます。

## 適用される場合

この設定は、すべてのプロセス起動を強制的に昇格させるものではありません。Sandboxie はまず通常の `CreateProcess` パスを使用します。フォールバックは、その試行が `ERROR_ELEVATION_REQUIRED` で失敗し、呼び出し元プロセスに対して有効な **ApplyElevateCreateProcessFix** ルールが有効な場合にのみ検討されます。

Sandboxie は `runas` 動詞を使用して `ShellExecuteExW` で起動を再試行します。成功した場合、Sandboxie は元のプロセス情報構造を通じて新しいプロセス ハンドルを返します。昇格プロンプトをキャンセルすると起動がキャンセルされます。Sandboxie はまた、起動がすでに `ShellExecute` を通じて処理されている場合はこのフォールバックをスキップし、再帰的な昇格の試行を防ぎます。

結果として生じる `runas` 要求は、その後 Sandboxie の UAC プロキシに入ることがあります。[No UAC Proxy](NoUACProxy.md) は、サポートされている昇格 RPC を傍受するかどうかを制御し、[Use Sandboxie UAC](UseSandboxieUAC.md) はプロキシがアクティブな場合の拡張プロンプトを制御します。

## 従来の動作である理由

古い Sandboxie バージョンは、Windows Program Compatibility Assistant によって時々適用される ElevateCreateProcess 互換 shim を自動的にエミュレートしていました。自動エミュレーションは、アプリケーションが呼び出しの失敗を期待していた場合でも、通常の `ERROR_ELEVATION_REQUIRED` の結果を昇格プロンプトに変えることがありました。そのため、Sandboxie Plus 0.8.0 / Classic 5.50.0 では、この動作をオプトインにしました。

この回避策は、従来の動作を必要とするアプリケーションにのみ使用してください。Windows が昇格を承認すること、またはターゲット アプリケーションが正常に起動することを保証するものではありません。

## SandMan の構成

ボックス全体のチェックボックスは **Sandbox Options > Various Options > Compatibility** にあります:

> Apply ElevateCreateProcess Workaround (legacy behaviour)

専用のチェックボックスはボックス全体の値を書き込みます。SandMan の詳細オプション エディターにも、プロセス固有の構成のために **ApplyElevateCreateProcessFix** がリストされます。

## 変更の適用

Sandboxie は、該当する `CreateProcess` の失敗が発生したときに有効なルールを評価します。構成が保存および再読み込みされた後、すでに実行中のサンドボックス化されたプロセスからの後続の起動試行は新しい値を使用できます。通常、SandMan、SbieSvc、またはドライバーを再起動する必要はありません。

## バージョン履歴

この設定は、以前は自動だった互換動作がオプトインになったときに、Sandboxie Plus 0.8.0 / Classic 5.50.0 で導入されました。専用の SandMan チェックボックスは Sandboxie Plus 1.4.2 / Classic 5.59.2 で追加されました。

1.4.2 / 5.59.2 の変更履歴では、この設定を必要とするプロセスに対してメッセージ `SBIE2226` も発表されました。現在の実装はメッセージ テキストを保持していますが、積極的に発行しないため、ユーザーはその通知を受け取ることに依存しないでください。

## 関連ページ

* [No UAC Proxy](NoUACProxy.md)
* [Sandboxie Ini](SandboxieIni.md)
* [Use Sandboxie UAC](UseSandboxieUAC.md)
