# Environment

## How to Add a New Environment Object

1. Import your custom model into the project.
2. Turn the model into a prefab.
3. Go to **FANNΞC > Rail Express > Level Editor > Field Elements**.
4. Click **Create New Object** next to **Environment**.
5. Select the new entry in the list, or locate it directly in the `Data` folder.
6. Fill in its fields in the Inspector:

   - **Category** — which group this object is filed under in the Field Elements palette, so it
     shows up alongside similar objects when you're placing pieces in the Level Editor.
   - **Rail Overlap** — whether this object is allowed to be placed on top of a Rail tile.
     Environment props leave this off, since they only belong on Filler tiles or empty ground.
   - **Editor Texture** — the icon shown for this object in the Level Editor's palette. It's a
     preview only and has no effect on the object placed in-game.
   - **Hide In Level Editor** — hides the object from the placement palette while keeping it
     registered, useful for pieces you don't want placed by hand.
   - **Size** — how many grid cells the object occupies, so the Level Editor knows what it will
     collide or overlap with once placed.
   - **Spawn Offset** — a local position offset applied when the object is instantiated, for
     lining up its visual model with the grid cell it's placed on.
   - **Game Prefab** — the prefab actually instantiated in the Game scene. This is the model
     players see at runtime, separate from the Editor Texture used only in the Level Editor.
