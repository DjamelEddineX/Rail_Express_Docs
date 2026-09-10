Overview
########

First launch
************

To run the game, open the Game scene located at ``Assets/Rail Express/Scenes/Game.unity`` or use
the menu **Tools > FANNΞC > Rail Express > Actions > Game Scene**, then press **Play**.

* Levels are **not** baked into the scene. When the game runs, ``LevelManager`` builds the current
  level dynamically from a ``LevelData`` asset. To preview or edit a layout, use the
  :doc:`level_editor`, not the scene.

Project structure
*****************

Everything lives under ``Assets/Rail Express/``:

* **Scripts/** - all C# scripts, in the ``Fannec.RailExpress`` namespace. Editor-only scripts sit
  in ``Scripts/Editor/`` under ``Fannec.RailExpress.Editor``.
* **Data/** - ScriptableObject assets: ``Game Settings.asset``, level data, level element
  definitions, and the ``Colors/`` folder (color elements + ``Color Preset Database.asset``).
* **Prefabs/** - organized by type: ``Rails/``, ``Trains/``, ``Wagons/``, ``Passengers/``,
  ``Environment/``, ``Fillers/``, ``Particles/``.
* **Scenes/** - ``Initializer.unity`` and ``Game.unity``.
* **Textures/Editor/** - icons and images used by the custom Editor windows.

Scenes
------

The project has two scenes:

* **Initializer** - a small boot scene loaded first, used to initialize services before handing
  off to the Game scene. Controlled by ``ProjectSetting.autoLoadInitializer``.
* **Game** - the main scene; all gameplay happens here.

Game scene contents
-------------------

* **LevelManager** - the central runtime controller. Loads levels, tracks passenger/coin progress,
  fires ``OnLevelLoadedEvent`` / ``OnLevelVictoryEvent`` / ``OnLevelDefeatEvent``, and owns the
  restart / continue flow.
* **StationManager** - manages the station-arrival sequence at the end of a level.
* **Terrain**, **Canvas**, **EventSystem** - standard scene scaffolding.
* **Banner_Camera** / **Canvas_Camera** - dedicated cameras for the ad banner and UI overlay.
* **Global Volume** - the URP post-processing volume.
* **[Auto] Level_Environment_Builder** - created automatically by ``LevelManager`` at runtime if
  not already present; hosts the ``LevelBuilder`` component that instantiates the current level's
  grid, rails, train and passenger zones.

Core managers
*************

All managers use the same static-singleton pattern - created once, persisted with
``DontDestroyOnLoad``:

* **LevelManager** - level load / restart / victory / defeat, passenger & coin progress.
* **SaveController** - persistent player progression (PlayerPrefs-backed). See :doc:`ui_and_store`.
* **GameSettingsManager** - runtime access to the ``GameSetting`` asset (speed, acceleration...).
* **AudioManager** - SFX and music playback.
* **AdsManager** / **MonetizationManager** - ad provider routing and monetization gating.
* **IAPManager** - in-app purchases.

Two ScriptableObject assets configure the whole project:

* **ProjectSetting** - project-wide paths, scene names, and the Fannec promo toggle.
    * ``dataFolder`` (``Assets/Rail Express/Data``), ``scenesFolder``, ``GameSceneName`` (``Game``)
    * ``minimumLoadingTime`` (2.5), ``autoLoadInitializer`` (true)
    * ``enableFannecPromotions`` (true) - see :doc:`monetization`
* **GameSetting** - gameplay tuning.
    * ``topSpeed`` (10), ``accelerationIncrement`` (1) - train speed and ramp rate
    * ``minSwipeDistance`` (45) - minimum swipe distance to register a turn
    * ``startingCoins`` (1000), ``baseUnlockPrice`` / ``priceIncrement`` (250 / 250)
    * ``autoSaveDelay`` (0), ``cleanSaveStart`` (false), ``webGLPrefix`` (``RailExpress_``)
    * ``setFrameRateAutomatically``, ``defaultFrameRate``, ``batterySaveFrameRate``
    * ``requireNetworkToPlay``, ``pingUrl``, ``pingTimeoutSeconds``, ``networkCheckInterval``

Access from code:

.. code-block:: csharp

   GameSettingsManager.TopSpeed          // shortcut for GameSetting.topSpeed
   ProjectSetting.Instance.scenesFolder

Editor Tools
************

Everything lives under **Tools > FANNΞC > Rail Express**:

* **Level Editor** - the grid-based level building tool (see :doc:`level_editor`).
* **Game Settings** / **Project Settings** - select the two settings assets in the Inspector.
* **About** - credits, support email, Discord and documentation links (``Editor/AboutWindow.cs``).
* **Actions >**
    * **Remove Save** - wipes only this project's own save keys (never ``PlayerPrefs.DeleteAll()``).
    * **Currency > Get 20K / No Money** - quick coin-balance testing while in Play Mode.
    * **Game Scene** - opens the Game scene directly, bypassing the Initializer.
    * **Show Developer Panel** - toggles the in-game dev panel button on / off.
    * **Promo > Reset First-Run Flag / Force Show First-Run Banner** - testing aids for the
      first-run promo banner (see :doc:`monetization`).
