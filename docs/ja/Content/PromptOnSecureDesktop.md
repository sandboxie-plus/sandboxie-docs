# Prompt On Secure Desktop

**PromptOnSecureDesktop** は [Sandboxie Ini](SandboxieIni.md) のグローバル サンドボックス設定で、v1.16.0 / 5.71.0 以降で使用できます。サンドボックス化されたアプリケーションからの User Account Control (UAC) 昇格プロンプトを、ホスト システムの動作に影響を与えずにセキュア デスクトップに表示するかどうかを制御します。

**注:** この設定は [UseSandboxieUAC](UseSandboxieUAC.md) が有効な場合にのみ効果があります。

使用法:

```ini
   .
   .
   .
   [GlobalSettings]
   PromptOnSecureDesktop=n
```

この設定は、システムが別の設定になっていても、サンドボックス化されたアプリケーションからの UAC プロンプトがセキュア デスクトップに表示されないようにします。


