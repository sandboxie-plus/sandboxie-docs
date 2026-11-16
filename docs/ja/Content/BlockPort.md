# Block Port

**この機能は v0.9.0 / 5.51.0 以降で削除されました。[Sandboxie Ini](SandboxieIni.md) にカスタムの BlockPort エントリがある場合は、新しい形式に手動で更新する必要があります。たとえば `BlockPort=137,138,139,445` は `NetworkAccess=*,Block;Port=137,138,139,445` になります (現在は _Templates.ini_ ファイルの `[Template_BlockPorts]` セクションに含まれています)。**

_BlockPort_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定でした。発信通信のためにブロックする IP ポート番号を指定していました。

使用法:

```
   .
   .
   .
   [DefaultBox]
   BlockPort=137-139,445
   BlockPort=*,80,8080
```

上記のポート番号は SMB/CIFS ネットワーク ファイル共有サブシステムに関連付けられています。

この設定の主な目的は、SMB/CIFS ポートでの発信通信をブロックすることです。これは、悪意のあるサンドボックス化されたプログラムが、ローカル システムに直接要求を発行するのではなく、SMB/CIFS サブシステムを通じてファイルにアクセスするのを防ぐためです。

この設定は複数行にわたって繰り返し指定でき、効果は累積します。ポート範囲は最初の例のように指定できます。2 番目の例は否定の使用法を示しています。アスタリスク (スター) 文字の後に指定されたポートを除くすべてのポートをブロックします。

この設定は、定義済みの既定のブロック ポート リストを有効または無効にする場合を除き、Sandboxie Control を通じて構成できません:

[Sandbox Settings > Applications > Miscellaneous](ApplicationsSettings.md#misc) > Default list of blocked TCP/IP ports

この設定により、[smbclient](http://www.samba.org/samba/docs/man/manpages-3/smbclient.1) などのプログラムが Sandboxie の下で適切に実行できなくなることに注意してください。これが必要な場合は、設定をオフにできます。
