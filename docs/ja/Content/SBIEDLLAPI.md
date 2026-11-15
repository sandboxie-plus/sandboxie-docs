# SBIE DLL API

このページでは、_SbieDll.dll_ 動的リンク ライブラリ (DLL) 内の呼び出し可能なエントリポイントについて説明します。これらのエントリポイントは、Sandboxie の一部の機能をプログラムから、つまり Sandboxie と対話する人を通してではなく他のプログラムからアクセスできるように公開します。

Sandboxie をプログラムから使用するには 3 つの側面があります。

*   Start.exe プログラムを使用していくつかの機能を操作する。[Start コマンド ライン](StartCommandLine.md)を参照してください。
*   カスタム DLL をサンドボックス化されたプログラムにインジェクトする。[InjectDll](InjectDll.md) を参照してください。
*   実行中のプログラム (サンドボックス化されているかどうかを問わず) から Sandboxie のエントリポイントを呼び出す。ここで説明します。

ここで説明するエントリポイントは _SbieDll.dll_ によってエクスポートされます。呼び出し元のアーキテクチャに適した DLL を読み込み、`GetProcAddress` で正確なエクスポート名を解決してください。インストールされている DLL に一致する関数ポインター シグネチャを使用してください。引数の数と順序、スカラー型とポインター型、ポインター幅、および呼び出し規約がすべて重要です。これらの宣言は現在のソースを記述したものであり、任意のリリース間での ABI 保証ではありません。

x86 ビルドは `__stdcall` を使用します。その[エクスポート定義](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/SboxDll32.def)は、装飾された実装シンボルにマップされた、装飾されていない公開名を提供します。他のアーキテクチャはプラットフォーム ABI とコンパイラ エクスポートを使用します。それらに x86 の名前装飾を適用しないでください。現在の宣言は [sbieapi.h](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/sbieapi.h) と [sbiedll.h](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/sbiedll.h) にあります。

この検索フラグメントは、インジェクトされた DLL が提供する SbieDll ハンドルを使用します。アプリケーション固有のターゲット セットアップは省略されています。以下のフックの例は 4 引数の呼び出しを示しています。

```c
#include <windows.h>

typedef void *(__stdcall *P_SbieDll_Hook)(
    const char *name, void *source, void *detour, HMODULE module);

__declspec(dllexport) void __stdcall InjectDllMain(
    HINSTANCE hSbieDll, ULONG_PTR UnusedParameter)
{
    P_SbieDll_Hook p_SbieDll_Hook =
        (P_SbieDll_Hook)(ULONG_PTR)GetProcAddress(hSbieDll, "SbieDll_Hook");
    (void)UnusedParameter;
    if (!p_SbieDll_Hook)
        return;

    /* ターゲット、デトゥア、および関連するモジュールを解決した後:
       p_SbieDll_Hook(name, source, detour, module); */
}
```

読み込まれた SbieDll のインスタンスへのハンドルを取得するために _InjectDllMain_ ([Inject Dll](InjectDll.md) を参照) を使用していることに注意してください。これが推奨されるアプローチです。ただし、LoadLibrary または GetModuleHandle を使用して名前で SbieDll を検索することも問題ありません。

エクスポートを解決しても、すべての呼び出し元コンテキストで使用できることが確立されるわけではありません。ドライバー/サービスの可用性、承認、サンドボックス コンテキスト、および初期化要件は API ごとに異なります。各結果を確認してください。これらの API は普遍的な `GetLastError()` 契約を共有していません。例は、ARM64 または ARM64EC を含め、ランタイムまたは配布 DLL の互換性を保証するものではありません。

* * *

### サンドボックス名の列挙

*    プロトタイプ:
```
        typedef LONG (__stdcall *P_SbieApi_EnumBoxes)(
                LONG index,                 // -1 に初期化
                WCHAR *box_name);           // WCHAR [40] へのポインター
```

*    エクスポート名:
```
        SbieApi_EnumBoxes
```

*    パラメーター:
```
        index [in] は、どのサンドボックスを返すかを指定します。-1 に初期化します。
        対象となる構成済みサンドボックスは、読み込まれた構成セクションの
        順序で返され、永続的な物理 INI ファイルの順序契約ではありません。

        box_name [out] は、成功時に null 終端されたサンドボックス名を受け取ります。
        40 WCHAR 分のストレージを提供してください。無効または対象外の
        セクションは必ずしも返されません。

        注: これはサンドボックス化された呼び出し元のための一般的な
        ボックス名列挙子ではありません。基になる空セクション クエリは、
        構成セクションを列挙するのではなく、自身のボックスに解決されます。
```

*    戻り値:
```
        index パラメーターに使用する次の値を返します。
        列挙を停止するには -1 を返します。このセンチネルは、
        使い果たした場合と、基になるすべての構成クエリの失敗を
        区別しません。
```


*    サンプル コード:

```
        WCHAR name[40];
        LONG index = -1;
        while (1) {
                index = SbieApi_EnumBoxes(index, name);
                if (index == -1)
                    break;
                SandboxNames_StringArray.add(name); // アプリケーション固有の擬似コード
        }
```

* * *

### サンドボックス名によるサンドボックス パスのクエリ

*    プロトタイプ:
```
        typedef LONG (__stdcall *P_SbieApi_QueryBoxPath)(
                const WCHAR *box_name,      // パディングされた WCHAR [40] 入力
                WCHAR *file_path,
                WCHAR *key_path,
                WCHAR *ipc_path,
                ULONG *file_path_len,
                ULONG *key_path_len,
                ULONG *ipc_path_len);
```

*    エクスポート名:
```
        SbieApi_QueryBoxPath
```

*    パラメーター:
```
        box_name [in] は、サンドボックス化されていない呼び出し元のために
        パス情報を構築する対象のサンドボックス名を指定します。パディングされた
        WCHAR [40] バッファーに明示的な名前を指定してください。サンドボックス化された
        呼び出し元は、この引数に関係なく既存のボックスを使用します。NULL は
        普遍的に有効な現在のボックス セレクターではありません。

        file_path [out] は、FileRootPath 設定で設定された、
        サンドボックスのルート ディレクトリへのパスを受け取ります。
        バッファーは、file_path_len パラメーターで指定された
        バイト数まで受け取ります。このパラメーターを無視するには
        NULL を渡します。

        key_path [out] は、KeyRootPath 設定で設定された、
        サンドボックス レジストリのルート キーへのパスを受け取ります。
        バッファーは、key_path_len パラメーターで指定された
        バイト数まで受け取ります。このパラメーターを無視するには
        NULL を渡します。

        ipc_path [out] は、IpcRootPath 設定で設定された、
        サンドボックスのルート オブジェクト ディレクトリへのパスを
        受け取ります。バッファーは、ipc_path_len パラメーターで指定された
        バイト数まで受け取ります。このパラメーターを無視するには
        NULL を渡します。

        file_path_len [in/out] は、file_path バッファーの
        バイト単位の長さを指定します。戻り時に、完全なバッファーを
        受け取るために必要なバイト単位の長さを受け取ります。

        key_path_len [in/out] は、key_path バッファーの
        バイト単位の長さを指定します。戻り時に、完全なバッファーを
        受け取るために必要なバイト単位の長さを受け取ります。

        ipc_path_len [in/out] は、ipc_path バッファーの
        バイト単位の長さを指定します。戻り時に、完全なバッファーを
        受け取るために必要なバイト単位の長さを受け取ります。

        必要な長さには null 終端が含まれます。指定された各出力バッファーには、
        対応する長さポインターが必要です。出力を省略した場合、その長さ
        ポインターで必要なサイズを要求できます。そのパスが不要な場合は
        両方とも NULL にできます。

        出力容量は USHORT (16 ビット バイト) フィールドを通過します。
        パスは展開されたネイティブ ファイルシステム、レジストリ、および
        オブジェクト パスであり、必ずしも DOS パスや INI 設定の
        リテラル テキストではありません。
```

*    戻り値:
```
        成功時はゼロ、エラー時は非ゼロ値を返します。
```

[パス クエリ コンシューマー](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/process_api.c#L601-L755)は、文字列をコピーする前に必要な長さを書き込みます。不十分なバッファーは失敗します。呼び出しが成功しない限り、出力文字列を使用しないでください。

*    サンプル コード:

このヘルパーは、`query` が上記のプロトタイプで解決されたことを前提としています。`DefaultBox` を意図した構成済みボックスに置き換えてください。すべてのインストールにその名前があるわけではありません。成功時には、呼び出し元が 3 つの割り当てすべてを所有し、それらを `free` する必要があります。呼び出し間で構成が変更される可能性があるため、失敗した場合はサイズ クエリを繰り返す必要があるかもしれません。

```c
#include <windows.h>
#include <stdlib.h>
#include <limits.h>

LONG ReadBoxPaths(P_SbieApi_QueryBoxPath query,
                  WCHAR **file, WCHAR **key, WCHAR **ipc)
{
    WCHAR box[40] = L"DefaultBox";
    ULONG FileLen = 0, KeyLen = 0, IpcLen = 0;
    WCHAR *FileBuf = NULL, *KeyBuf = NULL, *IpcBuf = NULL;
    LONG status;

    if (!query || !file || !key || !ipc)
        return (LONG)0xC000000DL; /* STATUS_INVALID_PARAMETER */
    *file = NULL; *key = NULL; *ipc = NULL;

    status = query(box, NULL, NULL, NULL, &FileLen, &KeyLen, &IpcLen);
    if (status != 0)
        return status;
    if (FileLen < sizeof(WCHAR) || KeyLen < sizeof(WCHAR) ||
        IpcLen < sizeof(WCHAR) || FileLen > USHRT_MAX ||
        KeyLen > USHRT_MAX || IpcLen > USHRT_MAX ||
        FileLen % sizeof(WCHAR) || KeyLen % sizeof(WCHAR) ||
        IpcLen % sizeof(WCHAR))
        return (LONG)0xC000000DL;

    FileBuf = (WCHAR *)malloc(FileLen);
    KeyBuf = (WCHAR *)malloc(KeyLen);
    IpcBuf = (WCHAR *)malloc(IpcLen);
    if (!FileBuf || !KeyBuf || !IpcBuf) {
        status = (LONG)0xC0000017L; /* STATUS_NO_MEMORY */
        goto fail;
    }
    status = query(box, FileBuf, KeyBuf, IpcBuf, &FileLen, &KeyLen, &IpcLen);
    if (status != 0)
        goto fail;
    *file = FileBuf; *key = KeyBuf; *ipc = IpcBuf;
    return 0;

fail:
    free(FileBuf); free(KeyBuf); free(IpcBuf);
    return status;
}
```

文字数が必要な場合は、成功した出力に対して `wcslen` を使用してください。それらのカウントは、API 呼び出しに使用されるバイト容量とは別にしてください。

* * *

### プロセス ID によるサンドボックス パスのクエリ

*    プロトタイプ:
```
        typedef LONG (__stdcall *P_SbieApi_QueryProcessPath)(
                HANDLE process_id,
                WCHAR *file_path,
                WCHAR *key_path,
                WCHAR *ipc_path,
                ULONG *file_path_len,
                ULONG *key_path_len,
                ULONG *ipc_path_len);
```

*    エクスポート名:
```
        SbieApi_QueryProcessPath
```

*    パラメーター:
```
        process_id [in] は、クエリするサンドボックス化されたプロセスの ID を
        指定します。開かれたプロセス ハンドルではありません。数値 PID を
        (HANDLE)(ULONG_PTR)pid を使用して変換します。サンドボックス化されていない
        呼び出し元は、追跡されているサンドボックス化された PID を明示的に
        指定する必要があります。サンドボックス化された呼び出し元は、現在の
        プロセスに NULL または (HANDLE)(LONG_PTR)-1 を使用できます。

        file_path [out]

        key_path [out]

        ipc_path [out]

        file_path_len [in/out]

        key_path_len [in/out]

        ipc_path_len [in/out]

        最後の 6 つのパラメーターは、上記で説明した QueryBoxPath 関数の
        最後の 6 つのパラメーターと似ています。ただし、QueryProcessPath
        (この関数) は、実行中のプログラムで使用されているサンドボックス
        パスを返します。サンドボックス化されていない QueryBoxPath 呼び出し元は
        代わりに、現在読み込まれている構成とその ID/セッションからパスを
        構築します。

        別の言い方をすれば: サンドボックス化されたプログラムが PID 124 で
        開始され、その後、あるサンドボックス パス (たとえば FileRootPath) が
        新しい値に設定され、構成が再読み込みされたとします。
        サンドボックス化されていない名前付きボックスの QueryBoxPath 呼び出しは、
        新しい構成済みパスを返すことができますが、PID 124 の QueryProcessPath は
        その既存のパスを返します。サンドボックス化された QueryBoxPath 呼び出し元は
        依然として自身の既存のボックスを使用します。
```

*    戻り値:
```
        成功時はゼロ、エラー時は非ゼロ値を返します。
```

[プロセス パス コンシューマー](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/process_api.c#L653-L698)は、存在しない、サンドボックス化されていない、または終了したターゲットに対して `STATUS_INVALID_CID` で失敗する可能性があります。列挙を通じて取得された PID は、プロセスの有効期間を保証するものではありません。

* * *

### 実行中のプロセスの列挙

*    プロトタイプ:
```
        typedef LONG (__stdcall *P_SbieApi_EnumProcessEx)(
                const WCHAR *box_name,      // パディングされた WCHAR [40] 入力、または NULL
                BOOLEAN all_sessions,
                ULONG which_session,
                ULONG *boxed_pids,         // ULONG [] へのポインター
                ULONG *boxed_count);
```

*    エクスポート名:
```
        SbieApi_EnumProcessEx
```

*    パラメーター:
```
        box_name [in] は、プロセスが列挙されるサンドボックスの名前を
        指定します。サンドボックス化されていない呼び出し元は、すべての
        ボックスに対して NULL または空の名前を指定できます。サンドボックス化
        された呼び出し元は、指定された名前に関係なく自身のボックスに
        制限されます。

        all_sessions [in] は、すべてのログオン セッションでプロセスを
        列挙する場合は TRUE、特定のログオン セッションの場合は FALSE を
        指定します。

        which_session [in] は、プロセスが列挙されるログオン セッション
        番号を指定します。all_sessions が TRUE の場合は無視されます。
        現在のログオン セッションを指定するには (ULONG)-1 を渡します。
        これらのセッション引数は、呼び出し元が自身のボックスに制限されて
        いる場合でも適用されます。

        boxed_pids [out] は、プロセス ID (PID) 番号を受け取ります。
        そのレイアウトは、以下に示すように boxed_count に依存します。

        boxed_count [in/out] は、PID 配列とともに指定された場合、
        配列の容量を ULONG 要素で指定し、書き込まれた PID の数を
        受け取ります。PID 配列が NULL の場合はカウントのみを要求します。
```

| モード | 必要な入力 | 出力レイアウト |
|---|---|---|
| `boxed_count == NULL` | 固定の `ULONG pids[512]` | `pids[0]` はカウント、PID は `pids[1]` から始まり、最大 511 個の PID |
| カウント ポインターと PID 配列を指定 | 初期の `*boxed_count` は配列容量 | PID は `pids[0]` から始まり、返される `*boxed_count` は書き込まれた数 |
| カウント ポインターを指定、PID 配列は `NULL` | 書き込み可能なカウント出力 | カウントのみ。後続のリスト結果と等しいことは保証されません |

[ドライバー列挙](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/process_api.c#L983-L1127)は、容量を使い果たした後に成功を返すことがあります。成功はリストが完全であることを証明しません。カウントのみのパスと PID リストのパスは異なり、呼び出し間でプロセスが開始または終了する可能性があります。両方の出力ポインターも指定しないのは無効です。

`SbieApi_EnumProcess(box, pids)` は、レガシー レイアウトを使用して `SbieApi_EnumProcessEx(box, FALSE, -1, pids, NULL)` をラップするヘッダー マクロです。`GetProcAddress` で解決する別個のエクスポートではありません。

*    戻り値:
```
       成功時はゼロ、エラー時は非ゼロ値を返します。
```

* * *

### プロセス情報のクエリ

*    プロトタイプ:
```
        typedef LONG (__stdcall *P_SbieApi_QueryProcess)(
                HANDLE process_id,
                WCHAR *box_name,            // WCHAR [40] へのポインター
                WCHAR *image_name,          // WCHAR [96] へのポインター
                WCHAR *sid_string,          // WCHAR [96] へのポインター
                ULONG *session_id);
```

*    エクスポート名:
```
        SbieApi_QueryProcess
```


*    パラメーター:
```
        process_id [in] は、(HANDLE)(ULONG_PTR)pid として表現される PID で、
        開かれたプロセス ハンドルではありません。サンドボックス化されて
        いない呼び出し元は、明示的なターゲットを指定する必要があります。
        サンドボックス化された呼び出し元は、現在のプロセスに NULL または
        (HANDLE)(LONG_PTR)-1 を使用できます。

        box_name [out] は、プロセスが実行されているサンドボックスの名前を
        受け取ります。このパラメーターを無視するには NULL を渡します。

        image_name [out] は、完全なパスではなくプロセス イメージ名を
        受け取ります。96 WCHAR を提供するか、このパラメーターを無視するには
        NULL を渡します。長いイメージ名は、この固定バッファーに収まるのでは
        なく失敗する可能性があります。新しい QueryProcessEx バリアントは、
        明示的なイメージ バッファー容量を許可しています。

        sid_string [out] は、プロセスの SID 文字列を受け取ります。
        このパラメーターを無視するには NULL を渡します。

        session_id [out] は、プロセスが実行されているログオン セッション
        番号を受け取ります。このパラメーターを無視するには NULL を渡します。

        正常にコピーされた文字列には null 終端が含まれます。ボックス名と
        SID 出力にはそれぞれ 40 と 96 WCHAR が必要です。
```


*    戻り値:
```
        成功時はゼロ、エラー時は非ゼロ値を返します。
```


[プロセス クエリ](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/process_api.c#L208-L319)は、存在しない、サンドボックス化されていない、または終了した PID (列挙後に消えたプロセスを含む) に対して失敗する可能性があります。通常の失敗時には、DLL は要求された文字列をクリアし、指定されたセッション出力をゼロにリセットします。

* * *

### 単一のサンドボックス化されたプロセスの終了

*    プロトタイプ:
```
        typedef BOOLEAN (__stdcall *P_SbieDll_KillOne)(
                ULONG process_id);
```


*    エクスポート名:
```
        SbieDll_KillOne
```


*    パラメーター:
```
        process_id [in] は、終了させるサンドボックス化されたプロセスの
        プロセス ID を 32 ビット ULONG として指定します。
```


*    戻り値:
```
        成功時は TRUE、失敗時は FALSE を返します。

        DLL は SbieSvc を通じて終了を要求します。TRUE は成功した
        サービス応答を表し、完了したプロセス終了待機ではありません。
```

[サービス ハンドラー](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/ProcessServer.cpp#L129-L239)は、追跡されているサンドボックス化されたターゲットを必要とします。クロスセッション要求には管理者承認が必要で、サンドボックス化された呼び出し元はこのハンドラーを通じて別のボックスをターゲットにできません。存在しない、またはすでに終了したターゲットは失敗する可能性があります。特定の終了コードや統一された `GetLastError()` 結果は約束されません。


* * *

### すべてのサンドボックス化されたプロセスの終了

*    プロトタイプ:
```
        typedef BOOLEAN (__stdcall *P_SbieDll_KillAll)(
                ULONG session_id,
                const WCHAR *box_name);
```


*    エクスポート名:
```
        SbieDll_KillAll
```


*    パラメーター:
```
        session_id [in] は、サンドボックス化されたプログラムを終了させる
        ログオン セッション番号を指定します。呼び出し元の現在のセッションには
        (ULONG)-1 を指定します。明示的に異なるセッションを指定する場合は
        管理者承認の対象となります。

        box_name [in] は、サンドボックス化されたプログラムを終了させる
        サンドボックス名を指定します。NULL は呼び出し元の初期化された
        SbieDll ボックス名を使用します。すべてのボックスを意味するものでは
        ありません。空の名前はサービスによって拒否されます。サンドボックス化
        された呼び出し元は自身のボックスに制限されます。
```


*    戻り値:
```
        成功時は TRUE、失敗時は FALSE を返します。

        サービスは一致するプロセスを繰り返し列挙して終了を試みます。
        TRUE はその応答を反映するものであり、すべてのプロセスがすでに
        終了したこと、または新しいプロセスが現れないことを保証するものでは
        ありません。
```

これは具体的なボックス/セッション要求であり、普遍的な全ボックス/全セッション操作ではありません。より高レベルの全ボックス呼び出し元はボックスを反復します。[サービス実装](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/ProcessServer.cpp#L248-L374)を参照してください。


* * *

### Sandboxie.ini からの構成のクエリ

*    プロトタイプ:
```
        typedef LONG (__stdcall *P_SbieApi_QueryConf)(
                const WCHAR *section_name,  // 最大 64 文字
                const WCHAR *setting_name,  // WCHAR [66] へのポインター
                ULONG setting_index,
                WCHAR *value,
                ULONG value_len);
```


*    エクスポート名:
```
        SbieApi_QueryConf
```


*    パラメーター:
```
        section_name [in] は、クエリする設定を含むセクション名を
        指定します。空または NULL のセクションは、サンドボックス内では
        呼び出し元のボックスに解決されます。サンドボックス外では、
        名前付き設定を持つ空のセクションは GlobalSettings をクエリします。

        setting_name [in] は、クエリする設定名を指定します。名前付き
        セクションを持つ空の設定は設定名を列挙します。サンドボックス外では、
        両方の名前が空の場合にセクション名を列挙します。

        setting_index [in] は、複数回出現する可能性のある設定のための
        ゼロベースのインデックス番号を指定します。下位 24 ビットが
        インデックスを保持します。インデックス番号は、これらの特別な値と
        論理 OR できます:

            0x40000000 (CONF_GET_NO_GLOBAL) - GlobalSettings
            フォールバックを抑制します。

            0x20000000 (CONF_GET_NO_EXPAND) - 変数を展開しません。

            0x10000000 (CONF_GET_NO_TEMPLS) - テンプレート由来の
            設定を無視します。

        value [out] は、成功時に null 終端された値を受け取ります。
        書き込み可能なストレージを提供してください。NULL はサイズ クエリ
        メカニズムを提供しません。

        value_len [in] は、value が指すバッファーの最大長をバイト単位で
        指定します。終端スペースを含みます。これは USHORT 容量フィールドを
        通過します。不十分なストレージは、必要なサイズを返すのではなく
        失敗します。
```

これはドライバーの読み込まれた構成をクエリします。該当するテンプレート値とグローバル フォールバックは、抑制されない限り参加できます。変数展開は、呼び出し元のサンドボックス コンテキスト、またはサンドボックス外ではその ID/セッションと要求されたセクションを使用します。`SbieApi_QueryConfAsIs` は展開のみを抑制するヘッダー ラッパーであり、本質的にテンプレートやグローバル フォールバックを無効にするものではありません。[構成コンシューマー](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/conf.c#L1824-L1968)を参照してください。


*    戻り値:
```
        成功時はゼロを返します。設定が見つからなかった場合は
        0xC000008B を返します。その他の戻り値は他のエラーを
        示します。
```


* * *

### Sandboxie.ini の構成の更新

*    プロトタイプ:
```
        typedef ULONG (__stdcall *P_SbieDll_UpdateConf)(
                WCHAR operation_code,
                const WCHAR *password,
                const WCHAR *section_name,
                const WCHAR *setting_name,
                const WCHAR *value);
```


*    エクスポート名:
```
        SbieDll_UpdateConf
```


*    パラメーター:
```
        operation_code [in] は、要求された設定を更新する方法を指定します:
        's' は設定 (上書き) し、既存の値を置き換えます
        'a' は値のリストの最下部に新しい値を追加します
            (まだ値がない場合は単に新しい値を設定します)
        'i' は値のリストの最上部に新しい値を挿入します
            (まだ値がない場合は単に新しい値を設定します)
        'd' は値のリスト内の既存の値を削除します

        password [in] は、必要な場合に使用するパスワードを指定します。
        それ以外の場合は NULL または空の文字列を指定します。

        section_name [in] は必須パラメーターで、設定する設定を含む
        セクション名を指定します。空の文字列は GlobalSettings を選択します。
        NULL は無効です。

        setting_name [in] は必須パラメーターで、設定する設定名を
        指定します。

        value [in] は、新しい値を指定するオプション パラメーターです。

        's' または 'd' では、NULL または空の値は、名前付き設定の
        すべての出現を削除します。setting_name が L"*" の場合、
        その組み合わせはセクション全体を削除します。'a' または 'i' では、
        NULL または空の値は何も追加しません。

        password、section、および setting の文字列は、終端を除いて
        64 WCHAR 文字以内に保ってください。呼び出し元が安全な長さを
        確保する必要があります。過大な入力の拒否に依存しないでください。
        値は構成行と要求サイズの制約にも収まる必要があります。
```


*    戻り値:
```
        成功時はゼロ、エラー時は非ゼロ ステータスを返します。
```

これはサービス ベースの INI 更新プログラムです。サンドボックス化された呼び出し元は拒否されます。該当する管理者/パスワード制限はサービスによって確認されます。受け入れられた変更は保存と構成の更新を要求しますが、これはアトミックなトランザクションではありません。失敗は状態が変更されていないことを保証せず、ゼロの結果はすべてのディスク書き込みまたは実行中のコンシューマーの更新を独立して確認したものとして扱ってはなりません。[DLL 要求](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/callsvc.c#L873-L934)と[サービスの保存/再読み込みワークフロー](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/sbieiniserver.cpp#L1276-L1384)を参照してください。

[サービスの変更ハンドラー](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/svc/sbieiniserver.cpp#L1036-L1103)は、1 つの空でない値の削除と、すべての出現またはセクションの削除を区別します。構成を更新する前に、NULL 引数と空引数を慎重に確認してください。

これを `SbieApi_UpdateConf` と混同しないでください。その別個の 4 引数ドライバー メモリ更新プログラムは、この INI 永続化ワークフローなしで、数値操作と異なる承認を使用します。その現在のラッパーは有効な値文字列を必要とし、DLL 更新プログラムの NULL 値の動作はそれには適用されません。


* * *

### Sandboxie.ini からの構成の再読み込み

*    プロトタイプ:
```
        typedef LONG (__stdcall *P_SbieApi_ReloadConf)(
                ULONG session_id,
                ULONG flags);
```


*    エクスポート名:
```
        SbieApi_ReloadConf
```


*    パラメーター:
```
        session_id [in] は、Sandboxie がエラー メッセージを記録する
        ログオン セッション番号を指定します。現在のセッションには
        (ULONG)-1 を渡します。これは独立したセッションごとの構成を
        選択するものではありません。

        flags [in] は操作を選択します:
        0 - 通常の構成再読み込み。
        SBIE_CONF_FLAG_RECONFIGURE (0x1) - 選択されたドライバー
            再構成動作も評価します。
        SBIE_CONF_FLAG_RELOAD_CERT (0x80000000) - 証明書検証。
            これは通常の INI 再読み込みではなく、別個の早期分岐を
            取ります。他のフラグと組み合わせた場合も同様です。
```


*    戻り値:
```
        成功時はゼロ、エラー時は非ゼロ値を返します。
```


サンドボックス化された呼び出し元は `STATUS_NOT_IMPLEMENTED` を受け取ります。INI ファイルが見つからない場合は、ドライバーの構成をリセットして成功を返すことがあります。通常の再読み込みはドライバー構成を更新してサービスに通知しますが、既存のプロセス/ボックス オブジェクトを普遍的に再構築したり、プロセス ローカル キャッシュを更新したり、フックを再インストールしたりしません。即時更新または普遍的な再起動要件のいずれかを前提とするのではなく、各設定のライフサイクルを参照してください。[再読み込みコンシューマー](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/drv/conf.c#L1696-L1815)を参照してください。

以前に解決された関数ポインターの場合、例示的な通常の再読み込みは次のとおりです。

```c
LONG status = p_SbieApi_ReloadConf((ULONG)-1, 0);
if (status != 0) {
    /* 返されたステータスを処理します。 */
}
```

* * *

### ユーザー モード エントリポイントのフック

*    プロトタイプ:
```
        typedef void *(__stdcall *P_SbieDll_Hook)(
                const char *name,
                void *source_func,
                void *detour_func,
                HMODULE module);
```


*    エクスポート名:
```
        SbieDll_Hook
```


*    パラメーター:
```
        name [in] は、フックするエントリポイントを命名する ASCII 文字列を
        指定します。診断とスキップ フックのマッチングに使用されます。

        source_func [in] は、フックする関数へのポインターです。

        detour_func [in] は、フック コードへのポインターです。

        module [in] は、関連するモジュール ハンドルで、トレースと
        モジュール関連のフック/リソース管理に使用されます。未使用では
        ありません。

        インストールされると、デトゥアはフックされたエントリポイントを
        通じた呼び出しを傍受します。フック インストールは、すべての
        Windows エントリポイント、呼び出し元コンテキスト、命令シーケンス、
        またはアーキテクチャで保証されるわけではありません。
```


*    戻り値:
```
        デトゥア関数がソース関数を呼び出すために使用できる関数
        ポインター、または失敗時は NULL を返します。スキップ フック
        パスは source_func を変更せずに返すため、非 NULL の結果は
        デトゥアがインストールされたことを普遍的に証明するものでは
        ありません。
```

フックが使用されている間は、デトゥア コードと関連モジュールを生かしておいてください。Sandboxie はモジュール関連のトランポリン リソースを管理します。それらを手動で解放したり、モジュール/リソースの有効期間後に使用したりしないでください。[フック実装](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/dllhook.c#L1308-L1472)と[モジュール クリーンアップ](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/dllhook.c#L1577-L1613)を参照してください。


*    サンプル コード:

これは上記の `P_SbieDll_Hook` と、すでに読み込まれた SbieDll ハンドルを使用します。ドライブ プレフィックスのテストは例示的なものであり、完全なファイルシステム セキュリティ ポリシーではありません。アプリケーションは適切な初期化コンテキストを準備し、フック セットアップ中の同時呼び出しを制御する必要があります。

```c
#include <windows.h>

typedef BOOL (__stdcall *P_DeleteFileW)(const WCHAR *Path);
static P_DeleteFileW pDeleteFileW = NULL;

BOOL __stdcall MyDeleteFileW(const WCHAR *Path)
{
    if (!pDeleteFileW) {
        SetLastError(ERROR_INVALID_FUNCTION);
        return FALSE;
    }
    if (Path && (Path[0] == L'C' || Path[0] == L'c') && Path[1] == L':') {
        SetLastError(0);
        return TRUE; /* このつづりだけの例示的な抑止。 */
    }
    return pDeleteFileW(Path);
}

BOOL InstallDeleteFileHook(HMODULE hSbieDll)
{
    HMODULE module = GetModuleHandleW(L"kernel32.dll");
    P_SbieDll_Hook hook;
    void *source, *original;
    if (!hSbieDll || !module)
        return FALSE;
    hook = (P_SbieDll_Hook)(ULONG_PTR)GetProcAddress(hSbieDll, "SbieDll_Hook");
    source = (void *)(ULONG_PTR)GetProcAddress(module, "DeleteFileW");
    if (!hook || !source)
        return FALSE;
    original = hook("DeleteFileW", source, (void *)(ULONG_PTR)MyDeleteFileW, module);
    if (!original)
        return FALSE;
    pDeleteFileW = (P_DeleteFileW)(ULONG_PTR)original;
    return TRUE; /* スキップ フックの結果はデトゥアがアクティブであることを意味しません。 */
}
```


* * *

### DLL 読み込み/アンロード コールバックの登録

*    プロトタイプ:
```
       typedef BOOLEAN (__stdcall *P_SbieDll_RegisterDllCallback)(
               void *Callback);
```

レガシーの Vista 以降のディスパッチャーはこのコールバック形状を使用します。歴史的な XP ディスパッチャーは代わりに最初の引数に `const WCHAR *` を使用します:

```
       typedef void (__stdcall *P_DllCallback)(
               const UCHAR *ImageName,
               HMODULE ImageBase,
               BOOL LoadState);
```


*    エクスポート名:
```
       SbieDll_RegisterDllCallback

       歴史的なドキュメントは Sandboxie 3.46 を最初の可用性として
       特定しています。その帰属は現在の提供を保証するものでは
       ありません。
```


*    パラメーター:
```
       Callback は、レガシー ディスパッチャーのためのプロセス ローカル
       コールバックを指定します。適切な Sandboxie ローダー初期化が
       必要です。サンドボックス化されていないプログラムで単に SbieDll を
       読み込むことは同等ではありません。登録解除 API は確立されて
       いません。コールバック コードを生かしておいてください。
```

```
       コールバック関数への ImageName (最初の) パラメーターは、
       レガシーの Vista 以降のディスパッチャーのための ANSI DLL
       ベース名を指定します。完全なパスではありません。XP は
       ワイド文字名を使用しました。名前はコールバックの間、
       借用データとして扱ってください。
```

```
       コールバック関数への ImageBase (2 番目) パラメーターは、
       モジュール ベースを指定します。レガシーのアンロード通知は
       古いモジュール ベースを保持します。ゼロをイベント判別子として
       使用しないでください。

       LoadState (3 番目) は読み込みで TRUE、アンロードで FALSE です。
```


*    戻り値:
```
       成功時は TRUE、コールバックを登録できない場合は FALSE を
       返します。登録は既に読み込まれたモジュールを再生しません。
       容量は限られています: 現在の 8 スロット テーブルには
       Sandboxie 自身のコールバックが含まれ、重複登録は追加の
       スロットを消費します。
```

Windows 8.1 以降では、現在のローダー通知パスは通常、このレガシー登録テーブルを通じてディスパッチしません。したがって、登録の成功は、最新の Windows での DLL イベント通知を保証しません。これを普遍的なローダー通知機能として扱わないでください。[ローダー初期化](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/ldr.c#L387-L475)、[登録とレガシー ディスパッチ](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/ldr.c#L535-L608)、および[最新の通知処理](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/ldr.c#L283-L295)を参照してください。


* * *

### Sandboxie ホーム フォルダーの取得

*    プロトタイプ:
```
       typedef LONG (__stdcall *P_SbieApi_GetHomePath)(
               WCHAR *NtPath,
               ULONG NtPathMaxLen,
               WCHAR *DosPath,
               ULONG DosPathMaxLen);
```


*    エクスポート名:
```
       SbieApi_GetHomePath

       歴史的なドキュメントは Sandboxie 3.52 を最初の可用性として
       特定しています。
```


*    パラメーター:
```
       NtPath は、NT パス構文で Sandboxie インストール フォルダーの
       完全なパスを受け取るバッファーへのポインターを指定します。

       NtPathMaxLen は、バイトではなく、null 終端のスペースを含む
       WCHAR 要素単位の容量を指定します。NT パスを受け取らない場合は
       NtPath に NULL、NtPathMaxLen にゼロを指定します。

       DosPath は、DOS パス構文で Sandboxie インストール フォルダーの
       完全なパスを受け取るバッファーへのポインターを指定します。

       DosPathMaxLen も同様に、WCHAR 要素単位の容量を指定します。
       DOS パスを受け取らない場合は DosPath に NULL、DosPathMaxLen に
       ゼロを指定します。
```


*    戻り値:
```
       成功時はゼロ、エラー時は非ゼロ値を返します。

       STATUS_BUFFER_TOO_SMALL (0xC0000023) は、NtPathMaxLen または
       DosPathMaxLen が小さすぎるバッファーを指定していることを
       示します。入力バッファーのサイズを増やして呼び出しを再試行して
       ください。
```

出力は独立して省略可能ですが、省略された出力は必要な長さを返しません。[ラッパー](https://github.com/sandboxie-plus/Sandboxie/blob/43b629be6c17628e6298befccfec279774895ba5/Sandboxie/core/dll/sbieapi.c#L484-L516)は WCHAR 容量を 16 ビット バイト フィールドを通じて変換します。任意の過大な最大値を指定しないでください。すべてのインストール パスが選択した固定配列に収まると仮定しないでください。
