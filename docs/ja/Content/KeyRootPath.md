# Key Root Path

_KeyRootPath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。特定のサンドボックスのレジストリ ハイブがマウントされるレジストリの場所を指定します。ハイブのバッキング ファイル `RegHive` は [FileRootPath](FileRootPath.md) の下に存在し、2 つのルートは交換可能ではありません。

ボックスに対して設定するか、`[GlobalSettings]` または該当する有効なテンプレートを通じて提供できます。展開されたルートは Sandboxie がボックス パス情報を構築するときに確立され、既にマウントされたハイブは同じレジストリ ターゲットへの変更を制約することがあります。

ハイブ ファイルとレジストリ マウント ポイントの区別については [Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md) および [Sandbox Hierarchy](SandboxHierarchy.md) を参照してください。

使用法:
```
   .
   .
   .
   [DefaultBox]
   KeyRootPath=\REGISTRY\USER\Sandbox_%USER%_%SANDBOX%
```

このパスでは次の置換変数が役立つことがあります。

*   サンドボックスの名前に展開される変数 %SANDBOX%
*   ユーザー名に展開される変数 %USER% (または %USERNAME%)
*   ユーザー セキュリティ ID (SID) に展開される変数 %SID%
*   Terminal Services セッション番号に展開される変数 %SESSION%

KeyRootPath が指定されていない場合、その既定値は:

*   _\REGISTRY\USER\Sandbox_%USER%_%SANDBOX%_

`%BOXNAME%` はこのルート展開パスでサポートされる別名ではありません。`%SANDBOX%` を使用してください。現在のルート初期化子は、それ自体でカスタム値に `\REGISTRY\USER\` プレフィックスを強制しません。それでも、展開された値は使用可能なレジストリ マウント ターゲットである必要があり、そうでない場合はハイブのマウントが失敗します。`\REGISTRY\USER\` の下の既定値は、通常のボックスに適した選択です。

通常、この既定値を変更する理由はありません。サービスはまた、レジストリ ルートを使用してマウントされたイメージまたは RAM ディスクのボックスを識別します。ボックスの使用中に変更すると、マウント競合が発生することがあります。この設定はレジストリ アクセス許可を変更しません。

Sandboxie がサンドボックス化されたレジストリ ハイブを正常にマウントまたはアンマウントできない場合、それぞれメッセージ [SBIE1241](SBIE1241.md) および [SBIE2208](SBIE2208.md) を発行します。

SandMan では、グローバル既定は **Global Settings > Advanced Config > Sandboxie Config > Sandbox registry root** にあります。ボックスごとの値は **Sandbox Options > Advanced Options > Miscellaneous > Add Option** に入力できます。
