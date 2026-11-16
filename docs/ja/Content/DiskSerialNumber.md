# Disk Serial Number

_DiskSerialNumber_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、v1.15.2 / 5.70.2 以降で利用できます。[Hide Disk Serial Number](HideDiskSerialNumber.md) によって傍受される `GetVolumeInformationByHandleW` パスを使用するソフトウェアに、カスタムの Windows **ボリューム シリアル番号** を提供します。製造元の物理ディスク シリアル番号や、ディスクを識別するすべての方法を変更するものではありません。

## 構文と例

修飾されていない値を一般的な置き換えとして使用するか、デバイス名で特定のボリュームを選択できます:

```ini
DiskSerialNumber=1234-ABCD
DiskSerialNumber=HarddiskVolume1,1234-ABCD
```

たとえば、ボックスは名前付きボリュームに対して異なる値を構成できます:

```ini
[DefaultBox]
HideDiskSerialNumber=y
DiskSerialNumber=HarddiskVolume1,1234-ABCD
DiskSerialNumber=HarddiskVolume2,5678-EF01
DiskSerialNumber=HarddiskVolume3,9ABC-DEF0
```

デバイス セレクターは、照会されたハンドルに対して解決された NT パスの `\Device\` の後の最初のコンポーネントです。`HarddiskVolume1` は例であり、ドライブ文字への永続的なマッピングではありません。プログラム名セレクターではありません。一致するデバイス固有の値は、修飾されていない値よりも優先されます。Windows のドライブ文字の一覧、ディスクの管理、およびボリューム シリアル コマンドは、それ自体では、このフックが解決する NT 名や、アプリケーションが傍受された API を使用するかどうかを確立しません。

## 値の形式と動作

16 進数の数字を使用し、省略可能でハイフンで区切ります (例: `1234ABCD`、`1234-ABCD`、`12-34-AB-CD`、または `DEADBEEF`)。上記の従来の例は 4 バイトを表します。16 進数以外の文字および桁数が奇数の場合は無効です。該当する有効なカスタム値が利用できない場合、Sandboxie はこのパスで置き換えを生成します。それによってホスト シリアルへのフォールバックを約束するものではありません。

このフックがこれらのエントリを使用するには、有効な `HideDiskSerialNumber=y` 値が必要です。この設定は、決定論的テストや、`GetVolumeInformationByHandleW` を通じてボリューム シリアルを読み取るソフトウェアとの互換性に役立ちますが、他のディスクまたはボリュームの API や WMI クラスを通じた識別を防ぐものではありません。

置き換えは、デバイス パスではなく元のボリューム シリアルによって、サンドボックス化された各プロセス内でキャッシュされます。その元のシリアルに対する繰り返しの照会は、選択された値を再利用します。元のシリアルを共有するボリュームは、そのプロセス内で最初にキャッシュされた置き換えを共有することがあります。カスタム値を変更しても、既存のキャッシュ エントリは更新されません。キャッシュを再構築するには、影響を受けるサンドボックス化されたプロセスを再起動してください。

期待される値が観察されない場合は、`HideDiskSerialNumber` が有効に有効化されていること、カスタム値が有効な 16 進数であること、選択された NT デバイス名が一致すること、およびアプリケーションが実際に傍受された by-handle API を使用していることを確認してください。異なる照会パスでは、この設定の効果は示されません。

## 構成の利用可否

SandMan には **Sandbox Options > Advanced Options > Privacy** の下に **Hide Disk Serial Number** チェックボックスがありますが、カスタム `DiskSerialNumber` 値専用のエディターは確認されていません。カスタム値は INI で構成できます。チェックボックスは直接のボックス値を表示しますが、有効な有効化値は該当するテンプレートまたはグローバル構成から取得することもできます。

## 関連する設定

- [Hide Disk Serial Number](HideDiskSerialNumber.md) はこのボリューム シリアル置換パスを有効にします。
- [Hide Firmware Info](HideFirmwareInfo.md) は別個の SMBIOS 照会パスに影響します。
- [Hide Network Adapter MAC](HideNetworkAdapterMAC.md) は別個のネットワーク アドレス パスに影響します。
- [Random Registry UID](RandomRegUID.md) は選択されたボックス化されたレジストリ値に影響します。
