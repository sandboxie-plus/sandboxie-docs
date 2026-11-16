# Restrict Devices

*RestrictDevices* は、サンドボックス化されたプロセスから NT `\Device` 名前空間下の任意のドライバーおよびデバイス エンドポイントへのアクセスを削減します。Sandboxie のファイル/パス フィルター ルールを使用します。広範なデバイス パス制限が、より具体的な組み込みの互換性例外と組み合わされます。万能のハードウェア ブロッカーでもネットワーク ファイアウォールでもありません。

## 構成

この設定は既定では無効です。サンドボックスに対して有効にするには、次を追加します:

```ini
[DefaultBox]
RestrictDevices=y
```

この設定は、該当する構成の継承を含め、サンドボックス全体に対して評価されます。実行可能ファイル修飾形式はありません。変更後は影響を受けるサンドボックス化されたプロセスを再起動してください。

[Security Hardened Mode](../PlusContent/security-mode.md) (`UseSecurityMode=y`) は、`RestrictDevices` が存在しないか明示的に `n` に設定されていても、同じデバイス制限の動作を有効にします。また、他のセキュリティ機能も有効にします。そのモードを選択するために別個の `RestrictDevices=y` エントリは必要ありません。

## デバイス パス ポリシー

現在の組み込みポリシーは、`Templates.ini` の内部 `[TemplateSModPaths]` セクションに保持されており、`ClosedFilePath` で `\Device\*` を広範に閉じ、より具体的な `NormalFilePath` 例外を含めています。これらには `\Device\CNG` や `\Device\NamedPipe\*` などの Windows 互換エンドポイントが含まれます。NT `\Device` 名前空間には、物理ハードウェアではない名前付きパイプなどのオブジェクトも含まれます。出荷される例外リストはリリース間で変更されることがあります。

この制限は Sandboxie のパス ポリシーです。Windows のデバイス ACL を変更したり、デバイスをアンインストールしたり、ホスト ドライバーを無効にしたり、`\Device` 下のすべての操作がブロックされることを保証したりするものではありません。ホスト ドライバーが強力なデバイス制御インターフェイスを提供する場所で、サンドボックス化されたアプリケーションにさらされる攻撃面を削減します。すべての脆弱なドライバーのエクスプロイトを防ぐものではありません。

デバイス制限はまた、`UseRuleSpecificity=n` が構成されていても [Rule Specificity](../PlusContent/RuleSpecificity.md) を有効にします。これにより、十分に具体的な例外が広範なデバイス パスの閉鎖より優先されることがあります。

通常のドライブおよびボリューム パスは別の扱いを受けるため、制限を有効にしても通常のファイルシステム アクセスが単に使用不能になるわけではありません。Privacy Mode 以外では、組み込みのドライブ パターンは通常パスの扱いを受けます。[Privacy Mode](../PlusContent/privacy-mode.md) では、デバイス制限はアクティブなままですが、それらのドライブ パターンは代わりに Privacy Mode の `WriteFilePath` の扱いを受けます。これは無制限の生ディスク アクセスの許可ではありません。

## 特定のエンドポイントを許可する

アプリケーションが広範なルールで閉じられるデバイス エンドポイントを必要とする場合、実際の NT パスを特定した後で、最も狭い適切な [Normal File Path](NormalFilePath.md) 例外を使用します。たとえば、下の `VendorDevice` は単なるプレースホルダーです:

```ini
[DefaultBox]
RestrictDevices=y
NormalFilePath=\Device\VendorDevice*
```

一致するエンドポイントに対して、`NormalFilePath` は Sandboxie の通常のパス処理を復元します。読み取りは実際のパスを使用でき、書き込みは該当する場合に通常のサンドボックス コピー/仮想化の動作の対象のままです。非ファイルシステムのドライバー エンドポイントは通常のファイルのように動作しないことがあります。対照的に、[Open File Path](OpenFilePath.md) は実際のホスト パスへの直接アクセスを要求します。これはこの設定の標準的な互換性例外ではありません。Windows のアクセス許可と他の Sandboxie コントロールは依然として適用されます。

> [!WARNING]
> 互換性に必要な例外のみを追加してください。`\Device` 名前空間の大部分をカバーする広範な `NormalFilePath` ルールは、組み込みのデバイス閉鎖よりも具体的な場合、保護を大幅に弱める可能性があります。互換性の問題を解決する最も狭いエンドポイント固有のルールを優先してください。

トラブルシューティング時は `RestrictDevices=y` を維持し、利用可能な場合は Sandboxie の Trace Log または Resource Access Monitor を使用して拒否された `\Device\...` パスを特定し、狭い `NormalFilePath` ルールを追加して再度テストします。すべての拒否に専用の SBIE メッセージがあるわけではありません。特定の周辺機器の結果は、その NT エンドポイント、Windows のアクセス許可、デバイス制御操作、および他の Sandboxie ルールにも依存します。

## 他の設定との相互作用

- [Block Network Files](BlockNetworkFiles.md): これが無効な場合、Sandboxie はそのネットワーク リダイレクターおよび MUP パスに対して通常パスの例外を追加します。有効な場合、それらの特定の例外は追加されません。`RestrictDevices` はネットワーク アクセス ルールや Windows Filtering Platform 強制を置き換えません。
- [Disable File Filter](DisableFileFilter.md): デバイス制限は Sandboxie のファイル/パス フィルター レイヤーに依存します。プロセスに対してそのレイヤーを無効にすると、このデバイス パス ポリシーの強制が損なわれます。
- [Application Compartment](NoSecurityIsolation.md): `NoSecurityIsolation=y` だけではデバイス制限はオフになりません。ただし、Application Compartment では、[No Security Filtering](NoSecurityFiltering.md) がそれを強制するために使用されるファイル フィルター レイヤーを無効にします。
- [Open Dev CM API](OpenDevCMApi.md): 組み込みのデバイス ポリシーには `\Device\DeviceApi*` ファミリに対する通常パスの例外があります。`OpenDevCMApi` は CMApi エンドポイントを通じて選択された Configuration Manager 操作を別途制御します。同じ制限ではありません。
- [Block Register Device Notification](BlockRegisterDeviceNotification.md) および [USB Sandboxing](../PlusContent/USBSandboxing.md) は、別個の通知および USB 強制実行の動作に対処します。`RestrictDevices` はどちらも有効にしません。

既存のデバイス ハンドルは、このパス ポリシーによって遡って権限を剥奪されることはありません。この設定は関連する以降のパス/オープン評価に影響します。パス ルール リストは実行中のプロセスに対して更新できますが、更新はそのプロセスの保存された `RestrictDevices` 状態を再計算しません。設定自体を変更した後の一貫したテストのために、影響を受けるプロセス ツリーを再起動してください。新しく開始されたプロセスには Windows の再起動や通常のドライバー/サービスの再起動は必要ありません。

## SandMan インターフェイスと証明書

SandMan で **Sandbox Options > Security Options > Security Hardening** を開き、**Restrict driver/device access to only approved ones** を選択します。通常のサンドボックスでは既定でチェックされていません。**Enable all security enhancements (make security hardened box)** コントロールは、それをチェック済みとして表示し、`UseSecurityMode=y` が既にその動作を有効にしているため、個々のチェックボックスを無効にします。Rule Specificity のチェックボックスも同様に、デバイス制限が選択されている間はチェック済みかつ無効として表示されます。その表示は別個の `UseRuleSpecificity=y` エントリが保存されることを意味しません。

*RestrictDevices* は、Sandboxie のセキュリティ強化機能を持つ適格なサポーター証明書を必要とします。これがない場合、現在のランタイムは機能の可用性メッセージをログに記録し、約 5 分の評価期間後に通常の影響を受けるプロセスの終了をスケジュールします。起動を即座に普遍的に拒否するものではありません。

## バージョン履歴

- Sandboxie Plus 1.0.7 / Classic 5.55.7 が古い `DeviceSecurity` テンプレートを導入しました。
- Sandboxie Plus 1.3.0 / Classic 5.58.0 がそれを `RestrictDevices=y` 設定に置き換え、現在の Security Hardened モードの関係を導入しました。
- Sandboxie Plus 1.7.1 / Classic 5.62.1 が `BlockNetworkFiles=y` との相互作用を修正しました。
- Sandboxie Plus 1.8.0 / Classic 5.63.0 が組み込みのアクセス ルールをテンプレート セクションに移動しました。現在のデバイス ルールは、非推奨の `Template_DeviceSecurity` テンプレートではなく、内部 `[TemplateSModPaths]` セクションにあります。

## 関連ページ

- [Sandboxie Ini](SandboxieIni.md)
- [Security Hardened Mode](../PlusContent/security-mode.md)
- [Rule Specificity](../PlusContent/RuleSpecificity.md)
- [Normal File Path](NormalFilePath.md)
- [Block Network Files](BlockNetworkFiles.md)
