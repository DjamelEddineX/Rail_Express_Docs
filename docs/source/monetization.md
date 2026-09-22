# Monetization (Ads & IAP)

## About

Rail Express ships with a complete mobile monetization module covering both advertising and
in-app purchases. It supports **AdMob**, **AppLovin (MAX)**, and **LevelPlay (ironSource)**, plus
a built-in **Dummy** provider for testing without a real network, and it drives banners,
interstitials, and rewarded videos through one shared settings asset. Every ad type is configured
from the Inspector — no code changes are needed to add ads or purchases to your build.

## Usage

The module's settings live on one asset:

```
Assets/Rail Express/Data/AdsSettings
```

Everything in this document is configured on that asset.

Two master toggles at the top of the Inspector control the whole module:

- **Ads Enabled** — turns advertising on or off entirely. With it off, no provider initializes and
  no ad ever shows, regardless of how the rest of the asset is configured.
- **IAP Enabled** — turns in-app purchases on or off entirely. With it off, the Store's purchase
  button has nothing to sell.

## General Module Settings

The **Settings** section on the AdsSettings asset controls the pacing of ads shown during a
session:

- **Load Ads On Start** — when enabled, ad providers begin loading the moment the game launches,
  so an ad is already on hand instead of loading on demand.
- **Interstitial First Start Delay** — seconds after the very first app launch before an
  interstitial is allowed to show, giving a brand-new player a few uninterrupted minutes.
- **Interstitial Start Delay** — seconds after every subsequent app launch before an interstitial
  is allowed to show.
- **Interstitial Showing Delay** — the minimum gap enforced between two interstitials, so players
  are never hit with back-to-back ads.
- **Loading Ad Duration** — how long a "loading ad" message stays on screen at minimum, even if
  the ad is ready sooner. Set to 0 to skip it entirely once the ad is ready.
- **Ad Request Timeout** — how long the game waits for an ad to respond before giving up and
  handing control back to the player.

## Advertisement

### Basic Settings

The **Advertisement** section lets you assign a provider to each ad type independently:

- **Banner Type**
- **Interstitial Type**
- **Rewarded Video Type**

Each dropdown chooses between **Dummy**, **AdMob**, **AppLovin**, or **LevelPlay** — this only
tells the module which provider to call for that ad type, it doesn't configure that provider.
An ad type won't work until its chosen provider is properly set up further down the asset.

There's no separate "off" switch per ad type — leave a slot on **Dummy** to keep it inert during
development, or turn off **Ads Enabled** to stop every ad type at once.

**Dummy** is a no-network provider that shows a placeholder test ad. Use it to verify your reward
and interstitial hookups before wiring up a real network.

## Providers Configuration

Each provider has its own foldout further down the AdsSettings asset. Once its SDK is imported,
the foldout automatically shows a detected/not-detected status, so you always know whether the
matching plugin is present.

### AdMob

1. Open the **AdMob** foldout on the AdsSettings asset and check its detected/not-detected status
   to confirm which plugin version it expects.
2. Download the Google Mobile Ads Unity plugin from its official GitHub releases page and import
   it into the project.
3. On the AdsSettings asset, set **Banner Type**, **Interstitial Type**, and/or **Rewarded Video
   Type** to **AdMob**.
4. AdMob requires your test device's ID before it will serve test ads to you — add it to AdMob's
   test device list following Google's own device ID guide.
5. Create your app on the AdMob dashboard and follow Google's setup guide to register it.
6. Create an Ad Unit for each ad type you plan to use (banner, interstitial, rewarded video).
7. Copy each ID from the AdMob dashboard into the matching field in the **AdMob** foldout.
8. Run **Assets > External Dependency Manager > Android Resolver > Resolve**.
9. Your game is ready to publish. AdMob won't serve live ads until it finishes reviewing the app
   after your first release — until then, only test ads will show.

### LevelPlay

1. Open **Window > Package Manager**, set the source to **Unity Registry**, find the **Ads
   Mediation** package, and install it.
2. On the AdsSettings asset, set **Banner Type**, **Interstitial Type**, and/or **Rewarded Video
   Type** to **LevelPlay**.
3. Open the **LevelPlay** foldout and copy your app key and each ad unit ID from the LevelPlay
   dashboard into the matching fields.
4. Go to **Edit > Project Settings > Player > Publishing Settings** and enable **Custom Main
   Manifest**, **Custom Main Gradle Template**, and **Custom Gradle Properties Template**.
5. Open `Assets/Plugins/Android/AndroidManifest.xml` and add this line right before the
   `<application>` tag:

   ```xml
   <uses-permission android:name="com.google.android.gms.permission.AD_ID"/>
   ```

6. Open `Assets/Plugins/Android/gradleTemplate.properties` and add these lines to the end of the
   file:

   ```
   android.enableDexingArtifactTransform=false
   android.useAndroidX=true
   android.enableJetifier=true
   ```

7. Run **Assets > External Dependency Manager > Android Resolver > Resolve**.
8. Your game is ready to publish.

### + Add your custom

Every provider — including **Dummy**, AdMob, and LevelPlay above — is a plain C# class that
implements `IAdProvider`. `AdsManager` never talks to a network SDK directly; it only calls
methods on whichever `IAdProvider` is assigned to each ad type. Adding your own network means
writing one more class that speaks the same interface.

```
Assets/Rail Express/Scripts/Monetization/Core/IAdProvider.cs
Assets/Rail Express/Scripts/Monetization/Core/AdsManager.cs
Assets/Rail Express/Scripts/Monetization/Providers/Dummy/DummyHandler.cs
```

`IAdProvider` is small:

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

`AdsManager` calls `Initialize` once per ad type at startup (or on demand, depending on **Load Ads
On Start**), then calls `ShowInterstitial`/`ShowRewarded` with a callback your provider must invoke
with `true` (ad watched/closed successfully) or `false` (failed, skipped, or timed out). It also
runs its own timeout watchdog around that callback, so your provider doesn't need one of its own —
just call it exactly once per request.

**Steps:**

1. Add a settings block for your network to `AdSettings.cs`, next to the existing `AdMob
   Settings` / `LevelPlay Settings` / `AppLovin Settings` headers — typically an app key/ID and one
   ad unit ID per ad type you support:

   ```csharp
   [Header("MyNetwork Settings")]
   public string myNetworkAppId = "";
   public string myNetworkAndroidBannerId = "";
   public string myNetworkAndroidInterstitialId = "";
   public string myNetworkAndroidRewardedId = "";
   ```

2. Add your network to the `AdProvider` enum in the same file:

   ```csharp
   public enum AdProvider { Dummy, AdMob, LevelPlay, AppLovin, MyNetwork }
   ```

   This is what makes it selectable from the **Banner Type** / **Interstitial Type** / **Rewarded
   Video Type** dropdowns already described above.

3. Create your provider class under
   `Assets/Rail Express/Scripts/Monetization/Providers/MyNetwork/`, implementing `IAdProvider`.
   Use `DummyHandler.cs` as the shape to follow, and your network's own SDK calls inside each
   method — initialize the SDK in `Initialize`, load/show ads in the `Show...` methods, and invoke
   the callback you were given when the SDK reports a result.

4. Register the new class in `AdsManager.CreateProvider`:

   ```csharp
   private IAdProvider CreateProvider(AdProvider provider)
   {
       switch (provider)
       {
           case AdProvider.Dummy: return new DummyHandler();
           case AdProvider.AdMob: return new AdMobHandler();
           case AdProvider.AppLovin: return new AppLovinHandler();
           case AdProvider.LevelPlay: return new LevelPlayHandler();
           case AdProvider.MyNetwork: return new MyNetworkHandler();
           default: return new DummyHandler();
       }
   }
   ```

5. Import your network's SDK, add whatever manifest/gradle changes it requires (the same pattern
   as step 4–6 of the LevelPlay setup above), and select **MyNetwork** on the AdsSettings asset for
   each ad type you've implemented.

Unlike the built-in providers, adding a new one is not purely an Inspector task — steps 2 and 4
edit project code, so this isn't something a non-programmer buyer can do from the Inspector alone.

```{note}
`IAPManager` is a separate system from `AdsManager` and doesn't use `IAdProvider` — it talks to
Unity IAP (`com.unity.purchasing`) directly, which already supports every major store (Google
Play, Apple App Store, etc.) without a provider class of its own. There's nothing to plug a custom
*ad* network into there; the only IAP-side switch is `useFakeStore` on the AdsSettings asset, which
swaps real purchases for a simulated one for testing.
```
