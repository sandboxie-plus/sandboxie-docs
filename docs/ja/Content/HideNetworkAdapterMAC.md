# Hide Network Adapter MAC Address

HideNetworkAdapterMAC は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。

```ini
[DefaultBox]
HideNetworkAdapterMAC=y
```

有効にすると、Sandboxie はインターセプトされた `NsiAllocateAndGetTable` パスを通じて返される一致するエントリの MAC アドレス データを置き換えます。この置換は、元のクエリが成功した後に選択された NSI/NDIS テーブルに適用され、アダプター アドレスを取得するすべての方法に適用されるわけではありません。他のネットワーク API、レジストリ クエリ、および WMI クラスは異なるパスを使用することがあります。

サンドボックス化されたプロセスで最初に検出された各元のアドレスについて、Sandboxie は [Network Adapter MAC](NetworkAdapterMAC.md) の値を使用するか、置換バイトを生成します。その元のアドレスに繰り返し遭遇すると、プロセス ローカルにキャッシュされた値が再利用されます。カスタム値を変更しても、既存のキャッシュ エントリは書き換えられません。

有効な値が構成されていない場合、ランタイム フォールバックは無効です。ブールの照会はプロセス イメージによって修飾でき、該当するテンプレートまたはグローバル構成を含めることができます。有効化の値は、該当する `nsi.dll` 初期化パスが実行されるときに読み取られます。影響を受けるサンドボックス化されたプロセスを再起動するのが、フックの状態とアドレス キャッシュを再構築する確実な方法です。

**Sandbox Options > Advanced Options > Privacy** で、**Hide Network Adapter MAC Address** はボックスの直接の設定を制御します。継承された有効な値はチェックボックスの状態と異なることがあります。
