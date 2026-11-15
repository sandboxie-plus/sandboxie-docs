# Disable Custom Title Optimization

_DisableCustomTitleOpt_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定です。その名前にもかかわらず、アプリケーションのカスタム タイトル バーを無効にするものではありません。カスタムまたはクライアント描画のタイトル バーに対する Sandboxie の回避最適化を無効にします。

その実際の効果は、通常はスキップされるウィンドウに、Sandboxie が `[#]` またはサンドボックス名のタイトル マーカーを追加しようと試みるようにすることです。

```ini
[DefaultBox]
DisableCustomTitleOpt=y
```

この設定は、無効にしたり、プログラムに限定したりすることもできます:

```ini
DisableCustomTitleOpt=n
DisableCustomTitleOpt=program.exe,y
```

## 既定の動作

この設定が存在しないか `n` に設定されている場合、Sandboxie はジオメトリ ベースのヒューリスティックを使用して、カスタムまたはクライアント描画のタイトル バーの可能性が高いものを識別し、それらのタイトルの変更を回避します。Delphi VCL、Qt、Electron などのフレームワークで構築されたアプリケーションは、そのようなタイトル バーを使用する可能性のある例です。Sandboxie は、この決定のためにそれらのフレームワークを名前で識別しません。

`DisableCustomTitleOpt=y` の場合、Sandboxie はその回避チェックをスキップし、通常のタイトル マーカー処理を続行します。ウィンドウは他のタイトル適格性チェックを依然として通過する必要があるため、マーカーは保証されません。

## 互換性に関する考慮事項

この回避動作は、一部のカスタムまたはクライアント描画ウィンドウのタイトルを変更すると、過度のデスクトップ ウィンドウ マネージャーの再描画アクティビティと高い CPU 使用率を引き起こす可能性があるために導入されました。_DisableCustomTitleOpt_ を有効にすると、影響を受けるアプリケーションでその問題が再発する可能性がありますが、すべての VCL、Qt、Electron、またはその他のカスタム タイトル アプリケーションが影響を受けることを意味するものではありません。

この設定は Sandboxie のタイトル マーカーおよびタイトル変更パスのみを制御します。次は制御しません:

- 色付きのサンドボックス境界または境界オーバーレイ。
- ウィンドウ クラスの名前変更。
- トレイ アイコンの装飾。
- アプリケーション自体のカスタム タイトル バー。

[`BoxNameTitle`](BoxNameTitle.md) およびその他の独立したタイトル ルールは引き続き適用されます。

## 変更の適用

この設定は、プロセスがその GUI タイトル処理を初期化するときに読み取られます。変更後は影響を受けるアプリケーションを再起動してください。

この設定には、SandMan または Sandboxie Control Classic に専用のコントロールがありません。`Sandboxie.ini` で、または INI エディターを通じて手動で構成してください。

## バージョン履歴

- Sandboxie Plus 1.17.6 / Classic 5.72.6 は、過度の DWM 再描画アクティビティに対処するためにカスタム タイトル回避動作を導入しました。
- Sandboxie Plus 1.17.8 / Classic 5.72.8 は、オプトアウトとして _DisableCustomTitleOpt_ を追加しました。

## 関連する構成

- [Box Name Title](BoxNameTitle.md)
- [Sandboxie Ini](SandboxieIni.md)
