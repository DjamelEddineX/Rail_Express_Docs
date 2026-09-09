# UI

All UI screens live under the scene's `UI Main Canvas` and are coordinated by `UIManager`, which
subscribes to `LevelManager`'s events (`OnLevelLoadedEvent`, `OnLevelVictoryEvent`,
`OnLevelDefeatEvent`) to show/hide the right panel at the right time.

## Gameplay HUD (`UIGameplay`)

The main in-game screen: the level number / "Gold Rail" label, progress bar, coin counter, and the
swipe-input surface the player uses to steer at intersections. Also hosts the **Dev** button that
toggles the developer panel (`UIDev`) — a quick level-jump tool for testing, gated behind
**Tools > FANNΞC > Rail Express > Actions > Show Developer Panel** in the Editor.

## Crash screen (`UICrash`)

Shown on `OnLevelDefeatEvent`. Offers a countdown between two pathways:

- **Continue** — watch a rewarded ad to resume with progress preserved.
- **No Thanks** — decline and restart the level completely fresh.

See [Gameplay Systems → Restart flow](gameplay-systems.md#restart-flow-continue-vs-no-thanks) for
exactly what each button preserves.

## Win screen (`UIWin`)

Shown on `OnLevelVictoryEvent`. Displays the level-complete state and transitions into the next
level, re-activating the gameplay canvas that was hidden while the win panel was up.

## Fade (`UIFade`)

A shared fade-to-black transition used by every level load, restart, and next-level flow, so scene
state never changes visibly mid-transition.

## Station (`StationManager` / `UIStation`)

Handles the station-arrival sequence — the visual moment the train pulls into the end-of-level
station before handing off to the win screen.
