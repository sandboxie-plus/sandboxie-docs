# Ipc Root Path

_IpcRootPath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。ディスク上のフォルダーではなく、ボックスの NT 名前付きオブジェクト 名前空間ルートを指定します。Sandboxie はまた、このルートから関連するパイプ パス表現を導出します。

ボックスに対して設定するか、`[GlobalSettings]` または該当する有効なテンプレートを通じて提供できます。その既定値には `%SESSION%` が含まれるため、展開された名前空間ルートは Windows セッション間で異なることがあります。

他のルートとの関係については [Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md) および [Sandbox Hierarchy](SandboxHierarchy.md) を参照してください。

使用法:
```
   .
   .
   .
   [DefaultBox]
   IpcRootPath=\Sandbox\%USER%\%SANDBOX%\Session_%SESSION%
```

このパスでは次の置換変数が役立つことがあります。

*   サンドボックスの名前に展開される変数 %SANDBOX%
*   ユーザー名に展開される変数 %USER% (または %USERNAME%)
*   ユーザー セキュリティ ID (SID) に展開される変数 %SID%
*   Terminal Services セッション番号に展開される変数 %SESSION%

IpcRootPath が指定されていない場合、その既定値は:

*   _\Sandbox\%USER%\%SANDBOX%\Session_%SESSION%_

この設定の既定値を変更する理由はおそらくなく、変更は推奨されません。

`%BOXNAME%` はこのルート展開パスでサポートされる別名ではありません。`%SANDBOX%` を使用してください。この名前空間ルートを変更しても、それ自体でホスト IPC オブジェクトへのアクセスが許可されたり、[NT Namespace Isolation](NtNamespaceIsolation.md) や IPC アクセス ルールが置き換えられたりするわけではありません。変更後は影響を受けるサンドボックス化されたプロセスを再起動してください。既存のプロセスは初期化されたルートを保持します。

SandMan では、グローバル既定は **Global Settings > Advanced Config > Sandboxie Config > Sandbox ipc root** にあります。ボックスごとの値は **Sandbox Options > Advanced Options > Miscellaneous > Add Option** に入力できます。
