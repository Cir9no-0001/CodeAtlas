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

readme = f"""# LeetCode Tracker [Pre-Alpha Testing Open]

![Version](https://img.shields.io/badge/version-v0.3.0--alpha-orange)
![Python](https://img.shields.io/badge/python-3.12-blue)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-black)

> An automated LeetCode SQL solution archive powered by GitHub Actions, LeetCode GraphQL API synchronization, and structured metadata management.

Last updated: {stats["last_updated"]}

---

# Progress Statistics

| Difficulty | Count |
|---|---:|
| Easy | {stats["easy"]} |
| Medium | {stats["medium"]} |
| Hard | {stats["hard"]} |
| **Total** | **{stats["total"]}** |

---

<details>
<summary>Repository Structure</summary>

<br>
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

<br>
This repository automatically synchronizes accepted LeetCode submissions into organized SQL solution files.

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
        - `leetcode_meta.json` → generated repository metadata
        - `leetcode_notes.json` → manually maintained explanations and hints
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
<summary>Design Decisions</summary>

<br>
## Why Separate Notes From Solutions?

A common approach is to write comments directly into a LeetCode submission before submitting. This project intentionally takes a different approach.

Solutions and documentation are separated into different layers:

- `SQL file` → Stores the actual submitted solution and generated metadata.
- `leetcode_notes.json` → Stores personal explanations, hints, complexity analysis, and future annotations.

This design allows documentation to improve over time without changing the original solution. It also makes future features possible, such as:

- Automatic time and space complexity analysis
- SQL pattern detection (JOIN, CTE, Window Functions, etc.)
- Solution tagging
- AI-assisted explanations
- Web-based solution browsing

The goal is not just to archive solved problems, but to build a system that can continue improving and analyzing solutions after they are created.

</details>

---

<details>
<summary>Implemented Features</summary>

<br>
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

<br>
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
<summary>Author Notes</summary>

<br>
- The hints are the notes btw :>
- Repo is based on my alt: leetcode.com/u/C1rn0_Fum0/
- Repo meant for SQL LeetCode questions until language recognition is implemented; did two sum by accident, pls ignore for now!
- Lmk if my questions solved counter ever breaks!

</details>
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("\nSync complete")
