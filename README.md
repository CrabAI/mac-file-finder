# mac-file-finder

A macOS CLI tool for local file search powered by Spotlight. Find files using natural language queries and open them in Finder or your default app directly from the terminal.

## Features

- **Natural Language Search:** Uses `mdfind` to search file names, content, and metadata simultaneously
- **Scoped Search:** Limits search to specified directories via `-onlyin` for better speed and accuracy
- **Metadata Display:** Shows file name, kind, and last modified date for each result
- **Interactive Actions:**
  - `[r]` Reveal file location in Finder (with file selected)
  - `[o]` Open file with its default application

## Requirements

- macOS (Spotlight is required)
- Python 3.9+

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/CrabAI/mac-file-finder.git
cd mac-file-finder
```

### 2. Create a virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your config file

```bash
cp config.example.py config.py
```

Edit `config.py` to set your search paths:

```python
# config.py
SEARCH_ROOTS = [
    "~/Documents",
    "~/Desktop",
    # "~/Downloads",  # add more paths as needed
]

TOP_N = 10  # maximum number of results
```

> **Note:** `config.py` is excluded from version control via `.gitignore` because it contains personal directory paths.

## Usage

```bash
python run.py
```

### Example session

```
macOS Local File Finder (Spotlight-based)
Search roots: ~/Documents, ~/Desktop

Enter a file description in natural language (q to quit): summer vacation photos

📁 Candidate files:
1. summer_vacation_2024.jpg | JPEG image | 2024-08-15 14:32:00 +0000
   /Users/yourname/Desktop/summer_vacation_2024.jpg
2. vacation_summary.pdf | PDF Document | 2024-08-20 09:10:00 +0000
   /Users/yourname/Documents/vacation_summary.pdf

Search complete.

Action: [r] Reveal in Finder / [o] Open file / [Enter] Skip: r
Enter number (1~2): 1
```

### Search tips

| Situation | Example input |
|-----------|---------------|
| File name keyword | `budget report` |
| File type | `invoice pdf` |
| Content keyword | `API key configuration` |
| Date + keyword | `2024 contract` |

> For best results, use concise keywords rather than long sentences.

## Project Structure

```
mac-file-finder/
├── run.py              # Main script (search loop + actions)
├── config.example.py   # Config template (committed)
├── config.py           # Your personal config (excluded via .gitignore)
├── requirements.txt    # Python dependencies
└── README.md
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SEARCH_ROOTS` | `["~/Documents", "~/Desktop"]` | List of directories to search |
| `TOP_N` | `10` | Maximum number of results to display |

## How It Works

```
User input (natural language)
       │
       ▼
  mdfind -onlyin <root> <query>     ← Searches macOS Spotlight index
       │
       ▼
  Deduplicate + take top TOP_N results
       │
       ▼
  mdls -name kMDItemDisplayName
       -name kMDItemKind
       -name kMDItemFSContentChangeDate   ← Fetch file metadata
       │
       ▼
  Display results → User selects action
       │
  ┌────┴────┐
  │ [r]     │ [o]
  ▼         ▼
open -R   open
(Finder)  (default app)
```

## Troubleshooting

### No results returned

- Make sure Spotlight indexing is complete: **System Settings → Siri & Spotlight**
- Verify that `SEARCH_ROOTS` paths exist and are correct
- Try shorter or more specific keywords

### `mdfind` command not found

- This tool is macOS-only. It does not work on Linux or Windows.

### Missing `config.py` error

```bash
cp config.example.py config.py
```

## License

MIT
