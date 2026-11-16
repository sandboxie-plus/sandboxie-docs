# Random Registry UID

RandomRegUID は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。

```ini
[DefaultBox]
RandomRegUID=y
```

初期のサンドボックス カスタマイズ中に、この設定はボックス化されたレジストリ ビュー内の 3 つの値の置き換えを書き込もうとします:

- `HKLM\Software\Microsoft\Windows NT\CurrentVersion\ProductId`
- `HKLM\Software\Microsoft\Cryptography\MachineGuid`
- `HKLM\Software\Microsoft\SQMClient\MachineId`

これはレジストリ読み取りフックではなく、読み取りのたびに新しい値を生成しません。他のレジストリ識別子はこの設定の対象ではありません。3 つの書き込みは個別に試行されるため、失敗すると一部の置き換えのみが残ることがあります。

有効な値が構成されていない場合、ランタイムのフォールバックは無効です。決定はイメージ修飾、テンプレート、またはグローバル構成を使用できますが、サンドボックス カスタマイズが実行されるときに発生します。各プロセス イメージに別個の永続的な ID を作成するものではありません。現在のプロセス初期化は、開始プロセスが Sandboxie の制限付きトークン状態も AppContainer トークン状態も使用していない場合にのみカスタマイズを呼び出します。これは Application Compartment に関する無条件のルールではありません。

正常に書き込まれた置き換えは、サンドボックス化されたレジストリ コンテンツとともに保持されます。ボックスがカスタマイズ済みとしてマークされると、`RandomRegUID` を変更したり、アプリケーションを再起動したりしても、それ自体では書き込みが繰り返されません。関連するサンドボックス コンテンツが削除され、その後再作成された場合、カスタマイズは通常の初期化条件の下で再び実行されることがあります。

**Sandbox Options > Advanced Options > Privacy** では、**Obfuscate known unique identifiers in the registry** が直接のボックス設定を制御します。直接の値が構成されていない場合、チェックボックスはチェックされていません。有効な値は、適用可能なテンプレートまたはグローバル構成から取得することもできます。
