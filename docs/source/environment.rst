Environment
###########

Environment covers the decorative and level-wide scenery around the track: filler ground, the
empty-space rules that govern where things can be placed, and the per-side Sea / Rocks extras.

Fillers and empty space
***********************

* **Fillers**:
    * Purely decorative ground-fill Environment objects, identified by name (``Filler_...``).
    * They are the **only** thing a Passenger Zone or another Environment object is allowed to be
      placed on top of - see :doc:`level_editor`.
    * The prefabs live in ``Assets/Rail Express/Prefabs/Fillers/`` and
      ``Assets/Rail Express/Prefabs/Environment/``.

* **Empty space**:
    * A cell with nothing in it. Placing a Passenger Zone or Environment object on empty ground is
      always valid; the object is written straight into the base grid layer.
    * When placed on a Filler instead, the object is layered as a tile overlay so the Filler
      underneath is preserved.

Editor placement rules recap
****************************

* **Passenger Zone** -> Filler or empty ground only.
* **Coin** -> a Rail only.
* **Environment object** -> Filler or empty ground only.
* **Rail on Rail** -> allowed; the new rail replaces the old one.
* Everything else -> rejected.

An asset's ``railOverlapMode`` field no longer gates whether a placement is allowed - it only
controls build-time visual elevation (whether the model sits *on top of* the tile below it).

Sea & Rocks
***********

Sea and Rocks are level-wide environment extras rather than per-tile objects.

* **What it does**:
    * Each can be set to **None**, **Top Only**, **Bottom Only**, or **Both** sides of the level.
    * The two are mutually exclusive per side - setting one on a side that the other already
      occupies automatically clears the other from that side.

* **Automatic migration**:
    * Levels authored before this placement system existed migrate the first time their grid is
      validated. Their old on/off ``enableSea`` / ``enableRocks`` booleans map to the equivalent
      single-side placement, one time only, so an existing level's appearance never silently
      changes.

Color Palette Presets
*********************

See :doc:`level_editor` for the authoring workflow. At a glance:

* Presets live in one runtime-visible ``ColorPresetDatabase`` asset
  (``Assets/Rail Express/Data/Colors/Color Preset Database.asset``), not the old Editor-only,
  EditorPrefs-backed system - this is what lets the game actually randomize colours at runtime.
* Each preset stores a name, a list of colours, and an ``isGoldRailPreset`` flag.
* The randomizer picks a preset matching the level's Gold Rail status and avoids repeating the last
  preset applied.
