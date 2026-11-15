# Closed Key Path

_ClosedKeyPath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。優先する Closed ルールが、新しいフックされたレジストリ オープンまたは作成を、 _読み取り_ アクセスを含めて拒否するパス パターンを指定します。

[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:

```
   .
   .
   .
   [DefaultBox]
   ClosedKeyPath=!msimn.exe,HKEY_CURRENT_USER\Software\Microsoft\Internet Account Manager
```

この例は、Outlook Express (_msimn.exe_) _以外_ のあらゆるプログラムが、アクティブなユーザー アカウントの構成済み電子メール アカウントを含むレジストリ キーにアクセスするのをブロックします。

_ClosedKeyPath_ に指定する値にはワイルドカードを含めることができますが、レジストリ キーの場合、ワイルドカードの使用が必要になることはほとんどありません。これに関する詳細 (ワイルドカードの使用を示す例を含む) については、[OpenFilePath](OpenFilePath.md) を参照してください。(_OpenFilePath_ はファイルを扱い、レジストリ キーは扱いませんが、ワイルドカードを使用する原則は同じです。)

**注:** 新しいフックされたレジストリ オープン/作成では、通常のサンドボックス コピー パスの前に優先する Closed ルールがチェックされます。サンドボックス コピーの存在自体がルールをバイパスするわけではありません。既に開かれているハンドルは別個です。ルールを変更しても、以前に付与されたハンドルが取り消されることを意味しません。

**注:** [OpenKeyPath](OpenKeyPath.md) の通常の適格性制限とは異なり、Closed ルールは実行可能ファイルがサンドボックス内にある場合でも適用されます。`AlwaysCloseForBoxed` がアクティブな場合、否定のプログラム セレクターはサンドボックス内の実行可能ファイルに対する通常の免除を提供しません。これは上記の例を限定するものです。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Resource Access > Registry Access > Blocked Access](ResourceAccessSettings.md#registry-access-blocked-access)

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Registry > Add Reg Key > Access column > Closed
