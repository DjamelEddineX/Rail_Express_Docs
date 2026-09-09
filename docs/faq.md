# F.A.Q

### The game doesn't play any ads — what's wrong?

Check the Console for `AdsManager`'s init lines
(`"Banner (X) Ready."` / `"Interstitial (X) Ready."` / `"Rewarded (X) Ready."`). If one never
appears, that provider's SDK likely isn't imported/detected — open the **Ads Settings** asset and
check the green/red status shown in that provider's foldout. See
[Monetization](monetization.md) for the full setup guide.

### Color randomization doesn't seem to do anything.

Open the Level Editor once — it auto-creates and wires the `ColorPresetDatabase` asset onto your
`LevelDatabase` if one isn't assigned yet. If it's already wired and still not randomizing, check
the Console: `LevelManager.ApplyRandomColorPreset` logs a specific warning for every possible
silent-failure case (missing database, empty preset list, no preset matching the level's Gold Rail
state), so the exact cause should be visible there.

### A promo/banner popup keeps appearing every time I press Play.

It shouldn't — the FANNEC Promo check only runs on genuine Editor startup or script recompile,
never as a side effect of entering Play Mode. If you're still seeing it every Play press, make
sure `Editor/PromotionManager.cs`'s `isPlayingOrWillChangePlaymode` guard hasn't been removed.

### How do I preview the first-run promo banner without waiting for a real first install?

Use **Tools > FANNΞC > Rail Express > Actions > Promo > Force Show First-Run Banner** for an
instant preview, or **Reset First-Run Flag** to make the *next* Editor restart trigger it for real.

### The train misses a turn / drives straight through an intersection.

This is almost always a rail placement issue at the intersection, not a physics bug — check that
the intersection's `IntersectionManager` correctly lists every Stopper belonging to that junction,
and that no two path chains share an overlapping node (`Rails.ResolveOverlappingDestinationPoints`
cleans up accidental duplicates automatically, but a genuinely wrong prefab wiring won't be fixed
by that pass). See [Rails & Trains](rails-and-trains.md).

### Where do I change the support email / Discord / docs links shown in the About window?

`Editor/AboutWindow.cs` — `SupportEmail`, `DiscordUrl`, and `DocsUrl` constants near the top of the
file.

### Still stuck?

Reach out at [hello@fannec.net](mailto:hello@fannec.net).
