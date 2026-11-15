# Border Color

_BorderColor_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックスごとの設定です。SandMan が該当するサンドボックス化されたウィンドウの周囲に表示する色付き境界線とオプションのサンドボックス名ラベルを制御します。境界線は視覚的なインジケーターにすぎません。アプリケーション ウィンドウのサイズ変更や再配置を行ったり、サンドボックスの分離を変更したりしません。

## 構文

現在の形式は次のとおりです:

```ini
BorderColor=#hex_color_code,border_mode,border_width,border_color_alpha,label_mode[,label_font_size]
```

例:

```ini
[DefaultBox]
BorderColor=#00FFFF,ttl,6,192,in,6
```

色は #BBGGRR 順の 6 桁の 16 進数値として指定します。青、緑、次に赤です。

* ハッシュ記号は 6 桁の 16 進数の前に付けます。
* 最初の 2 桁は青の成分を指定します。
* 次の 2 桁は緑の成分を指定します。
* 最後の 2 桁は赤の成分を指定します。

残りのフィールドの意味は次のとおりです:

| フィールド | 値と動作 |
| --- | --- |
| `border_mode` | 境界線を表示するタイミングと場所を選択します。[境界線モード](#border-modes)を参照してください。 |
| `border_width` | 境界線の幅 (ピクセル)。現在の既定は `6` です。 |
| `border_color_alpha` | `0` から `255` までの境界線の不透明度。現在の既定および無効値のフォールバックは `192` です。 |
| `label_mode` | `no` はラベルを隠し、`out` は境界線の上に配置し、`in` は境界線の内側に配置します。 |
| `label_font_size` | ラベルのオプションの参照サイズ。省略または無効な場合、境界線の幅を使用します。 |

## 境界線モード {#border-modes}

SandMan は現在、主要なモードを次のように提示します:

| INI モード | SandMan ラベル | 動作 |
| --- | --- | --- |
| `off` | **Border disabled** | 境界線を表示しません。 |
| `ttl` | **Show only when title is in focus** | タイトル フォーカスの動作に従って境界線を表示します。 |
| `on` | **Always show (focused window only)** | フォーカスされた該当ウィンドウに境界線を表示します。 |
| `all` | **Show for all windows in this box** | サンドボックス内のすべての該当ウィンドウに境界線を表示します。 |

`ttloutside`、`onoutside`、および `alloutside` バリアントは対応するモードを使用しますが、アプリケーション フレームの外側に境界線を描画します。SandMan はこれらのエントリをセレクターで **(outside)** と識別します。

ランタイムは `ttllbl`、`onlbl`、および `alllbl` も受け入れます。これらのラベルのみの形式は、色付き境界線フレームなしでサンドボックス名またはエイリアスを表示します。ラベルのみのモードは非 outside 配置を使用します。そのモードでは `outside` サフィックスは保持されません。

## ラベルの配置

`label_mode` フィールドは次の SandMan の選択肢に対応します:

| INI 値 | SandMan ラベル |
| --- | --- |
| `no` | **Don't show in border** |
| `out` | **Show above the border** |
| `in` | **Show within the border** |

表示されるテキストは、[Box Alias](BoxAlias.md) で説明されているサンドボックス エイリアスおよびグローバル エイリアス表示設定の影響を受けることがあります。

## BorderInsideMaximized

_BorderInsideMaximized_ は、最大化または整列 (スナップ) されたウィンドウに対して、外側の境界線または外側配置のラベルをどのように配置するかを制御します。既定で有効です。

有効な場合、外側配置がアプリケーション フレームを超えて広がる場合に、SandMan はそのようなウィンドウの内側にオーバーレイを描画します。これは境界線オーバーレイの配置のみを変更し、アプリケーション ウィンドウのサイズや位置を変更しません。

自動の内側配置を無効にするには:

```ini
[DefaultBox]
BorderInsideMaximized=n
```

設定メタデータは _BorderInsideMaximized_ をバージョン 1.18.1 で追加されたものとして記載していますが、この機能は Sandboxie Plus 1.18.2 / Classic 5.73.2 のリリース ノートで説明されています。

## SandMan インターフェイス

現在のコントロールは次にあります:

**Sandbox Options > General Options > Box Options > Appearance**

この領域は、境界線モード、色、幅、不透明度、ラベル配置、ラベルのみのオプション、およびラベル サイズのコントロールを提供します。外側モードの場合、**Inside when maximized or snapped** が _BorderInsideMaximized_ を有効にします。そのツールチップは、モニターの端でクリップされる外側の境界線が、代わりに最大化またはスナップされたウィンドウの内側に描画されることを説明しています。

現在の Sandboxie Plus の境界線は SandMan のオーバーレイです。外観の変更は通常、サンドボックス化されたアプリケーションの再起動を必要としませんが、そのオーバーレイを表示するには SandMan が実行されている必要があります。

## Sandboxie Control Classic

Sandboxie Control Classic は、[Sandbox Settings > Appearance](AppearanceSettings.md) の下に確立された境界線コントロールを提供します。利用可能な Classic コントロールは、現在の SandMan のモードとオプションとは異なることがあります。特に、すべての新しい SandMan モードが歴史的な Classic インターフェイスによって公開されていると仮定しないでください。
