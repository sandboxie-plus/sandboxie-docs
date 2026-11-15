# 技術的側面

Sandboxie はオープンソースになったため、もはや秘密はありません。興味のある開発者が Sandboxie の内部動作を理解できるように、このページでは採用されているメカニズムとセキュリティ保証についてのさまざまな詳細な解説を提供します。

### トピック

* [分離メカニズム](IsolationMechanism.md)
* [コード インジェクション](CodeInjection.md)
* [Sandboxie DLL API](SBIEDLLAPI.md)

### トークンの互換性

* [高度なトークン設定](AdvancedTokenSettings.md)
* [AppContainer トークンの互換性](AppContainerTokens.md)

### システム コールとフック

* [システム コール設定](SyscallSettings.md)
* [Win32k フック](Win32kHooks.md)

### ローダーとアーキテクチャの互換性

* [フックとローダーの互換性](HookAndLoaderCompatibility.md)
* [高度なローダーと SxS の互換性](AdvancedLoaderCompatibility.md)
* [ARM64 と CHPE の互換性](Arm64ChpeCompatibility.md)
* [ホスト インジェクション](HostInjection.md)

### 実行時オブジェクトとプロセス

* [オブジェクト参照の互換性](ObjectLookupCompatibility.md)
* [サンドボックス デスクトップとウィンドウ ステーション](SandboxDesktop.md)
* [ジョブ オブジェクト](JobObjects.md)
* [プロセス速度設定](ProcessSpeedSettings.md)
