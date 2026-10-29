# How to run Vaultwise from the terminal

Vaultwise runs entirely on your computer with **one command**. It needs only Python and Ollama: no Docker,
no GPU, and no internet connection (internet is needed only once, to download the AI models).

---

## Every day: start Vaultwise with one command

1. Open the project folder in VS Code (**File → Open Folder → `IDT FINAL PROJECT`**).
2. Open a terminal: **Terminal → New Terminal** (or press <kbd>Ctrl</kbd> + <kbd>`</kbd>).
3. Type:

   ```powershell
   .\run.bat
   ```

Your browser opens Vaultwise at **http://127.0.0.1:8000** automatically.
Keep the terminal open while you use it. To stop Vaultwise, click in the terminal and press **Ctrl + C**.

You can also start it without VS Code: open the folder in File Explorer and double-click **`run.bat`**.

What `run.bat` does, so you know what to expect:

| Step | What happens |
|---|---|
| 1 | If Vaultwise is already running, it just opens the browser |
| 2 | Checks Python, and installs the required packages the first time |
| 3 | Checks that **Ollama** (the local AI engine) is running, and starts it if not |
| 4 | Checks the AI models, and downloads any that are missing the first time (about 7 GB in total) |
| 5 | Starts Vaultwise on `127.0.0.1`, so only this computer can open it, and opens your browser |

Options:

```powershell
.\run.bat -Port 8001      # use another port if 8000 is busy
.\run.bat -NoBrowser      # start without opening the browser
```

> The first question after starting takes 30-60 seconds while the AI model loads; after that answers take
> about 5-15 seconds and summaries about 1-2 minutes.

---

## First time only: setup on a new computer

You only need this if you move the project to another computer. On this laptop everything is installed.

1. **Python 3.10 or newer**: https://www.python.org/downloads/ (tick **"Add python.exe to PATH"** during setup).
2. **Ollama**: https://ollama.com/download (install and leave it running; it starts with Windows).
3. In the project folder, run `.\run.bat`. It installs the Python packages and downloads the models:
   `llama3.2:3b` (answers), `nomic-embed-text` (search) and `llama3.1:8b` (summaries, optional).

To do the same by hand:

```powershell
python -m pip install -r requirements.txt
ollama pull llama3.2:3b
ollama pull nomic-embed-text
ollama pull llama3.1:8b
```

---

## Manual start (if you prefer typing the commands yourself)

```powershell
cd "C:\Users\91830\OneDrive\Desktop\IDT FINAL PROJECT"
python -m uvicorn vaultwise.api:app --app-dir src --host 127.0.0.1 --port 8000
```

Then open http://127.0.0.1:8000 in your browser.

---


## Running the tests and the evaluations (for the project report)

```powershell
python -m pytest -q                                   # 39 automated tests, about 5 seconds, no AI needed

# Evaluation 1: company-policy questions (results already in results/; re-running takes about 1.5 hours)
python eval/run_eval.py retrieval
python eval/run_eval.py generate
python eval/run_eval.py generate --systems rag_hybrid,llm_only --model llama3.1:8b
python eval/report.py                                 # rebuilds tables and charts from saved outputs (seconds)
python eval/audit.py score                            # automatic scorer vs manual labels

# Evaluation 2: private company documents (about 30 minutes)
python eval/run_private_eval.py answers
python eval/run_private_eval.py summaries
python eval/run_private_eval.py report                # writes results/private_results.md
```

`eval/report.py` and `eval/run_private_eval.py report` only re-score saved outputs, so they run in seconds
and give the same numbers every time.

---

## Where your documents are stored

Your private documents, their search index and logs are kept in:

```
C:\Users\91830\.vaultwise\
```

That folder is outside OneDrive, so it is never uploaded to the cloud. To remove a document, use **Delete**
in the app (it removes the file and its index entries). To wipe everything, close Vaultwise and delete that folder.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `.\run.bat` is "not recognized" | Make sure the terminal is in the project folder: `cd "C:\Users\91830\OneDrive\Desktop\IDT FINAL PROJECT"` |
| "Port 8000 is used by another program" | Vaultwise may already be running in another terminal; close it, or run `.\run.bat -Port 8001` |
| Badge says **AI engine not running** | Open **Ollama** from the Start menu, then reload the page |
| "Python was not found" | Install Python and tick "Add to PATH", then open a new terminal |
| First answer is slow | Normal: the model loads into memory the first time (30-60 s) |
| A PDF gives "No text could be extracted" | It is a scanned image; export it as a text PDF or run OCR first |
| The page does not open | Go to http://127.0.0.1:8000 yourself while the terminal is still running |
