# DisableForceRules

`DisableForceRules` は、そのボックスのすべての "force" ルールを無効にするボックスごとの設定です (v1.9.1 / 5.64.1 で導入)。設定すると、ドライバーはボックスで定義された `ForceFolder`、`ForceProcess`、および `ForceChildren` エントリの処理をスキップし、それらのルールに基づく自動サンドボックス強制を事実上防ぎます。

この設定は、ボックスを存在させたいが自動強制の決定に関与させたくない場合 (たとえば、手動実行または特殊な操作にのみボックスを使用する場合) に主に役立ちます。

## 構文

Sandboxie 構成のボックス セクションの下にこれを設定します:

```ini
[DefaultBox]

DisableForceRules=<y|n>
```

有効な値:

- `y` — 有効: ボックスの強制ルールは無視されます。
- `n` — 無効 (既定): 強制リストを構築するときにボックスの強制ルールが評価されます。

## 動作

- ドライバーが構成セクションを列挙してメモリ内の強制ルールを構築するとき、`Conf_IsBoxEnabled` を呼び出してから `DisableForceRules` をチェックします。ボックスに `DisableForceRules` が設定されている場合、そのボックスは強制ルール処理のためにスキップされ、その `ForceFolder`、`ForceProcess`、または `ForceChildren` エントリは使用されません。[^1]

- ボックスがまったく考慮されるかどうかに影響するその他の設定には、現在の SID/セッションに対するボックスの有効化が含まれます。現在のユーザー/セッションに対して有効でないボックスは、強制リストの作成中に考慮されません。[^2]

- `DisableForceRules` はボックスを削除したり、他の非強制動作を変更したりしません。ドライバーがそのボックスの強制エントリをランタイム強制リストに追加するのを防ぐだけです。[^3]

## 例

`NoAutoForce` という名前のボックスの強制ルールを無効にします:

```ini
[NoAutoForce]

DisableForceRules=y
```

強制ルールを有効のままにします (既定):

```ini
[MyBox]

DisableForceRules=n
```

## GUI (Sandboxie Manager / SandMan)

Sandboxie Manager (SandMan) UI の次のいずれかの場所で `Disable Force Rules` を切り替えます:

- コンテキスト メニュー -> Sandbox Presets -> Disable Force Rules
	- ボックス リスト内のサンドボックスを右クリックし、"Sandbox Presets" サブメニューを開き、"Disable Force Rules" 項目を切り替えます。
- ボックス オプション -> Force タブ
	- サンドボックスを右クリックし、"Sandbox Options" を選択し、"Program Control" タブの下の "Force Programs" に切り替え、"Disable forced Process and Folder for this sandbox" チェックボックスをオン/オフにしてから保存します。

これらの UI コントロールは `DisableForceRules` ボックス設定に直接マップされ、選択されたボックスに対してすぐに更新します。[^4][^5]

## 実装に関する注意 (ドライバーの動作)

- ドライバーは `Process_CreateForceData` を呼び出して、有効なボックスごとに `FORCE_BOX` エントリのメモリ内リストを構築します。作成中に構成セクションを反復処理し、`Conf_Get_Boolean(section, L"DisableForceRules", 0, FALSE)` が true を返すボックスをスキップします。[^1]

- `Process_CreateForceData` でボックスをスキップすると、その `ForceFolder`、`ForceProcess`、または `ForceChildren` リストは、`Process_GetForcedStartBox` および関連するチェックで使用されるランタイム `boxes` リストに追加されません。

## 参照

- [ForceProcess](ForceProcess.md) — 名前またはパスでプロセスを強制します。
- [ForceFolder](ForceFolder.md) — フォルダー パスまたはパターンでプロセスを強制します。
- [ForceChildren](ForceChildren.md) — 親ベースの強制ルール (一致する親の子が強制されます)。

## 脚注

[^1]: `Process_CreateForceData` がすべての構成セクションをループし、`if (Conf_Get_Boolean(section, L"DisableForceRules", 0, FALSE)) continue;` でこの設定が有効なボックスをスキップする方法を参照してください。

[^2]: Conf_IsBoxEnabled は、ボックスの強制リストが構築される前に、そのボックスが現在の SID/セッションに対してアクティブかどうかを判断するために使用されます。

[^3]: ドライバーは、プロセスを強制できるかどうかを判断するときに `AllowForceSystem` およびセッション ベースの強制無効フラグなどのグローバル/セッション レベルのフラグをチェックします。`DisableForceRules` は、強制リストへのボックスごとの包含にのみ影響します。

[^4]: プリセット メニューの切り替えは SandMan の `SbieView.cpp` (`m_pMenuPresetsForce`) に実装されており、`SetBoolSafe("DisableForceRules", ...)` を呼び出して設定を変更します。

[^5]: ボックス オプション ダイアログは `OptionsForce.cpp` のチェックボックス `ui.chkDisableForced` を読み書きし、オプションが保存されるときに `DisableForceRules` 設定を永続化します。
