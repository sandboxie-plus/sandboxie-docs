# Force Disable Seconds

_ForceDisableSeconds_ は [Sandboxie Ini](SandboxieIni.md) のグローバル設定です。[Disable Forced Programs](FileMenu.md#disable-forced-programs) モードが有効なままになる時間を秒単位で指定します。

使用法:
```
   .
   .
   .
   [GlobalSettings]
   ForceDisableSeconds=25
   ForceDisableSeconds=0
```

この設定の既定値は 10 秒です。値をゼロに設定すると、_Disable Forced Programs_ 機能自体が事実上無効になります。[ForceDisableAdminOnly](ForceDisableAdminOnly.md) も参照してください。

_Disable Forced Programs_ モードは [Sandboxie Control](SandboxieControl.md) を通じて有効になり、秒数を構成することもできます。[FileMenu > Disable Forced Programs](FileMenu.md#disable-forced-programs) コマンド、または [Tray Icon Menu](TrayIconMenu.md) から同じコマンドを使用します。

アクティブな場合、_Disable Forced Programs_ モードは、強制プログラムが開始されるたびに Sandboxie がメッセージ [SBIE1301](SBIE1301.md) を発行するようにします。
