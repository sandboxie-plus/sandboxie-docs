# Box Name Title

_BoxNameTitle_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。Sandboxie が、サンドボックス化されたアプリケーションに属するウィンドウのタイトル バーにサンドボックスの名前を表示するかどうかを制御します。

使用法:

```
   .
   .
   .
   [DefaultBox]
   BoxNameTitle=y
```

既定では、Sandboxie はサンドボックス化されたアプリケーションに属するウィンドウのタイトル バーに、サンドボックス化されたことを示す [#] インジケーターのみを表示します。例:

[#] Sandboxie - Front Page - Windows Internet Explorer [#]


_BoxNameTitle=y_ を指定すると、サンドボックス名がタイトル バーに配置されます:

[#] [DefaultBox] Sandboxie - Front Page - Windows Internet Explorer [#]

Sandboxie は、過度の DWM 再描画アクティビティと高い CPU 使用率を避けるため、カスタムまたはクライアント描画のタイトル バーを使用していると検出されたウィンドウのタイトル変更をスキップすることがあります。プログラムごとのオプトアウトについては [Disable Custom Title Optimization](DisableCustomTitleOpt.md) を参照してください。


関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Appearance](AppearanceSettings.md)
