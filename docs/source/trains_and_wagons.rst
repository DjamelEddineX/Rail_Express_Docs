Trains & Wagons
###############

Rail Express ships with 9 locomotive skins and 10 wagon skins (including a dedicated Gold Rail
wagon). The locomotive drives itself along the track; wagons follow behind it.

Prefabs
*******

* **Locomotive**: ``Assets/Rail Express/Prefabs/Trains/Train.prefab`` is the functional prefab
  (``TrainController``, sensors, Rigidbody). ``Trains/Skins/Train_01`` ... ``Train_09`` hold the
  visual models that get swapped onto it.
* **Wagons**: ``Assets/Rail Express/Prefabs/Wagons/Wagon_01`` ... ``Wagon_09``, plus
  ``Wagon_Gold`` for Gold Rail levels. Each carries a ``WagonController``.

How the train follows track
***************************

``TrainController`` does not path-find a route in advance - it reacts to whichever rail trigger its
front sensor (``TrainSensor``, on a small collider at the front of the locomotive) just entered:

* **Normal / Curve rail** -> ``steeringTarget`` updates to that rail; the train smoothly turns to
  face it over the next few physics ticks.
* **Stopper** -> the train stops, shows the stopper's direction indicators, and waits for a swipe.

A safety net, ``CatchUpSensorDetection``, sweeps the sensor's movement each ``FixedUpdate`` and
catches any trigger the discrete collision check may have skipped at speed.

Speed & acceleration
--------------------

Tuned on the ``GameSetting`` asset:

* **topSpeed** (10) - cruising speed on ordinary track.
* **accelerationIncrement** (1) - the units/sec^2 ramp rate ``SpeedControlEngine`` uses when
  ``currentSpeed`` needs to catch up to ``targetSpeed``.
* Entering / exiting an intersection sets speed **instantly**, bypassing the ramp - acceleration
  only matters for a normal speed-up / slow-down on straight track.
* **intersectionSpeedMultiplier** (0.5) - speed factor while inside a mapped intersection.

Wagons
******

* **Following**: a ``WagonController`` follows the locomotive (or the wagon ahead of it) at a
  fixed spacing, using each segment's own recorded position history rather than chasing the
  segment ahead's current transform. This keeps the chain smooth around tight curves.
* **Growth**: a new wagon is added automatically once enough passengers / coins have been
  delivered (``passengersPerWagon``). See :doc:`ui_and_store` for the passenger / coin progress
  bar.
* **Victory animation**: on level complete, a short elevate-and-return wave runs down every wagon
  in sequence before the win screen appears.

How to change the train or wagon model
**************************************

Skins are defined on a ``LevelElement`` asset of the **Train** (or **Wagon**) category. Each skin
entry holds:

* **ID** - a unique string used by the store and by ``SaveController.SelectedSkin``. Use the
  **Copy** / **Reset** buttons in the Inspector to manage it.
* **Train Prefab** / **Wagon Prefab** - the model prefab for that skin.
* **Offset Position** (train only) - fine model positioning.
* **Gold Rail Wagon** (wagon only) - marks a wagon skin as the Gold Rail variant.

To add a new skin:

1. Import your model and make a prefab from it (roughly matching the proportions of the existing
   locomotive / wagon).
2. Open the Train / Wagon ``LevelElement`` asset, increase **Skins Count**, and assign your prefab
   to the new slot.
3. Keep the order consistent with any store product that references it by index.

Forcing a skin per level
------------------------

On a ``LevelData`` asset:

* **forceTrainSkins** - when enabled, the level ignores the player's chosen skin.
* **forcedLocomotiveSkinIndex** / **forcedWagonSkinIndex** - the skin indices used when
  ``forceTrainSkins`` is on (used for Gold Rail levels, for example).

At runtime ``TrainController.ApplySkins(loco, wagon)`` applies either the forced indices or
``SaveController.SelectedSkin``.
