# Write File Path

WriteFilePath は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。ボックス専用のファイル アクセスのパス パターンを指定します。ホスト側の内容は通常のファイル オープンから隠されますが、ファイルとフォルダーは対応するサンドボックスの場所に作成できます。

[Shell Folders](ShellFolders.md) を指定できます。[Program Name Prefix](ProgramNamePrefix.md) を指定できます。

例:
```
   .
   .
   .
   [DefaultBox]
   WriteFilePath=%Cookies%
```

この例は、サンドボックス内のプログラムが、サンドボックス外の Internet Explorer Cookies フォルダーにある既存の Cookie を通常開くことができないが、サンドボックス内の対応するフォルダーにファイルを作成できることを意味します。ホストの Cookie は通常のファイル オープンでは存在しないものとして扱われます。サンドボックス側の作成は依然として要求された操作とアクセス チェックに依存します。

WriteFilePath はファイル パスとフォルダー パスの両方の一致に適用されます。「Write Only」はサンドボックス化された内容の読み取りを禁止しません。既存のサンドボックス コピーは、操作と付与されたハンドル権限が許す場合に読み取り可能なままにできます。

ホストとサンドボックス コピーの両方のアクセスを閉じる [ClosedFilePath](ClosedFilePath.md) とは異なり、選択された WriteFilePath ルールは通常、ホスト側を閉じる一方でサンドボックス コピー側を許可します。

サンドボックス コピー アクセスを許可しても操作が成功することは保証されません。結果は、有効なルール、既存のサンドボックス コピーの状態、要求された操作とアクセス権、ファイルとフォルダーの作成条件、Windows のアクセス許可、および適用可能な仮想化と強制のパスによって異なります。

関連する [Sandboxie Control](SandboxieControl.md) 設定: [Sandbox Settings > Resource Access > File Access > Write-Only Access](ResourceAccessSettings.md#file-access-write-only-access)

関連する Sandboxie Plus 設定: Sandbox Options > Resource Access > Files > Add File/Folder > Access column > Box Only (Write Only)
