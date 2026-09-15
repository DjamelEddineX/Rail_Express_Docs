# Overview

**Rail Express** is a hyper-casual train puzzle template for Unity, built around a custom Level
Editor. This section covers how the project is organized and how to launch it for the first time.

## First Launch

Open the Game scene at `Assets/Rail Express/Scenes/Game`, or use the menu
**FANNΞC > Rail Express > Actions > Game Scene** to load it directly, then press **Play**.

## Project Structure

`Assets/Rail Express` is split into two kinds of folders:

- **Data** — settings assets and databases for the game's systems, stored as ScriptableObjects.
- **Everything else** — the game's assets, organized into folders by type (Prefabs, Scripts,
  Textures, Shaders, and so on).

## Scenes

The project ships with two scenes:

- **Initializer** — a lightweight boot scene, loaded first, that sets up core services before
  handing off to gameplay.
- **Game** — the main scene. Levels are loaded into it dynamically as the player progresses.

## Editor Tools

### Actions Menu

**FANNΞC > Rail Express > Actions** is a menu of quick shortcuts for common testing tasks, so you
don't have to dig through the Hierarchy or Project window while iterating. It gives you:

- **Remove Game Save** — wipes this project's saved progress, so the next Play session starts as
  if the game were installed fresh.
- **Manage Money** — set the player's in-game currency directly, without playing through levels to
  earn it.
- **Open Scenes** — jump straight to the Initializer or Game scene from the menu.

## Contents

```{toctree}
:maxdepth: 2

index
level-creation
environment
rails
trains
coins
monetization
```
