# Use Rule Specificity

_UseRuleSpecificity_ は [Sandboxie Ini](SandboxieIni.md) のブール サンドボックス設定です。複数のファイル、レジストリ、または IPC リソース ルールが一致する場合に、具体性ベースの比較を有効にします。標準のサンドボックス既定では無効です。

```ini
[DefaultBox]
UseRuleSpecificity=y
```

プロセス セレクター、リソース パターン、アクセス リスト、および古典的優先度のルールについては [Rule Specificity](../PlusContent/RuleSpecificity.md) を参照してください。

## 有効な状態

ランタイムは、次の条件のいずれかが真の場合に Rule Specificity を有効にします:

```text
RestrictDevices OR UsePrivacyMode OR UseRuleSpecificity
```

`UseSecurityMode=y` は Restrict Devices 動作を有効にするため、間接的に Rule Specificity を強制します。その結果、Privacy Mode または Restrict Devices がアクティブな間は、`UseRuleSpecificity=n` でその動作をオフにすることはできません。

## SandMan インターフェイス

コントロールは次にあります:

**Sandbox Options > Resource Access > Access Policies**

そのラベルは次のとおりです:

> **Prioritize rules based on their Specificity and Process Match Level**

Privacy Mode または Restrict Devices がアクティブな場合、SandMan はオプションをアクティブとして表示し、個々のチェックボックスを無効にします。これは有効な動作を反映しています。SandMan が別個の `UseRuleSpecificity=y` エントリを書き込むことを必ずしも意味するわけではありません。

## 可用性

Rule Specificity の直接使用は、Sandboxie のサポーター証明書セキュリティ機能の可用性の対象です。その可用性がない場合、ランタイムは利用できない機能をログに記録し、すべてのプロセスを直ちに拒否するのではなく、評価期間後に影響を受ける通常のプロセスの終了をスケジュールすることがあります。別のセキュリティ機能が具体性を強制する場合、代わりにその強制機能が識別されることがあります。

## 変更の適用

有効な値はサンドボックス化されたプロセスが初期化されるときに保存されます。設定を変更した後は、影響を受けるサンドボックス化されたプロセス、できれば完全なサンドボックス プロセス ツリーを再起動してください。Windows の再起動は通常必要ありません。

## バージョン履歴

Rule Specificity および Normal リソース ルールは、Sandboxie Plus 1.0.0 / Classic 5.55.0 でオプションの動作として導入されました。以降のリリースではワイルドカード、タイ、およびプライマリ一致の処理が改善されました。現在のアルゴリズムは [Rule Specificity](../PlusContent/RuleSpecificity.md) ページで説明されています。
