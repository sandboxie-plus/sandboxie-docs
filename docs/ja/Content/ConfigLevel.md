# Config Level

**注: Sandboxie バージョン 3.xx より前では、ConfigLevel は [GlobalSettings] セクションのグローバル設定でした。グローバルな ConfigLevel 設定は現在使用されておらず、構成ファイルに存在する場合は無視されます。**

_ConfigLevel_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。[Sandboxie Control](SandboxieControl.md) がサンドボックスの既定の構成を管理するために使用します。

ConfigLevel が存在しない場合、数値でない場合、または 9 未満の数値の場合、Sandboxie Control は次の構成をサンドボックスに追加します:

```
   .
   .
   .
   [DefaultBox]
   ConfigLevel=9
   Template=OpenSmartCard
   Template=OpenBluetooth
```
ConfigLevel の値は、Sandboxie v0.7.5 / 5.49.8 のリリースで 8 から 9 に変更されたことに注意してください。

将来的には、Sandboxie の後のバージョンで新しい構成レベルが追加される可能性があります。
