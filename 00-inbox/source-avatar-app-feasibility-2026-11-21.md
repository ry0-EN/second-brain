# ホーム画面アバターアプリ 実現可能性リサーチ（2026-11-21 Muse収集）

# Android Home-Screen Avatar App — Technical Feasibility

**Date:** 2026-11-21 · **Scope:** Personal, self-use, sideloaded, NOT published on Google Play. Kotlin, written mostly by an AI coding agent (Claude Code), directed by a non-programmer owner.
**Method:** Official Android developer documentation preferred for platform restrictions; vendor pricing pages for APIs; app listings/reviews for precedents. Anything not confirmed on a source page is labelled **[unverified]**.

## Summary — the short answer

**The concept is feasible, and the overlay route is the right one.** Every core piece has a shipped precedent (Shimeji-type apps have done the walking overlay pet at 10M+ installs) and a documented Android API. Nothing in Android 12–15 makes the concept impossible for a *sideloaded, single-user* app — most of the harshest modern rules (Play foreground-service declarations, `specialUse` justification review, Play Protect developer verification) are Play-store gates that a personal sideload simply does not pass through. The real costs are: (1) a permanent foreground-service notification, (2) battery drain proportional to frame rate and pet count, (3) OEM battery killers that must be whitelisted by hand on Xiaomi/Samsung/Huawei-type phones, (4) fiddly soft-keyboard focus handling in the overlay chat panel, and (5) the chat "brain" cannot be the owner's personal Muse agent itself — but, contrary to the assumption in the brief, **Meta now sells a public Muse model API (verified 2026-11-21)**, so the avatar can be powered by the Muse Spark model, just not by the owner's existing personal Muse with its memory and tools.

Recommended v1 architecture: foreground service (`specialUse` type) → `TYPE_APPLICATION_OVERLAY` window holding a small sprite-sheet character (PNG frames, `AnimationDrawable`/custom `View` at ~12–24 fps, paused when screen is off) + a second, focusable overlay window for the chat panel → HTTPS call to an LLM API (Meta Model API / Claude Haiku / Gemini Flash-Lite all cost roughly $0.50–$2/month at personal chat volumes; see §6 worked estimate).

---

## 1. Overlay approach — SYSTEM_ALERT_WINDOW / TYPE_APPLICATION_OVERLAY

**How it works.** Declare `android.permission.SYSTEM_ALERT_WINDOW`, check `Settings.canDrawOverlays(context)`, and if false send the user to the system settings screen with `Settings.ACTION_MANAGE_OVERLAY_PERMISSION` — this is a *special app-access* grant, not a normal runtime permission; the user must toggle it in Settings, the app cannot grant it itself. Since Android 8.0 (API 26) overlay windows must use `WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY`, added via `WindowManager.addView()` from a Service. Overlay windows sit above all app windows but **below critical system windows such as the status bar and the IME (keyboard)** — which is actually convenient for chat (§5).
Sources: https://developer.android.com/reference/android/service/wallpaper/WallpaperService (window-type context) · permission/flow summary at http://umatechnology.org/android-overlays-explained-permission-setup-and-limits/ · official behaviour-change doc https://developer.android.com/about/versions/12/behavior-changes-all?hl=en&authuser=6

**Android 12–15 restrictions that actually bite:**

- **Untrusted-touch blocking (Android 12+).** If your overlay lets touches pass through (`FLAG_NOT_TOUCHABLE`), touches that pass through an obscuring overlay are *blocked* for the app underneath unless an exception applies (invisible window, opacity limits, your own app, trusted windows like IME/accessibility). Practical consequence: make the avatar window **exactly avatar-sized** (not full-screen transparent), so it only ever obscures its own pixels; use a separate tiny window rather than one full-screen canvas. Source: https://developer.android.com/about/versions/12/behavior-changes-all?hl=en&authuser=6
- **Apps can opt out of being overlaid (Android 12+).** An app holding `HIDE_OVERLAY_WINDOWS` (typical: banking, password, payment apps) can hide other apps' overlays over itself. Your pet will simply vanish over those screens — expected, not a bug. Source: https://developer.android.com/security/fraud-prevention/activities?authuser=0
- **Foreground service is mandatory for an always-on pet.** Since Android 8, background services are killed; since Android 12 an app generally **cannot start a foreground service from the background** except in listed exemptions. Android 15 tightened the SYSTEM_ALERT_WINDOW exemption: to start an FGS from the background the app must hold SAW *and currently have a visible overlay window*. Source: https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start?hl=en&authuser=00
- **FGS type declaration (Android 14+).** Every foreground service must declare a type or `startForeground()` throws `MissingForegroundServiceTypeException`. The avatar fits **`specialUse`** ("covers any valid foreground service use cases that aren't covered by the other types"), permission `FOREGROUND_SERVICE_SPECIAL_USE`, plus a `<property android:name="android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE" …>` explanation in the manifest. That subtype text is *reviewed in Play Console* — irrelevant for a sideload. Do **not** use `dataSync`: Android 15 caps `dataSync`/`mediaProcessing` FGS at **6 hours total per 24 h** and then force-stops them — fatal for an all-day pet, and `specialUse` has no such cap in the docs found. Sources: https://developer.android.com/about/versions/14/changes/fgs-types-required · https://developer.android.com/develop/background-work/services/fgs/service-types?authuser=7 · https://developer.android.com/develop/background-work/services/fgs/timeout?hl=en&authuser=002
- **Persistent notification.** A foreground service must post an ongoing notification the user can see (Android 13+ also needs `POST_NOTIFICATIONS` granted for it to be fully visible; users can swipe/hide it in some versions, which can stop the service on some OEM builds — **[unverified] OEM-dependent**). This is a permanent cosmetic cost of the design.
- **Boot restart.** A `BOOT_COMPLETED` receiver may not launch `dataSync`, `camera`, `mediaPlayback`, `phoneCall`, `mediaProjection`, or `microphone` FGS on Android 15 — `specialUse` is not on that list, so auto-restarting the pet after reboot via BOOT_COMPLETED + specialUse appears allowed; alternatively the user just taps the app icon. Source: https://developer.android.com/about/versions/15/behavior-changes-15?authuser=002
- **Doze / App Standby.** With the screen off, Doze suspends network and defers CPU work — irrelevant if you do the right thing and **pause animation and timers when the screen turns off** (Shimeji does exactly this). With the screen on and an FGS running, stock Android (Pixel) rarely kills it. Source: https://developer.android.com/training/monitoring-device-state/doze-standby?hl=en&authuser=1
- **OEM task killers are the #1 real-world killer.** Xiaomi/HyperOS (autostart off by default), Samsung One UI (sleeping/deep-sleeping apps), Huawei, Oppo/Vivo add their own killers on top of AOSP. The fix is manual, per-device: set the app's battery to *Unrestricted*, enable autostart where offered, lock it in Recents. The canonical per-vendor instructions are at https://dontkillmyapp.com/ (referenced via https://github.com/fluttercommunity/flutter_workmanager/blob/HEAD/docs/troubleshooting.mdx and https://dev.to/szymonwalczak/surviving-android-battery-killers-in-capacitor-apps-4im7). For a one-user app this is a 5-minute setup chore, not a blocker.
- **Battery impact.** No controlled benchmark for this exact app was found **[unverified numbers]**. Evidence from the closest precedent (§3): the Shimeji developer states pets pause with the screen off and drain is "negligible" for a small cast, while users consistently report noticeable drain with 4–10 pets. Engineering expectation: one small sprite at 12–24 fps, screen-on only, should be a few percent of battery per hour of screen time at most; a 60 fps full-screen transparent overlay would be far worse (GPU never idles, and a full-screen window also worsens the untrusted-touch problem). Keep the window tiny, the frame rate low, and pause on screen-off / when the chat is idle.

**Verdict §1: Possible with caveats — the standard, proven route; caveats are the permanent notification, hand-whitelisting against OEM killers, and using `specialUse` (not `dataSync`).**

---

## 2. Alternatives comparison

| Approach | Walking character on home screen? | Tap → chat on home screen? | Keyboard chat? | Effort / fatal flaw |
|---|---|---|---|---|
| **Overlay (§1)** | Yes — anywhere, also over other apps | Yes — second focusable overlay window | Yes, with FLAG toggling (§5) | Medium. Needs SAW + FGS. **Best fit.** |
| **(a) Live Wallpaper** (`WallpaperService`) | Yes — genuinely *on* the home screen, behind icons; `Engine.setTouchEventsEnabled(true)` + `onTouchEvent()` and `onCommand()` (e.g. double-tap) exist | Partially — wallpaper can *react* to taps and draw a speech bubble on its Canvas/Surface, but it has **no window focus and no IME**: it cannot host an `EditText` | **No** — must launch an Activity for real text input, breaking the "chat right there" requirement | Medium. Also: user must give up their current wallpaper; pet disappears inside apps (it's only on the launcher); some launchers don't forward touch events reliably **[unverified, launcher-dependent]**. Sources: https://developer.android.com/reference/android/service/wallpaper/WallpaperService?authuser=2 · https://learn.microsoft.com/en-us/dotnet/api/android.service.wallpaper.wallpaperservice.engine.settoucheventsenabled?view=net-android-34.0 |
| **(b) Home-screen widget** (AppWidget / Glance → `RemoteViews`) | **No, not really** — `RemoteViews` has no frame loop, no Canvas/custom views, clicks only, no gestures or text input; system `updatePeriodMillis` minimum is 30 min. Frame-cycling bitmaps via frequent `updateAppWidget()` calls is a known hack and is janky + battery-hostile | Tap can only fire a `PendingIntent` → opens an Activity | No | Low effort, wrong tool. Sources: https://blogs.mobilebytesensei.com/blog/glance-widgets/ · https://pub.dev/documentation/flutter_android_widgets/latest/ |
| **(c) Full custom launcher** | Yes — total control of the home screen; avatar is a normal View in your own Activity, full Compose animation, chat is a normal screen with a normal keyboard (the *easiest* chat of all options) | Yes, natively | Yes, natively | **High.** You must reimplement the home screen itself: app grid/drawer, launching apps, widget hosting (`AppWidgetHost`), folders, gestures, default-home role (`CATEGORY_HOME` + `CATEGORY_DEFAULT` intent filter, Android 10+ role request), package-visibility declarations. And the pet then exists *only* in your launcher — never over other apps. Sources: https://www.androidauthority.com/make-a-custom-android-launcher-837342-837342/ · http://codezup.com/custom-android-launchers-guide/ |

A hybrid worth noting: **overlay for the pet + a transparent Activity for chat** (tap bubble → a half-screen Activity styled as a floating panel). It sacrifices the pure "never leaves the home screen" feel but makes keyboard, voice, scrolling history, and Compose UI all trivial. Many commercial floating-chat apps do exactly this. Keep it as the fallback if overlay-IME quirks (§5) annoy.

**Verdict §2: Possible with caveats — overlay wins; live wallpaper is a respectable pet-only variant that cannot do in-place chat; widgets are a dead end for animation; a custom launcher works but is 5–10× the work and loses the over-other-apps magic.**

---

## 3. Precedents

- **Shimeji: Play with Screen Pets (Android, Digital Cosmos)** — the direct precedent. 10M+ downloads, ~4.5★ across ~384k reviews (Play listing, crawled Oct 2026). Pets walk, climb screen edges, sit, sleep, can be dragged/flung, up to 10 at once. Tech, per its listing/reviews and independent reviews: requires the **"display over other apps" permission** (i.e. the §1 overlay-service architecture; no evidence it uses an accessibility service, and none is needed for this feature set), **Ghost Mode** = touch pass-through (the `FLAG_NOT_TOUCHABLE` pattern of §1), characters are **PNG frame sequences** (it imports classic PC Shimeji packs = PNG frames + XML behaviour files, and has a frame-by-frame pixel editor). Battery/stability reports: developer says pets pause when the screen is off and drain is negligible for a small cast; a paying user review (16 Jul 2026) says "it does drain your battery. I keep my phone on battery save mode all the time and that fixes it"; independent review consensus: drain scales steeply with pet count (keep 1–2 for all-day use). Sources: https://play.google.com/store/apps/details?id=com.digitalcosmos.shimeji&hl=en-gb&gl=bh · https://www.appireview.com/com.digitalcosmos.shimeji · https://shimeji-pals-anime-screen-pet.en.softonic.com/android (a clone, same overlay pattern)
- **Original Shimeji (Windows, 2009, Yuki Yamada / Group Finity)** and modern **Shijima** — behaviour defined in XML over PNG frame sets; the asset format is a useful free starting point for walk/sit/fall poses. Source: https://www.aidorable.ai/blog/shimeji-app
- **Desktop Mate (Steam, infiniteloop, Jan 2025)** — Windows/macOS only, 3D characters that sit on window title bars, react to cursor, voice lines, alarm. Proves demand, proves *nothing* about Android tech (desktop OSes have no overlay permission model). Source: https://store.steampowered.com/app/3301060/Desktop_Mate?snr=1_241_4_animationmodeling_salesmartpopularpurchased&curator_clanid=41316928
- **Desktop Goose-style apps** — Windows novelty (goose steals cursor/notes); Android knock-offs exist as overlay pets under the same SAW model **[unverified for any specific Android goose app]**.
- **Accessibility-service route:** some floating-button/assistive apps do use `TYPE_ACCESSIBILITY_OVERLAY` (a trusted window exempt from untrusted-touch blocking), but using Accessibility for a pet is off-label: Google restricts it, it scares users with a much scarier permission prompt, and it buys nothing this app needs. **Recommendation: do not use it.**

**Verdict §3: Straightforward as a concept — shipped, popular precedent on exactly the §1 architecture with PNG sprites; battery complaints are the known, manageable cost.**

---

## 4. Avatar animation options

| Option | Code effort (AI-written Kotlin) | Asset effort for a non-artist owner | Cost / licence | Fit |
|---|---|---|---|---|
| **PNG sprite sheets / frame sequences** | **Lowest.** One custom `View`/`ImageView`, a timer/Choreographer loop, swap frames; walk = move x + loop walk frames, sit = static frame set. State machine (idle/walk/run/sit) is ~a few hundred lines an AI writes reliably | **Highest per-pose but simplest to source:** need ~4–8 frames × (walk, run, sit, idle). Free Shimeji packs, itch.io sprite packs, or AI-generated frames (consistency between frames is the pain point) | Free; check pack licences | **Recommended for v1** — this is what Shimeji itself uses |
| **Jetpack Compose Canvas custom drawing** | Medium — draw a vector/procedural character with `Canvas`, animate parameters. Works in an overlay only with extra plumbing (you must supply `LifecycleOwner`/`SavedStateRegistryOwner`/`ViewModelStoreOwner` to a Compose view hosted in a Service window — a known, fiddly pattern **[well-known pattern; no single source cited]**) | Zero raster assets, but the character is limited to what code-drawn shapes look good doing — usually crude | Free | Good for a geometric/robot pet; poor for a cute character |
| **Lottie** | Low — `LottieAnimationView`/Compose Lottie, play/loop segments. Also a plain View, so it drops into an overlay window easily | Medium — needs After Effects/Bodymovin JSON or a Lottie editor; walk-cycle *locomotion* (character translating + legs) is awkward: Lottie plays in place, you still move the window yourself | Library free/open-source (Airbnb, Apache/MIT-family). Sources: https://new.airbnb.tech/opensource/lottie/ · https://openhub.net/p/lottie | Nice for idle/bubble micro-animations; mediocre as the main locomotion system |
| **Live2D Cubism SDK** | **High** — Cubism SDK for Java exists and "can be called from the Kotlin side", Android support listed to API 34 on the SDK page; integration (model loading, motion blending, physics, lip-sync) is the most complex option here and the least "AI writes it blind" friendly | **High** — needs a rigged Cubism model: layered PSD artwork + hours in Cubism Editor (free tier exists with limits). Rigging is a skilled manual task an AI cannot do for the owner | SDK free to download/develop; publication licence required at publish, **individuals/small-scale enterprises exempt** (except "Expandable Application") — a personal sideload should fall under the exemption, but read the terms. Source: https://www.live2d.com/en/sdk/about/ | Best-looking results (VTuber-style), worst fit for a beginner v1. Phase-2 upgrade |
| **Spine** | Medium-high — skeletal runtime; no first-class plain-Android/Kotlin runtime story as clean as its Unity/Godot ones **[unverified for current Android-native runtime status]**; usually adopted via a game engine | Medium — rig one character once, get walk/run/sit from one rig (far less drawing than sprite sheets) | Editor: Essential $69 / Professional $379 one-time (discounted list $99/$449). Sources: https://blog.makko.ai/ai-animation-tools-for-2d-characters/ · https://egmatic.com/blog/sprite-animation-software | Powerful but over-engineered for one pet |
| **Unity (game engine)** | High for this use — C# not Kotlin; Unity app is a full-screen Activity by nature; embedding it *inside a small overlay window/service* is fighting the engine; large APK/runtime overhead and worse battery for an always-on background pet | Same asset problem as above, plus engine pipeline | Free tier exists for small revenue; pricing changes frequently **[unverified current tier terms]** | **Not recommended** for an always-on overlay pet |

**Verdict §4: Straightforward if you choose PNG sprite sheets for v1 (Lottie as garnish); Live2D/Spine/Unity are possible with caveats and are all phase-2-or-never for this owner.**

---

## 5. Chat UI inside an overlay

**The keyboard problem is real, known, and solved.** Overlay windows are normally created with `FLAG_NOT_FOCUSABLE` so they don't steal input from the app beneath — but a non-focusable window can never receive IME input, so an `EditText` inside it will never raise the soft keyboard. The standard workaround (documented in the widely-followed "Floating Windows on Android" series):

1. Avatar window: `FLAG_NOT_FOCUSABLE` (+ `FLAG_NOT_TOUCHABLE` only in a "ghost" mode).
2. When the bubble is tapped, open the chat window (or update its LayoutParams) **without** `FLAG_NOT_FOCUSABLE`, call `requestFocus()` on the input field, and show the IME via `InputMethodManager`.
3. Use `FLAG_WATCH_OUTSIDE_TOUCH` on a container view to detect taps outside the chat panel; on outside-tap, re-add `FLAG_NOT_FOCUSABLE` and dismiss/hide the keyboard.
4. Remember the IME is a *higher* window than `TYPE_APPLICATION_OVERLAY`, so the keyboard will correctly cover the bottom of the screen; the chat panel must reposition/resize above it (listen to window insets / measure the visible display frame — expect 1–2 iterations of fiddling per device, the classic pain point).

Sources: https://dev.to/localazy/6-floating-windows-on-android-keyboard-input-phd · https://exchangetuts.com/how-to-display-the-soft-keyboard-from-a-service-1640244303511050

Expect quirks: keyboard behaviour varies slightly by OEM IME (Gboard vs Samsung Keyboard), predictive-text/autocorrect popups occasionally mis-anchor, and copy-paste menus can be flaky in service windows **[ anecdotal developer reports; unverified per-device]**. None are blockers; all are why the §2 transparent-Activity fallback exists.

**Voice input.** `android.speech.SpeechRecognizer`:
- Requires `RECORD_AUDIO` runtime permission.
- Official warning: "The implementation of this API is likely to stream audio to remote servers… **not intended to be used for continuous recognition**, which would consume a significant amount of battery and bandwidth." → Push-to-talk (tap mic, speak one utterance, tap again) is the correct UX; always-listening wake-word is **not** supported by this API.
- Offline: `SpeechRecognizer.createOnDeviceSpeechRecognizer()` + `isOnDeviceRecognitionAvailable()` exist; availability and language packs are device-dependent (best on Pixels with downloaded languages). Design: try on-device, fall back to default (network) recognizer.
- Android 12+ shows the green microphone privacy indicator and honours the system mic kill-switch; Android 14+ microphone-type FGS can only be *created* while the app is visibly in use (while-in-use permission rules) — fine here because the user taps the mic in a visible overlay, but do not design background listening. Sources: https://developer.android.com/reference/android/speech/SpeechRecognizer?authuser=45 · https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start?hl=en&authuser=00
- Alternative: Meta's Muse Voice Transcribe API at $0.18/hour of audio if cloud STT is ever wanted (§6). Source: https://dev.meta.ai/docs/overview

**Spoken replies.** `android.speech.tts.TextToSpeech` — built-in, free, offline-capable with downloaded voices, ~30 lines: init with `OnInitListener`, `speak(text, QUEUE_FLUSH, …)`, `shutdown()` on destroy. Voice quality is "phone TTS", not assistant-grade; cloud TTS is an optional upgrade. Source: https://developer.android.com/reference/kotlin/android/speech/tts/TextToSpeech?source=post_page-----109c342ecdd1-----------------------------------------

**Verdict §5: Possible with caveats — chat-in-overlay with a working keyboard is a solved pattern (toggle `FLAG_NOT_FOCUSABLE`), voice is push-to-talk only, TTS is straightforward.**

---

## 6. The chat "brain"

### 6.1 Meta Muse — the brief's expectation is outdated: there IS a public API (but not *your* Muse)

Verified by opening Meta's developer docs on 2026-11-21: **Meta Model API** is a pay-as-you-go inference API — base URL `https://api.meta.ai/v1`, bearer `MODEL_API_KEY`, OpenAI- and Anthropic-SDK-compatible surfaces, models `muse-spark-1.3`, `muse-ember-1.0`, `muse-wonder-1.0` (preview). Pricing (Standard mode): Muse Spark **$1.25 input / $4.25 output per MTok**; Muse Ember **$0.10 / $0.50** (≤200k context); Muse Wonder **$4.00 / $20.00**. A discounted **Contributor mode** for Spark ($0.10/$0.20) exists *in exchange for permission to use your content to train future Meta models* — a real privacy trade-off to choose knowingly. Sources: https://dev.meta.ai/docs/overview · https://dev.meta.ai/docs/pricing-rate-limits.md

**Critical distinction:** this API gives you the Muse *model* with a system prompt you write. It does **not** give your app the owner's existing **personal Muse agent** — the assistant in the Muse product with its accumulated personal context, memory, tools and connected apps. No source found documents any API that exposes that personal-agent state to a third-party/personal app **[no such integration documented as of 2026-11-21]**. So the avatar can *be* a Muse-Spark-powered character with a Muse-like persona you define, but it will not "be" the owner's Muse, remember their life, or act in their other apps — unless you build your own memory (store chat history/summary on-device and inject it into the prompt, which is easy and recommended).

### 6.2 Alternatives compared

Worked cost estimate **[author's arithmetic on the cited list prices]**: 20 chats/day × 30 days = 600 turns/month, ~1,000 input + ~300 output tokens per turn → 0.6 MTok in / 0.18 MTok out per month.

| Brain | Cost model | ≈ Cost at estimate above | Latency | Privacy | Complexity |
|---|---|---|---|---|---|
| **Meta Model API — Muse Spark 1.3** | $1.25/$4.25 per MTok (Standard); $0.10/$0.20 Contributor | ~$1.50/mo Standard; ~$0.10 Contributor | Cloud, typically 1–3 s to first token **[unverified, typical]** | Standard: API data terms; Contributor: **your content may train Meta models** | Low — OpenAI-compatible REST from Kotlin (OkHttp/Ktor) |
| **Meta Model API — Muse Ember 1.0** | $0.10/$0.50 per MTok | ~$0.15/mo | Cloud, fastest/cheapest tier | As above | Low; quality below Spark — good default for casual chat, escalate hard questions to Spark **[design suggestion]** |
| **Anthropic Claude API** | Haiku 4.5 **$1/$5**, Sonnet 4.6 **$3/$15** per MTok (rate card effective 2026-06-29) | Haiku ~$1.50/mo; Sonnet ~$4.50/mo | Cloud 1–3 s **[unverified, typical]** | Anthropic API data terms; no training on API data by default per Anthropic policy **[policy detail unverified in this pass]** | Low — Messages API REST. **Billing separation verified:** Claude Pro subscription ≠ API access; API is separate Console billing, pay-per-token. Secondary sources note a 2026 change — Max/Team plans now bundle monthly API credits, Pro still does not. Sources: https://www-cdn.anthropic.com/files/4zrzovbb/website/53da0764b66f75f6cc5521ed77e3e6426f144989.pdf · https://aionx.co/claude-ai-reviews/claude-pro-api-access/ · https://www.activepieces.com/blog/claude-api-pricing-2026-rates-for-every-model |
| **OpenAI API** | e.g. GPT-5 mini **$0.25/$2.00** per MTok | ~$0.50/mo | Cloud | OpenAI API data terms | Low — the most-documented REST shape; also what Meta's API is compatible with, so swapping providers is a base-URL + key change |
| **Google Gemini API (cloud)** | Gemini 3.1 Flash-Lite **$0.25/$1.50** per MTok; a free tier exists for Flash-class models | ~$0.40/mo, possibly $0 on free tier within its limits | Cloud | Google API terms; free tier data may be used to improve products **[terms detail unverified in this pass]** | Low. Sources: https://llmlearner.com/models/gemini-3-1-flash-lite/pricing · https://agentping.io/llm-api-pricing/gemini |
| **Gemini Nano (on-device, via AICore / ML Kit GenAI)** | $0 per call, forever | $0 | Fastest (no network), works offline | **Best possible** — nothing leaves the phone | Medium, and **capability/device-gated**: only on supported (mostly flagship/Pixel) devices, small model (weaker chat, limited context, task APIs like summarise/rewrite + Prompt API), availability must be checked at runtime with a cloud fallback. Sources: https://hokai.io/hub/models/gemini-nano · https://www.theagentecosystem.com/blog/on-device-ai-models-2026 |
| **Bridge to home PC/VM running Claude Code headlessly** | Your existing Claude subscription / API key on the PC; electricity only | ~$0 marginal if subscription already paid | **Worst** — phone → home network → agent loop with tool overhead; seconds to tens of seconds; fails when PC asleep/offline | **Best cloud-free option for a "real agent"**: data stays on your LAN/PC if accessed via VPN (e.g. Tailscale **[unverified recommendation]**); but you are exposing a code-execution agent to a network endpoint — lock it down (private VPN only, auth token, no port-forwarding) | **High.** `claude -p` / Agent SDK headless mode is officially documented (https://code.claude.com/docs/en/headless/), so a tiny HTTP/WebSocket relay on the PC is buildable by an AI agent, but session management, streaming, timeouts and security are all on you. Also note Claude Code is a *coding* agent — using it as a chat brain is off-label; the plain Claude API with a persona prompt is a better chat experience for 1% of the effort |

**Security note applying to all direct-from-phone API designs:** the API key lives in the APK. For a personal sideload on your own phone that is acceptable (worst case: rotate the key), but set a low monthly spend cap in the provider console on day one.

**Verdict §6: Possible with caveats — a Muse-powered brain is now genuinely available via Meta Model API (~$0.15–$1.50/mo at personal volumes) and is the closest match to the owner's wish; but it is the Muse model, not the owner's personal Muse agent, and the Claude-API / Gemini / OpenAI alternatives are equally easy and comparably cheap. The Claude-Code bridge is possible but hard and not recommended as the primary brain.**

---

## 7. Build / dev workflow with Claude Code

- **Headless build: yes, completely.** Official docs: the Gradle wrapper builds from any terminal — `./gradlew assembleDebug` produces a debug APK (auto-signed with the SDK debug key) in `…/build/outputs/apk/`, and `./gradlew installDebug` builds *and* installs on a connected device/emulator. Source: https://developer.android.com/build/building-cmdline?hl=en&authuser=002
- **Headless Linux VM recipe:** JDK 17+ (required by current Android Gradle Plugin) + Android SDK **command-line tools only** (`sdkmanager` installs `platform-tools`, `build-tools`, `platforms;android-35` etc.), accept licences with `sdkmanager --licenses`, set `ANDROID_HOME`. No Android Studio, no GUI, no display needed. Claude Code running in that VM can write Kotlin, run Gradle, read compiler errors, and iterate — this is a well-trodden agentic workflow. Sources: https://developer.android.com/build/building-cmdline?hl=en&authuser=002 · https://agenticdevelopercookbook.com/appendix/research/developer-tools/android/android-build-and-emulator
- **Testing on the real phone via adb:** enable Developer Options + USB debugging once; `adb devices`, `adb install app-debug.apk`, `adb logcat` for crash logs (essential: the AI cannot fix what it cannot see — pipe logcat back to it). Wireless debugging (Android 11+, `adb pair`) removes the cable. An emulator on a headless VM is possible but slow without KVM/GPU and is a poor substitute for overlay/IME/OEM testing — **test overlays on the real phone, always**, because OEM behaviour (§1) is the variable.
- **What genuinely needs Android Studio GUI?** Almost nothing for this project. Studio is *convenient* for: Layout Inspector / Compose Preview (visual UI debugging for a non-programmer owner who wants to *see* layouts), the Profiler (battery/CPU graphs), and Device Manager for emulators. A pragmatic setup: VM/CLI for Claude Code builds + real phone for testing; optionally install Studio on any desktop purely as a viewer/profiler. A non-programmer owner can operate the whole loop by asking Claude Code to build, then installing via `adb` (or opening the APK from the phone's file manager).
- **Signing for personal use:** debug builds are already signed (debug key) and install fine. For a "permanent" install, generate one release keystore with `keytool`, sign release builds with it (Gradle signing config), and **back the keystore up** — Android will refuse to update an installed app whose signature changes, so losing it means uninstall (losing app data) to install a differently-signed build.
- **Sideloading & Play Protect:** installing via `adb install` avoids most friction. Installing the APK file directly requires the per-source "Install unknown apps" allowance (Android 8+). Play Protect scans apps from all sources, warns about potentially harmful apps, "may prevent an application from being installed that is unverified and uses sensitive device permissions", and may reset app permissions — an overlay + microphone + foreground-service app is exactly the profile that can trigger a scary-looking warning on first install. For your own self-built APK this is normally a "Install anyway / scan" tap-through, but expect it, and expect Play Protect to occasionally re-prompt after updates. Source: https://support.google.com/android/answer/2812853?hl
  - Emerging, **[unverified in this pass]**: reports of phased Android "developer verification" for sideloading starting in some countries in late 2026, with ADB installs remaining available — another reason to standardise on `adb install`.

**Verdict §7: Straightforward — CLI-only Kotlin/Gradle builds on a headless Linux VM + adb install/logcat on a real phone is a fully supported, AI-agent-friendly loop; Android Studio is optional tooling, not a requirement.**

---

## 8. Risks and gotchas list (Android 12–15, this exact concept)

1. **Lock screen / keyguard:** `TYPE_APPLICATION_OVERLAY` windows do **not** show over a secure keyguard by default; the pet disappears on the lock screen. `FLAG_SHOW_WHEN_LOCKED` applies to top-most full-screen *activity* windows, not a fix for a service overlay pet. Accept: no pet on the lock screen. Source: https://developer.android.com/reference/kotlin/android/view/WindowManager.LayoutParams.html?authuser=437
2. **Hidden over sensitive apps:** `HIDE_OVERLAY_WINDOWS` apps (banking, payments, password fields in some apps) hide your overlay; also Android 12 untrusted-touch blocking can eat taps near a large/transparent overlay — keep windows tight to the artwork. (§1)
3. **Secure content:** windows flagged `FLAG_SECURE` (streaming/banking) may composite oddly with overlays and the pet won't appear in screenshots/screen-recordings of those apps — cosmetic only.
4. **Wrong FGS type = dead pet:** `dataSync` dies at 6 h/day on Android 15; missing type crashes on Android 14+. Use `specialUse`. (§1)
5. **Background-start rules:** after reboot, process death, or an OEM kill, the service may not be restartable from the background in all states (Android 12+; Android 15 SAW exemption needs a *visible* overlay — chicken-and-egg after a kill). Design for "user taps app icon to resurrect" as the reliable path.
6. **OEM killers & permission resets:** OEM battery managers and Play Protect permission-resetting can silently revoke/pause things (overlay grant can be toggled off by the user in Settings at any time — detect `canDrawOverlays()==false` on start and re-prompt gracefully). Samsung/Xiaomi devices need the §1 whitelist steps; re-check after major OS updates.
7. **Microphone limits:** no always-on listening (SpeechRecognizer explicitly not for continuous use; mic FGS creation requires visible app use on Android 14+; system mic toggle + green-dot indicator on Android 12+). Push-to-talk only.
8. **IME quirks per keyboard app:** Gboard/Samsung Keyboard differ in popup anchoring, autocorrect UI, and clipboard/toolbar behaviour inside service windows; budget testing time with the owner's actual keyboard. (§5)
9. **Battery & heat:** a runaway animation loop (e.g. 60 fps, full-screen window, no screen-off pause) is the single easiest way to make this app miserable. Cap ~12–24 fps, tiny window, pause on screen-off, pause when battery saver is on.
10. **API key in the APK + spend runaway:** a chat-loop bug (retry storm, runaway history growth) can burn API credit; set provider spend caps, cap history tokens, add client-side rate limiting. (§6)
11. **Contributor-mode privacy trap:** Meta's cheapest Muse tier trades your chat content for training use. Default to Standard mode. (§6)
12. **Persona ≠ memory:** whichever API is chosen, the avatar has no memory unless you build it (local history DB + summarised profile injected into the system prompt). Build it deliberately — it's also the privacy-friendly design (memory lives on the phone).
13. **Gesture/navigation conflicts:** a pet sitting at the screen bottom can sit on the gesture bar / keyboard; keep it off the bottom ~navigation-bar strip or make it dodge the IME when the chat is open.
14. **OS upgrades:** target-SDK bumps each year can change FGS/overlay rules (this area has changed in 12, 14, and 15). Since the owner controls the phone, *not* upgrading the app's targetSdk immediately is a valid personal-use strategy — but new phones ship new rules regardless of target in some cases (several Android 12 behaviours apply to *all* apps).

**Verdict §8: Possible with caveats — no single gotcha kills the concept; the lock-screen absence and OEM kills are permanent facts of life to design around, everything else is engineering discipline.**

---

## Could not verify / open questions

- No controlled, measured battery figure (%/hour) for a single-pet overlay app exists in sources found; §1/§3 figures are developer statements and user reports, not benchmarks.
- Whether Meta Model API is available in the owner's country/account tier, and its exact data-retention terms for Standard mode, were not opened in this pass — check https://dev.meta.ai/docs/pricing-rate-limits.md and the linked terms before committing.
- Anthropic's current help-centre wording on Pro-vs-API separation was confirmed via multiple secondary sources citing it, not by opening the help page directly; the 2026 Max/Team bundled-API-credit change is secondary-source only.
- Gemini API free-tier data-use terms and Gemini Nano Prompt API availability on the owner's specific (unspecified) phone model — device model was not given in the mission; Nano support is highly model-dependent.
- Spine's current first-class Android-native (non-engine) runtime status, Unity's current free-tier terms, and Android developer-verification sideloading rollout status: flagged [unverified] where mentioned.
- The owner's phone make/model/Android version were not specified — OEM-killer severity (§1) and Nano availability (§6) both hinge on it.

## Sources

Official Android / Google:
- https://developer.android.com/about/versions/12/behavior-changes-all?hl=en&authuser=6 — untrusted touches (Android 12)
- https://developer.android.com/about/versions/14/changes/fgs-types-required — FGS types required (Android 14)
- https://developer.android.com/develop/background-work/services/fgs/service-types?authuser=7 — FGS types incl. specialUse
- https://developer.android.com/develop/background-work/services/fgs/timeout?hl=en&authuser=002 — dataSync/mediaProcessing 6 h timeout (Android 15)
- https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start?hl=en&authuser=00 — background FGS start restrictions
- https://developer.android.com/about/versions/15/behavior-changes-15?authuser=002 — Android 15 changes incl. BOOT_COMPLETED
- https://developer.android.com/training/monitoring-device-state/doze-standby?hl=en&authuser=1 — Doze & App Standby
- https://developer.android.com/security/fraud-prevention/activities?authuser=0 — FLAG_SECURE / HIDE_OVERLAY_WINDOWS
- https://developer.android.com/reference/android/service/wallpaper/WallpaperService?authuser=2 — WallpaperService
- https://developer.android.com/reference/android/speech/SpeechRecognizer?authuser=45 — SpeechRecognizer
- https://developer.android.com/reference/kotlin/android/speech/tts/TextToSpeech?source=post_page-----109c342ecdd1----------------------------------------- — TextToSpeech
- https://developer.android.com/reference/kotlin/android/view/WindowManager.LayoutParams.html?authuser=437 — window flags incl. FLAG_SHOW_WHEN_LOCKED
- https://developer.android.com/build/building-cmdline?hl=en&authuser=002 — build from command line
- https://support.google.com/android/answer/2812853?hl — Google Play Protect

AI APIs / vendors:
- https://dev.meta.ai/docs/overview — Meta Model API & Muse models (opened 2026-11-21)
- https://dev.meta.ai/docs/pricing-rate-limits.md — Meta Model API pricing
- https://www-cdn.anthropic.com/files/4zrzovbb/website/53da0764b66f75f6cc5521ed77e3e6426f144989.pdf — Anthropic Claude rate card (2026-06-29)
- https://aionx.co/claude-ai-reviews/claude-pro-api-access/ — Pro vs API separation; Max/Team credits
- https://www.activepieces.com/blog/claude-api-pricing-2026-rates-for-every-model — Claude API pricing summary
- https://code.claude.com/docs/en/headless/ — Claude Code programmatic/headless use
- https://llmlearner.com/models/gemini-3-1-flash-lite/pricing — Gemini 3.1 Flash-Lite pricing (from Google's page)
- https://agentping.io/llm-api-pricing/gemini — Gemini API pricing summary
- https://hokai.io/hub/models/gemini-nano — Gemini Nano / AICore overview
- https://www.live2d.com/en/sdk/about/ — Live2D Cubism SDK & licensing

Precedents / community / tooling:
- https://play.google.com/store/apps/details?id=com.digitalcosmos.shimeji&hl=en-gb&gl=bh — Shimeji listing & reviews
- https://www.appireview.com/com.digitalcosmos.shimeji — Shimeji review (battery, Ghost Mode)
- https://www.aidorable.ai/blog/shimeji-app — Shimeji history & Android overlay model
- https://store.steampowered.com/app/3301060/Desktop_Mate?snr=1_241_4_animationmodeling_salesmartpopularpurchased&curator_clanid=41316928 — Desktop Mate
- https://dev.to/localazy/6-floating-windows-on-android-keyboard-input-phd — keyboard in floating windows
- https://dev.to/szymonwalczak/surviving-android-battery-killers-in-capacitor-apps-4im7 — OEM battery killers
- https://github.com/fluttercommunity/flutter_workmanager/blob/HEAD/docs/troubleshooting.mdx — dontkillmyapp per-vendor fixes
- https://blogs.mobilebytesensei.com/blog/glance-widgets/ — Glance/RemoteViews limits
- https://www.androidauthority.com/make-a-custom-android-launcher-837342-837342/ — custom launcher basics
- https://new.airbnb.tech/opensource/lottie/ — Lottie
- https://blog.makko.ai/ai-animation-tools-for-2d-characters/ — Spine pricing

---

# Key findings — read 2026-11-21, all index unless noted

- Overlay: SYSTEM_ALERT_WINDOW special access via Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Settings.canDrawOverlays(); TYPE_APPLICATION_OVERLAY API26+, below status bar/IME, system may move/hide. Android 12 untrusted touches blocked. HIDE_OVERLAY_WINDOWS opt-out Android 12 (banking etc can hide overlays).
- FGS: Android 14 must declare type; specialUse fits avatar, needs FOREGROUND_SERVICE_SPECIAL_USE + PROPERTY_SPECIAL_USE_FGS_SUBTYPE (Play review only matters for Play; sideloaded no review). Android 15: dataSync/mediaProcessing 6h/24h timeout — avoid dataSync. BOOT_COMPLETED cannot launch dataSync/camera/mediaPlayback/phoneCall/mediaProjection/microphone FGS. Android 12+ cannot start FGS from background except exemptions; Android 15 exemption for SAW requires visible overlay.
- Doze defers network/CPU screen-off; pause animation screen-off anyway. OEM killers: dontkillmyapp, Xiaomi/Samsung/Huawei worst.
- Keyboard in overlay: FLAG_NOT_FOCUSABLE blocks IME; toggle it off when chat opens, on when closed (Localazy floating-windows series). Well-known pattern.
- SpeechRecognizer: RECORD_AUDIO required, likely streams to server, not for continuous recognition, battery/bandwidth warning (official ref). createOnDeviceSpeechRecognizer / isOnDeviceRecognitionAvailable for offline, device-dependent. TTS official, trivial.
- Wallpaper: WallpaperService.Engine setTouchEventsEnabled/onTouchEvent exists, draws on Canvas/Surface behind launcher; no IME/focusable UI → chat must launch Activity.
- Widgets: RemoteViews/Glance — no animation frame loop, no Canvas/custom views, clicks only, updatePeriodMillis min 30 min official-ish.
- Precedents: Shimeji Android (Digital Cosmos, 10M+, 4.5★ ~384k reviews) uses display-over-other-apps, Ghost Mode = FLAG_NOT_TOUCHABLE pass-through, pauses screen-off, dev says 1 pet negligible, users report drain with 4-10 pets. Desktop Mate = Windows/Mac 3D, not Android tech. Desktop Goose = Windows.
- Meta Muse API: REFUTES mission expectation as of Nov 2026. dev.meta.ai/docs/overview (opened, verified index fetch 2026-11-21) — Meta Model API, base https://api.meta.ai/v1, MODEL_API_KEY, muse-spark-1.3 standard $1.25/$4.25 per MTok, contributor $0.10/$0.20 (data used for training), muse-ember $0.10/$0.50 (≤200k), muse-wonder $4/$20. BUT this is the Muse *model*, not the owner's personal Muse agent (its memory/tools/personal context in the Muse product) — no source found that API exposes that personal-agent state. Label that distinction as inference from docs, not a documented negative.
- Claude API: Haiku 4.5 $1/$5, Sonnet 4.6 $3/$15 (Anthropic rate card 2026-06-29). Pro separate from API — secondary sources agree, Anthropic help position; note 2026 change: Max/Team now include API credits per secondary sources (unverified against Anthropic help directly).
- Claude Code headless: claude -p official docs code.claude.com/docs/en/headless — bridge feasible, but needs home PC on, networking (Tailscale etc — general knowledge, unverified), latency, security of exposing it.
- Build: official building-cmdline — gradlew assembleDebug/installDebug, debug key auto-signed, release needs own keystore. Headless Linux VM fine: JDK17+ + cmdline-tools sdkmanager. Android Studio GUI only genuinely useful for Layout Inspector/profilers/emulator/emulator-only testing & visual previews.
- Play Protect: support.google.com/android/answer/2812853 — scans sideloaded, may warn/block unverified apps using sensitive permissions, may reset permissions.
