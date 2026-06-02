## Thread Replies and Follow-Ups

### 1. `@hardiktiw` (HT)

Created: `Mon Jun 01 19:21:23 +0000 2026`

@prukalpa The other big unlock for enterprise agent native infra is to make the context layer multiplayer- so both memory and context accrue for you individually as well as for the whole company.

We have tried this in our small teams and maintaining this coordination has been a challenge

### 2. `@cortexdbai` (CortexDB.ai by creator of Cassandra)

Created: `Mon Jun 01 20:14:21 +0000 2026`

@prukalpa reasoning is the model. context layer is knowledge: data, semantics, skills, all ownerless. the third thing, experience, isn't here. it's the journey a six-month hire has that day-one with the same docs doesn't. we are calling it the third wall - https://t.co/VI1LBCicB9

#### Quoted Post: `@cortexdbai` - "Reasoning, Knowledge, Experience"

Created: `Thu May 14 09:47:39 +0000 2026`

Reasoning, Knowledge, Experience

The way I understand AI, it's three problems, stacked together and only two of them have been solved.

## The first two walls

The first wall was reasoning. Could the model think? For most of the last decade the honest answer was no - it could autocomplete, it could pattern-match, but it couldn't hold a chain of thought long enough to be useful. Then it could. GPT-3, then the o-series, then Sonnet 4. Reasoning isn't finished. Nothing in AI is finished. But it's good enough to ship. We crossed the wall.

The second wall was knowledge. The model could think, but it didn't know anything past its training cutoff, and it didn't know anything about your company, your codebase, your customers. RAG climbed that wall. Vector databases, retrievers, chunking strategies. Pinecone, Weaviate, the rest. Knowledge is also not finished - RAG has failure modes nobody's solved cleanly - but it's good enough to ship. We crossed the second wall.

## The third wall nobody's climbed

The third wall is experience. Nothing has climbed it. Every agent in production today is a brilliant amnesiac.

This is the wall the industry keeps tripping over because it keeps calling it the wrong thing. We call it "memory" and then we mean five different things by it. ChatGPT remembering you're vegetarian. A vector store of past conversations. A markdown file the agent reads at startup. A summary the LLM writes about itself after every session. None of these are wrong, exactly. They're all just way too small.

The thing missing from agents is not memory in the casual sense. It's experience.

## Knowledge vs memory

The distinction matters and the rest of this essay turns on it.

Knowledge is what's true about the world. Memory is what's true about you in the world.

Knowledge has no owner. Memory has exactly one owner. The Pythagorean theorem is the same for everyone who reads it. The fact that your biggest customer's procurement lead hates Tuesday calls is true only for the agent that learned it. The first is in a textbook. The second isn't anywhere - unless someone built a place for it to live.

This is the gap every enterprise has lived. It's why a six-month employee is five times more useful than a day-one hire who's read the same documents. It's why losing a key person feels like losing something the wiki didn't capture - because it is. Today, every agent in your company is a permanent day-one employee. Same docs. No journey.

## Two parallel rivers, not one

People want to collapse this. They want to say: well, isn't memory just knowledge that hasn't been written down yet? Won't memory eventually mature into knowledge?

No. They're two parallel rivers, not one river flowing into the other.

Knowledge comes from codification - humans abstracting truths and freezing them for general use. Memory comes from living through events - one agent, in one place, accumulating personal understanding nobody else has. Sometimes a human reads their own memory and chooses to codify a piece of it into a playbook or a case study. That's a deliberate act, not an automatic process. Most memory never gets codified, and that's fine.

Two tests if you get stuck. The copy test: if you sent this fact to a stranger, would it still be useful? Universal physical constants survive. Per-user preferences become nonsense. The time test: does the fact need a timestamp to make sense? Water didn't start boiling at 100C - it just is, outside time. A decision made in a meeting last October is anchored to that meeting; the when is part of what makes it meaningful.

Knowledge floats outside time. Memory is embedded in time. That's not a stylistic difference. It's the substrate.

## What experience actually needs

Once experience is the third layer, the architecture question gets sharper: what kind of system does experience actually need?

This is where the industry has been improvising and getting it mostly wrong.

A summary is not experience. Summaries throw away the sequence, the timestamps, the small contradictions that turn out to matter later. The moment you compress "user struggled with onboarding" into a single sentence, you've lost the three specific moments it happened, the exact words used, the gap between when they gave up and when they came back. Summary-based memory works until the question you need to answer is the one the summary threw away.

A vector store of past chats isn't experience either. Cosine similarity is a knowledge retrieval pattern - find things that mean roughly the same thing. Experience needs temporal retrieval - find what happened, in order, with cause and effect intact. A vector store can tell you "this conversation is similar to that one." It can't tell you "this happened because of that."

A knowledge graph alone isn't experience. Graphs are good at facts and relationships, weak at episodes - the lived sequence of what happened before it got distilled into a fact. Experience is graph-shaped on top, event-shaped underneath.

## Why event sourcing

The only data structure that natively preserves experience is an event log. Lossless, append-only, timestamped, ordered. Every interaction, every decision, every outcome, written down as it happened, never overwritten. Layers of structure - entities, relationships, summaries, beliefs - get built on top of the event stream, asynchronously, by background processes that can change their minds. The events themselves never get rewritten. They're the source of truth. Everything else is derived.

This is why an experience layer has to be event-sourced. Not because event sourcing is a clever architecture choice - because experience genuinely is a sequence of events, and any system that flattens that sequence has thrown away the thing you came for.

## What CortexDB is

Not the library. Not the filing cabinet. Not the notes file. Not the framework. Not the runtime. The experience layer.

Lossless event-sourced write path - no LLM on the hot path, nothing summarised or interpreted before it's written down. Four-channel hybrid retrieval - BM25, vector, entity, synonym, fused via reciprocal rank - because experience needs to be queryable across multiple shapes at once. Six-phase recall with an irrelevance gate, so the model doesn't drown in everything that ever happened. Async knowledge graph enrichment, building structure on top of the event stream without ever touching the events themselves. Multi-tenant from day one, because experience is inherently per-agent, per-user, per-organisation.

It's built by the co-creator of Apache Cassandra. The lineage matters here. Cassandra was a bet that the right substrate for the next decade of data was an append-only log with derived structure on top. That bet was right. CortexDB is the same bet, made for a different problem - agents accumulating experience instead of users posting tweets.

## The three-layer frame

Reasoning is the model. Knowledge is RAG. Experience is memory. Every production agent stack will eventually have all three. The ones missing the third layer will feel hollow no matter how good the model gets, no matter how clean the RAG. They'll be brilliant strangers. They'll never become employees.

Models think. RAG knows. CortexDB remembers.

### 3. `@Burachenok` (Artem Burachenok, CEO @alloy.cx)

Created: `Mon Jun 01 21:56:22 +0000 2026`

@prukalpa have been thinking a lot about this lately, in a context of the AI native company workspace  https://t.co/Ri7ExRiSpO

#### Quoted Post: `@Burachenok` - "The shape of the AI workspace"

Created: `Sat May 30 15:07:19 +0000 2026`

The shape of the AI workspace

We started Alloy to discover the shape of the AI workspace: one that helps you run your AI-native company instead of getting in the way. And we feel it's the right time to share an update on that quest.

We are an AI-native team ourselves, so this comes from dogfooding, as well as working with a group of design-partners, as obsessed as we are with getting the most out of AI.

We believe that the workspace infrastructure should be:

- agent agnostic - as agents from many vendors (Claude, Codex, Gemini, etc.) will coexist in every organization;

- agent independent - agents will come and go, but your organizational knowledge and learning should not be stuck in their individual memories and go with them;

- composable - not locked into a single monolith, so organizations can use the pieces they need alongside the rest of their stack.

Below is the outline of the key building blocks of this workspace:

- Bringing together humans and agents from any vendor: Claude, Codex, Alloy, etc., into one shared environment to leverage their relative strengths.

- Shared artifact storage, designed in an agent-native way. People and AI collaborate on artifacts. Shared instructions and skills for agents are stored there. Storage is designed around the tools agents already know.

- Communications happen in a human-native way with humans and in an agent-native way between agents. Agents interact with humans through text and voice in Teams, Slack, WhatsApp, etc., and, with each other, via APIs and MCPs, when humans are not involved.

- Organizational knowledge isn't trapped in individual agents' memories. It's available to every agent and human in the organization. This is achieved with the shared knowledge layer, where the biggest chunk is organizational memory collected and maintained by the agents as they work: what is stored where, who makes which decisions, how things are done, and lessons learned. The human-authored wiki is only a small part. Agent communication and reasoning traces are also stored there, as well as artifact / key decision logs.

- Work is organized with tasks and workflows, not with endless lists of AI chats. Chats are where things get lost. They are great for ad-hoc asks, but not the right structure for the core work.

- Actions in systems of record are done through agents (e.g. reschedule this meeting or change that opportunity deadline) to record WHY it was done, which is the key knowledge that is lost when humans make changes directly.

- The insights and improvement layer creates a virtuous cycle. It turns observed work and collected knowledge into the highest-leverage fixes: the top 2 things the company, a team, or an individual human or agent can change to keep improving.

- The workspace itself is configured by agents. All the workflows, communication channels, systems of record, access management, monitoring, and so on.

This is what we're building at Alloy. I’m going to share more about what we’ve learned from operating this way in future posts.

In the meantime, we invite you to explore Alloy at https://alloy.cx/ to start building your company's shared context and run autonomous agents.

Also, hit me up if you want to chat about this.

### 4. `@sdhilip` (Dhilip Subramanian)

Created: `Mon Jun 01 22:39:52 +0000 2026`

@prukalpa Nicely written, shared it with my team already.
Something I keep wondering when I read writing this sharp, how much time goes into it? The agent can draft, but the structure and the original thinking are what take the hours. Curious how you approach it.

### 5. `@najmuzzaman` (najmuzzaman)

Created: `Mon Jun 01 22:44:10 +0000 2026`

@prukalpa why does the arrow also not flow from agent to shared context layer. that is the missing piece for most "enterprise context layers"

### 6. `@ThuHuong2806` (Huong Analyst | AI & Tech)

Created: `Tue Jun 02 03:10:59 +0000 2026`

@prukalpa The integration of varied context types is crucial for effective AI deployment. It's fascinating how interconnected these concepts are!

### 7. `@prukalpa` reply to `@sdhilip`

Created: `Tue Jun 02 04:09:04 +0000 2026`

@sdhilip These are truly human original thoughts :) AI mainly helps edit/ clarify communication. Thanks so much for noticing!

### 8. `@prukalpa` reply to `@najmuzzaman`

Created: `Tue Jun 02 04:34:17 +0000 2026`

@najmuzzaman Yeah, I talk about them as compounding feedback loops in the article. https://t.co/CsjpJq6srP

Attached image URL: https://pbs.twimg.com/media/HJyD2J7b0AADMDd.jpg

#### Image Transcription

Title: `The AI Context Layer Architecture`

Left column: `Context Mining`
- Systems of Record
- Systems of Data
- Systems of Knowledge
- Systems of Work
- Runtime Signals

Center block: `The Context Substrate`
- AI-Ready Data and Knowledge Graph
  - Trusted data, assets, lineage, usage, facts
- Semantics and Ontology
  - Meaning, relationships, taxonomies, definitions
- Skills
  - Workflows, playbooks, procedures, know-how

Middle loop: `Compounding Learning Loops`

Bottom middle: `Context Development Lifecycle`
- Build
- Test
- Review
- Approve
- Deploy
- Learn

Lifecycle notes
- AI bootstraps and simulates
- Humans resolve ambiguity, add tacit knowledge, and approve

Right column: `Context Activation`
- Search
- APIs
- SQL
- MCP
- Vector Retrieval
- Hybrid Assembly

Activation targets
- Copilots
- Agents
- Analytics
- Workflows
- Enterprise Apps

Bottom bar: `Context Governance and Observability`
- Context Quality
- Drift
- Lineage
- Versioning
- Approval Workflows

Image credit on diagram: `Image by Atlan`

### 9. `@RexCAnderson` (Rex C. Anderson)

Created: `Tue Jun 02 13:57:21 +0000 2026`

@prukalpa Great article, thank you for this. We've been building something similar for a solo entrepreneur, so on a reduced scale, but still providing external memory layers that all agents can access. Working on the self-improvement autonomous agents now.

### 10. `@NaijaBet` (NaijaBet.com)

Created: `Tue Jun 02 15:06:10 +0000 2026`

@prukalpa Thinking about your request
