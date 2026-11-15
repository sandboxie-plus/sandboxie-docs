# Closed File Path

_ClosedFilePath_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。サンドボックス化されたプログラムによる _すべて_ のアクセス ( _読み取り_ アクセスを含む) を Sandboxie が拒否するパス パターンを指定します。この設定は基本的に、サンドボックス化されたプログラムがファイルおよびフォルダーにアクセスするのをブロックします。

[Shell Folders](ShellFolders.md) を指定できます。[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:

```
   .
   .
   .
   [DefaultBox]
   ClosedFilePath=!iexplore.exe,%Cookies%
   ClosedFilePath=%Personal%
```

```
   ClosedFilePath=!iexplore.exe,\Device\RawIp
   ClosedFilePath=!iexplore.exe,\Device\Ip*
   ClosedFilePath=!iexplore.exe,\Device\Tcp*
   ClosedFilePath=!iexplore.exe,\Device\Afd*
```

この例は、Internet Explorer (_iexplore.exe_) _以外_ のあらゆるプログラムが、アクティブなユーザー アカウントのダウンロードされたインターネット Cookie を含むフォルダーにアクセスするのをブロックします。これにより、ダウンロードされた悪意のあるソフトウェアが Cookie をスパイするのをブロックできます。

(これは、アドオン ツールバーなどのブラウザー拡張機能が Cookies フォルダーを調べるのを止めるものではないことに注意してください。これらの拡張機能は Internet Explorer プログラム プロセス内で実行されるためです。)

2 番目の例は、サンドボックス化されたプログラムが _Documents_ フォルダーにアクセスするのをブロックするように Sandboxie を構成する方法を示しています。

ClosedFilePath に指定する値にはワイルドカードを含めることができます。これに関する詳細 (ワイルドカードの使用を示す例を含む) については、[OpenFilePath](OpenFilePath.md) を参照してください。

3 番目の例 (4 行にわたる) は、Internet Explorer (_iexplore.exe_) を _除いて_、サンドボックス内のインターネット アクセスを無効にします。[Sandbox Settings > Restrictions > Internet Access](RestrictionsSettings.md#internet-access) も参照してください。

**注:** 対応する OpenFilePath 設定とは異なり、_ClosedFilePath_ 設定は、プログラムの実行可能ファイルがサンドボックス内にあるか外にあるかに関係なく、常にサンドボックス化されたプログラムに適用されます。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Resource Access > File Access > Blocked Access](ResourceAccessSettings.md#file-access-blocked-access)

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Files > Add File/Folder > Access column > Closed
