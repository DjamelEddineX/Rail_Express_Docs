Monetization (Ads & IAP)
########################

About
*****

The Monetization module is a provider-agnostic solution for mobile Ads and In-App Purchases. Every
ad network implements one shared interface, so the rest of the game never has to know which network
is active. It supports **AdMob**, **AppLovin (MAX)**, **LevelPlay (ironSource)** and a built-in
**Dummy** provider for testing, and you can add your own.

Usage
*****

The module is configured on the ``AdSettings`` asset. It can be disabled entirely with the
``adsEnabled`` / ``iapEnabled`` master toggles - with those off, nothing initializes and no ads or
IAPs appear (the buttons may still be visible in the scene but do nothing).

General module settings (``AdSettings``)
****************************************************

* **Master toggles** - ``adsEnabled``, ``iapEnabled``.
* **Timing** - ``interstitialFirstStartDelay``, ``interstitialStartDelay``, ``loadingAdDuration``,
  ``adRequestTimeoutSeconds``.
* **Reward / IAP** - ``useFakeStore``, ``noAdsAndroidProductId`` / ``noAdsIosProductId``,
  ``purchaseText``, ``claimText``.
* **Legal** - ``supportUrl``, ``privacyPolicyUrl``, ``termsOfUseUrl``.
* Per-provider foldouts for Dummy / AdMob / LevelPlay / AppLovin hold each network's ad unit IDs,
  banner position / type and (AppLovin) adaptive banner + background colour.

Advertisement
*************

The provider architecture
-------------------------

Every provider implements ``IAdProvider``:

.. code-block:: csharp

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

``AdsManager`` selects a provider **independently per ad type** - banner, interstitial and rewarded
each have their own choice on ``AdSettings`` - so you can mix and match (e.g. banner via AdMob,
rewarded via AppLovin).

Providers
---------

* **Dummy**:
    * No SDK required. Renders an on-screen test panel with Show / Get Reward / Close buttons.
    * Use this to verify your own gameplay hookups before touching a real network.
* **AdMob**:
    * Requires the Google Mobile Ads Unity plugin.
    * App ID is set at **Assets > Google Mobile Ads > Settings**, not on ``AdSettings``.
    * For testing, paste Google's official test ad unit IDs into the AdMob foldout.
* **AppLovin (MAX)**:
    * Requires the AppLovin MAX Unity plugin and a real SDK key (no universal test key).
    * Use the in-app Mediation Debugger (shake gesture) to force-test each mediated network.
* **LevelPlay (ironSource)**:
    * Requires the LevelPlay Unity SDK. Auto-serves test networks for apps not yet approved for
      live traffic. Use its built-in Test Suite to verify per-network init status.

``Editor/DependencyDetector.cs`` automatically adds the matching scripting define
(``TT_ADS_ADMOB``, ``TT_ADS_APPLOVIN``, ``TT_ADS_LEVELPLAY``) the moment it detects the
corresponding SDK class - you never set these manually, and the **Ads Settings** Inspector shows a
green / red status per provider.

Verifying in the Console
------------------------

All four providers share ``AdsManager``'s generic init lines - ``Banner (X) Ready.`` /
``Interstitial (X) Ready.`` / ``Rewarded (X) Ready.``. If one never appears, that provider's
``Initialize()`` never completed.

In-App Purchasing
*****************

``IAPManager`` handles the **No Ads** purchase and purchase restoration.

* **No Ads** disables forced ads (banners, interstitials); rewarded videos still work. On success,
  ``SaveController.HasPurchasedNoAds`` is set and the IAP button hides itself.
* **Use Fake Store** (``AdSettings``) simulates purchases in the Editor without a real store
  connection.

The FANNEC Promo banner
***********************

A small Editor-only popup (``Editor/PromotionManager.cs`` + ``Editor/PromotionWindow.cs``) can
show a promo banner - controlled by ``ProjectSetting.enableFannecPromotions``. It **only** checks
on genuine Editor startup / script recompile, never on every Play Mode press.

Condition A - first template install (local)
--------------------------------------------

* **What it does**:
    * Shown exactly once per machine, using a one-time ``EditorPrefs`` flag
      (``RailExpress_FirstRunPromoShown``).
    * No network required - it loads a bundled local image.
* **Image path**: ``Assets/Rail Express/Textures/Editor/Editor_PromoBanner_Default.png``. If the
  file is missing, the window draws a plain placeholder instead of a blank panel.
* **Testing**:
    * **Tools > FANNΞC > Rail Express > Actions > Promo > Force Show First-Run Banner** - instant
      preview, doesn't touch the flag.
    * **... > Promo > Reset First-Run Flag** - clears the flag so the *next* Editor startup
      triggers Condition A for real.

Condition B - remote web push
-----------------------------

* **What it does**:
    * On every Editor startup, ``PromotionManager`` fetches a small JSON file hosted online.
    * If it returns a ``campaignId`` different from the last one seen, it downloads and shows that
      banner instead.
    * A failed fetch, malformed response, or repeat campaign shows nothing - no local fallback for
      Condition B.
* **JSON shape**:

.. code-block:: json

   {
     "title": "Check Out My New Game!",
     "bannerUrl": "https://yourdomain.com/promo/banner.png",
     "targetUrl": "https://yourdomain.com/store-link",
     "campaignId": "campaign-2026-01"
   }

* The window title is ``FANNEC PROMO`` unless the remote JSON supplies its own ``title``.
