# Block Win Hooks

**BlockWinHooks 機能は SBIE バージョン 4.+ 以降で削除されました。現在は利用できません。**

_BlockWinHooks_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定でした。Sandboxie がサンドボックス化されたプログラムによるシステム グローバル フックのインストールを許可するかどうかを指定していました。

使用法:

```
   .
   .
   .
   [DefaultBox]
   BlockWinHooks=n
```

1 つのアプリケーションは、Windows フックと呼ばれるメカニズムを使用して、システム内の他のアプリケーションにアタッチできます。このメカニズムは、要求元アプリケーションのコンポーネント (DLL ファイルと呼ばれる) を他のすべてのアプリケーションに関連付けます。

既定では、Sandboxie はグローバル フックのインストール要求を拒否し、代わりにそのフックをアプリケーション固有のフックに変換して、要求元アプリケーションと同じサンドボックス内で実行されているアプリケーションにのみこの変換されたフックをインストールします。

事実上、これはグローバル フックの効果を特定のサンドボックスに制限し、グローバル フックに依存するアプリケーションが正しく実行できるようにしつつ、Sandboxie が提供する保護を向上させます。

_BlockWinHooks=n_ を指定すると、この保護が無効になり、サンドボックス化されたアプリケーションが、サンドボックス内外の両方で実行されているすべてのアプリケーションにグローバル フックをインストールできるようになります。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Restrictions > Low-Level Access](RestrictionsSettings.md#low-level-access-removed)
