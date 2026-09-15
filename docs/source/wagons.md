# Wagons

## How to Add New Wagons

1. Import your custom model into the project.
2. Turn the model into a prefab.
3. Go to **FANNΞC > Rail Express > Level Editor > Field Elements**.
4. Click the existing Wagon ScriptableObject, or locate it directly in the `Data` folder, and fill
   in its fields in the Inspector:

   - **Category** — which group this entry is filed under in the Field Elements palette.
   - **Editor Texture** — the icon shown for this entry in the Level Editor's palette.
   - **Size** — how many grid cells a wagon occupies.
   - **Skins Count** — how many wagon skins are listed below. Raising it adds a new skin entry;
     lowering it removes the last one.
   - **ID** — the unique identifier for that skin entry, used to remember which wagon skin the
     player has selected.
   - **Wagon Prefab** — the prefab actually instantiated as that wagon skin at runtime.
   - **Gold Rail Wagon** — marks this skin as the special wagon used on Gold Rail levels instead
     of the player's normal selection.

Dragging your new model into a skin entry's **Wagon Prefab** field is the only step needed to
register it — once assigned, it's available as a playable wagon skin.

## How Wagons Chain Behind the Train

Every collected passenger adds one more wagon to the back of the train. Each new wagon attaches
behind the last segment in the chain — the locomotive if the train has no wagons yet, or the
wagon currently at the end of the line — and follows the exact path that segment already drove,
keeping a fixed distance behind it. Because every wagon replays the path of the one ahead rather
than steering on its own, the whole chain trails smoothly through curves and intersections no
matter how long it gets.
