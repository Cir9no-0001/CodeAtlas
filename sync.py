import os
import requests
import re
import json
from datetime import datetime
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("America/Toronto")
META_FILE = "leetcode_meta.json"
NOTES_FILE = "leetcode_notes.json"
username = os.environ.get("LEETCODE_USERNAME")
session = os.environ.get("LEETCODE_SESSION")

if not username or not session:
    raise Exception("Missing LEETCODE_USERNAME or LEETCODE_SESSION")

headers = {
    "cookie": f"LEETCODE_SESSION={session}",
    "referer": "https://leetcode.com",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0"
}

def now():
    return datetime.now(LOCAL_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")

def post(query):
    try:
        r = requests.post(
            "https://leetcode.com/graphql",
            json=query,
            headers=headers,
            timeout=15
        )
        data = r.json()
        if "errors" in data:
            print("GRAPHQL ERROR:", data["errors"])
        return data

    except Exception as e:
        print("REQUEST ERROR:", e)
        return {}

def clean(name):
    return (
        re.sub(
            r"[^a-zA-Z0-9\- ]",
            "",
            name.strip()
        )
        .lower()
        .replace(" ", "-")
        .strip("-")
    )


def repair_notes_json():

    print("\nChecking missing notes entries...")

    added = 0

    for difficulty in ["easy", "medium", "hard"]:

        folder = f"leetcode/{difficulty}"

        if not os.path.exists(folder):
            continue

        for file in os.listdir(folder):

            if not file.endswith(".sql"):
                continue

            slug = file[:-4]   # removes .sql

            if slug not in notes:

                notes[slug] = {
                    "notes": ""
                }

                print("Added missing notes entry:", slug)
                added += 1


    if added == 0:
        print("All SQL files already have notes entries.")

    else:
        print(f"Added {added} missing notes entries.")
    
def format_notes(note_text):

    max_length = 90

    formatted_lines = []

    if note_text:

        for paragraph in note_text.split("\n"):

            words = paragraph.split(" ")

            current_line = ""

            for word in words:

                if len(current_line) + len(word) + 1 <= max_length:
                    current_line += word + " "

                else:
                    formatted_lines.append(current_line.rstrip())
                    current_line = word + " "

            if current_line:
                formatted_lines.append(current_line.rstrip())

    else:
        formatted_lines.append("")


    return [
        "/*",
        "Notes:",
        *formatted_lines,
        "*/"
    ]

if os.path.exists(META_FILE):
    with open(META_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
else:
    meta = {}

if os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        notes = json.load(f)
else:
    notes = {}

response = post({
    "query": """
    query recentAcSubmissions($username:String!){
        recentAcSubmissionList(username:$username){
            title
            titleSlug
        }
    }
    """,
    "variables": {
        "username": username
    }
})

subs = (
    response
    .get("data", {})
    .get("recentAcSubmissionList", [])
)

if not subs:
    raise Exception("No submissions returned")

print("\nAccepted submissions:")

for s in subs:
    print("-", s["title"])

difficulty_cache = {}

def get_difficulty(slug):

    if slug in difficulty_cache:
        return difficulty_cache[slug]

    response = post({
        "query": """
        query questionData($titleSlug:String!){
            question(titleSlug:$titleSlug){
                difficulty
            }
        }
        """,
        "variables": {
            "titleSlug": slug
        }
    })

    difficulty = (
        response
        .get("data", {})
        .get("question", {})
        .get("difficulty", "unknown")
        .lower()
    )

    difficulty_cache[slug] = difficulty

    return difficulty

def get_submission(slug):

    history = post({
        "query": """
        query submissionList(
            $offset:Int!,
            $limit:Int!,
            $questionSlug:String!
        ){
            submissionList(
                offset:$offset,
                limit:$limit,
                questionSlug:$questionSlug
            ){
                submissions{
                    id
                }
            }
        }
        """,
        "variables": {
            "offset": 0,
            "limit": 1,
            "questionSlug": slug
        }
    })

    try:
        submission_id = (
            history["data"]
            ["submissionList"]
            ["submissions"][0]
            ["id"]
        )

    except Exception:
        print("No submission history:", slug)
        return {
            "code": "",
            "runtime": None
        }

    detail = post({
        "query": """
        query submissionDetails($submissionId:Int!){
            submissionDetails(
                submissionId:$submissionId
            ){
                code
                runtime
            }
        }
        """,
        "variables": {
            "submissionId": int(submission_id)
        }
    })


    result = (
        detail
        .get("data", {})
        .get("submissionDetails")
    )


    if not result:
        print("No code returned:", slug)
        return {
            "code": "",
            "runtime": None
        }


    return {
        "code": result.get("code", ""),
        "runtime": result.get("runtime")
    }

def update_notes_in_files():

    print("\nUpdating notes from leetcode_notes.json...")

    for slug, data in notes.items():

        note_text = data.get("notes", "")

        found = False

        for difficulty in ["easy", "medium", "hard"]:

            path = f"leetcode/{difficulty}/{slug}.sql"

            if not os.path.exists(path):
                continue

            found = True

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            if "-- Notes:" in content or "/*\nNotes:" in content:
                if "/*\nNotes:" in content:

                    before_notes = content.split("/*\nNotes:")[0]
                    notes_index = content.index("/*\nNotes:")
                
                    code_start = content.find("*/", notes_index)
                
                    if code_start != -1:
                        code = content[code_start + 2:].lstrip("\n")
                        code = "\n\n" + code
                    else:
                        code = ""
            
                else:
                
                    before_notes = content.split("-- Notes:")[0]
                    notes_index = content.index("-- Notes:")
                
                    code_start = content.find("\n\n", notes_index)
                
                    if code_start != -1:
                        code = content[code_start:].lstrip("\n")
                        code = "\n\n" + code
                    else:
                        code = ""

            else:

                lines = content.split("\n")
                insert_position = 0

                for i, line in enumerate(lines):
                    if not line.startswith("--"):
                        insert_position = i
                        break

                before_notes = "\n".join(lines[:insert_position]) + "\n"
                code = "\n".join(lines[insert_position:])

            new_content = before_notes

            for line in format_notes(note_text):
                new_content += line + "\n"
            
            new_content += code

            if new_content != content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print("Updated notes:", path)

            else:
                print("Already correct:", path)

            break

        if not found:
            print("SQL file not found:", slug)
            
for submission in subs:

    title = submission["title"]
    slug = submission["titleSlug"]

    difficulty = get_difficulty(slug)

    if difficulty not in ["easy", "medium", "hard"]:
        print("Unknown difficulty:", title)
        continue


    data = get_submission(slug)

    code = data["code"]
    runtime = data["runtime"]

    if not code:
        print("Skipped:", title)
        continue

    if slug not in meta:
        meta[slug] = {
            "first_seen": now()
        }

    if slug not in notes:
        notes[slug] = {
            "notes": ""
        }

    folder = f"leetcode/{difficulty}"

    os.makedirs(
        folder,
        exist_ok=True
    )

    path = f"{folder}/{clean(title)}.sql"


    content = [
        f"-- {title}",
        f"-- https://leetcode.com/problems/{slug}",
        f"-- difficulty: {difficulty}",
        f"-- first_seen: {meta[slug]['first_seen']}"
    ]

    if runtime:
        content.append(
            f"-- runtime: {runtime}ms"
        )

    content.extend([
        ""
    ])
    
    content.extend(
        format_notes(notes[slug]["notes"])
    )
    
    content.extend([
        "",
        code
    ])

    new_content = "\n".join(content)
    old_content = ""

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            old_content = f.read()


    if new_content != old_content:

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print("Updated:", title)

update_notes_in_files()

repair_notes_json()

stats = {
    "easy": 0,
    "medium": 0,
    "hard": 0,
    "total": 0,
    "last_updated": now()
}

for difficulty in ["easy", "medium", "hard"]:

    folder = f"leetcode/{difficulty}"

    if os.path.exists(folder):

        stats[difficulty] = len([
            file
            for file in os.listdir(folder)
            if file.endswith(".sql")
        ])

stats["total"] = (
    stats["easy"]
    +
    stats["medium"]
    +
    stats["hard"]
)

with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)

with open(NOTES_FILE, "w", encoding="utf-8") as f:
    json.dump(notes, f, indent=2)

with open("leetcode_stats.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2)

readme = f"""# CodeAtlas 

**Status:** Pre-Alpha Testing

![Version](https://img.shields.io/badge/version-v0.3.0--alpha-orange)
![Python](https://img.shields.io/badge/python-3.12-blue)
![GitHub Actions](https://github.com/Cir9no-0001/CodeAtlas/actions/workflows/leetcode.yml/badge.svg)

> An automated LeetCode solution synchronization platform that retrieves accepted submissions, organizes solutions, manages documentation, and tracks programming progress through GitHub Actions.

Last updated: {stats["last_updated"]}

---

# Statistics

| Difficulty | Count |
|---|---:|
| Easy | {stats["easy"]} |
| Medium | {stats["medium"]} |
| Hard | {stats["hard"]} |
| **Total** | **{stats["total"]}** |

---

## Table of Contents

- [Statistics](#statistics)
- [Project Overview](#project-overview)
  - [What is this?](#what-is-this)
  - [Tech Stack](#tech-stack)
  - [Key Features](#key-features)
  - [Why was this built?](#why-was-this-built)
- [Design Decisions](#design-decisions)
- [Example Output](#example-output)
- [Setup Guide](#setup-guide)
- [Repository Structure](#repository-structure)
- [How It Works](#how-it-works)
- [Implemented Features](#implemented-features)
- [Incoming Features](#incoming-features)
- [Limitations / Known Issues](#limitations--known-issues)
- [License](#license)

---

# Project Overview

## What is this?

CodeAtlas is an automated solution archive designed to synchronize accepted LeetCode submissions into a structured SQL repository.

Instead of manually copying solutions, organizing files, tracking metadata, and maintaining documentation, this project automates the process through GitHub Actions and the LeetCode GraphQL API.

Currently focused on SQL solutions, this project automatically:

- Retrieves accepted LeetCode submissions
- Creates and organizes SQL solution files
- Tracks solution metadata and timestamps
- Maintains separate personal notes and explanations
- Generates repository statistics
- Keeps documentation synchronized with the repository

The long-term goal is to transform a simple solution archive into a continuously improving platform for analyzing, organizing, and exploring programming solutions.

## Tech Stack

- **Language:** Python 3.12
- **API Integration:** LeetCode GraphQL API
- **CI/CD:** GitHub Actions (scheduled + manual workflow dispatch)
- **Data Persistence:** JSON (metadata, notes, statistics)
- **Dependencies:** `requests`
- **Standard Library:** `zoneinfo` (timezone-aware timestamps), `re` (filename normalization), `json`, `os`
- **Version Control Automation:** Git (automated commits via GitHub Actions bot identity)

## Key Features

### Automated Synchronization

- Automatically retrieves accepted LeetCode submissions
- Generates organized solution files
- Runs through GitHub Actions
- No manual copying required

### Documentation System

- Personal notes stored separately
- Notes automatically injected into solutions
- Preserves original submission code

### Repository Management

- Automatic statistics generation
- Metadata tracking
- Solution organization
- README auto-updates

## Why was this built?

Learning software engineering often creates a documentation problem.

Developers build projects, learn new technologies, and solve problems, but the evidence of that growth becomes scattered across repositories, notes, and forgotten experiments.

CodeAtlas was created to solve this problem by automatically capturing progress, organizing solutions, and preserving the reasoning behind the code.

This project started as a 3:00 AM SYDEquest from a Python API-handling tutorial hell on a scuffed idea to automatically save and organize my LeetCode SQL progress without having to maintain files manually.

Over time, it evolved into a larger system focused on separating:

- The original solution code
- Personal learning notes
- Generated metadata
- Future analysis features
    
This allows solutions to remain unchanged while documentation, complexity analysis, tagging, and other features can continue improving after the solution is created.

---

<details>
<summary>Design Decisions</summary>
<a name="design-decisions"></a>

## Why Separate Notes From Solutions?

**Decision:** Solution code and personal documentation are stored in separate layers rather than as comments inside the submission itself.

- `*.sql` files - the submitted solution code and generated metadata (title, difficulty, timestamps, runtime)
- `leetcode_notes.json` - personal hints, explanations, and complexity notes
- `leetcode_meta.json` - generated repository metadata

**Why:** A common approach is writing notes directly into the LeetCode submission before solving. This project deliberately avoids that, so documentation can keep improving after a problem is solved without ever touching the original, already-submitted code - and so future automated analysis (complexity detection, pattern tagging, AI-assisted explanations - see [Incoming Features](#incoming-features)) has a clean layer to build on rather than parsing free-text comments out of code.

**Trade-off:** This adds a synchronization step where notes have to be correctly matched back to their solution file on every run, rather than using the simpler but less durable approach of directly editing the submission comment.

## Repository as the Source of Truth

**Decision:** The repository's own files are treated as ground truth, not the LeetCode API.

**Why:** Statistics are computed by counting existing `.sql` files on disk rather than trusting a running counter or re-querying the API. If LeetCode's API changes or synchronization temporarily breaks, the repository stays accurate and functional on its own.

**Trade-off:** Solution filenames are derived from the problem title, while metadata/notes are keyed by LeetCode's slug. These are expected to match but aren't strictly guaranteed to, a known constraint to keep in mind if problem titles ever contain unusual formatting.

## Credential Security

**Decision:** Authentication is handled entirely through GitHub Actions Secrets, never committed to source control.

**Why:** `LEETCODE_SESSION` and `LEETCODE_USERNAME` are injected as environment variables at runtime. Keeping credentials out of the repository entirely removes an entire class of accidental-exposure risk (no history to scrub, nothing to `.gitignore` correctly, nothing to accidentally push).

## Minimizing Unnecessary Repository Changes

**Decision:** Files are only written when their content actually changes.

**Why:** Generated output is diffed against the existing file before any write. This keeps the commit history meaningful (a commit means something actually changed), avoids triggering unnecessary downstream GitHub Actions runs, and reduces disk I/O on every sync.

</details>

---

<details>
<summary>Example Output</summary>
<a name="example-output"></a>

## Example: Generated Solution File

`leetcode/easy/find-users-with-valid-e-mails.sql`

​```sql
-- Find Users With Valid E-Mails
-- https://leetcode.com/problems/find-users-with-valid-e-mails
-- difficulty: easy
-- first_seen: 2026-08-01 20:11:01 EDT
-- runtime: 744ms

/*
Notes:
Hint: use regexp_like to get case sensitivity for the suffix, or use an extra
like binary. Watch out for the period in the suffix, which is a wildcard, so
put it in square brackets. [TC: O(N), 1 pass]
*/

select *
from Users u
where regexp_like(u.mail, '^[a-zA-Z][a-zA-Z0-9._-]*@leetcode[.]com$', 'c')
```

Every field above is generated automatically by `sync.py`: the header
(title, URL, difficulty, timestamp, runtime) and the code are written by
the sync engine on each run. The `Notes` block is the one exception as it's
independently maintained in `leetcode_notes.json` and re-injected into the
file without touching the surrounding code or header, so documentation can
keep improving without ever risking the submitted solution itself.

</details>

---

<details>
<summary>Setup Guide</summary>
<a name="setup-guide"></a>

## Installation

Clone the repository:

```bash
git clone https://github.com/Cir9no-0001/CodeAtlas
cd CodeAtlas
```

## Requirements

Before running CodeAtlas, make sure you have:

- Python 3.12+
- A LeetCode account with accepted submissions
- A GitHub repository (required for GitHub Actions synchronization)

Install dependencies:

```bash
pip install requests
```

## Authentication Setup

CodeAtlas requires LeetCode authentication to retrieve accepted submissions.

Choose one of the following methods:

1. GitHub Actions (recommended)
2. Running locally

### Option 1: GitHub Actions Setup (recommended)

This project uses GitHub Actions secrets to authenticate with LeetCode.

Navigate to: Repository -> Settings -> Secrets and variables -> Actions -> New repository secret

Add the following secrets:

1. `LEETCODE_USERNAME` (Your LeetCode username)
2. `LEETCODE_SESSION` (Your LeetCode session cookie)

To find LEETCODE_SESSION:

1. Open https://leetcode.com/
2. Log into your LeetCode account.
3. Open Developer Tools:
4. Chrome / Edge: F12 Or Ctrl + Shift + I
5. Navigate to: Application -> Cookies -> https://leetcode.com -> LEETCODE_SESSION
6. Copy the full cookie value.
7. Add it as a GitHub Actions secret: LEETCODE_SESSION = your_cookie_value

Keep this value private. This cookie provides access to your LeetCode session.

After completing authentication setup, run the workflow to synchronize your LeetCode submissions.

1. Navigate to:
   Repository -> Actions -> LeetCode Sync

2. Select:
   Run workflow -> Run workflow

3. Wait for the workflow to complete.

After a successful synchronization, CodeAtlas will:

- Create or update SQL solution files
- Update solution metadata
- Synchronize personal notes
- Refresh repository statistics
- Update README progress tracking

## Running Locally (Optional)

Set environment variables:

Windows PowerShell

```powershell
$env:LEETCODE_USERNAME="your_username"
$env:LEETCODE_SESSION="your_session_cookie"
```

Linux / Mac

```bash
export LEETCODE_USERNAME="your_username"
export LEETCODE_SESSION="your_session_cookie"
```

After setting the variables, run:

```bash
python sync.py
```

## Expected Output

Your repository should contain:

```text
leetcode/
├── easy/
├── medium/
└── hard/
```

along with updated:

- `leetcode_meta.json` (Tracks generated solution first-seen metadata)
- `leetcode_notes.json` (Stores personal notes and explanations)
- `leetcode_stats.json` (Stores repository statistics)

## Troubleshooting Checklist

- Your LeetCode account has accepted submissions.
- Your submissions are available through LeetCode's recent accepted submission history.
- LEETCODE_USERNAME matches your LeetCode username.
- LEETCODE_SESSION has not expired.
- The complete session cookie was copied correctly.
- GitHub Actions does not run
- GitHub Actions is enabled for the repository.
- Repository secrets are configured correctly.
- The workflow file exists in .github/workflows/.

</details>

---

<details>
<summary>Repository Structure</summary>
<a name="repository-structure"></a>

    .
    ├── sync.py
    ├── leetcode_meta.json
    ├── leetcode_notes.json
    ├── leetcode_stats.json
    ├── README.md
    │
    └── leetcode/
        ├── easy/
        │   └── *.sql
        │
        ├── medium/
        │   └── *.sql
        │
        └── hard/
            └── *.sql

</details>

---

<details>
<summary>How It Works</summary>
<a name="how-it-works"></a>

## Architecture

```mermaid
flowchart TD
    A[GitHub Actions] -->|scheduled/manual trigger| B[sync.py]
    B --> C[LeetCode GraphQL API]
    B --> D[Local repository]
    C --> E[Submission processing]
    D --> E
    E --> F[Solution files .sql]
    E --> G[Metadata & notes JSON]
    F --> H[README generation]
    G --> H
```

## Workflow

1. **Automation**
- GitHub Actions runs `sync.py` automatically on a scheduled interval.
- Manual synchronization can also be triggered through GitHub Actions.

2. **Authentication & API Connection**
- The script authenticates with the LeetCode GraphQL API.
- Credentials are securely stored through GitHub Actions secrets:
  - `LEETCODE_USERNAME`
  - `LEETCODE_SESSION`

3. **Submission Retrieval**
- The script queries LeetCode's `recentAcSubmissionList` GraphQL endpoint.
- The endpoint currently provides access to the 15 most recently accepted submissions.
- Retrieved submissions are processed and synchronized automatically.

4. **Metadata Collection**
- Additional GraphQL requests collect:
  - Problem title
  - Difficulty
  - Runtime performance
- Repository tracking timestamps are stored separately in `leetcode_meta.json`.

5. **Solution Generation**
- SQL solution files are automatically created or updated.
- Solutions are organized by difficulty:
    
    leetcode/
        ├── easy/
        ├── medium/
        └── hard/

6. **Metadata & Notes Separation**
- Automated metadata is stored separately from manual notes:
- `leetcode_meta.json` -> generated repository metadata
- `leetcode_notes.json` -> manually maintained explanations and hints
- Prevents API synchronization from overwriting personal documentation.

7. **Notes Synchronization**
- Manual notes are injected into SQL files independently from LeetCode API responses.
- Notes are formatted into SQL block comments.
- Long notes are automatically wrapped for readability.
- Existing SQL solutions are preserved while comments are updated.

8. **Repository Repair & Consistency Checks**
- Existing SQL files are scanned for missing note entries.
- Missing entries are automatically added to `leetcode_notes.json`.
- Recently detected accepted submissions can regenerate missing SQL files when available through the LeetCode API.

9. **Optimization & Reliability**
- LeetCode difficulty requests are cached to reduce unnecessary API calls.
- Problem titles are normalized into safe filenames.
- SQL comments and notes are reformatted consistently during synchronization.

10. **Statistics Generation**
- Solution counts are calculated from existing `.sql` files.
- `leetcode_stats.json` is updated.
- README statistics are automatically regenerated.

</details>

---

<details>
<summary>Implemented Features</summary>
<a name="implemented-features"></a>

## Automation & CI/CD

- [x] GitHub Actions automated synchronization
- [x] Scheduled workflow execution
- [x] Manual workflow triggering
- [x] Secure GitHub Secrets authentication
- [x] Automatic repository updates

## LeetCode Integration

- [x] Fetch accepted submissions through GraphQL API
- [x] Retrieve submitted SQL code
- [x] Retrieve problem difficulty
- [x] Track runtime performance
- [x] Cache repeated difficulty requests
- [x] Handle API failures

## File Management

- [x] Automatically create SQL solution files
- [x] Avoid unnecessary file rewrites when no changes occur
- [x] Organize solutions by difficulty
- [x] Clean problem titles into filenames
- [x] Preserve existing solutions
- [x] Avoid unnecessary file writes
- [x] Repair missing note entries and synchronize existing solutions

## Metadata System

- [x] Track when solutions are first added to the repository
- [x] Maintain `leetcode_meta.json`
- [x] Maintain `leetcode_notes.json`
- [x] Generate `leetcode_stats.json`
- [x] Timezone-aware timestamps

## Notes System

- [x] Separate manual notes from generated files
- [x] Automatically create missing notes
- [x] Inject notes into SQL solutions
- [x] Convert notes into SQL block comments
- [x] Preserve SQL code during updates
- [x] Wrap long notes automatically
- [x] Support comment format migration

</details>

---

<details>
<summary>Incoming Features</summary>
<a name="incoming-features"></a>

## Automated Analysis Features

- [ ] Automatic time complexity analysis
- [ ] Automatic space complexity analysis
- [ ] Generate solution explanations
- [ ] Generate problem summaries
- [ ] Detect inefficient queries
- [ ] Suggest SQL optimizations

## Organization

- [ ] Automatic solution tagging system:
  - JOIN
  - CTE
  - Window Functions
  - Subqueries
  - Aggregations
  - Ranking
  - Date Manipulation
  - etc

- [ ] Search and filter system
- [ ] Detect duplicate solutions
- [ ] Detect renamed files

## Analytics

- [ ] Progress graphs
- [ ] Daily/weekly/monthly solving streaks
- [ ] Difficulty distribution charts
- [ ] Advanced README dashboard

## Platform Expansion

- [ ] Multi-language support
- [ ] Automatically deploy a web interface/extension for browsing solutions through CI/CD
- [ ] Interactive solution explorer

</details>

---

<details>
<summary>Limitations / Known Issues</summary>
<a name="limitations--known-issues"></a>

## API Limitations

- The project currently relies on LeetCode's `recentAcSubmissionList` GraphQL endpoint.
- This endpoint only provides access to the 15 most recently accepted submissions.
- If a solution is missed because it falls outside this limit, the problem may need to be resubmitted on LeetCode to appear in synchronization.

## Current Scope

- Currently optimized for SQL LeetCode solutions.
- Multi-language support is planned but not currently implemented.
- Some metadata depends on information available through the LeetCode API.

## Repository Tracking

- `first_seen` represents the first time a solution was detected and added to this repository.
- It does not necessarily represent the actual date the LeetCode problem was first solved.

## Repair System

The repair system can restore missing or corrupted solution files when the problem is available through the recent accepted submission list.

However:

- Deleted solutions outside the API retrieval window cannot be automatically recovered.
- Manual edits to metadata files may not be recoverable.

</details>

---

## License

This project is source-available but **not open source**. Copyright (c)
2026 Stanley Chen — All Rights Reserved.

You may clone, fork, and run this project locally for personal, non-commercial
evaluation, testing, and code review. Commercial use, redistribution,
hosting as a service, and incorporation into other projects are not
permitted. See [LICENSE](LICENSE) for the full terms.
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("\nSync complete")
