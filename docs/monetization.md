# Monetization (Ads & IAP)

## Architecture

Every ad provider implements one shared interface, `IAdProvider`, so the rest of the game never
has to know which network is active:

```csharp
public interface IAdProvider
{
    bool IsInitialized { get; }
    bool HasInterstitialLoaded { get; }
    bool HasRewardedLoaded { get; }
    void Initialize(AdSettings settings, Action onInitialized);
    void ShowBanner();
    void HideBanner();
    void ShowInterstitial(Action<bool> onClosed);
    void ShowRewarded(Action<bool> onRewardResult);
}
```

`AdsManager` selects a provider **independently per ad type** — banner, interstitial, and rewarded
each have their own `AdProvider` choice on the `AdSettings` asset, so you can mix and match (e.g.
banner via AdMob, rewarded via AppLovin).

### Providers

| Provider | Notes |
|---|---|
| **Dummy** | No SDK required. Renders an on-screen test panel with Show/Get Reward/Close buttons — use this to verify your own gameplay hookups before touching a real network. |
| **AdMob** | Requires the Google Mobile Ads Unity plugin. App ID is set at **Assets > Google Mobile Ads > Settings**, not on `AdSettings`. |
| **AppLovin (MAX)** | Requires the AppLovin MAX Unity plugin and a real SDK key (no universal test key). |
| **LevelPlay (ironSource)** | Requires the LevelPlay Unity SDK. Auto-serves test networks for apps not yet approved for live traffic. |

`Editor/DependencyDetector.cs` automatically adds the matching scripting define
(`TT_ADS_ADMOB`, `TT_ADS_APPLOVIN`, `TT_ADS_LEVELPLAY`) the moment it detects the corresponding SDK
class in the project — you never set these manually, and the **Ads Settings** Inspector shows a
green/red status per provider so you always know whether a network is wired up.

## Testing each provider

- **Dummy** — works immediately in Play Mode, no setup.
- **AdMob** — paste Google's official test ad unit IDs into the AdMob foldout while testing
  (search "AdMob test ad unit IDs" for the current list); requires a real device build, doesn't
  render in the Editor.
- **AppLovin** — needs a real SDK key even for testing; use the in-app Mediation Debugger (shake
  gesture) to force-test each mediated network.
- **LevelPlay** — use its built-in Test Suite to verify per-network init status.

All four providers share `AdsManager`'s generic init log lines
(`"Banner (X) Ready."` / `"Interstitial (X) Ready."` / `"Rewarded (X) Ready."`) — if one of those
never appears in the Console, that provider's `Initialize()` never completed.

## In-App Purchases

`IAPManager` handles the "No Ads" purchase and purchase restoration. A **Use Fake Store** toggle on
`AdSettings` lets you simulate purchases in the Editor without a real store connection while
testing the surrounding UI/flow.

## Settings reference (`AdSettings`)

- **Master toggles** — `adsEnabled`, `iapEnabled`.
- **Timing** — `interstitialFirstStartDelay`, `interstitialStartDelay`, `loadingAdDuration`,
  `adRequestTimeoutSeconds`.
- **Reward/IAP** — `useFakeStore`, `noAdsAndroidProductId` / `noAdsIosProductId`, `purchaseText`,
  `claimText`.
- **Legal** — `supportUrl`, `privacyPolicyUrl`, `termsOfUseUrl`.
- Per-provider foldouts for Dummy / AdMob / LevelPlay / AppLovin hold each network's own ad unit
  IDs, banner position/type, and (for AppLovin) adaptive-banner + background color options.
