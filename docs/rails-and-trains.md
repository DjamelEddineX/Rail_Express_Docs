# Rails & Trains

This page covers how the train actually follows the track at runtime — the sensor system,
intersections, and the physics tuning that governs speed and turning.

## Rails

Every rail waypoint is a `Rails` component with a trigger collider. Its `DestinationPoint`
property (`transform.position`) is what every proximity/sensor check in the project measures
against.

```csharp
public enum RailType { Normal, Stopper, Curve }
```

- **Normal** — plain waypoint; passing through it just updates the train's steering target.
- **Curve** — one node in a multi-node curve chain (see Curve Lock below). Standard node spacing
  along a chain is **0.5 world units**.
- **Stopper** — a decision point with up to three onward paths (`pathRight` / `pathLeft` /
  `pathForward`), each hidden until the player picks a direction.

### Overlap cleanup

`Rails.ResolveOverlappingDestinationPoints()` runs once after a level's rails are instantiated
(and again whenever a Stopper's path is activated). It cleans up accidental duplicate placements:

- A **Stopper** always wins over an overlapping Normal point — the Normal point is deactivated.
- Two overlapping **Normal** points collapse to one.
- **Curve** rails are exempt — they're never deactivated by this pass, no matter what they overlap.

## How the train follows track

`TrainController` doesn't path-find a route in advance — it reacts to whichever rail trigger its
front sensor (`TrainSensor`, on a small collider mounted on the front of the locomotive) just
entered:

- **Normal / Curve rail** → `steeringTarget` is updated to that rail's transform; the train
  smoothly turns to face it over the next few physics ticks.
- **Stopper** → the train comes to a full stop, shows the stopper's direction indicators, and
  waits for a swipe.

A secondary safety net, `CatchUpSensorDetection`, sweeps the sensor's movement each `FixedUpdate`
tick and catches any trigger the discrete collision check might have skipped at high speed.

## Intersections

A **Stopper** can belong to an `IntersectionManager`, which groups every physical Stopper at one
junction. While the train is inside a mapped intersection:

- Every *other* Stopper in that intersection is ignored (never causes a full stop) — except the
  exact Stopper the train just departed from, which is still treated as a fresh decision point if
  the track loops back to it.
- Speed drops to `TopSpeed × intersectionSpeedMultiplier` (default **0.5**) for the duration of the
  turn, restoring to full speed once the intersection is cleared.
- The moment a path is chosen, every Stopper in that intersection is fully deactivated
  (`GameObject.SetActive(false)`) for the time it takes to physically clear the intersection, then
  reactivated — this prevents a Stopper's own trigger from double-firing or overriding the chosen
  path mid-turn. The duration is calculated, not hardcoded:

```
distance = curveChainLength × 0.5 (DestinationPoint spacing)
transitSpeed = TopSpeed × intersectionSpeedMultiplier
duration = (distance / transitSpeed) × intersectionClearSafetyMargin
```

### Curve Lock

While `curveLockRemainingCount > 0`, Normal rails are ignored so a nearby straight tile can't steal
focus mid-turn. It's armed to `curveChainLength - 1` (default chain length: **3**) whenever a
chosen path starts on a Curve rail, and decrements on each subsequent Curve hit. Reaching *any*
Stopper unconditionally clears it, as a safety net against a mismatched chain length leaving it
stuck.

## Speed & acceleration tuning

These live on the `GameSetting` asset (see [Save System & Settings](save-system.md)):

- **`topSpeed`** — the train's cruising speed on ordinary track.
- **`accelerationIncrement`** — units/sec² ramp rate used by `SpeedControlEngine` whenever
  `currentSpeed` needs to catch up to `targetSpeed`. Note that entering/exiting an intersection sets
  speed *instantly*, bypassing this ramp entirely — acceleration only matters for a normal
  speed-up/slow-down on straight track.

At the default 50 Hz physics tick, per-tick travel distance is `speed × 0.02`. Since
`DestinationPoint` spacing is 0.5 units, keep an eye on this ratio if you push `topSpeed`
significantly higher than the defaults — the sensor sweep radius (`sensorSweepRadius` on
`TrainController`) should stay under half that spacing so it can't span two nodes at once.
