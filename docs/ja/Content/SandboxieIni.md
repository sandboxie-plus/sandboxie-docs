# Sandboxie Ini

Sandboxie の動作の一部は、Sandboxie.ini と呼ばれる人間が読めるテキスト構成ファイルを使用して変更または微調整できます。このセクションでは、ファイルの構造と内容について説明します。

一般的な原則として、構成ファイルの手動編集は推奨されません。構成の変更には [Sandboxie Control](SandboxieControl.md) を使用することをお勧めします。[サンドボックス設定](SandboxSettings.md)を参照してください。

## 場所

Sandboxie は、次のフォルダーでこの順序で Sandboxie.ini ファイルを探します。

* Windows フォルダー内: ほとんどの Windows インストールでは `C:\Windows`
* Sandboxie インストール フォルダー内: 通常 `C:\Program Files\Sandboxie` または `C:\Program Files\Sandboxie-Plus`

Sandboxie.ini の検索は、ファイルのインスタンスが見つかった時点で終了し、他のすべてのインスタンスは無視されます。

[Sandboxie Control](SandboxieControl.md) が構成を更新すると、最後に構成が読み取られたフォルダー内の Sandboxie.ini ファイルを書き換えます。したがって、ファイルを手動で移動した場合は、Sandboxie 構成を手動で[再読み込み](ConfigureMenu.md#reload-configuration)する必要があります。（コンピューターを再起動しても同じ効果があります。）

**注:** Sandboxie は Sandboxie.ini ファイルの他のカスタム場所をサポートしていません。

## 構造

ファイル内の構成設定は、グループつまりセクションに分割されます。セクションは、角括弧で囲まれた名前を指定する行で始まります。例: [SomeSectionName]。セクションはファイルの末尾まで、または別のセクションが始まるまで続きます。セクションには 3 つの種類があります。

* グローバル設定セクションには、Sandboxie にグローバルな設定が含まれます。これらは何らかの形ですべてのサンドボックスとすべてのユーザー アカウントに適用されます。グローバル設定セクションは 1 つだけ存在でき、通常は構成ファイルの先頭にあります。
* Sandboxie が認識する各サンドボックスに対して 1 つのサンドボックス設定セクション。有効なサンドボックス名は英字と数字の文字列で、最大長は 32 文字です。サンドボックス設定セクションには設定 [Enabled](Enabled.md)=y を含める必要があります。
* 各ユーザー アカウントに対して 1 つのユーザー設定セクション。これらの設定は特定のユーザー アカウントの [Sandboxie Control](SandboxieControl.md) の状態を記録し、ウィンドウのサイズなどの情報を含みます。これらの設定はここでは文書化されていませんが、以下で簡単に説明します。

単純な Sandboxie.ini ファイルは次のようになります。

```
   # Sample Sandboxie Configuration File
   [GlobalSettings]
   FileRootPath=C:\Sandbox\%USER%\%SANDBOX%
   # Settings for sandbox DefaultBox
   [DefaultBox]
   Enabled=y
   # Settings for sandbox InstallBox
   [InstallBox]
   Enabled=y
   FileRootPath=D:\Sandbox\Install
   # Sandboxie Control settings for some user
   [UserSettings_054A02CE]
   SbieCtrl_UserName=tzuk
```

この例は 4 つのセクションを示しています。グローバル セクション（GlobalSettings）、2 つのサンドボックス セクション（DefaultBox と InstallBox）、および 1 つのユーザー アカウント セクション（UserSettings_054A02CE）です。

シャープ記号（#）で始まる行はコメントです。これらの行はスキップされます。

**注:** [Sandboxie Control](SandboxieControl.md) は動作中に Sandboxie.ini ファイルを定期的に書き換え、この書き換えではすべてのコメントが失われます。ただし、認識されない設定は書き換え中に失われないため、回避策の 1 つは Comment=text の形式でコメントを書くことです。

構成ファイルには最大 30,000 行のテキストを含めることができます。各行は最大 1000 文字です。

ファイルは UNICODE エンコードされています。つまり、各文字は 2 バイトで構成されます。システムのメモ帳を含む多くのテキスト ファイル エディターは、このエンコードを適切に処理します。

## 設定

個々の設定とその文書化されたスコープを見つけるには、[全ページ インデックス](AllPages.md)を使用してください。

### グローバル設定:

* 設定は、特定のサンドボックスではなく、Sandboxie の一般的な動作に適用されます。
* グローバル設定は GlobalSettings セクションに配置する必要があり、サンドボックス セクションにも含めることで上書きすることはできません。
* サンドボックス設定は GlobalSettings セクションに表示される場合があり、サンドボックス セクションにも含めることで上書きできます。

### サンドボックス設定:

* 設定は、関連するサンドボックス セクションで指定された場合、特定のサンドボックスに適用されます。
* 設定は、[GlobalSettings] セクションで指定された場合、すべてのサンドボックスに適用されます。
* サンドボックス セクションの設定は、[GlobalSettings] の対応する設定を上書きします。

上記の例では、サンドボックス設定 [FileRootPath](FileRootPath.md) が [GlobalSettings] に表示され、すべてのサンドボックスに適用されますが、セクション [InstallBox] で上書きされていることに注意してください。

* サンドボックス設定は特定のプログラムに適用できます。[プログラム名プレフィックス](ProgramNamePrefix.md)を参照してください。
* 一部のサンドボックス設定は[はい/いいえ設定](YesOrNoSettings.md)です。
* サンドボックス設定は、Sandboxie が認識する[展開可能な変数](ExpandableVariables.md)を指定できます。

### ユーザー設定

* 設定は、たとえばウィンドウの位置など、[Sandboxie Control](SandboxieControl.md) の状態を記録します。
* 各ユーザー アカウントは別の [UserSettings_XXXXXXXX] セクションに誘導されます。
* 新しい [UserSettings_XXXXXXXX] が作成されると、既定値は存在する場合 [UserSettings_Default] セクションから取得されます。
* セクション [UserSettings_Portable] が存在する場合、すべてのユーザー アカウントはこのセクションを使用するように誘導されます。

## 自動化

Sandboxie には、Sandboxie.ini 構成ファイルを照会または更新するためのコマンド ライン ユーティリティが含まれています。このユーティリティは、直接のコマンド ライン操作だけでなく、スクリプトやプログラムからの呼び出しにも適しています。このユーティリティは Sandboxie インストール ディレクトリに SbieIni.exe としてあります。詳細については、[コマンド ラインによるサンドボックスの作成](https://github.com/sandboxie-plus/Sandboxie/issues/278#issuecomment-856207910)と [SbieIni.exe の使用法](https://sandboxie-website-archive.github.io/www.sandboxie.com/old-forums/viewtopica6bca6bc.html#p126947)セクションを参照してください。
