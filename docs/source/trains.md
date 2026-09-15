# Trains

## How to Add New Trains

1. Import your custom model into the project.
2. Turn the model into a prefab.
3. Go to **FANNΞC > Rail Express > Level Editor > Field Elements**.
4. Click the existing Train ScriptableObject, or locate it directly in the `Data` folder, and fill
   in its fields in the Inspector:

   - **Category** — which group this train is filed under in the Field Elements palette.
   - **Editor Texture** — the icon shown for this train in the Level Editor's palette.
   - **Size** — how many grid cells the locomotive occupies.
   - **Skins Count** — how many alternate skin variants this train offers in the in-game skin
     selector.
   - **ID** — the unique identifier used to remember which skin the player has selected.
   - **Train Prefab** — the prefab actually instantiated as the playable locomotive at runtime.
   - **Offset Position** — a local position offset applied when the train spawns, for lining up
     its model with the track.

Dragging your new model into the **Train Prefab** field is the only step needed to register it —
once assigned, it's available as a playable locomotive.
