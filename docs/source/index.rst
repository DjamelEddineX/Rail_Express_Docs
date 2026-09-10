Rail Express
============

.. image:: images/Rail_Express_Thumbnail.png
   :width: 600
   :alt: Rail Express

**Rail Express** is a hyper-casual train puzzle template for Unity. A locomotive rides a rail
network you build tile by tile in a custom in-editor Level Editor, picking up passengers and coins
while the player swipes at intersections to choose which way the train turns. It ships with a full
level authoring pipeline, a mobile monetization module (Ads & IAP), a save system, and a store.

=========================  ======================================
Recommended Unity version  Unity 6 (6000.4.x LTS)
Render pipeline            Universal Render Pipeline (URP)
Target platforms           Android / iOS (mobile)
Publisher                  FANNΞC
=========================  ======================================


Features
--------

* **Custom Level Editor**: Build levels on a snapping grid, no scene editing required.
* **0.5-unit rail grid**: Rails, curves and stoppers snap to a fine grid for smooth turns.
* **Swipe-to-turn gameplay**: Stoppers act as decision points; the player swipes a direction.
* **Passenger Zones**: Multi-tile pickup areas with per-side eligibility and balanced distribution.
* **Coins & Wagons**: Collectibles feed one unified progress bar; wagons grow the train over time.
* **Color Palette Presets**: Randomize a level's palette on load and retry, with Gold Rail variants.
* **Environment system**: Fillers, empty-space rules, and per-side Sea / Rocks extras.
* **Monetization Module**: Provider-agnostic Ads (AdMob, AppLovin, LevelPlay, Dummy) plus IAP.
* **FANNEC Promo banner**: Local first-run banner plus an optional remote web push.
* **Save System**: Key-scoped PlayerPrefs progression that never wipes unrelated data.


How to start
------------

1. Import the template into a new Unity 6 project.
2. Open ``Assets/Rail Express/Scenes/Game.unity``.
3. Press **Play**, or use **Tools > FANNΞC > Rail Express > Actions > Game Scene** to open the
   Game scene directly and skip the splash / Initializer flow.
4. To build and edit levels, open **Tools > FANNΞC > Rail Express > Level Editor**.

Use the navigation on the left to find documentation for any part of the project. There is also an
:doc:`faq` at the end covering common setup questions.


Support
-------

If you have any questions, issues or an idea for a new feature, get in touch via :doc:`contact`.


Contents
--------

.. toctree::
   :maxdepth: 2

   overview
   level_editor
   environment
   trains_and_wagons
   ui_and_store
   monetization
   faq
   changelog
   contact
