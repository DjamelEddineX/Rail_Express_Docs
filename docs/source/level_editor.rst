Level Creation
##############

Levels are authored in a dedicated Editor window, not by editing the Game scene. Open it with
**Tools > FANNΞC > Rail Express > Level Editor**.

How to add a level
******************

1. Open the Level Editor and select the **Levels** tab.
2. Use the pagination bar at the bottom of the level list (``<<``  ``<``  Page X / Y  ``>``
   ``>>``) to browse pages - levels are paginated **35 per page** to keep long lists usable - and
   press **+** to add a new level.
3. Select the new level and set its **X** / **Y** grid size.
4. Pick an object from the palette, click a cell to place it, and click again to place another.
   Click-drag to paint continuously.
5. Right-click to rotate the object you're holding, or (when holding nothing) to erase an existing
   object.
6. Middle-click a **Passenger Spawner Zone** or **Coin** to open its settings, or a **Color**
   object to open its color wheel.
7. Press the **Escape Key** to drop / deselect the object you're currently holding.
8. Use **Control + Z** / **Control + Y** to undo / redo placement and erase actions.
9. Press **Test Level** to enter Play Mode directly on the selected level, skipping the Initializer.

All changes save automatically. A batched save runs on mouse-up rather than on every placement, so
painting a long stretch of track never stutters the editor.

The 0.5-unit grid
*****************

Levels are built on Unity's standard 1-unit tile grid, but rail geometry is finer than that:

* **DestinationPoint spacing**: consecutive rail waypoints along a chosen path are exactly
  **0.5 world units** apart. A composite intersection piece therefore packs several waypoints into
  a single 1x1 tile, which is what lets curves feel smooth rather than stepped.
* Every proximity check in the project - the train's front sensor, the sensor "catch-up" sweep,
  passenger-zone side eligibility - measures against a rail's ``DestinationPoint`` (its
  ``transform.position``).
* Because the gap between waypoints is only 0.5 units, the sensor sweep radius
  (``sensorSweepRadius`` on ``TrainController``) is kept under half that spacing so a single sweep
  can never span two waypoints at once. If you raise ``GameSetting.topSpeed`` well above the
  defaults, keep an eye on the ratio ``speed x 0.02`` (per-tick travel at 50 Hz physics) against
  that 0.5-unit spacing.

Rail types
**********

Rails come in three types (``Rails.RailType``):

Normal
------

* **What it does**:
    * An ordinary straight or gentle-curve waypoint. The train passes through automatically -
      hitting it simply updates the train's ``steeringTarget``.

Curve
-----

* **What it does**:
    * One node in a multi-node curve chain inside a composite intersection piece.
    * Standard chain length is **3** nodes (``curveChainLength`` on ``TrainController``).
* **Curve Lock**:
    * While the train is mid-turn, Normal rails are ignored so a nearby straight tile can't steal
      the steering focus. The lock is armed when a chosen path starts on a Curve rail and clears
      once the chain is fully traversed - or unconditionally when any Stopper is reached.

Stopper
-------

* **What it does**:
    * A decision point. When the train reaches a Stopper it comes to a full stop, shows its
      direction indicators, and waits for the player to swipe.
    * Holds up to three onward paths - ``pathRight``, ``pathLeft``, ``pathForward`` - each hidden
      until the player picks that direction.
* **Placement tip**:
    * Placing a Stopper directly on top of an existing Normal rail is allowed - the new rail
      *replaces* the old one rather than being blocked. This is how you cap the end of a straight
      run with a Stopper.

Intersections
*************

Group every physical Stopper at one junction into an ``IntersectionManager`` component. While the
train is inside a mapped intersection:

* Sibling Stoppers in that intersection are ignored (no full stop) - except the exact Stopper the
  train just departed from, which is still a valid fresh decision point if the track loops back to
  it.
* Speed drops to ``TopSpeed x intersectionSpeedMultiplier`` (default **0.5**) for the turn, then
  restores.
* The instant a path is chosen, every Stopper in the intersection is fully deactivated for the
  calculated time it takes to physically clear the turn, then reactivated. This prevents a
  Stopper's own trigger from double-firing or overriding the chosen path mid-turn. The duration is
  computed, not hardcoded:

.. code-block:: text

   distance     = curveChainLength x 0.5            (0.5 = DestinationPoint spacing)
   transitSpeed = TopSpeed x intersectionSpeedMultiplier
   duration     = (distance / transitSpeed) x intersectionClearSafetyMargin

Overlapping rail cleanup
------------------------

``Rails.ResolveOverlappingDestinationPoints()`` runs once after a level's rails are built (and
again whenever a Stopper's path is activated) to clean up accidental duplicate placements:

* A **Stopper** always wins over an overlapping **Normal** point - the Normal point is deactivated.
* Two overlapping **Normal** points collapse to one.
* **Curve** rails are exempt - never deactivated by this pass, whatever they overlap.

Passenger Spawner Zones
***********************

A Passenger Spawner Zone is a merged group of grid tiles that spawns a population of passengers.

* **Eligible sides** (``PickupSide`` = Left / Right / Top / Bottom):
    * A side is eligible only if a rail's ``DestinationPoint`` genuinely borders that exact edge of
      the zone. A rail merely overlapping the zone's own footprint does **not** make a side
      eligible - so a side can never be falsely triggered.
* **Balanced distribution**:
    * When a zone has multiple eligible sides, its total passenger count is split as evenly as
      possible across them. No single side ever holds 100% of the population while another eligible
      side is empty.
    * Passengers spawn clustered toward whichever edge they'll be picked up from, rather than
      sitting in the tile's center.
* **Pickup rules**:
    * Only the **locomotive** triggers a pickup - trailing wagons never collect on their own.
    * Nothing is collected until the train has actually started moving.
    * If a single pickup would complete the level on its own, the train pauses so the pickup
      animation plays out before the victory sequence fires.
* **Middle-click** a zone in the editor to open its settings; use **Randomize Passenger Count** to
  reassign each zone's population randomly-but-exactly.

Object stacking rules
*********************

Placement is validated per grid cell. Only these combinations may overlap:

+---------------------+-----------------------------------------+
| Placing...          | ...on top of                            |
+=====================+=========================================+
| Passenger Zone      | a **Filler** tile, or empty ground      |
+---------------------+-----------------------------------------+
| Coin                | a **Rail**                              |
+---------------------+-----------------------------------------+
| Environment object  | a **Filler** tile, or empty ground      |
+---------------------+-----------------------------------------+

Rail-on-Rail is the special replace case described above. Every other combination is rejected
outright. See :doc:`environment` for what counts as a Filler.

Color Palette Presets
*********************

Levels can randomize their colour palette on load and retry. Presets are stored in a single
runtime-visible asset:

* **Path**: ``Assets/Rail Express/Data/Colors/Color Preset Database.asset``

* **What it does**:
    * ``LevelManager.ApplyRandomColorPreset`` picks a random preset matching the level's Gold Rail
      status every time a level loads or retries, avoiding an immediate repeat of the last preset.
    * Colours are applied via ``_BaseColor`` (URP) checked ahead of the legacy ``_Color`` property
      - never the ``Material.color`` shorthand, which throws on shaders that have no ``_Color``.

* **How to add a preset**:
    * From the Color Palette Presets section, save the level's current colours as a new named
      preset.
    * Flag a preset as **Gold Rail only** so it's only ever chosen for Gold Rail levels (regular
      levels never pick a Gold Rail preset, and vice versa).

Line Assist
***********

While painting Rail-category objects, dragging locks to whichever axis you moved first, so a
straight run of track can't drift diagonally from an uneven drag.
