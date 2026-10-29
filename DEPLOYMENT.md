# CI/CD pipeline and cloud deployment

Every push to GitHub runs an automated pipeline that tests Vaultwise, checks that the AI's quality has not
dropped, builds the Docker images, and, on the `main` branch, deploys the app to **Hugging Face Spaces**.

```
 git push ──► 1. TEST ─────────────► 2. BUILD ─────────────────► 3. DEPLOY ───────────► 4. VERIFY
              lint (ruff)             server image builds          upload to the HF Space   wait until running
              41 unit/API tests       cloud image: app + Ollama    (main branch only)       ask the live app
              AI quality gate         + models                                               "What is my notice
              (9 checks)              ask the real model one                                 period?" → must say 60
                                      question end-to-end
              ✗ any failure stops the pipeline: nothing broken is ever deployed
```

| Stage | What it proves | File |
|---|---|---|
| Lint | code follows the style rules, no undefined names or unused imports | `pyproject.toml` (`[tool.ruff]`) |
| Tests | 41 tests of chunking, search, citations, refusals, uploads, privacy, cloud mode | `tests/` |
| **Quality gate** | re-scores the stored evaluation answers with the current code; fails if accuracy, refusals, citation precision or the margin over the no-AI-search baseline drop below set thresholds | `eval/quality_gate.py` |
| Build + end-to-end | the cloud image builds, starts, loads the model and answers a real question correctly | `deploy/huggingface/Dockerfile`, `deploy/hf_deploy.py` |
| Deploy + verify | the live Space is updated and answers the same question correctly | `.github/workflows/ci-cd.yml` |

---

## One-time setup (about 10 minutes)

### 1. Put the project on GitHub (private)

1. Sign in at https://github.com and click **New repository**.
2. Name it `vaultwise`, choose **Private**, and **do not** tick "Add a README" (the project already has one).
3. In the VS Code terminal, inside the project folder, run the two commands GitHub shows under
   "…or push an existing repository", which look like:

   ```powershell
   git remote add origin https://github.com/<your-github-username>/vaultwise.git
   git push -u origin main
   ```

   Git opens a browser window the first time to sign you in.

### 2. Create a Hugging Face account and token

1. Sign up at https://huggingface.co/join (free).
2. Go to **Settings → Access Tokens → Create new token**, choose **Write**, name it `github-deploy`, and copy it.

### 3. Connect GitHub to Hugging Face

In your GitHub repository: **Settings → Secrets and variables → Actions**.

| Where | Name | Value |
|---|---|---|
| *Secrets* tab → New repository secret | `HF_TOKEN` | the token from step 2 |
| *Variables* tab → New repository variable | `HF_SPACE` | `<your-hf-username>/vaultwise` |
| *Secrets* tab (recommended) | `VAULTWISE_ADMIN_KEY` | any password; only someone with it can upload or delete documents on the cloud demo |

### 4. Run it

Open the **Actions** tab → **CI/CD** → **Run workflow** (or just push any change). The four stages appear
with green ticks as they pass. The first deployment takes about 20-30 minutes, because Hugging Face downloads
and builds the AI model into the image. Later ones are faster.

The pipeline creates the Space for you (private) and prints its address, which looks like:

```
https://<your-hf-username>-vaultwise.hf.space
```

---

## Showing it to your professor

The Space is created **private**, so only you can open it while signed in to Hugging Face. To let your
professor open it, either:

- make it public: Space page → **Settings → Change visibility → Public** (it only contains the fictional
  sample documents, and uploads need the admin key), or
- show it from your own browser, signed in.

The GitHub repository stays private; invite your professor under **Settings → Collaborators** if they need
to see the code and the pipeline runs.

---

## What the cloud version is (and is not)

| | Local version (`run.bat`) | Cloud demo (Hugging Face) |
|---|---|---|
| Where the AI model runs | your laptop | inside the cloud container (no third-party AI service) |
| Where documents are stored | `C:\Users\<you>\.vaultwise`, outside OneDrive | the cloud server's disk, wiped on restart |
| Documents | your real files | three fictional samples, preloaded |
| Uploads | anyone using your laptop | only with the admin key |
| Summary model | Llama 3.1 8B | Llama 3.2 3B (the free CPU is too slow for 8B) |
| Speed | 5-15 s per answer | about 15-40 s per answer on the shared free CPU |
| Banner | "Offline · Private" | amber "Cloud demo: do not upload real confidential files" |

**Use the local version for real confidential documents.** The cloud demo exists to show that the system
deploys and runs in the cloud. A company would run the same container inside its *own* cloud account
(for example a private Azure or AWS network), so documents never reach an outside AI provider.

---

## Costs (free tiers at the time of writing; check the providers' current pages)

- **GitHub Actions:** private repositories on the free plan include a monthly allowance of minutes. One full
  pipeline run takes about 25-35 minutes, mostly building the cloud image.
- **Hugging Face Spaces:** the free "CPU basic" hardware (2 vCPU, 16 GB RAM) is enough; free Spaces go to sleep
  after a period without visitors and wake up on the next visit (about a minute).

---

## Troubleshooting

| Problem | Fix |
|---|---|
| The **deploy** stage says "skipping deployment" | `HF_TOKEN` (secret) or `HF_SPACE` (variable) is missing or misspelled |
| Deploy fails with 401/403 | the token must have **Write** permission |
| Space shows **Build error** | open the Space → **Logs**; usually a temporary download failure, so re-run the workflow |
| Smoke test fails but the Space runs | the free CPU was busy; re-run the job. It must answer "60 days" for the sample contract |
| **Quality gate** fails | a code change lowered the measured quality; the log shows which check, value and threshold |
| Want to test the cloud image on your laptop | `python deploy/hf_deploy.py bundle build/space`, then `docker build -t vaultwise:cloud build/space`, then `docker run -p 7860:7860 vaultwise:cloud`, and open http://localhost:7860 |
