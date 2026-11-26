# Border Label Position

`BorderLabelPosition` controls the edge and position of the sandbox-name label
on the [Sandboxie Plus border](BorderColor.md). It is a per-sandbox setting
available since version 1.19.1. The label must be enabled in `BorderColor`.

## Usage

```ini
[DefaultBox]
BorderLabelPosition=left,50,rotated,adaptive-any
```

This places the label halfway along the left edge, with text reading from top to
bottom. The adaptive mode may choose another edge when the selected position
would be clipped. SandMan exposes these controls under **Sandbox Options >
General Options > Box Options > Appearance**.

## Syntax

```ini
BorderLabelPosition=placement,percent[,text_mode[,movement_mode]]
```

| Field | Values |
| --- | --- |
| `placement` | `top`, `bottom`, `left`, or `right`. |
| `percent` | Integer from `0` to `100`, measured along the usable travel after label size and frame margins. Top and bottom run left to right; left and right run top to bottom. |
| `text_mode` | `stacked`, `stacked-compact`, `rotated`, or `mirrored`; defaults to `stacked` when omitted. |
| `movement_mode` | `fixed`, `adaptive`, `adaptive-opposite`, or `adaptive-any`; defaults to `adaptive-any` when omitted. |

Missing or invalid values use `top,50,stacked,adaptive-any`. Existing two-field
values, such as `bottom,50`, remain valid.

## Side Label Text

Text on the top and bottom edges is horizontal. The text mode controls left and
right edges:

| Mode | Behavior |
| --- | --- |
| `stacked` | Upright characters arranged vertically. |
| `stacked-compact` | Upright characters with no extra row gap and one pixel of top and bottom padding; the font size is unchanged. |
| `rotated` | Text reads top to bottom; shown as **Rotated down** in SandMan. |
| `mirrored` | Text reads bottom to top; shown as **Rotated up** in SandMan. |

Stacked modes use vertical parentheses when supported by the font. Text that
does not fit is clipped rather than shrinking the font.

## Movement When Clipped

| Mode | Behavior |
| --- | --- |
| `fixed` | Does not use automatic label movement. |
| `adaptive` | Moves a clipped label inward on the selected edge. |
| `adaptive-opposite` | Tries the opposite edge first; if it also clips, falls back inward on the selected edge. |
| `adaptive-any` | Tries the selected edge, the opposite edge, then the remaining edges before falling back inward. It returns to the selected edge when it fits again. |

Among fitting remaining edges, `adaptive-any` chooses the one with more
clearance to the monitor boundary, using a stable tie order. Adaptive placement
uses the monitor work area when `BorderExcludeTaskbar` applies, and monitor
bounds otherwise; the existing topmost-window exception still applies. Fully
offscreen windows or insufficient visible space can prevent a fully visible
label.

The `BorderColor` label modes `in` and `out` apply relative to the chosen edge.
`BorderInsideMaximized` is independent and can still move an outside border and
label inside a maximized or snapped window, even with `fixed` movement. See
[Border Label Font](BorderLabelFont.md) for font selection.
