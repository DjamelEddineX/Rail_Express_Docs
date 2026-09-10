UI & Store
##########

All UI lives under the scene's ``UI Main Canvas`` and is coordinated by ``UIManager``, which
subscribes to ``LevelManager``'s events (``OnLevelLoadedEvent``, ``OnLevelVictoryEvent``,
``OnLevelDefeatEvent``) and shows / hides the right panel at the right time.

UI screens
******************************************************************

Gameplay HUD (``UIGameplay``)
-----------------------------------------------------------------

The main in-game screen.

* **What it shows**:
    * ``levelUIText`` - the ``LEVEL NN`` label, or ``Gold Rail`` for a Gold Rail level.
    * ``passengersUIText`` / ``passengerCountBar`` - the unified passenger + coin progress bar
      (coins feed the same counter as passengers, via ``LevelManager.AddPassenger``).
    * ``safeZoneArea`` - the region the player swipes in to steer at Stoppers.
* **Buttons**: ``playButton``, ``stationButton``, ``settingsButton``, ``devButton``.
* The **Dev** button toggles the developer panel (``UIDev``) - a quick level-jump tool, enabled in
  the Editor via **Tools > FANNΞC > Rail Express > Actions > Show Developer Panel**.

Crash screen (``UICrash``)
-----------------------------------------------------------------

Shown on ``OnLevelDefeatEvent``, with a countdown between two pathways:

* **Continue** - watch a rewarded ad to resume with progress preserved.
* **No Thanks** - decline and restart the level completely fresh.

See :ref:`gameplay-restart` below for exactly what each button preserves.

Win screen (``UIWin``)
-----------------------------------------------------------------

Shown on ``OnLevelVictoryEvent``. Displays the level-complete state and transitions into the next
level, re-activating the gameplay canvas that was hidden while the win panel was up.

Coins (``UICoins``)
-----------------------------------------------------------------

Animated coin counter shown after a level; tick speed ramps between ``minTickSpeed`` and
``maxTickSpeed`` over ``totalAnimationTime``.

Station (``StationManager`` / ``UIStation``)
-----------------------------------------------------------------

Handles the station-arrival sequence - the visual moment the train pulls into the end-of-level
station before the win screen.

Fade (``UIFade``)
-----------------------------------------------------------------

A shared fade-to-black transition used by every level load, restart and next-level flow, so scene
state never changes visibly mid-transition.

Helper (``UIHelper``)
-----------------------------------------------------------------

The swipe-hint overlay that appears when the train has been stopped at a Stopper for a while
without input (``LevelManager.helperUIWaitTime``).

The Store (Settings & IAP)
******************************************************************

Rail Express's store surface is the **Settings** panel plus the **No Ads** in-app purchase.

Settings (``UISettings``)
-----------------------------------------------------------------

* **Toggles**: ``soundToggle``, ``HapticToggle`` - backed by ``SaveController.SoundEnabled`` /
  ``HapticsEnabled``.
* **Buttons**:
    * ``noAdsButton`` - triggers the No Ads IAP.
    * ``restoreButton`` - restores previous purchases.
    * ``supportButton`` - opens ``AdSettings.supportUrl``.
    * ``privacyPolicyButton`` / ``termsOfUseButton`` - open ``AdSettings.privacyPolicyUrl`` /
      ``termsOfUseUrl`` (buttons hide themselves if the URL is blank).

No Ads purchase (``UIIAP``)
-----------------------------------------------------------------

* **What it does**:
    * Buys the No Ads product (``AdSettings.noAdsAndroidProductId`` / ``noAdsIosProductId``),
      which disables forced ads (banners, interstitials). Rewarded videos still work.
    * On success, ``SaveController.HasPurchasedNoAds`` is set and the IAP button hides itself.
* **Testing**:
    * Enable **Use Fake Store** on the ``AdSettings`` asset to simulate purchases in the Editor
      without a real store connection while you test the surrounding UI.

Train / wagon skins
-----------------------------------------------------------------

Skins are selected via ``SaveController.SelectedSkin`` and applied by
``TrainController.ApplySkins``. Skin definitions (id, model prefab, offset) live on Train / Wagon
``LevelElement`` assets - see :doc:`trains_and_wagons` for how to add a new skin.

.. _gameplay-restart:

Restart flow: Continue vs. No Thanks
******************************************************************

After a crash the player is offered two distinct pathways:

* **Continue** (rewarded ad) - on a successful ad view, ``RestartLevelWithSavedPassengers()``
  reloads the level layout fresh but **preserves** accumulated coins / passengers. Each Passenger
  Spawner Zone's remaining population is snapshotted before reload and restored afterward, and
  coins already collected this session are tracked by grid position so they don't respawn and get
  double-collected.
* **No Thanks** (decline) - goes straight to ``RestartLevel()``, a **full reset**: progress, zone
  populations and coins all return to the level's original authored state.

Endless tail
******************************************************************

Once the player passes the last authored level, ``LevelManager.NextLevel()`` picks a random
previous level instead of resetting. The player-facing level number
(``LevelManager.DisplayLevelNumber``, persisted separately from the raw level index) keeps counting
upward and skips incrementing for Gold Rail levels, since those don't consume a player-facing
number.
