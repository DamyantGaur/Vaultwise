# Vaultwise: Competitor Analysis

*Researched 28–29 October 2026. Every price and data-handling claim was checked against a live web page on those
dates (sources at the end). Prices change often; "not verified" means no current source was found. Some vendor
pages showed local currency, and a few could not be fetched; those cases are marked and use a named secondary
source.*

Vaultwise is compared with four groups of products:

| Group | Examples | Where your documents go |
|---|---|---|
| A. Cloud "chat with your documents" assistants | ChatGPT, Microsoft 365 Copilot, Gemini, Claude, Acrobat AI | the vendor's cloud |
| B. Enterprise knowledge search platforms | Glean, Rovo, Guru, Notion AI, Box AI | the vendor's cloud (Glean can run in the customer's own cloud) |
| C. Local / self-hosted document AI | AnythingLLM, PrivateGPT, GPT4All, Open WebUI, LM Studio, Kotaemon, Khoj | your machine or your server: **the closest competitors** |
| D. Contract-specific AI | Luminance, Spellbook, Ironclad, Kira, Harvey | the vendor's cloud |

---

## A. Cloud "chat with your documents" assistants

| Product | What it is | Where data goes | Cites sources? | Pricing | Strength vs Vaultwise | Weakness vs Vaultwise |
|---|---|---|---|---|---|---|
| **ChatGPT Business / Enterprise** (OpenAI) | ChatGPT workspace with file uploads, projects, connectors | OpenAI cloud; business data not used for training by default | not verified for uploads | Business: $20/user/mo annual, $25 monthly; Enterprise: contact sales *(secondary sources; OpenAI's page was blocked)* | frontier models, very capable | confidential files leave the laptop; internet; paid per seat |
| **Microsoft 365 Copilot** | assistant grounded in M365 files, mail, Teams | Microsoft 365 service boundary; prompts not used to train the models | yes, lists sources | $30/user/mo annual (enterprise); Copilot Business $18/user/mo promotional (normally $21) | native SharePoint/OneDrive access, permissions, compliance tooling | expensive add-on on top of M365; cloud only |
| **Google Gemini in Workspace / Gemini Notebook** (NotebookLM was renamed in July 2026) | Gemini in Workspace apps plus a source-grounded notebook | Google cloud; Workspace data not used for training without permission | yes (answers from uploaded sources) | bundled in Workspace Business plans, ≈ $14/user/mo annual for Business Standard *(secondary source; Google's page showed INR)* | closest cloud match to Vaultwise's "answer from my documents" | data goes to Google; no offline mode |
| **Claude Team / Enterprise** (Anthropic) | Claude with projects and file uploads | Anthropic cloud; no model training by default | not verified | Team $20/seat/mo annual ($25 monthly); Enterprise $20/seat/mo annual + usage, 20-seat minimum | strong long-document reasoning | cloud; per-seat plus usage cost |
| **Adobe Acrobat AI Assistant** | Q&A and summaries inside Acrobat | Adobe cloud; content never used to train Adobe's models | yes, always cited | add-on £4.98/mo (UK page); Acrobat Studio £24.98/mo | best PDF handling, including OCR of scanned PDFs | cloud; subscription |
| **Humata** | web app to chat with PDFs | Humata cloud; SOC 2 on Team plans only | not stated | Free; Expert $9.99/mo; Team $49/user/mo | cheap, no setup | cloud; thin published data-handling terms |
| **ChatPDF** | web app to chat with PDFs | ChatPDF cloud, encrypted | yes, clickable citations | free (2 docs/day); Plus price not verified | simplest experience | confidential documents go to a third party |

## B. Enterprise knowledge search / RAG platforms

| Product | What it is | Where data goes | Cites? | Pricing | Strength vs Vaultwise | Weakness vs Vaultwise |
|---|---|---|---|---|---|---|
| **Glean** | permission-aware search and assistant across 100+ apps | single-tenant SaaS, or a tenant in the customer's own AWS/GCP | yes | contact sales | connectors, permissions, certifications (SOC 2, ISO 42001, HIPAA) | expensive, heavy to adopt |
| **Atlassian Rovo** | AI search, chat and agents over Jira, Confluence and connected apps | Atlassian cloud | not verified | included in Standard/Premium/Enterprise plans, with monthly credits; extra $0.01/credit | free if you already use Atlassian | only useful inside Atlassian |
| **Guru** | governed knowledge base with cited answers | hosted; customer data never trains an LLM | yes, with audit trail | contact sales | knowledge-verification workflows | cloud; for curated wikis, not ad-hoc contracts |
| **Notion AI** | AI agent and search inside Notion | Notion cloud and LLM providers; zero retention on Enterprise | not verified | Business $20/member/mo (AI included) | cheap if the team already uses Notion | documents must live in Notion |
| **Box AI** | Q&A and summaries over files in Box | Box cloud plus model providers; no training on customer data | not verified | per-plan prices not shown; ≈ $50/user/mo Enterprise Plus *(Capterra, not verified)* | governance where company files already live | cloud; expensive tiers |

## C. Local / self-hosted private document AI (closest competitors)

| Product | What it is | Where data goes | Cites? | Pricing | Strength vs Vaultwise | Weakness vs Vaultwise |
|---|---|---|---|---|---|---|
| **AnythingLLM** | desktop and Docker "private AI assistant" with document chat | fully local (desktop), self-hosted, or their cloud | yes | desktop/self-hosted free (MIT); cloud $50–$99/mo | mature, one-file install, multi-user, 67k+ GitHub stars | general-purpose; refusing when the document is silent isn't its core design |
| **PrivateGPT** (Zylon) | open-source RAG API on local models | self-hosted / local | yes | free (Apache-2.0); Zylon enterprise: contact sales | production-oriented, enterprise path | a developer framework, not an end-user app |
| **GPT4All LocalDocs** (Nomic) | desktop LLM app with local document chat | fully local | yes, file-level sources | free | very easy for non-experts | meaning-only search (Vaultwise is hybrid); file-level, not clause-level; last release Feb 2025 |
| **Open WebUI + Ollama** | self-hosted ChatGPT-style interface with RAG | fully local / offline-capable | yes, page-number citations configurable | free (Open WebUI License); enterprise plan | already has hybrid BM25 + vector search with reranking; LDAP/SCIM | general chat tool, not built for strict "answer only from the document" |
| **LM Studio** | desktop app to run local LLMs, with document attach | fully local | not stated | free, including for work | excellent model management | basic RAG |
| **Kotaemon** (Cinnamon) | open-source document Q&A interface | local / self-hosted (Ollama) | yes, with highlighted passages in a PDF viewer | free (Apache-2.0) | hybrid retrieval with reranking and passage highlighting: the closest feature match | heavier setup |
| **Khoj** | self-hostable "AI second brain" | local, self-hosted or Khoj cloud | not verified | free self-host (AGPL-3.0) | many source integrations | focus shifting to a newer project |

## D. Contract-specific AI (brief)

| Product | Target | Data | Pricing | Note vs Vaultwise |
|---|---|---|---|---|
| **Luminance** | legal, procurement and HR teams in enterprises | vendor cloud; ISO 27001, SOC 2 | contact sales | deep legal analytics; enterprise only |
| **Spellbook** | lawyers, as a Word add-in | cloud with zero data retention | per seat, contact sales | for drafting, not for employees reading documents |
| **Ironclad** | legal and operations contract lifecycle | US-hosted Google Cloud | custom quote | a workflow platform, not personal Q&A |
| **Kira (Litera)** | law firms, clause extraction | cloud or on-premise | quote only *(third-party estimates $45k–$200k+/yr, not verified)* | very costly |
| **Harvey** | law firms and in-house legal teams | vendor cloud; SOC 2, ISO 27001/42001 | contact sales | top legal reasoning; not available to an ordinary employee |

---

## Where Vaultwise stands

**Where it genuinely differs**
- **The combination, not any single feature.** Local inference exists elsewhere (AnythingLLM, GPT4All, Open
  WebUI, Kotaemon). Vaultwise combines four things in one tool for a non-legal employee:
  1. local inference;
  2. **strict grounding with refusal** when the document lacks the answer;
  3. **clause-level citation**;
  4. hybrid retrieval.
- **Measured trust.** Vaultwise publishes its own evaluation: 100% correct refusals on unanswerable questions,
  4% answers with an unsupported number against 49% for an AI model alone, and a held-out document scored
  15/15 (see `docs/REPORT.md`). None of the local competitors above publishes refusal or hallucination
  measurements for document Q&A.
- **Zero cost and no vendor exposure.** Everything in groups A, B and D sends documents to a vendor cloud and
  costs about $14–$50+ per user per month, or needs a sales quote. Vaultwise needs no procurement approval or
  data-processing agreement.
- **CPU-only and offline after setup.** It runs on an ordinary laptop with no internet connection.

**Where it is clearly weaker** (it is a student prototype)
- **Answer quality on hard documents.** Llama 3.2 3B / 3.1 8B are far weaker than the frontier models behind
  Copilot, ChatGPT, Claude and Gemini, especially on long, complex contracts.
- **Enterprise features.** No OCR for scanned PDFs, no SharePoint/Drive connectors, no SSO, multi-user
  administration, audit dashboards, support or compliance certifications.
- **Retrieval is not a moat.** Open WebUI and Kotaemon already ship hybrid search with reranking.
- **Scale.** Small, synthetic evaluation sets (114 questions) against competitors with millions of users.

**The three most direct competitors**
1. **Kotaemon:** open source, local via Ollama, hybrid retrieval, passage-highlighted citations. Vaultwise's
   angle is simpler setup, stricter refusals and measured trust.
2. **AnythingLLM (desktop):** free, fully local, one-file install. The tool a privacy-conscious employee is
   most likely to install instead.
3. **Open WebUI + Ollama:** the same Ollama stack, hybrid search and citations, widely adopted, but a general
   chat interface rather than a document-grounded assistant.

Among cloud tools, the closest idea is **Gemini Notebook (formerly NotebookLM)**, which also answers from
uploaded sources, but on Google's cloud.

## Why the problem matters: market evidence

- **Employees paste confidential data into public AI tools.** In a TELUS Digital survey of 1,000 US employees at
  companies with 5,000+ staff (January 2025), **57% of enterprise employees using generative AI admitted entering
  sensitive information into public AI assistants**, and 68% used them through personal accounts.
- **Risky prompts are common.** Harmonic Security found 8.5% of employee prompts in Q4 2024 posed potential
  security risks (reported January 2025).
- **The market is large and growing.** Gartner forecast worldwide AI spending of **$2.59 trillion in 2026, up
  47%** (May 2026), later raised to about **$2.7 trillion, up 49.5%** (16 September 2026, press-release title).
- **Document-grounded AI is mainstream.** Google reports 30M+ users and 600k+ organisations for NotebookLM /
  Gemini Notebook *(secondary report of the July 2026 announcement)*.

---

## Sources

**Group A**
- Claude pricing: https://claude.com/pricing
- Microsoft 365 Copilot pricing: https://www.microsoft.com/en-us/microsoft-365-copilot/pricing
- Microsoft 365 Copilot enterprise: https://www.microsoft.com/en-us/microsoft-365-copilot/enterprise
- Copilot sources: https://support.microsoft.com/en-us/Microsoft-365-Copilot/control-review-sources-copilot-chat
- OpenAI business data: https://openai.com/business-data/
- ChatGPT Business pricing (secondary): https://paretotalent.com/guides/chatgpt-for-business/
- ChatGPT Business pricing (secondary): https://www.eesel.ai/blog/chatgpt-work-pricing
- Google Workspace pricing: https://workspace.google.com/pricing
- Google Workspace pricing in USD (secondary): https://www.dragapp.com/blog/google-workspace-pricing/
- Gemini in Workspace privacy: https://support.google.com/docs/answer/14615114
- Gemini Notebook rename: https://workspaceupdates.googleblog.com/2026/07/notebooklm-now-gemini-notebook.html
- Adobe Acrobat AI Assistant: https://www.adobe.com/acrobat/generative-ai-pdf.html
- Humata pricing: https://www.humata.ai/pricing
- ChatPDF: https://www.chatpdf.com/

**Group B**
- Glean pricing: https://www.glean.com/pricing
- Glean deployment models: https://docs.glean.com/get-started/build/about-deployment
- Atlassian Rovo pricing: https://www.atlassian.com/software/rovo/pricing
- Guru pricing: https://www.getguru.com/pricing
- Notion pricing: https://www.notion.com/pricing
- Box pricing: https://www.box.com/pricing
- Box AI principles: https://www.box.com/legal/boxaiprinciples
- Box Enterprise Plus price (secondary): https://www.capterra.com/p/148766/Box/pricing/

**Group C**
- AnythingLLM: https://anythingllm.com/pricing
- AnythingLLM on GitHub: https://github.com/Mintplex-Labs/anything-llm
- PrivateGPT: https://github.com/zylon-ai/private-gpt
- GPT4All LocalDocs: https://docs.gpt4all.io/gpt4all_desktop/localdocs.html
- GPT4All releases: https://github.com/nomic-ai/gpt4all/releases
- Open WebUI: https://github.com/open-webui/open-webui
- Open WebUI RAG docs: https://docs.openwebui.com/features/chat-conversations/rag/
- LM Studio RAG docs: https://lmstudio.ai/docs/app/basics/rag
- LM Studio, free for work: https://www.lmstudio.ai/blog/free-for-work
- Kotaemon: https://github.com/Cinnamon/kotaemon
- Khoj: https://github.com/khoj-ai/khoj

**Group D**
- Luminance: https://www.luminance.com/
- Spellbook pricing: https://spellbook.com/pricing
- Ironclad pricing: https://ironcladapp.com/pricing
- Harvey: https://www.harvey.ai/
- Kira price estimates (third-party): https://costbench.com/software/ai-legal-tools/kira-systems/

**Market data**
- TELUS Digital survey: https://www.silicon.co.uk/press-release/telus-digital-survey-reveals-enterprise-employees-are-entering-sensitive-data-into-ai-assistants-more-than-you-think
- Harmonic Security prompt study: https://thejournal.com/Articles/2025/01/22/1-in-10-AI-Prompts-Could-Expose-Sensitive-Data.aspx
- Gartner, May 2026 (via CIO Dive): https://www.ciodive.com/news/global-AI-spending-2026/820656/
- Gartner, September 2026 (title only; page blocked): https://gartner.com/en/newsroom/press-releases/2026-09-16-gartner-forecasts-worldwide-ai-spending-to-grow-49-point-5-percent-in-2026
