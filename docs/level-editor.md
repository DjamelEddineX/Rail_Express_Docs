# Level Editor

The Level Editor is a custom Editor window for building and editing levels tile by tile, without
touching the Game scene directly.

## Opening the Level Editor

Use the menu **Tools > FANNΞC > Rail Express > Level Editor**.

## How to add a level

1. Open the Level Editor and select the **Levels** tab.
2. Use the pagination bar at the bottom of the level list (`<<`  `<`  Page X / Y  `>`  `>>`) to
   find the page you want, or press **+** to create a new level (levels are paginated 35 per page
   to keep long lists browsable).
3. Select the level and set its **X** / **Y** grid size.
4. Pick an object from the palette, click a grid cell to place it, and click again to place another
   — click-drag paints continuously. Right-click rotates the object you're currently holding, or
   erases an existing object if you aren't holding anything.
5. Middle-click a Passenger Spawner Zone or Coin to open its settings, or a Color object to open
   its color wheel.
6. Press **Escape Key** to drop/deselect whatever you're currently holding.
7. Use **Control + Z** / **Control + Y** to undo/redo placement and erase actions.
8. Press **Test Level** to enter Play Mode directly on the selected level, skipping the Initializer.

All changes save automatically — a batched save runs on mouse-up rather than on every single
placement, so painting a long stretch of track doesn't stutter the editor.

## Object stacking rules

Placement is validated per grid cell. Only these combinations are allowed to overlap:

| Placing... | ...on top of |
|---|---|
| Passenger Zone | a **Filler** tile, or empty ground |
| Coin | a **Rail** |
| Environment object | a **Filler** tile, or empty ground |

Placing a **Rail** directly on top of another **Rail** is a special case: rather than being
blocked, the new rail *replaces* the old one (this is how you cap a Normal rail with a Stopper, for
example). Every other combination is rejected outright.

## Rail placement

Rails come in three types (`Rails.RailType`):

- **Normal** — an ordinary straight/curve waypoint; the train passes through it automatically.
- **Curve** — part of a multi-node curve chain inside a composite intersection piece.
- **Stopper** — a decision point. When the train arrives at a Stopper, it comes to a full stop and
  waits for the player to swipe a direction.

See [Rails & Trains](rails-and-trains.md) for how these actually drive the train at runtime.

### Duplicate name protection

Creating a new level, level element, or color preset checks for a name collision first — you'll
get a dialog instead of silently overwriting or duplicating an existing asset.

## Color Palette Presets

Levels can randomize their color palette on load and retry. Presets are stored in a single
`ColorPresetDatabase` asset (not one asset per palette):

- **Path:** `Assets/Rail Express/Data/Colors/Color Preset Database.asset`

From the Level Editor's Color Palette Presets section you can save the level's current colors as a
new named preset, and flag a preset as **Gold Rail only** so it's only ever picked for Gold Rail
levels (regular levels never pick a Gold Rail preset, and vice versa). The randomizer also avoids
repeating the same preset twice in a row when more than one candidate is available.

## Sea & Rocks placement

Sea and Rocks environment extras can each be placed **Top Only**, **Bottom Only**, or **Both**
sides of the level. Sea and Rocks are mutually exclusive per side — setting one on a side that the
other already occupies automatically clears the other from that side.

## Randomize buttons

- **Randomize Passenger Count** — reassigns each Passenger Spawner Zone's population, split
  randomly-but-exactly across the zone's count.
- **Randomize Coin Count** — mirrors the same logic for coins.

## Line Assist

While painting Rail-category objects, dragging locks to whichever axis (horizontal/vertical) you
moved first, so a straight run of track can't drift diagonally from a slightly uneven drag.
