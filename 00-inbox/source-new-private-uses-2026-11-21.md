# 新規プライベート活用法リサーチ（2026-11-21 Muse収集）

出典一覧は末尾。個別項目のURLは本文中に記載。

# New Private/Personal Use Cases: Muse, Claude Code, Obsidian

## Summary
At least 26 distinct, NEW use cases were found from real public reports (articles, personal blogs, note/Zenn, forums, YouTube), excluding the requester's already-known list (LLM Wiki/second brain, daily journaling, PARA, Google Calendar/Tasks split, basic reading notes, generic travel/shopping, generic personal app dev, family task basics, Claude Code basics, SessionStart hooks). The richest veins are: (1) turning years of personal data (bank exports, Apple Health, WHOOP/Strava, receipts) into dashboards/models, (2) Claude Code running a whole house / a Raspberry-Pi life-admin fleet, (3) Obsidian as a media/nutrition/receipt ledger with Dataview/Bases, not a journal, and (4) Muse (Meta, launched in Japan 2026-10-23) doing phone calls, price-watches, health nudges and — in Japan — Yahoo! Shopping to checkout, with Mercari / Money Forward ME / Ticket Pia integrations announced as upcoming. Most cases below are **Real reported** (the person doing it); a few second-hand or announced items are labelled as such. Difficulty: ★1 easy for a non-programmer, ★2 medium, ★3 advanced.

## Findings

### A. Personal data analysis — finances & health

#### 1. Household spending dashboard that unmasks “Amazon” charges
- **What:** A non-coding executive puts bank/card exports + Amazon order history in one Claude Code folder; Claude Code builds a local HTML dashboard by category/month, matches large retail charges to the actual orders/items behind them, de-duplicates overlapping exports and excludes own-account transfers. He spot-checks totals against statements, and can run a second fresh session as auditor. A parallel open-source version by Mahmoud Halat does the same from CSV/XLS exports — subscriptions’ true monthly run-rate, real spending vs transfers, offline single-file dashboard, no bank login.
- **Tools:** Claude Code | **Difficulty:** ★1 | **Status:** Real reported
- **Source:** Blog/playbook — https://playbooks.bot/playbooks/family-budget-dashboard-from-statements-and-orders/ ; personal project site — https://finance.mahmoudhalat.com/

#### 2. Receipt-photo household ledger in Obsidian, auto-totalled monthly (Japan)
- **What:** A Japanese mother of three photographs receipts; an iPhone Shortcut auto-registers them into her Obsidian vault as files with a `[spend::YYYY-MM, category, amount]` line. One monthly DataviewJS page (code written by Claude, she says she barely understands it) then shows, on opening: totals by category with share/count, split household vs personal allowance (お小遣い), and an itemised list — on iPhone/iPad too.
- **Tools:** Obsidian (+ Dataview) + Claude (for the code) + iPhone Shortcuts | **Difficulty:** ★1–★2 (copy-paste code, change only month + folder) | **Status:** Real reported
- **Source:** Personal blog (くらしとITログ) — https://lifeandit-log.com/archives/169

#### 3. Ten years of Apple Health (1.8 GB, 4.26M records) → SQLite → ask in natural language via MCP
- **What:** The author exports a decade of iPhone/Apple Watch health data, loads the XML into a local SQLite DB on a Mac mini, and exposes it to Claude via a FastMCP read-only server (`query_health` for raw SQL + `get_daily_summary` shortcuts). He can ask “show 2 years of monthly VO2max”, “find days with large walking asymmetry”, HRV/resting-HR/sleep by month — questions the Health app cannot answer. Monthly manual re-export is enough for long-term trends.
- **Tools:** Claude Code / Claude + MCP (self-built) | **Difficulty:** ★3 | **Status:** Real reported
- **Source:** Zenn article — https://zenn.dev/hideakitamai/articles/8ab4733e65e0dc

#### 4. Wearable early-warning model for a chronic disease flare-up
- **What:** A Reddit user (u/ThatAi_guy) with episodic Graves’ disease gave Claude Code ~9.5 years of Apple Watch + WHOOP readings plus labelled past episodes/lab dates. Claude Code tried several models, settled on XGBoost, back-tested on a time-based holdout (not shuffled), and reported precision/recall, false alarms/month and how many days before each past episode it would have warned — framed explicitly as “alert, then get a lab check”, not diagnosis.
- **Tools:** Claude Code | **Difficulty:** ★3 | **Status:** Real reported (second-hand summary of the Reddit report; original Reddit post not opened)
- **Source:** Playbook summarising the Reddit case — https://playbooks.bot/playbooks/wearable-history-early-warning-model/

#### 5. “Signal” — a personal health agent over WHOOP + Strava + Apple Health
- **What:** Michael Surtees built, with Claude Code, a daily-use agent whose morning “Now” page gives one headline observation across all three data sources at once — e.g. skin temperature, resting HR and HRV all drifting together as early illness signs, a pattern no single tracking app surfaces. Chat is only a depth mechanism on top of the briefing. He also built a separate Strava dashboard (4,905 rides since 2020) with coach-style weekly synthesis that one-click posts a recap to Strava.
- **Tools:** Claude Code (builder) + WHOOP/Strava/Apple Health data | **Difficulty:** ★3 | **Status:** Real reported
- **Source:** Personal portfolio/case study — https://michaelsurtees.com/casestudy-signal.html

#### 6. CSV life-log analysis: household, health and investment logs in one monthly report (Japan)
- **What:** A Japanese note guide shows exporting household-budget, health-record (sleep/steps/HR/weight) and investment spreadsheets as CSV and having Claude Code find, e.g., the conditions of “good-condition days” (7h+ sleep → next-day steps averaging 11,240 in the example), savings points, and one’s investment “winning pattern”, then generating an integrated monthly Markdown report from `LifeLog/finance/` + `LifeLog/health/` folders.
- **Tools:** Claude Code | **Difficulty:** ★1 | **Status:** Proposal/guide with worked example prompts — presented as a practical guide, NOT verified as the author’s own long-running personal dataset
- **Source:** note article — https://note.com/duke_pearson700/n/n07b638c20589

### B. Home automation & life-admin infrastructure

#### 7. Whole smart home built from scratch with Claude Code + Home Assistant
- **What:** After moving house, a long-time Home Assistant user rebuilt everything via Claude Code scripts talking to the HA API instead of hand-editing YAML: 60+ lights (Matter/Xiaomi) with adaptive lighting, Guest/Theater/Sleep scenes, unified switch bindings plus a printable HTML manual for family/guests, presence lighting, water-leak alert (phone + red flashing lamp), washer/dryer/dishwasher-done announcements via HomePod TTS, and pet monitoring — litter-box use, water intake, low-litter/full-bin alerts that also add shopping reminders to a to-do list. Claude Code also analyses logs to suggest new automations.
- **Tools:** Claude Code + Home Assistant | **Difficulty:** ★3 | **Status:** Real reported, open-sourced config
- **Source:** Home Assistant Community forum post — https://community.home-assistant.io/t/building-my-smart-home-from-scratch-with-claude-code-home-assistant/994464

#### 8. Claude Code living *inside* the Home Assistant box, driven by phone
- **What:** A Portuguese user runs Claude Code inside an Advanced SSH add-on on a Home Assistant Green (reinstall-on-boot + state kept in `/config/.claude-box`). Since June 2026: 580 commits, 129 automations, 147 devices / 1,163 entities, and a 10-tab dashboard generated by 7,600 lines of Python. He talks to it in Portuguese, usually from his phone; it edits `/config`, validates, reloads and verifies. A second report (D3X) built a full home in a week — Zigbee/Z-Wave, Frigate cameras with local AI, bilingual EN/PL voice, circadian lighting — plus a weekly health report that headless `claude -p` writes itself from collected logs/battery/energy data.
- **Tools:** Claude Code + Home Assistant | **Difficulty:** ★3 | **Status:** Real reported
- **Sources:** DEV blog — https://dev.to/marcelo_sqe/how-i-built-my-entire-home-assistant-with-claude-code-running-inside-it-26ch ; field log — https://d3x-solutions.com/home-assistant-claude-code-smart-home/ ; also https://blog.beguelin.com/2026/04/claude-code-home-assistant (MCP-connected HA in Puerto Rico, edit→scp→reload→verify loop)

#### 9. Raspberry Pi life-admin fleet: drop a task note in Obsidian, it gets done every 15 minutes
- **What:** Ross Goodman turned a home Raspberry Pi 4 into his life admin with Claude Code, with every change documented back into his ~5,600-note Obsidian vault. Concrete jobs: **InboxProcessor** (drop a task note in the vault Inbox from his phone; headless Claude picks it up every 15 min and does it), **InvoiceCapture** (supplier “your bill is ready” emails → headless-browser login → PDF filed in Paperless-ngx with amounts extracted), **BankSync/FinanceImport + monthly FinancialReview** note (spending/savings/mortgage/“items to watch” — transaction data deliberately never shown to the AI), **EventCapture** (weekly scan of email/calendar recording shows, cinema, restaurants actually attended), **PeopleReview**, **RemarkableSync** (Sunday archive of his reMarkable notebook), and a desk LED matrix that scrolls next train / bin day / aircraft overhead. 38 regression-test scripts + a watchdog keep it running. *Verified live in this research.*
- **Tools:** Claude Code + Obsidian (combination) + Raspberry Pi/Home Assistant/n8n/Paperless | **Difficulty:** ★3 | **Status:** Real reported
- **Source:** Personal blog — https://rossgoodman.com/2026/10/03/what-i-have-built-with-claude-code-so-far/

### C. Media libraries, collections & life logging

#### 10. 10,260 media notes: movies, anime, games, board games, manga — after TV Time shut down
- **What:** When TV Time shut down in July 2026 and took 15 years of his viewing history, Sébastien Dubois rebuilt everything as one Obsidian note per work (movies, shows+seasons, anime, manga, comics, video/board games + expansions, music albums), with covers, status, ratings, ownership, prices and play dates. Obsidian Bases give gallery/Kanban/wishlist-by-priority/“pile of shame”/“Year in Media” views; one-click buttons log a session, add playtime, mark episodes watched, rate, lend, or track a Kickstarter pledge; importers pull from IMDb, BoardGameGeek and Steam, and AI skills run imports like “import my IMDb collection”. The wishlist doubles as a public gift list.
- **Tools:** Obsidian (+ Bases, Media DB) + AI skills | **Difficulty:** ★2–★3 at this scale (★1–★2 for a small version) | **Status:** Real reported
- **Source:** Personal blog — https://www.dsebastien.net/media-management-system-obsidian/

#### 11. Auto-generated music library + “what you actually watched/read” curators
- **What:** In the same Pi/vault system as #9: **MusicNotes** auto-creates a note for every artist/album in his NAS music collection (3,700+ music notes, the vault’s largest folder); **YouTubeReview** does a monthly review of YouTube/YouTube Music history, flags missed uploads and neglected subscriptions and builds “Claude Picks” playlists; **InstapaperCurator** picks 10 articles every Friday from his reading history and saves them to Instapaper.
- **Tools:** Claude Code + Obsidian | **Difficulty:** ★2–★3 | **Status:** Real reported
- **Source:** Personal blog — https://rossgoodman.com/2026/10/03/what-i-have-built-with-claude-code-so-far/

#### 12. Gamified habit RPG in Obsidian (XP, streak badges, locked habits, reward machine)
- **What:** Tired of habit apps, the author turned daily notes into an RPG with DataviewJS + Templater: completed habits earn XP shown on a character-sheet dashboard; streaks for meditation/workout/reading unlock badges (“Mindfulness Sprout” at 7 days, “Zen Master” at 30); harder habits stay “locked” until prerequisite counts are hit; and hitting a daily goal draws a random reward from his own list (“watch a movie guilt-free”, “30 min of gaming”, “dessert”).
- **Tools:** Obsidian (+ Dataview, Templater) | **Difficulty:** ★2 (scripts are copy-pasteable) | **Status:** Real reported
- **Source:** XDA article by the system’s author — https://www.xda-developers.com/gamify-habits-obsidian-using-dataview-templater/

### D. Food, recipes & nutrition

#### 13. Sunday-morning automated meal plan + grocery list from your own Obsidian recipes (~$0.50/month)
- **What:** Louis Racicot’s recipes live as structured Markdown in his Obsidian vault (in GitHub). Every Sunday 07:00 a GitHub Action parses recipes to JSON, makes a first Claude API call on metadata only to select a week’s menu against his constraints file, then a second call with full details of just the chosen recipes to build the grocery list — and emails him the menu + list. Two-step prompting is the cost trick (~$0.50/month, no subscription app).
- **Tools:** Obsidian + Claude API (not Claude Code) + GitHub Actions | **Difficulty:** ★2–★3 | **Status:** Real reported
- **Source:** Medium personal blog — https://medium.com/@lracicot/automating-my-weekly-meal-planning-with-ai-and-obsidian-d61e73fd21c3

#### 14. Nutrition/calorie ledger linked to the daily journal
- **What:** Oscar López keeps one note per meal/recipe with inline Dataview fields (calories, protein, fat, carbs, fibre, sugars — estimated via an AI from the recipe/portions), links the day’s breakfast/lunch/dinner/snacks from his journal note, and a DataviewJS report totals the day’s intake multiplied by portions eaten. Restaurant meals get the same treatment with their own note type.
- **Tools:** Obsidian (+ Dataview) | **Difficulty:** ★2 | **Status:** Real reported
- **Source:** Personal blog — https://oscarlp6.dev/en/blogs/nutrition-system-obsidian/

#### 15. Recipe manager where un-ticking an ingredient *is* the shopping list
- **What:** A long-running Obsidian Forum showcase: recipes are only added after being cooked and liked, ingredients are checkboxes tagged `#ingredients`; when planning the week or using up a staple (flour, sugar) while cooking, you simply uncheck it and the Checklist plugin auto-populates a sidebar shopping list — checking items off at the store checks them back in the recipe files. A Dataview cookbook view sits on top.
- **Tools:** Obsidian (+ Checklist, Dataview) | **Difficulty:** ★1 | **Status:** Real reported (forum showcase/tutorial)
- **Source:** Obsidian Forum — https://forum.obsidian.md/t/obsidian-as-recipe-manager-and-shopping-list-tutorial/40799?ref=obsidian-roundup.ghost.io

### E. Voice notes, chat bots & capture pipelines

#### 16. 82 iPhone voice memos (2018– , 1.1 GB) transcribed across two machines → printable PDF workbook
- **What:** Brett Ridenour had Claude Code SSH into his MacBook over Tailscale, copy 82 `.m4a` memos to his Linux desktop, install Whisper and batch-transcribe in parallel — and when his old GPU was too slow, Claude Code SSH’d back, installed Whisper on the M1 Pro MacBook and ran a second parallel job, killing two blocking 5h/8h recordings and re-running the 24 missing files. Result: 69 memos transcribed, summarised and compiled into a printable PDF workbook via Python/reportlab.
- **Tools:** Claude Code + Whisper | **Difficulty:** ★2 | **Status:** Real reported
- **Source:** Personal blog — https://www.brettridenour.com/blog/what-im-actually-doing-with-claude-code

#### 17. Telegram bot whose long-term memory is an Obsidian vault, with WHOOP intelligence
- **What:** Steve Haddad’s “Second Brain” runs 24/7 on a Hetzner VPS (~$15–25/month total): message his Telegram bot in text or voice (Whisper transcribes), it semantically searches ~2,300 chunks of his Obsidian vault before answering, runs scheduled briefings, manages tasks in SQLite, ingests documents/books, and pulls WHOOP health data. The same vault is exposed to the Claude app and Claude Code through a hosted MCP server (search_vault / get_note / list_assets / save_note) behind a Cloudflare tunnel.
- **Tools:** Claude API + Obsidian + MCP (combination; Claude Code is one client) | **Difficulty:** ★3 | **Status:** Real reported, “live in production”
- **Source:** Personal project page — https://www.stevehaddad.io/work/second-brain

#### 18. Voice-first Telegram life coach (psychologist-designed) → Todoist + Calendar + Obsidian
- **What:** “Life Pilot Agent”: send a Telegram voice message and Groq Whisper transcribes it, Claude classifies it and creates a Todoist task, calendar context or Obsidian note linked to your goals — no forms, no app-opening. Built by a practising psychologist, its coaching/reflection protocol uses psychology frameworks rather than generic productivity advice; `/recall` does semantic search over the whole vault. Runs 24/7 on a VPS on Claude Code + MCP.
- **Tools:** Claude Code + Obsidian + MCP | **Difficulty:** ★3 to self-host (★1 to use once running) | **Status:** Real reported (builder’s open-source project)
- **Source:** GitHub project — https://github.com/VDanchAI/life-pilot-agent

#### 19. A Discord assistant that *grows its own tools*
- **What:** “LogBot / OpenCClaw”: a minimal Discord ↔ Claude Code CLI bridge that started with **zero** MCP tools. Because Claude Code can write files, when asked for something new it creates the tool itself in a `tools/` folder that an MCP server auto-registers — it built its own current-time, weather (Open-Meteo), Google Calendar OAuth + listing tools, then composed them into a `departure-check` tool (calendar + travel time + weather → “when should I leave”). Cron wakes it for proactive notifications in Discord.
- **Tools:** Claude Code + Discord + MCP | **Difficulty:** ★3 | **Status:** Real reported
- **Source:** DEV blog by the builder — https://dev.to/quolu/how-i-built-an-ai-assistant-that-grows-its-own-tools-572g

#### 20. Two one-word personal skills: `/maintenance` (apartment portal) and `/meme` (video memes)
- **What:** Same author as #16. (a) He walked Claude Code once through his apartment complex’s clunky maintenance portal via Chrome MCP (cross-domain login, cookie banner, nested dropdowns: General → Pest control → …); that learning became a `/maintenance` skill — now he types `/maintenance` + “my AC is broken” and the request is filed. (b) `/meme`: describe a meme, Claude Code finds the clip on Instagram/YouTube with yt-dlp, probes it with ffprobe, builds an ffmpeg filter chain (text bar, exact 9:16) and outputs a finished `.mp4`.
- **Tools:** Claude Code (+ Chrome MCP, ffmpeg) | **Difficulty:** ★2 (after the one-time guided setup) | **Status:** Real reported
- **Source:** Personal blog — https://www.brettridenour.com/blog/what-im-actually-doing-with-claude-code

### F. Photos & files

#### 21. Sorting 1,400 screenshots/photos with meaningless filenames
- **What:** The author pointed Claude Code (in plan mode, guided by a `FILE_CLEANUP_REFERENCE.md` defining her categories/projects) at a desktop holding 1,400+ screenshots from live and discontinued projects, eBook covers, receipts and artwork. Claude triaged the 20% with meaningful names first, then reviewed the rest in batches — identifying content visually, weeding duplicates/near-blanks, renaming files understandably and filing them into the agreed folder structure. She notes the same works for personal photos named `IMG523.jpg`, assigning user-defined categories (children, pets, places…).
- **Tools:** Claude Code | **Difficulty:** ★1 | **Status:** Real reported
- **Source:** Substack personal blog — https://wonderingaboutai.substack.com/p/i-used-claude-code-to-organize-1400

### G. Hobby coding with Claude Code — specific, not “personal app dev” in general

#### 22. A working truck driver builds a car-carrier loading browser game
- **What:** A Japanese career-car (vehicle transporter) driver is building “僕らは陸送屋”, a browser game faithfully simulating loading 7 cars onto a semi-trailer, wheel-chocking and securing them — almost all code written by Claude Code, art/SFX/BGM/voices by other generative AI. His twist: the repo’s CLAUDE.md splits work into five “departments” (implementation, graphics, sound…) each allowed to touch only its own files, to stop the AI breaking unrelated parts; physics-like real-vehicle movement is specified to the AI as formulas. Playable free on GitHub Pages/itch.io.
- **Tools:** Claude Code (+ other generative AI) | **Difficulty:** ★2 (no code written by him) | **Status:** Real reported
- **Source:** Zenn article — https://zenn.dev/wadome_do/articles/wadome-ai-game-dev-notes

#### 23. Zero-programming roguelike, sold for its first $2 — then Claude Code builds the marketing machine
- **What:** A self-described programming-zero author directed Claude Code to build DUNG: Azure Flame, a 15,000-line Python CLI hack-and-slash roguelike (choosing text/CLI deliberately to dodge the graphics-asset wall), playtesting and feeding back only on game feel (“drops don’t feel hack-and-slash enough”). Claude Code suggested itch.io, registered, built the store page and priced it at $2 — first sale in 2 weeks. It then built a “Chrome Bridge” (CDP browser automation) to auto-post launch articles to Zenn, note, Qiita, Hatena and dev.to and create Ko-fi/Gumroad pages: 11 platforms in 2 days. He is candid about cost: $200/month of Claude Code vs $2 revenue so far.
- **Tools:** Claude Code | **Difficulty:** ★2 | **Status:** Real reported
- **Source:** Zenn article — https://zenn.dev/yurukusa/articles/f62a4d0e9d9eb1

#### 24. Three audience-of-one tools spotted in the wild (via XDA roundup of Reddit reports)
- **What:** (a) **Alexandria** — turns any ebook into a fully multi-voice audiobook, running entirely locally (can point at a local LLM via LM Studio/Ollama, no cloud, ~700 GitHub stars); built by Reddit user Finrandojin with Claude. (b) **Crochet translator** — user knowbit, learning crochet to get off his laptop, used Claude Code to build a web app that rewrites cryptic pattern abbreviations into plain English and walks him through row-by-row; crocheting friends then asked for logins. (c) **Treadmill remote** — user pdawes replaced his generic desk-treadmill’s clunky proprietary app/remote with his own Bluetooth remote built with Claude Code, which lets him “walk” through Google Maps routes.
- **Tools:** Claude Code | **Difficulty:** ★2 | **Status:** Real reported — second-hand (XDA roundup of the original Reddit reports; the Reddit primaries were not opened in this research)
- **Source:** XDA roundup — https://www.xda-developers.com/most-useful-things-people-built-with-claude-code/

### H. Muse (Meta) — specific personal uses

#### 25. Muse makes the phone call, waits on hold, and haggles on Marketplace
- **What:** In the NYT’s two-week test (Eli Tan), Muse phoned his dental insurer, gave his member ID, answered a security question and waited on hold before handing him the human rep; put card statements into a spreadsheet and found a duplicate subscription; efficiently filled online forms; paid a parking ticket; and spent time bargaining with sellers over second-hand ceramic bowls/plates on Facebook Marketplace (in one retelling it lowballed for days until he stepped in and paid full price). Caveats from the same coverage: Amazon blocked Muse from buying, some non-partner web forms failed, and a Yahoo Finance tester got a recommended restaurant that had closed years ago and an invented phone number — check its facts.
- **Tools:** Muse only | **Difficulty:** ★1 | **Status:** Real reported (reviewer tests, summarised by a review roundup; NYT original is paywalled — see Could not verify)
- **Source:** Review roundup with links to originals — https://personalagentbench.com/meta-muse-review/

#### 26. Muse standing automations: price watch, health coach nudge, leave-now alerts, habit streaks
- **What:** Tom’s Guide’s Elton Jones set up 10 Muse automations and reports all worked. The non-obvious ones: a **daily price watch** that found a WWE Blu-ray under $20 with free shipping on eBay; an **iPhone Health coach** that pulls steps/workouts/sleep and “pokes” him at 14:00 on days he has barely moved, plus a wind-down reminder 30 min before his (learned, weekday vs weekend-different) bedtime; **leave-now traffic alerts** before any calendar event with a location (arrive 10 min early); a **habit streak keeper** (daily gallon-of-water check-in at 21:00, “gets annoying” after two misses); a Sunday digest of new game/graphic-novel releases in his taste; and an end-of-day accountability check-in producing tomorrow’s top 3. *Verified live in this research.*
- **Tools:** Muse only | **Difficulty:** ★1 | **Status:** Real reported (hands-on test)
- **Source:** Tom’s Guide — https://www.tomsguide.com/ai/i-used-meta-muse-to-automate-10-tasks-from-reminders-to-trip-alerts-and-i-cant-believe-how-well-metas-ai-handled-everything

#### 27. Muse books dinner for six and babysits a delivery
- **What:** In a disclosed two-day head-to-head by Lindy (a competitor — treat framing accordingly, facts are concrete): Muse found restaurants near his sister’s hotel, booked dinner for six at 19:30, paid the deposit with a one-time virtual card only after his approval, and watched a package-tracking page, messaging him on WhatsApp when the delivery slipped. The same test found Muse’s weakness: a finished personal session cannot be shared with a coworker — it is personal-only by design.
- **Tools:** Muse only | **Difficulty:** ★1 | **Status:** Real reported (competitor’s own test, bias disclosed in the article)
- **Source:** Lindy blog — https://www.lindy.ai/blog/meta-muse-vs-lindy

#### 28. Muse in Japan: Yahoo! Shopping to the checkout screen, Instagram-reel shopping lists, station nudges — and Japanese integrations coming
- **What:** Muse launched in Japan on **2026-10-23** (first region after North America; iOS/Android/muse.ai; no WhatsApp channel in the Japanese announcement). A Japanese editorial test asked it (in the web version) to buy a 2L×6 case of water on **Yahoo! Shopping** “up to the final confirmation, don’t actually buy”: Muse opened the Yamada Denki Yahoo! store product page, used the address/card registered in Stripe Link (card number never shown in chat; a single-use card number is issued to the store), and stopped at an approval panel showing Permit/Reject — though the chat total (¥1,392) and the panel’s estimate (¥1,397) differed by ¥5. Meta’s announced examples/useful tricks include: turning an **Instagram saved recipe Reel into a shopping list**; with location linked, a proactive message on arriving at a station (“there’s a supermarket nearby — here’s your shopping memo” — observed by the editorial team); and writing to **two calendars at once** (personal event + an “out of office” block on the work calendar that auto-declines new meetings). Announced as *upcoming* for Japan (not yet live at writing): **Mercari, Money Forward ME and Ticket Pia** integrations; live partners include Stripe Link, Shopify, Trip.com, Agoda and Klook.
- **Tools:** Muse only | **Difficulty:** ★1 | **Status:** Real reported (editorial hands-on) for Yahoo! Shopping / calendars; **Announced, not yet verified live** for Mercari / Money Forward ME / Ticket Pia
- **Sources:** Japanese explainer with hands-on test — https://lolipop.jp/ai/media/what-is-meta-muse/ ; Impress DIGITAL X launch news — https://dcross.impress.co.jp/docs/news/004914.html

#### 29. Muse as a family operating layer: morning family newsletter, podcasts on demand, ongoing goals
- **What:** In Claire’s “How I AI” hands-on (YouTube/podcast): Muse produced, on the first attempt, a polished PDF **family morning newsletter** (better, she says, than versions she had made with other agents), tracks **long-horizon personal goals** conversationally — her example is gently sleep-training an 8.5-month-old while room-sharing, with context gathered over turns and reminders set — and, per Meta/user reports collected elsewhere, can generate a **podcast episode on any topic** on request (one user had it read a whole article aloud that way). Permission requests arrive at the moment access is needed, not as an upfront bundle.
- **Tools:** Muse only | **Difficulty:** ★1 | **Status:** Real reported (hands-on review; podcast feature is a reported user/Meta claim, not independently verified here)
- **Sources:** Lenny’s Newsletter / How I AI episode page — https://www.lennysnewsletter.com/p/how-i-ai-metas-muse-review-how-warp ; video — https://www.youtube.com/watch?v=2UwemqPkJSQ

## YouTube videos worth watching

| Title | Channel / creator | URL | Why |
|---|---|---|---|
| How I Use Obsidian + Claude Code to Run My Life | Startup-ideas podcast episode with Vin (“Internet Vin”) — live demo of custom commands /trace, /connect, /ideas, /ghost, /drift, /challenge over a real vault | https://www.youtube.com/watch?v=6MBq1paspVU | Thinking-partner uses beyond journaling: tracing how an idea evolved, bridging two domains |
| Obsidian plus Claude works. I'm the one who said it wouldn't. | Paperless Movement / Tom (myICOR) — channel name as shown in video description | https://www.youtube.com/watch?v=B35SWx_4BNM | Journal-from-a-screenshot workflow and building a People Base with Obsidian Bases |
| スマホ1台でObsidian × Claude Codeを操る ─ Remote Control活用術（非エンジニア向け） | Japanese creator (channel name not captured in search excerpt — unverified) | https://www.youtube.com/watch?v=lUE5MF06zIU | Non-engineer, phone-only control of a home-Mac Claude Code + vault: sofa/commute use, one-command + QR setup |
| How I AI: Meta’s Muse review (+ how Warp ships with AI) | Claire / Lenny’s “How I AI” | https://www.youtube.com/watch?v=2UwemqPkJSQ | The family-newsletter, calendar and goal-tracking hands-on behind case #29 |
| Meta's Muse wants the keys to your life. Should you say yes? (Ep 12) | Personal Agent Bench (Ep 12) | https://www.youtube.com/watch?v=eDPfmTVTshY | Reviewer-task roundup + a copyable “five-errand test” to judge Muse yourself |
| I Built an AI Employee That Runs My Life 24/7 (Claude Code + Obsidian) | Creator name not captured in search excerpt — unverified | https://www.youtube.com/watch?v=XHQuJIw31Qg | Checkbox-in-Obsidian approval workflow: tick a box in the vault, the agent executes (Gmail/WhatsApp/social/invoicing watchers) — note: leans work/business |
| Obsidian: how to use it for your project working with Claude Code | Creator name not captured — unverified | https://www.youtube.com/watch?v=OdJhzIxCneo | Practical vault + Claude Code setup with custom slash commands (/resume, /compress, /preserve) |

## Could not verify / open questions
- **NYT / WSJ / Verge Muse originals** are paywalled or were only reached via the Personal Agent Bench roundup and secondary retellings; the dental-insurer, Marketplace and duplicate-subscription facts are consistent across at least two secondary sources but were not read in the NYT original.
- **XDA’s Alexandria / crochet / treadmill cases (#24)** trace to Reddit posts that were not opened; treat as real-but-second-hand.
- **The Graves’ wearable model (#4)** is known via playbooks.bot’s summary of a Reddit post, not the post itself; its backtest numbers were not independently checked, and it is an experiment, not medical advice.
- **Mercari / Money Forward ME / Ticket Pia Muse integrations** are announced as upcoming for Japan in the launch coverage — no source found showing them live and usable as of 2026-11-21. Whether Stripe Link purchase protection applies to Japanese users was explicitly unconfirmed in the Lolipop article.
- **Muse availability/pricing details conflict slightly across sources** (e.g. “US only” in some Oct 2026 comparisons vs the documented Japan launch on 2026-10-23 and a Singapore/Canada mention elsewhere); the Japan launch is corroborated by two Japanese sources (Lolipop, Impress).
- **The hiro note guide (#6)** uses worked examples that may be illustrative rather than the author’s own data — labelled as a guide/proposal accordingly.
- Several YouTube channel names were not present in search excerpts and are flagged “unverified” in the table rather than guessed.
- No Japanese-language *personal* (non-editorial) Muse diary/blog was found — Japanese Muse coverage so far is news/explainer + editorial tests, unlike the rich Japanese first-person literature for Claude Code + Obsidian.

## Sources
All URLs are listed inline with each case above. Types: personal blogs (Dubois, Ridenour, Goodman, Surtees, Racicot, López, Haddad), Japanese personal/technical platforms (Zenn: hideakitamai, wadome_do, yurukusa; note: hiro/duke_pearson700; personal blog lifeandit-log), community/forum (Home Assistant Community, Obsidian Forum, DEV), project pages (GitHub Life Pilot, Mahmoud Halat), editorial tests (Tom’s Guide, Lindy blog, Lolipop, XDA), review roundup (Personal Agent Bench), and YouTube (IDs verified from search-result URLs). Two sources were verified live by opening them in the research browser on 2026-11-21: Ross Goodman’s Pi life-admin post and Tom’s Guide’s Muse 10-automations test; the remainder are from the web index on 2026-11-21, as recorded in notes/sources.md.

---

# Sources read 2026-11-21 (index search + 2 live opens: Tom's Guide Muse, Ross Goodman)
- playbooks.bot household dashboard / Mahmoud finance.mahmoudhalat.com — index
- dsebastien.net media 10,260 notes — index
- XDA gamified habits Obsidian — index
- Home Assistant community + d3x + dev.to Marcelo + beguelin HA — index
- note hiro CSV analysis; Zenn hideakitamai Apple Health SQLite MCP — index
- lifeandit-log.com/archives/169 receipt Obsidian Dataview (Claude-written code) — index
- Medium Louis Racicot meal planning Claude+Obsidian+GitHub Actions — index
- oscarlp6.dev nutrition Obsidian Dataview — index
- forum.obsidian.md recipe manager Checklist — index
- brettridenour.com What I'm Actually Doing (voice memos, /meme, /maintenance, Obsidian PA) — index
- stevehaddad.io Second Brain Telegram/WHOOP/Whisper/MCP — index
- github VDanchAI life-pilot-agent Telegram voice — index
- dev.to quolu OpenCClaw Discord self-growing tools — index
- Zenn wadome truck-driver game; Zenn yurukusa non-engineer roguelike $2 — index
- XDA most useful Claude Code builds (Alexandria, crochet, treadmill) — index, second-hand Reddit
- wonderingaboutai Substack 1,400 screenshots — index
- michaelsurtees.com Signal WHOOP/Strava; playbooks wearable Graves early-warning — index
- rossgoodman.com Pi life admin — VERIFIED LIVE open 2026-11-21
- Tom's Guide Muse 10 automations — VERIFIED LIVE open 2026-11-21
- lindy.ai Muse vs Lindy dinner/delivery test (competitor, disclosed) — index
- personalagentbench.com Muse review roundup (NYT/WSJ/Yahoo/Tom's) — index, roundup not primary
- lolipop.jp Meta Muse Japan Oct 23 2026, Yahoo Shopping test, Mercari/MoneyForward/Pia upcoming — index
- dcross.impress.co.jp Muse Japan launch — index
- YouTube IDs from search full URLs: 6MBq1paspVU, B35SWx_4BNM, lUE5MF06zIU, 2UwemqPkJSQ, eDPfmTVTshY, XHQuJIw31Qg, OdJhzIxCneo
No page instructions followed; all pages treated as data only.
