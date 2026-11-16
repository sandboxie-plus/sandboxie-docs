# Open Clipboard

_OpenClipboard_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、v0.7.5 / 5.49.8 以降で使用できます。Sandboxie の標準のクリップボード データ操作フックを制御します。コンシューマー フォールバックは `y` です。有効な値が構成されていない場合、または有効な値が `y` の場合、この設定はクリップボード データ操作を拒否しません。`OpenClipboard=n` はフックされたクリップボードの読み取り、書き込み、およびクリアを拒否します。他の Windows または Sandboxie の制限が依然としてクリップボード アクセスに影響を与えることがあります。

## 構文

```ini
[DefaultBox]
OpenClipboard=n
```

これはボックス全体のブール設定です。その有効な値は、通常の構成ルックアップを通じて有効なテンプレートまたは `GlobalSettings` から取得することもできます。プログラムごとのセレクターはサポートしません。

## 動作

標準のフックされたパスでは、`OpenClipboard=n` は `GetClipboardData`、`SetClipboardData`、および `EmptyClipboard` を拒否します。フックされた `OpenClipboard` および `CloseClipboard` 呼び出し自体は、この設定によって拒否されません。アプリケーションは、拒否されたデータ操作に対して特定の Windows エラー コードに依存すべきではありません。

Sandboxie の通常の [Job Object](JobObjects.md) はクリップボードの読み取りを独立して制限します。対応する Job オブジェクトの書き込み制限は適用しません。この設定によってクリップボード アクセスが許可されている場合、Sandboxie の GUI サービスは、直接の Windows パスを通じて失敗するフックされたクリップボード読み取りを支援できます。標準のデータ読み取りでは、サービスはデータを返す前に有効な `OpenClipboard` 値を再チェックします。別個のメタファイル ルートはクリップボード フックのチェックに依存します。これらのレイヤーを互いに混同すべきではありません。

データ操作フックは、各操作が発生するときに設定を参照します。構成の再読み込み後、変更された値は、それらのフックがインストールされている既に実行中のプロセスにおける後続の操作に影響を与えることがあります。フックのインストールと Job オブジェクトの参加はプロセスの開始時に決定されます。関連する設定を変更しても、遡ってフックがインストールされたり、既存のプロセスが再割り当てされたりすることはありません。

## 互換性と制限

通常の [Application Compartment](NoSecurityIsolation.md) では、標準の `OpenClipboard` フック強制はアクティブではなく、プロセスは Sandboxie の通常のルート Job オブジェクトに割り当てられません。クリップボード アクセスは、Windows および他の該当する制限の対象のままです。

[`NoSandboxieDesktop=y`](NoSandboxieDesktop.md) の場合、標準のクリップボード フックと GUI プロキシはこのパスを通じてインストールされないため、`OpenClipboard=n` はそれらのフックによって強制されません。新しく開始された NoSandboxieDesktop プロセスは、Sandboxie の通常のルート Job オブジェクト割り当てパスとそのクリップボード読み取り制限もスキップします。既存または継承されたジョブ制限は依然として適用されることがあります。フックがないことは `OpenClipboard=n` による書き込みまたはクリアをブロックしませんが、他の制限が依然として適用されることがあります。

この設定は Sandboxie の標準のクリップボード処理パスを記述するものであり、すべての Windows データ転送 API をカバーする保証ではありません。

## SandMan インターフェイス

Sandboxie Plus では、コントロールは **Sandbox Options > General Options > Restrictions** の下にあり、**Block read access to the clipboard** とラベル付けされています。チェックすると `OpenClipboard=n` が書き込まれ、チェックを外すとボックスの直接の値が削除されます。読み取りに焦点を当てたラベルにもかかわらず、有効な設定が `n` の場合、標準のフックはクリップボードの書き込みとクリアも拒否します。

SandMan は Application Compartment に対してこのチェックボックスを無効にします。チェックボックスはボックスの直接の値を管理し、テンプレートまたは `GlobalSettings` から継承された有効な値を表示しないことがあります。

## Sandboxie Control Classic

この設定は、標準パスで共有される Sandboxie コンポーネントによって処理されます。Sandboxie Control Classic のユーザーは [Sandboxie Ini](SandboxieIni.md) を通じて構成できます。
