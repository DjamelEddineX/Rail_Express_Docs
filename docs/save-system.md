# Save System & Settings

## SaveController

A static-property API backed by `PlayerPrefs`, prefixed with an optional `webGLPrefix`
(`GameSetting.webGLPrefix`) so a WebGL build sharing a domain with other games doesn't collide keys.

| Property | Purpose |
|---|---|
| `SoundEnabled` / `HapticsEnabled` | Audio/haptics toggles |
| `CurrentSavedLevel` | Raw level index to resume into |
| `UnlockedLevel` | Highest level index unlocked |
| `DisplayLevelNumber` | Player-facing "LEVEL N" counter — separate from the raw index, since Gold Rail levels don't consume a number and the index stops being meaningful once the endless random tail kicks in |
| `HasPurchasedNoAds` | IAP state |
| `PlayerCoins()` / `SetPlayerCoins()` | Wallet balance |
| `SelectedSkin` | Chosen train/wagon skin |
| `GetUnlockedSkins()` / `SetUnlockedSkins()` | Unlocked skin list |

**Wiping save data:** `SaveController.DeleteSaveFile()` (and the `GameSetting.cleanSaveStart`
toggle) only ever clear the specific keys this list above owns — never `PlayerPrefs.DeleteAll()` —
so nothing outside the save system's own domain is ever touched by a "clean save."

## `GameSetting` (gameplay tuning)

| Field | Default | Notes |
|---|---|---|
| `topSpeed` | 10 | Train cruising speed |
| `accelerationIncrement` | 1 | Ramp rate (units/sec²) toward `topSpeed` |
| `minSwipeDistance` | 45 | Minimum swipe distance to register a turn input |
| `arrowMoveSpeed` / `arrowBounceDistance` | 3 / 0.5 | Stopper direction-arrow animation |
| `startingCoins` | 1000 | New-save wallet balance |
| `baseUnlockPrice` / `priceIncrement` | 250 / 250 | Level-unlock pricing curve |
| `autoSaveDelay` | 0 | Debounce before flushing a dirty save to disk (0 = immediate) |
| `cleanSaveStart` | false | Wipes save data (via the safe key-scoped method above) on next launch |
| `webGLPrefix` | `"RailExpress_"` | PlayerPrefs key prefix |
| `setFrameRateAutomatically`, `defaultFrameRate`, `batterySaveFrameRate` | — | Target frame rate management |
| `requireNetworkToPlay`, `pingUrl`, `pingTimeoutSeconds`, `networkCheckInterval` | — | Connectivity gate before allowing play |

## `ProjectSetting` (project-wide paths)

| Field | Default | Notes |
|---|---|---|
| `dataFolder` | `Assets/Rail Express/Data` | Root for auto-created data assets |
| `scenesFolder` | `Assets/Rail Express/Scenes` | Used by **Actions > Game Scene** to resolve the scene path |
| `GameSceneName` | `Game` | |
| `minimumLoadingTime` | 2.5 | Splash/initializer minimum display time |
| `autoLoadInitializer` | true | Whether Play Mode routes through the Initializer scene first |
| `enableFannecPromotions` | true | See [Overview → The FANNEC Promo system](overview.md#the-fannec-promo-system) |

## Access from code

Both assets follow the same singleton pattern:

```csharp
GameSettingsManager.TopSpeed          // shortcut for GameSetting.topSpeed
ProjectSetting.Instance.scenesFolder
```

Use **Tools > FANNΞC > Rail Express > Game Settings / Project Settings** to jump straight to
either asset in the Inspector.
