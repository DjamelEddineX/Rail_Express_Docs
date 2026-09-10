F.A.Q
#####

The game doesn't play any ads
********************************************************************************

Check the Console for ``AdsManager``'s init lines (``Banner (X) Ready.`` / ``Interstitial (X)
Ready.`` / ``Rewarded (X) Ready.``). If one never appears, that provider's SDK likely isn't
imported / detected - open the **Ads Settings** asset and check the green / red status in that
provider's foldout. See :doc:`monetization`.

Color randomization doesn't seem to do anything
********************************************************************************

Open the Level Editor once - it auto-creates and wires the ``ColorPresetDatabase`` asset onto your
``LevelDatabase`` if one isn't assigned yet. If it's already wired and still not randomizing, check
the Console: ``LevelManager.ApplyRandomColorPreset`` logs a specific warning for every silent
failure case (missing database, empty preset list, no preset matching the level's Gold Rail
state).

A promo popup keeps appearing every time I press Play
********************************************************************************

It shouldn't - the FANNEC Promo check only runs on genuine Editor startup / script recompile. If
you still see it every Play press, make sure ``Editor/PromotionManager.cs``'s
``isPlayingOrWillChangePlaymode`` guard hasn't been removed.

Previewing the first-run promo banner without a clean machine
********************************************************************************

Use **Tools > FANNΞC > Rail Express > Actions > Promo > Force Show First-Run Banner** for an
instant preview, or **Reset First-Run Flag** so the next Editor restart triggers it for real.

The train misses a turn or drives straight through an intersection
********************************************************************************

Almost always a rail placement issue at the intersection, not a physics bug. Check that the
intersection's ``IntersectionManager`` lists every Stopper belonging to that junction, and that no
two path chains share an overlapping node. ``Rails.ResolveOverlappingDestinationPoints`` cleans up
accidental duplicates automatically, but a genuinely wrong prefab wiring won't be fixed by that
pass. See :doc:`level_editor`.

Changing the support email, Discord or docs links in the About window
********************************************************************************

``Editor/AboutWindow.cs`` - the ``SupportEmail``, ``DiscordUrl`` and ``DocsUrl`` constants near the
top of the file. Point ``DocsUrl`` at this site once it's live on Read the Docs.

Wiping save data for testing
********************************************************************************

**Tools > FANNΞC > Rail Express > Actions > Remove Save**, or enable ``GameSetting.cleanSaveStart``.
Both only clear this project's own save keys - never all of ``PlayerPrefs``.

Still stuck
********************************************************************************

Reach out via :doc:`contact`.
