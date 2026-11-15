# Leader Process

_LeaderProcess_ は [Sandboxie Ini](SandboxieIni.md) の繰り返し可能なボックスごとの設定です。Sandboxie がサンドボックス内の主要プログラムとしてまとめて扱うべき実行可能イメージを識別します。

```ini
[DefaultBox]
LeaderProcess=browser.exe
LeaderProcess=viewer.exe
```

名前は正確かつ大文字と小文字を区別せずに照合されます。現在のコンシューマーはワイルドカード マッチングを実行しません。

構成されたリーダーは、最初に実行中であることが観察されている必要があります。1 つ以上の構成されたリーダーが存在した後、構成されたリーダー イメージがいずれも残っていない場合、Sandboxie は残りのサンドボックス化されたプロセスの終了を要求します。上記の例では、`viewer.exe` がまだ実行されている間は `browser.exe` の終了によってクリーンアップはトリガーされません。

リーダーによってトリガーされるクリーンアップは、linger 固有のウィンドウ例外、寛容性の例外、および最近のプロセスの猶予チェックをバイパスします。一致するプロセスが観察される前にリーダー名が構成されているという理由だけで有効になるわけではありません。

このリストは、SandboxieRpcSs がサンドボックス内で初期化されるときに読み込まれます。予測可能な動作のために、変更後は影響を受けるサンドボックス プロセス ツリーを再起動または再作成してください。

Sandboxie Plus では、**Sandbox Options > Program Control > Stop Behaviour > Leader Programs** を開きます。Sandboxie Control Classic は、従来の [Sandbox Settings > Program Stop > Leader Programs](ProgramStopSettings.md#leader-programs) ページを公開しています。

ライフサイクルの完全な概要については [Program Stop Settings](ProgramStopSettings.md) を参照してください。
