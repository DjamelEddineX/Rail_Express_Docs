# Coins

## How to Change the Coin Model

1. Import your custom model into the project.
2. Turn the model into a prefab.
3. Go to **FANNΞC > Rail Express > Level Editor > Field Elements**.
4. Click the existing Coin ScriptableObject, or locate it directly in the `Data` folder, and fill
   in its fields in the Inspector:

   - **Category** — which group this coin is filed under in the Field Elements palette.
   - **Rail Overlap** — whether this object is allowed to be placed on top of a Rail tile. Coins
     leave this on, since a coin only ever sits on top of a Rail.
   - **Editor Texture** — the icon shown for this coin in the Level Editor's palette.
   - **Hide In Level Editor** — hides the coin from the placement palette while keeping it
     registered.
   - **Size** — how many grid cells the coin occupies.
   - **Spawn Position** — a local position offset applied when the coin is instantiated, for
     lining up its visual model with the rail it's placed on.
   - **Game Prefab** — the prefab actually instantiated in the Game scene at runtime.

Dragging your coin prefab into the **Game Prefab** field is the only step needed to register a new
coin model. If more than one Coin ScriptableObject exists in the project, the game picks one of
them at random for each level.
