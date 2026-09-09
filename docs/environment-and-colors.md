# Environment & Colors

## Fillers

Fillers are purely decorative ground-fill Environment objects (named `Filler_...`) used to dress
up empty grid space. They're the only Environment objects a Passenger Zone or another Environment
object is allowed to be placed on top of — see [Level Editor](level-editor.md#object-stacking-rules).

## Sea & Rocks

Sea and Rocks are level-wide environment extras rather than per-tile objects. Each can be set to
**None**, **Top Only**, **Bottom Only**, or **Both**, and the two are mutually exclusive per side —
placing one on a side clears the other from that same side automatically.

Levels authored before this placement system existed migrate automatically the first time their
grid is validated: their old on/off `enableSea` / `enableRocks` booleans map to the equivalent
single-side placement, one time only, so an existing level's appearance never silently changes.

## Color Palette Presets

See [Level Editor → Color Palette Presets](level-editor.md#color-palette-presets) for the authoring
workflow. At a glance:

- Presets live in one runtime-visible asset, `ColorPresetDatabase`
  (`Assets/Rail Express/Data/Colors/Color Preset Database.asset`), not the old Editor-only,
  EditorPrefs-backed system — this is what lets the game actually randomize colors at runtime, not
  just preview them in the Editor.
- Each preset stores a name, a list of colors, and an `isGoldRailPreset` flag.
- `LevelManager.ApplyRandomColorPreset` picks a random preset matching the level's Gold Rail status
  every time a level loads or retries, avoiding an immediate repeat of the last preset applied.
- Colors are applied via `_BaseColor` (URP) checked ahead of the legacy `_Color` property, never the
  `Material.color` shorthand — some shaders (e.g. the terrain shader) don't have a `_Color`
  property at all, and that shorthand throws if it's missing.
