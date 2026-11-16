# Mark Of The Web Box

_MarkOfTheWebBox_ は、[Force Mark of The Web](ForceMarkOfTheWeb.md) のプロセス開始評価の宛先サンドボックスを指定するグローバルな [Sandboxie Ini](SandboxieIni.md) 設定です。

```ini
[GlobalSettings]
ForceMarkOfTheWeb=y
MarkOfTheWebBox=Web_Box
```

`MarkOfTheWebBox` が存在しないか空の場合、ドライバーのランタイム フォールバックは `DefaultBox` です。宛先名は、強制の対象となるサンドボックスに対して大文字と小文字を区別せずに照合されます。サンドボックスは現在のユーザーとセッションに対して有効である必要があり、[DisableForceRules](DisableForceRules.md) はそれを対象リストから除外します。

Mark-of-the-Web チェックが一致しても宛先を選択できない場合、Sandboxie はこのパスがサンドボックス化されずに続行することを許可するのではなく、新しいプロセスを終了対象としてマークします。何がチェックされるか、およびこのプロセス開始ルールの制限については [Force Mark of The Web](ForceMarkOfTheWeb.md) を参照してください。
