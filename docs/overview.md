# Overview

## Project structure

Everything lives under `Assets/Rail Express/`:

- **Scripts/** — all C# scripts, in the `Fannec.RailExpress` namespace (Editor-only scripts sit in
  `Scripts/Editor/` under `Fannec.RailExpress.Editor`).
- **Data/** — ScriptableObject assets: `Game Settings.asset`, level data, level element
  definitions, and the `Colors/` folder (color LevelElements + `Color Preset Database.asset`).
- **Prefabs/** — organized by type: `Rails/`, `Trains/`, `Wagons/`, `Passengers/`, `Environment/`,
  `Fillers/`, `Particles/`.
- **Scenes/** — `Initializer.unity` (splash/boot) and `Game.unity` (the actual gameplay scene).
- **Textures/Editor/** — icons and images used by the custom Editor windows (About window,
  Promo banner, etc.).

## Scenes

The project has two scenes:

- **Initializer** — a small boot scene loaded first, used to initialize services before handing
  off to the Game scene. Controlled by `ProjectSetting.autoLoadInitializer`.
- **Game** — the main scene; all gameplay happens here.

### Game scene contents

- **LevelManager** — the central runtime controller. Loads levels, tracks passenger/coin progress,
  fires `OnLevelLoadedEvent` / `OnLevelVictoryEvent` / `OnLevelDefeatEvent`, and owns the
  restart/continue flow.
- **StationManager** — manages the station-arrival sequence at the end of a level.
- **Terrain**, **Canvas**, **EventSystem** — standard scene scaffolding.
- **Banner_Camera** / **Canvas_Camera** — dedicated cameras for the ad banner and UI overlay.
- **Global Volume** — URP post-processing volume.
- **[Auto] Level_Environment_Builder** — created automatically by `LevelManager` at runtime if not
  already present in the scene; hosts the `LevelBuilder` component that instantiates the current
  level's grid, rails, train, and passenger zones.

Levels are built dynamically at runtime by `LevelBuilder` from a `LevelData` asset — nothing about
a level's grid is baked into the scene itself. To preview and edit a level's layout, use the
[Level Editor](level-editor.md) rather than editing the scene directly.

## Core managers (singletons)

These all follow the same `Instance` static-singleton pattern, created once and persisted with
`DontDestroyOnLoad`:

| Manager | Responsibility |
|---|---|
| `LevelManager` | Level load/restart/victory/defeat, passenger & coin progress |
| `SaveController` | Persistent player progression (PlayerPrefs-backed) |
| `GameSettingsManager` | Runtime access to the `GameSetting` asset (speed, acceleration, etc.) |
| `AudioManager` | SFX/music playback |
| `AdsManager` / `MonetizationManager` | Ad provider routing and monetization gating |
| `IAPManager` | In-app purchases (No Ads, etc.) |

Two `ScriptableObject` assets configure the whole project — see
[Save System & Settings](save-system.md) for the full field reference:

- **`ProjectSetting`** — project-wide paths, scene names, and the Fannec promo toggle.
- **`GameSetting`** — gameplay tuning (train speed/acceleration, swipe sensitivity, save behavior).

## Editor Tools menu

Everything lives under **Tools > FANNΞC > Rail Express**:

- **Level Editor** — the grid-based level building tool (see [Level Editor](level-editor.md)).
- **Game Settings** / **Project Settings** — quick shortcuts that select the two settings assets
  above in the Inspector.
- **About** — credits, support email, Discord, and documentation links.
- **Actions >**
    - **Remove Save** — wipes only this project's own save keys (not all of PlayerPrefs).
    - **Currency > Get 20K / No Money** — quick coin-balance testing while in Play Mode.
    - **Game Scene** — opens the Game scene directly, bypassing the Initializer.
    - **Show Developer Panel** — toggles the in-game dev panel button on/off.
    - **Promo > Reset First-Run Flag / Force Show First-Run Banner** — testing aids for the
      first-run promo banner (see below).

## The FANNEC Promo system

A small Editor-only popup (`PromotionManager` / `PromotionWindow`) can show a promo banner in two
situations, controlled by `ProjectSetting.enableFannecPromotions`:

- **First install** — shown exactly once per machine, using a bundled local image
  (`Assets/Rail Express/Textures/Editor/Editor_PromoBanner_Default.png`), no network required.
- **Remote push** — on every Editor startup, it checks a small JSON file hosted online for a new
  campaign; if one is found, it fetches and shows that banner instead.

It only ever checks on genuine Editor startup/script recompile — never on every Play Mode press.
