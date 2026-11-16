# Box Root Folder

**この設定は非推奨です。代わりに [FileRootPath](FileRootPath.md) を使用してください。**

_BoxRootFolder_ は [Sandboxie Ini](SandboxieIni.md) の従来の設定です。Sandboxie が `\Sandbox\<box name>` を追加してボックスのファイル ルートを導出する基準フォルダーを指定します。削除された設定ではなく、アクティブな互換性フォールバックのままです。

Sandboxie バージョン 3 以降では、[FileRootPath](FileRootPath.md) が推奨されます。ランタイムはまずボックスの有効な `FileRootPath` を検索し、存在しない場合にのみ `BoxRootFolder` を参照します。したがって、有効なグローバル `FileRootPath` はボックス ローカルの `BoxRootFolder` よりも優先されます。

以下の歴史的な例では `[GlobalSettings]` を使用していますが、現在のフォールバック検索はボックスの有効な構成を使用します。ボックス セクションまたは該当する有効なテンプレートも `BoxRootFolder` を提供できます。グローバル専用として強制されるものではありません。新しい構成には使用しないでください。

詳細については [Sandbox Hierarchy](SandboxHierarchy.md) を参照してください。

使用法:

```
   .
   .
   .
   [GlobalSettings]
   BoxRootFolder=C:\Sandbox
```

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox menu > Set Container Folder](SandboxMenu.md#set-container-folder)

Classic/従来のダイアログは構成を変更し、ボックスに既にファイルが含まれている場合に警告します。それ自体がそれらのファイルを移動するわけではありません。ファイルが存在するボックスでこのフォールバックを変更すると、既存のコンテンツが以前のルートの下に残ることがあります。[Sandbox Roots and Volume Layout](SandboxRootsVolumeLayout.md) を参照してください。
