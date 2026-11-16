# Block Password

_BlockPassword_ は、現在のランタイムでも引き続き尊重される従来の設定です。古いユーザー インターフェイス コントロールは削除され、そのメタデータは、現代の Windows のパスワード変更互換性のケースについて _OpenSamEndpoint_ によって置き換えられたことを示しています。置き換えられたということは、_BlockPassword_ が無視されるという意味ではありません。

この設定は、別個の LSA 認証およびパスワード関連フィルターを制御します。_OpenSamEndpoint_ または _OpenLsaEndpoint_ の別名ではありません。_OpenLsaSSPI_ は現在の INI 設定として確認されていません。現在のエンドポイント フィルターについては [System Endpoints](SystemEndpoints.md) を参照してください。

使用法:

```
   .
   .
   .
   [DefaultBox]
   BlockPassword=n
```

従来のフィルターは既定で有効です。_n_ を指定すると、そのフィルターが無効になります。Windows 10 以降では、Sandboxie Plus 0.7.0 / Classic 5.48.0 以降、パスワード変更の動作に関して _OpenSamEndpoint_ が推奨される互換性設定になりました。[#938](https://github.com/sandboxie-plus/Sandboxie/issues/938) を参照してください。

~~関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Restrictions > Low-Level Access](RestrictionsSettings.md#low-level-access-removed)~~
