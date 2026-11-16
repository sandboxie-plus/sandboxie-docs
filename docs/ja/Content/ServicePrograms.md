# サービス プログラム


### 概要

Windows コンピューターには、アプリケーション プログラムからの要求を受け入れるように設計されたいくつかのサービス プログラムが含まれています。多くのサービス プログラムは特別な _svchost.exe_ プロセス（プログラム）内で実行されますが、他の一部はスタンドアロン プロセスとして実行されます。

Sandboxie の下で実行されているプログラムは、サンドボックスの分離により、それらのシステム サービス プログラムに到達することが許可されていません。代わりに、Sandboxie は独自のサービス プログラムを提供し、それらはサービスを要求するプログラムと同じサンドボックス内で実行されます。

Sandboxie サービス プログラムはオンデマンドで開始されます。以下にリストされているサービス プログラムのいずれかが特定の時点で実行されていなくても、エラーや問題ではありません。

* * *

### リモート プロシージャ コール (RPC) {#remote-procedure-call-rpc}
```
    Program Name:  SandboxieRpcSs.exe
    Service Name:  rpcss
```

Component Object Model (COM) のメイン サービス。このサービスは、あるアプリケーションが別のアプリケーションを起動するためのメカニズムを含む、サンドボックス内のアプリケーションへの幅広いサービスを提供します。サンドボックス化して実行するプログラムに応じて、サービスは開始する必要がある場合とない場合があります。

このサービスは、_DCOM Server Process Launcher_（以下を参照）と共に、他のサービス プログラムがサンドボックス内で開始できるようにします。

* * *

### DCOM Server Process Launcher
```
    Program Name:  SandboxieDcomLaunch.exe
    Service Name:  dcomlaunch
```

このサービスは、_Remote Procedure Call (RPC)_（上記を参照）と共に、他のサービス プログラムがサンドボックス内で開始できるようにします。

このサービスは Windows XP Service Pack 2 以降のオペレーティング システムで利用可能であることに注意してください。

* * *

### Cryptographic Services
```
    Program Name:  SandboxieCrypto.exe
    Service Name:  cryptsvc
```

ソフトウェア署名、セキュリティ証明書、およびソフトウェア カタログを管理します。このサービスは、同じサンドボックス内で実行されている他のプログラムによってインストールされたデジタル証明書またはカタログ情報を管理し、サンドボックス内に保存します。

このサービスは、ときどきインターネット アドレス _mscrl.microsoft.com_ に接続します。この接続は SandboxieCrypto.exe 内で実行されている Microsoft コードによって開始され、Web サイトとプログラムのデジタル証明書を検証または失効させる手順の一部です。

この接続は _SandboxieCrypto.exe_ に固有のものではなく、_svchost.exe_ プロセスの 1 つの下で実行されている「本物の」サービス プログラムによっても開始されます。[制限 > インターネット アクセス](RestrictionsSettings.md#internet-access)またはファイアウォールを通じてこの接続をブロックすることが可能です。ただし、これは推奨されません。証明書失効の詳細については、[Wikipedia の証明書失効リスト](https://en.wikipedia.org/wiki/Certificate_revocation_list)を参照してください。

* * *

### Background Intelligent Transfer Service
```
    Program Name:  SandboxieBITS.exe
    Service Name:  bits
```

要求元のアプリケーションに代わってバックグラウンドでファイルをダウンロードします。一部のインストール プログラム（最も一般的には Microsoft および Google 製品向け）は、このサービスに代わりに追加のリソース ファイルをダウンロードするよう要求します。サービスはこれらのファイルをサンドボックスにダウンロードします。

* * *

### Automatic Updates
```
    Program Name:  SandboxieWUAU.exe
    Service Name:  wuauserv
```

Windows の更新プログラムを確認し、_Background Intelligent Transfer Service_（上記を参照）を使用してそれらをダウンロードします。更新プログラムがサンドボックスにダウンロードされると、このサービスはそれらをサンドボックスにインストールしようとします。場合によっては、Windows の更新にコア システム ファイルの変更が含まれることに注意してください。そのような変更は、Sandboxie の監督下で実行された場合、失敗するか効果がない可能性があります。

* * *

### Windows Installer
```
    Program Name:  msiexec.exe
    Service Name:  msiserver
```

Windows Installer テクノロジを使用して準備されたソフトウェア パッケージをインストールします。ソフトウェアはサンドボックスにインストールされます。ソフトウェアのインストール中に _msiexec.exe_ の複数のインスタンスが開始および停止するのを確認するのが一般的です。
