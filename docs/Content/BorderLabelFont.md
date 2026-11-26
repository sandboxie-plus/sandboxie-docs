# Border Label Font

`BorderLabelFont` selects the font used for the sandbox-name label on the
[Sandboxie Plus border](BorderColor.md). It is a per-sandbox setting available
since version 1.19.1. An absent or empty value uses **Segoe UI Bold** and the
existing `BorderColor` label-size reference.

## Usage

```ini
[DefaultBox]
BorderLabelFont=Arial,bold,pt=12
```

The label must be enabled in `BorderColor` to be visible. SandMan also provides
font and label-size controls under **Sandbox Options > General Options > Box
Options > Appearance**. The font selector previews supported native fonts; its
Reset button clears the font override and restores legacy sizing.

## Syntax

```ini
BorderLabelFont=family[,weight][,italic][,underline][,strikeout][,style=name][,face=name][,native=family][,pt=points][,script=id]
```

| Field | Meaning |
| --- | --- |
| `family` | Font family. If omitted, Segoe UI is used. |
| `weight` | `thin`, `extralight`, `light`, `regular`, `medium`, `demibold`, `bold`, `extrabold`, or `black`. The default is bold. Use `weight=1` through `weight=1000` for other native weights. |
| `italic`, `underline`, `strikeout` | Optional formatting effects. |
| `style`, `face` | Native style name and full font face name. Named styles must resolve to the requested native outline face. |
| `native` | Native GDI family, when it differs from the Qt family. |
| `pt` | Explicit point size from `1` to `512`. Without it, the legacy `BorderColor` label-size reference is used. |
| `script` | Nonnegative writing-system filter ID remembered by the selector; `0` means Any. It does not set the label language, direction, or renderer charset. |

For example, a selection saved by SandMan may look like:

```ini
BorderLabelFont=Arial,bold,style=Bold,face=Arial Bold,pt=12.50,script=1
```

Native style metadata determines weight and italic for a named face; underline
and strikeout remain separate effects. If a saved face is unavailable or cannot
be used, SandMan reports a diagnostic and falls back to Segoe UI Bold.

## Font Names and Compatibility

Ordinary spaces, Unicode, and safe punctuation can remain readable. For keyed
name fields, encode percent signs, commas, control characters, and surrounding
whitespace as UTF-8 percent escapes. When the family needs escaping, use an
empty first field and the `family` key, for example:

```ini
BorderLabelFont=,bold,family=Example%2C Font
```

The `family` key overrides the first field. Older family and formatting-only
values remain valid; unknown old style tokens are ignored and the last weight
token wins. Duplicate or malformed recognized keyed fields are invalid.

See [Border Label Position](BorderLabelPosition.md) for label placement.
