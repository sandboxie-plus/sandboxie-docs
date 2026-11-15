# Block Sys Param

**BlockSysParam 機能は SBIE バージョン 4.+ 以降で削除されました。現在は利用できません。**


_BlockSysParam_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定でした。Sandboxie がサンドボックス化されたプログラムによるさまざまなシステム パラメーターの変更を許可するかどうかを指定していました。

使用法:

```
   .
   .
   .
   [DefaultBox]
   BlockSysParam=n
```

_n_ を指定すると、サンドボックス化されたプログラムが、デスクトップの壁紙など、さまざまなシステム パラメーターを変更する要求を発行することが許可されることを示します。

変更できるシステム パラメーターに関する詳細な説明については、Microsoft MSDN Web サイトの [SystemParametersInfo API](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfoa) に関する説明を参照してください。

**技術的な注記:** Sandboxie がシステム パラメーターを変更する要求をブロックすると、[Resource Access Monitor](ResourceAccessMonitor.md) に操作 _(SystemParametersInfo:nnnnnnnn)_ として記録されます。ここで _nnnnnnnn_ は SystemParametersInfo API に渡された _uiAction_ パラメーターに対応する 16 進値です。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Restrictions > Low-Level Access](RestrictionsSettings.md#low-level-access-removed)
