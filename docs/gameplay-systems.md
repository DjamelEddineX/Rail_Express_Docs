# Gameplay Systems

## Passenger Spawner Zones

A `PassengerSpawnerZone` is a merged group of grid tiles that spawns a population of passengers.
Each zone tracks its own eligible pickup sides independently:

```csharp
public enum PickupSide { Left, Right, Top, Bottom }
```

A side only counts as eligible if a rail's `DestinationPoint` genuinely borders that exact edge of
the zone — this is checked strictly (a rail merely overlapping the zone's own footprint doesn't
count) so a side can never be falsely marked eligible.

When a zone has multiple eligible sides, its total passenger count is split as evenly as possible
across them (never 100% on one side when others are eligible), and passengers spawn clustered
toward whichever edge they'll be picked up from rather than sitting in the middle of the tile.

Only the **locomotive** triggers a pickup — trailing wagons never collect on their own — and only
once the train has actually started moving, so nothing gets collected the instant a level loads.

If a single pickup would complete the level on its own, the train is paused (`PauseForGoalCompletionPickup`)
so the pickup animation plays out fully before the victory sequence fires, rather than the train
cruising straight through the win.

## Coins

`CoinsSpawner` places a coin that contributes `fillAmount` toward the same progress counter
passengers use (`LevelManager.AddPassenger`) — coins and passengers share one unified progress bar,
not two separate counters. Coins are Gold-Rail-only content.

## Wagons

`WagonController` instances follow the locomotive (or the wagon ahead of them) at a fixed spacing,
using each segment's own recorded position history rather than literally chasing the segment
ahead's current transform. A new wagon is added automatically once enough passengers/coins have
been delivered (`passengersPerWagon`).

## Victory & Defeat

- **Victory** — once the level's passenger/coin target is reached, `LevelManager` triggers the
  train's victory sequence (a short wave/bounce animation through every wagon) before firing
  `OnLevelVictoryEvent`.
- **Defeat (crash)** — colliding with another train segment or driving off the intended path
  triggers a crash sequence and `OnLevelDefeatEvent`.

## Restart flow (Continue vs. No Thanks)

After a crash, the player is offered two distinct pathways:

- **Continue** (rewarded ad) — on a successful ad view, `RestartLevelWithSavedPassengers()` reloads
  the level layout fresh but **preserves** accumulated coins/passengers: each Passenger Spawner
  Zone's remaining population is snapshotted before reload and restored afterward, and coins
  already collected this session are tracked by grid position so they don't respawn and get
  double-collected.
- **No Thanks** (decline) — goes straight to `RestartLevel()`, a full reset: progress, zone
  populations, and coins all return to the level's original authored state.

## Level looping / endless tail

Once the player advances past the last authored level, `LevelManager.NextLevel()` starts picking a
random previous level instead of resetting. The player-facing level number
(`LevelManager.DisplayLevelNumber`, persisted separately from the raw level index) keeps counting
upward indefinitely and skips incrementing for Gold Rail levels, since those don't consume a
player-facing number.
