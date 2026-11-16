# コード インジェクション

Sandboxie は、作成時にプロセスにコードを注入するという特に低レベルなアプローチを採用しています。

##### トリガー
ドライバーは `PsSetCreateProcessNotifyRoutine` コールバックを登録し、これがトリガーされるとプロセスをサンドボックス化すべきかどうかを検査し、そう決定するとブロックし、SbieSvc サービスにローダーをプロセス イメージに注入するよう要求します。あるいは、`API_START_PROCESS` を使用して中断されたプロセスを作成し、ドライバーが終了したらプロセスを再開してサンドボックスに配置するようドライバーをトリガーすることもできます。

インジェクション メカニズム自体は、ドライバーなしで利用できるように適応させることができます。バージョン 5.44 以降、ローダー コードは SbieSvc.exe から SbieDll.dll に移動されました。

##### 概要
コード インジェクション メカニズムは 3 つのコンポーネントで構成されています。インジェクター自体、低レベル シェル コード (LowLevel.dll)、および注入されるペイロード (SbieDll.dll) です。LowLevel.dll はリソースとしてローダーに埋め込まれていることに注意してください。

## リモート インジェクション
インジェクションは `_FX ULONG SbieDll_InjectLow(HANDLE hProcess, BOOLEAN is_wow64, BOOLEAN bHostInject, BOOLEAN dup_drv_handle)` を呼び出して必要な引数を提供することで行われ、関数は次のことを行います。

* まず `SBIELOW_DATA` 型のデータ ブロック `lowdata` を準備し、is_wow64、bHostInject などのさまざまな値を埋めます...
* 次に `SbieDll_InjectLow_CopyCode` を使用して、ターゲット プロセスに `sizeof(shell_code) + sizeof(SBIELOW_J_TABLE) + 0x400` バイトのメモリを割り当て、そこにシェル コードを書き込みます。

この関数は、無関係な最後のステップで `ntdll!LdrInitializeThunk` の先頭から 48 バイトを `lowdata.LdrInitializeThunk_tramp` にコピーします。

* 次に `dup_drv_handle` が設定されていた場合、`SbieDll_InjectLow_SendHandle` を使用してドライバーへのハンドルを開き、プロセスに複製し、その値を `lowdata.api_device_handle` に保存します。
* 次に、必要な NTDLL 関数のいくつかの複製が `lowdata` データ ブロックに保存され、`SBIELOW_J_TABLE` セクションのアドレスが `lowdata.Sbie64bitJumpTable` に格納されます。
* 次に、実際のトランポリンが `SbieDll_InjectLow_BuildTramp` によって `lowdata.LdrInitializeThunk_tramp` 内に構築されます。
* ここで、関数は `SbieDll_InjectLow_CopySyscalls` を使用して、別のメモリ セグメント `syscall_data` を割り当てて埋めます。

このブロックは 2 つのセクションで構成されています。1 つはすべてのシステムコールをフックするために使用されるドライバーからの情報を含み、
これはオプションで `bHostInject == 0` のときにシェル コードによって行われ、その後にメモリ ブロック内のその背後に格納された値を指す `SBIELOW_EXTRA_DATA` が続きます。
そこに格納されるデータはいくつかのオフセット、および後で注入される SbieDll.dll への完全なパスです。

* その補助メモリのアドレスは `lowdata.syscall_data` に保存され、`lowdata` ブロックは `SbieDll_InjectLow_CopyData` によってシェル コード メモリに直接書き込まれます。
* 最後に、ターゲット プロセス内の `ntdll!LdrInitializeThunk` が `SbieDll_InjectLow_WriteJump` を使用して、シェル コードのエントリ ポイントへのジャンプ命令で上書きされます。

これでプロセスを再開でき、注入されたコードがその処理を行います。

ここで重要な注意点は、この関数がネイティブ 64 ビット プロセスと wow64 エミュレート 32 ビット プロセスに対して同じことを行うことです。実際、64 ビット システムでは注入されるシェル コードは常に 64 ビットです。wow64 で実行されているプロセスの初期化のかなり後になって初めて、32 ビットに切り替わります。

## シェル コード (LowLevel.dll) の動作

LowLevel.dll は部分的にアセンブラーで、部分的に C で書かれており、そのベース アドレスは位置独立を得るために 0 に設定されています。
初期エントリ ポイント `_Start` は現在のアドレスを取得し、`SBIELOW_DATA` 型のデータ ブロック `data` のアドレスと、アセンブラーで書かれたいくつかのヘルパー関数のアドレスを計算し、それらの値をパラメーターとして `EntrypointC` 関数を呼び出して操作を C 部分に引き渡します。

`EntrypointC` 関数は、スピンロックを使用して 1 回だけ実行されることを保証し、次に `data->bHostInject` フィールドが `0` に設定されているかどうかをチェックします。設定されている場合、最初に `InitSyscalls` を使用してすべての ntdll システムコール関数をフックし、次に `InitInject` を使用して SbieDll.dll の後での読み込みを準備し、(64 ビット システムでのみ) `InitConsole` を呼び出して ConsoleHandle を変更します。`bHostInject != 0` の場合、関数は `InitInject` のみを呼び出します。最後に、元の関数 `data->LdrInitializeThunk_tramp` へのトランポリンが呼び出されます。

##### InitInject

`InitInject` 関数は、プロセスがネイティブで実行されているか (すなわち x86 システムでの 32 ビット、または x64 システムでの 64 ビット)、wow64 で実行されているか (すなわち 64 ビット システムでの 32 ビット プロセス) をチェックし、ネイティブ ntdll ベース アドレスまたは wow64 ntdll のいずれかを選択します。Windows 8 より前のバージョンでは、そのアドレスは `KUSER_SHARED_DATA::Wow64SharedInformation` 構造体にありましたが、以降のバージョンではそうではありません。Sandboxie はドライバーを使用してイメージ読み込み中に wow64 ntdll のアドレスを記録し、`InitInject` はそれについてドライバーに問い合わせました。しかしバージョン 5.44 以降、それはドライバーに依存せず、ローダー コードは `NtQueryVirtualMemory` を使用してイメージ ベース アドレスを見つけ、それをデータ ブロックの `ntdll_wow64_base` フィールドに保存します。

この時点で、`SBIELOW_EXTRA_DATA` 領域の前の `data->syscall_data` の上部はもはや不要になり、`INJECT_DATA` 型の一時データを格納するために再利用されます。

次に、関数はカスタムの `FindDllExport` ルックアップ関数を使用して、以前に選択された ntdll イメージを解析することにより `LdrLoadDll`、`LdrGetProcedureAddress`、`NtRaiseHardError`、および `RtlFindActivationContextSectionString` のアドレスを見つけます。これらのアドレスは `INJECT_DATA` 領域に格納され、次に `SBIELOW_EXTRA_DATA` からのいくつかの値もその領域にコピーされます。これには SbieDll.dll へのパス (32 ビットと 64 ビットの両方のパス)、および kernel32.dll の名前が含まれます。

64 ビット システムでは、関数はネイティブ実行と wow64 実行を区別し、後者の場合は `InitInjectWow64` に分岐します。
ネイティブの場合は、ntdll.dll 内の `RtlFindActivationContextSectionString` 関数のフックを続行します。

* まず、関数の先頭の元のコピーが `INJECT_DATA` 構造体に保存されます。
* 構造体のアドレスが、アセンブラーで実装されたデタッチ関数に書き込まれます。
* 次に、`RtlFindActivationContextSectionString` の先頭がデタッチ関数へのジャンプ命令で上書きされます。
* 最後に、`SBIELOW_DATA` 領域へのポインターが `INJECT_DATA` 領域の最上部に保存され、関数が終了します。

wow64 の場合、`InitInjectWow64` は wow64 ntdll.dll 内の関数の 32 ビット バージョンで `RtlFindActivationContextSectionString` フックを同様の方法で設定します。

##### RtlFindActivationContextSectionString デタッチ

常にネイティブで実行される上記の操作とは対照的に、`RtlFindActivationContextSectionString` デタッチ関数は、開始されたプロセスのビット数に一致するモードで実行されます。

* 関数はまず元の `RtlFindActivationContextSectionString` の先頭を復元します。
* 次に kernel32.dll を読み込み、続いて SbieDll.dll を読み込み、序数 1 のアドレスを取得します。
* 次に最初の引数の値を `INJECT_DATA` 構造体に保存し、それを前述の構造体へのポインターで置き換えます。
* 最後に、序数 1 のアドレスにジャンプします。呼び出すのではなくジャンプを使用してそれを呼び出すため、戻ると現在の呼び出し元に直接戻ります。

## ペイロード (SbieDll.dll) の動作

SbieDll.dll フック エントリ ポイント `Dll_Ordinal1` 関数は、最初の引数として渡された `INJECT_DATA` 構造体から、`SBIELOW_DATA` データ ブロックのアドレスや最初の引数の元の値など、いくつかの必要な値を取得することから始まります。必要な値をコピーした後、もはや不要になった `INJECT_DATA`、正式には `syscall_data` 領域を解放できます。
次に、関数は `bHostInject` が `0` に設定されているかどうかをチェックし、設定されている場合は `SbieDll!Dll_InitInjected` を呼び出します。この関数はほぼすべてをフックし、最後に `SbieDll!Ldr_Init` を呼び出します。これは dll 読み込みのコールバックを設定し、`SbieDll!Ldr_Inject_Init` を呼び出します。ただし `bHostInject != 0` の場合、`SbieDll!Ldr_Inject_Init` は `Dll_Ordinal1` から直接呼び出されます。初期化が完了すると、`Dll_Ordinal1` は元の引数で実際の `RtlFindActivationContextSectionString` を実行して戻ります。

これだけのフッキングでは不十分であるかのように、`SbieDll!Ldr_Inject_Init` はさらに別のフックを設定します。今回は開始プロセスの実際のエントリ ポイントを対象とします。関数はエントリ ポイントの初期バイトを保存し、`SbieDll!Ldr_Inject_Entry64` または `SbieDll!Ldr_Inject_Entry32` へのジャンプで上書きします。
これらはアセンブラーで実装されており、リターン アドレスの場所へのポインターを `SbieDll!Ldr_Inject_Entry` への引数として渡し、スタックをクリーンアップし、次にエントリ ポイントの先頭に戻ります。

##### Ldr_Inject_Entry

この関数はまず `SbieDll!Ldr_Inject_SaveBytes` から元のエントリ ポイント関数を復元し、その呼び出し元のリターン アドレスをエントリ ポイントの先頭を指すように変更します。これにより、呼び出し元が戻ると実際のエントリ ポイントが呼び出されます。次に、関数は `bHostInject` が `0` に設定されているかどうかをチェックし、設定されている場合は最初に `SbieDll!Ldr_LoadInjectDlls` を呼び出し、次に最後の初期化ステップを実行する `SbieDll!Dll_InitExeEntry` を呼び出します。`bHostInject != 0` の場合、`SbieDll!Ldr_LoadInjectDlls` のみを呼び出します。通常モードでは、このローダーはアーキテクチャ固有の [InjectDll](InjectDll.md)、[InjectDll64](InjectDll64.md)、または `InjectDllARM64` 構成を選択し、ホスト モードでは `HostInjectDll`、`HostInjectDll64`、または `HostInjectDllARM64` を選択します。ホスト プロセスのセマンティクスについては、[ホスト インジェクション](HostInjection.md)を参照してください。
