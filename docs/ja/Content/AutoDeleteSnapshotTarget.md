# AutoDeleteSnapshotTarget

*AutoDeleteSnapshotTarget* は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、Sandboxie Plus 1.18.2 以降で利用できます。サンドボックスのコンテンツを自動削除した後、SandMan が戻る保持済みスナップショット状態を選択します。

この設定は自動削除を有効にするものではなく、選択されたスナップショットを削除するものでもありません。[Auto Delete](AutoDelete.md) が有効で、サンドボックスに保持されたスナップショットがある場合にのみ重要になります。

## 使用法

```ini
[DefaultBox]
AutoDelete=y
AutoDeleteSnapshotTarget=Current
```

有効な値は `Current` と `Default` です。`y` や `n` などのブール値は有効ではありません。

## 復元ターゲット

### Current

`AutoDeleteSnapshotTarget=Current` は、自動削除後にサンドボックスを現在アクティブなスナップショット状態に戻します。アクティブ状態は空のボックス状態である場合もあります。その状態より上で行われたライブ変更は破棄され、保存されたスナップショット ツリーは保持されます。

### Default

`AutoDeleteSnapshotTarget=Default` は、既定としてマークされたスナップショットにサンドボックスを戻します。既定のスナップショットが構成されていない場合は、空のボックス状態に戻ります。既定のスナップショットは削除されず、保存されたすべてのスナップショットは引き続き利用できます。

例:

```text
Empty state
└── Snapshot A (default)
    └── Snapshot B (active)
        └── live unsaved changes
```

`Current` の場合、ライブ変更は破棄され、スナップショット B がアクティブのままになります。スナップショット A と B は保存されたままです。`Default` の場合、ライブ変更は破棄され、スナップショット A がアクティブな既定状態になります。スナップショット B も保存されたままです。

> [!WARNING]
> 自動削除は、選択されたターゲット状態より上にあるライブ ファイルとレジストリの変更を完全に破棄します。保存されたスナップショット履歴は、すべてのスナップショットを削除することを別途選択しない限り保持されます。Quick Recovery は削除前に該当するファイルを復元する機会を提供できますが、データ損失に対する万能の保護ではありません。

## 既定値と無効な値

この設定が存在しないか無効な場合の単一の固定されたフォールバックはありません。通常の同期自動クリーンアップはアクティブ状態に戻り、非同期またはサイレント クリーンアップは既定状態に戻ります。`y` や `n` を含む無効な値は、同じコンテキスト依存の従来の動作を使用します。予測可能な動作が必要な場合は、`Current` または `Default` を明示的に構成してください。

## 自動削除と手動削除

この設定は SandMan の自動削除パスにのみ影響します。自動クリーンアップは、[Auto Delete](AutoDelete.md) によって制御され、最後のサンドボックス化されたプロセスが終了したときに引き続きトリガーされます。

手動の **Delete Contents** 操作は独自のスナップショット動作を使用し、現在の状態と既定の状態の選択にこの設定を使用しません。すべてのスナップショットを削除する明示的な要求もこの設定をバイパスし、保存されたスナップショット履歴を削除することがあります。

*AutoDeleteSnapshotTarget* は、スナップショットの作成または切り替え、既定のスナップショットの選択、個々のスナップショットの削除、またはスナップショットのマージを制御しません。スナップショット管理については [Box Snapshots](../PlusContent/BoxSnapshots.md) を参照してください。

## 復元の動作

自動削除の前に、Sandboxie の通常の復元処理が該当するファイルを復元する機会を提供することがあります。この設定は、復元フォルダー、ファイルの対象範囲、[Auto Recover](AutoRecover.md)、または [Quick Recovery](QuickRecovery.md) のフィルタリングを変更しません。削除後に使用される保持状態を選択するだけです。

## サンドボックス オプション

Sandboxie Plus では、**Sandbox Options > File Options > Box Delete options** を開きます。**Auto delete content changes when last sandboxed process terminates** を有効にし、**After automatic deletion, restore from snapshot:** でターゲットを選択します:

- **Active snapshot** は `AutoDeleteSnapshotTarget=Current` を書き込みます。
- **Default snapshot** は `AutoDeleteSnapshotTarget=Default` を書き込みます。

ターゲット コントロールは、自動削除が有効な場合に有効になり、既存のスナップショットを必要としません。ここで **Active snapshot** は空のアクティブ状態を表すことがあります。

## 変更の適用

SandMan は、自動削除が開始されるときにこの設定を読み取ります。したがって、保存された変更は次回の該当する自動削除に適用されます。SandMan の再起動、サンドボックス化されたアプリケーションの再起動、またはスナップショットの再作成は必要ありません。

## Sandboxie Plus と Classic

このスナップショット ターゲット オプションは、SandMan/Sandboxie Plus のスナップショット ワークフローに属します。Sandboxie Classic は異なる削除パスを使用し、この Sandbox Options の動作を提供しません。

## 失敗時の動作

選択されたターゲットが存在しなくなった場合、そのデータの復元に失敗した場合、またはコンテンツを削除できない場合、自動削除はエラーを報告することがあります。この操作はトランザクション ロールバックを約束するものではなく、自動またはサイレント クリーンアップ中のすべての失敗が対話型ダイアログを生成することが保証されているわけでもありません。

## バージョン履歴

Sandboxie Plus 1.18.2 で、自動クリーンアップ実装全体でターゲット選択を一貫させるために、明示的な `Current` および `Default` の選択肢が導入されました。

## 関連する構成

- [Auto Delete](AutoDelete.md)
- [Box Snapshots](../PlusContent/BoxSnapshots.md)
- [Quick Recovery](QuickRecovery.md)
- [Auto Recover](AutoRecover.md)
- [Sandboxie Ini](SandboxieIni.md)
