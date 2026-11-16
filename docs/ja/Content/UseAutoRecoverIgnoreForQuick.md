# Use Auto Recover Ignore For Quick

_UseAutoRecoverIgnoreForQuick_ は Sandboxie Plus 1.18.0 以降で使用可能な [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。[AutoRecoverIgnore](AutoRecoverIgnore.md) 除外リストを [Quick Recovery](QuickRecovery.md) ウィンドウにも適用し、一致するファイルを復元可能なファイルのリストから非表示にするかどうかを指定します。

使用方法:

```
   .
   .
   .
   [DefaultBox]
   UseAutoRecoverIgnoreForQuick=n
```

設定メタデータは _n_ の既定を記述していますが、現在の SandMan は存在しない値を有効として読み取ります。したがって、通常の Quick Recovery リストは、オプションが明示的に _n_ に設定されているか、ウィンドウの表示コントロールがフィルター処理を上書きしない限り、一致するファイルを非表示にします。これは SandMan コンシューマーの既定であり、プロセス側の検出器の既定ではありません。_n_ を設定しても、自動復元が [AutoRecoverIgnore](AutoRecoverIgnore.md) をどのように適用するかは変わりません。

Quick Recovery の **Show All Files** または **Show Ignored** ビューは、このオプションによって通常非表示になるエントリを表示できます。SandMan はまた、報告された候補に対して初期の Immediate Recovery ダイアログを開くかどうかを決定するときにこの設定を参照します。SbieDll 検出器の無視の決定を変更するものではありません。

SandMan では、これは Sandbox Options > File Recovery > Immediate Recovery の下の「Use the above exclusion list to hide matching files from the Quick Recovery window」チェックボックスに対応します。

関連する [Sandboxie Ini](SandboxieIni.md) 設定: [AutoRecoverIgnore](AutoRecoverIgnore.md)、[RecoverFolder](RecoverFolder.md)。[Quick Recovery](QuickRecovery.md) も参照してください。

別個の復元ワークフローについては [File Recovery Architecture](RecoveryArchitecture.md) を参照してください。
