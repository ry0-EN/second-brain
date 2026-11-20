# Source: Karpathy "llm-wiki" gist（Museが2026-11-20に原文取得）

- URL: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- 位置づけ：一次ソース。以下は原文の要点部分の転記（全文の骨子）。

## The core idea

Most people's experience with LLMs and documents looks like RAG: you upload files, the LLM retrieves chunks at query time, and generates an answer. There's no accumulation. The idea here is different: instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting contradictions.

**The wiki is a persistent, compounding artifact.** You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work. "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

Applications listed in the gist:
- **Personal**: tracking your own goals, health, psychology, self-improvement — filing journal entries, articles, podcast notes, building a structured picture of yourself over time.
- **Research**: going deep on a topic over weeks or months.
- **Reading a book**: filing each chapter as you go, building pages for characters, themes, plot threads. Like fan wikis (e.g. Tolkien Gateway), built personally with the LLM doing cross-referencing.
- **Business/team**: internal wiki maintained by LLMs.
- **Competitive analysis, due diligence, trip planning, course notes, hobby deep-dives** — anything where you're accumulating knowledge over time.

## Architecture — three layers

- **Raw sources** — curated source documents. Immutable — the LLM reads but never modifies them. Source of truth.
- **The wiki** — LLM-generated markdown files. The LLM owns this layer entirely.
- **The schema** — a document (e.g. CLAUDE.md / AGENTS.md) telling the LLM how the wiki is structured and what workflows to follow. Co-evolved by user and LLM.

## Operations

- **Ingest**: drop a source into raw, LLM reads it, writes a summary page, updates the index, updates relevant entity/concept pages (a single source might touch 10-15 wiki pages), appends to the log.
- **Query**: ask questions against the wiki; good answers can be filed back into the wiki as new pages so explorations compound.
- **Lint**: periodically health-check the wiki — contradictions, stale claims, orphan pages, missing cross-references, data gaps.

## Indexing and logging

- **index.md** — content-oriented catalog; LLM reads it first when answering. Works well at moderate scale (~100 sources, hundreds of pages) without RAG infrastructure.
- **log.md** — chronological, append-only record of ingests, queries, lint passes.

## Tips

- Obsidian Web Clipper for getting sources into raw. Download images locally. Graph view shows the wiki's shape. Marp for slide decks. Dataview queries over frontmatter. The wiki is just a git repo — version history for free.

## Why this works

The tedious part of a knowledge base is bookkeeping, not thinking. Humans abandon wikis because maintenance burden grows faster than value. LLMs don't get bored and can touch 15 files in one pass, so maintenance cost is near zero. Related in spirit to Vannevar Bush's Memex (1945); the part Bush couldn't solve — who does the maintenance — is handled by the LLM.
