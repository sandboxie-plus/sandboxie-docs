# Hide Host Process

_HideHostProcess_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、v0.3 / 5.42 以降で使用できます。Sandboxie のフィルター処理されたネイティブ列挙パスを通じてサンドボックス化されたアプリケーションに返されるプロセス リストから、一致するエントリを削除します。複数のプロセス名に対してこの設定を繰り返すことができます。

```
   .
   .
   .
   [DefaultBox]
   HideHostProcess=program.exe
```

値は、提示されるプロセス名と正確かつ大文字と小文字を区別しない一致で比較されます。完全なパスやワイルドカード パターンではなく、実行可能ファイル名を使用してください。この設定は通常、サンドボックス関連付けのないエントリに適用されますが、提示される名前が `Sandboxie` で始まるエントリ (一部の Sandboxie サービスまたはワーカー プロセスを含む) にも一致することがあります。名前が一致するという理由だけで、別のボックスに割り当てられた通常のプロセスを削除することは通常ありません。

SandMan では、Sandbox Options > Advanced Options > Processes > Process Hiding でプロセス名のリストを管理します。リストにはテンプレートによって提供されるエントリも表示されることがあります。

この設定はプロセス リストの結果をフィルター処理するものであり、それ自体で既知の PID によるプロセスへのアクセスを拒否するものではありません。WMI を含む他の検出パスは別個です。関連するリスト フィルターについては [Hide Non System Processes](HideNonSystemProcesses.md) および [Hide Other Boxes](HideOtherBoxes.md) を参照してください。
