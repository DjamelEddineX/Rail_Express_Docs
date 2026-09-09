# Rail Express

**Owner:** FANNΞC · **Type:** Unity Template · **Genre:** Train puzzle / arcade

Rail Express is a mobile train-puzzle template: a locomotive follows a rail network you build
tile-by-tile in a custom in-editor Level Editor, collecting passengers and coins while the player
swipes at intersections to choose which way the train turns.

| | |
|---|---|
| **Recommended Unity version** | Unity 6 (6000.4.x LTS) |
| **Render pipeline** | Universal Render Pipeline (URP) |
| **Platform target** | Android / iOS (mobile) |

## How to start

1. Import the template into a new Unity 6 project.
2. Open `Assets/Rail Express/Scenes/Game.unity`.
3. Press **Play** — or use the menu **Tools > FANNΞC > Rail Express > Actions > Game Scene**,
   which opens the Game scene directly and skips the splash/initializer flow.
4. To build and edit levels, open **Tools > FANNΞC > Rail Express > Level Editor**.

Use the navigation on the left to find documentation for any specific part of the project:

- **[Overview](overview.md)** — project structure, scenes, core managers, and the Editor Tools menu.
- **[Level Editor](level-editor.md)** — building levels tile by tile, pagination, color presets.
- **[Rails & Trains](rails-and-trains.md)** — rail types, intersections, sensors, and train physics.
- **[Gameplay Systems](gameplay-systems.md)** — passengers, coins, wagons, victory/defeat flow.
- **[Environment & Colors](environment-and-colors.md)** — fillers, Sea/Rocks, color randomization.
- **[UI](ui.md)** — the main UI screens and how they're wired.
- **[Monetization (Ads & IAP)](monetization.md)** — the ad provider system and in-app purchases.
- **[Save System & Settings](save-system.md)** — persistent progression and the two settings assets.

There's also an **[F.A.Q](faq.md)** at the end covering common setup questions.

## Support

If you run into an issue that isn't covered here, reach out at
[hello@fannec.net](mailto:hello@fannec.net).

!!! note
    The in-editor **About** window (**Tools > FANNΞC > Rail Express > About**) links out to this
    documentation site and to our Discord — update `DocsUrl` / `DiscordUrl` in
    `Editor/AboutWindow.cs` once this site and your Discord invite are both live.
