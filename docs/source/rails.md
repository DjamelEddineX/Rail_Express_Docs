# Rails

## How to Add New Rails

1. Import your custom model into the project.
2. Turn the model into a prefab.
3. Go to **FANNΞC > Rail Express > Level Editor > Field Elements**.
4. Click **Create New Object** next to **Rails**.
5. Select the new entry in the list, or locate it directly in the `Data` folder, and fill in its
   fields in the Inspector:

   - **Category** — which group this rail is filed under in the Field Elements palette.
   - **Editor Texture** — the icon shown for this rail in the Level Editor's palette.
   - **Hide In Level Editor** — hides the rail from the placement palette while keeping it
     registered.
   - **Size** — how many grid cells the rail occupies.
   - **Spawn Offset** — a local position offset applied when the rail is instantiated, for lining
     up its visual model with the grid cell it's placed on.
   - **Game Prefab** — the prefab actually instantiated in the Game scene at runtime.

## Prefab Setup & Destination Points

1. Open your new rail's prefab.
2. Add Destination Point child objects along the track — plain cubes scaled to 0.5 on the grid.
   Space them roughly 1 unit apart so the train's movement across the rail stays smooth.
3. Add the `Rails` component to each Destination Point.
4. Set that Destination Point's Rail Type.

## Rail Types

- **Normal** — a plain track segment. The train drives straight across it without stopping.
- **Stopper** — a decision point. The train comes to a halt here and waits for the player to swipe
  a direction before it continues.
- **Curve** — bends the train's heading. Chain several Curve Destination Points together to build
  a smooth turn leading out of an intersection.
