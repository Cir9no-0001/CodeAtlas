# LeetCode Tracker [Pre-Alpha Testing Open]

![Version](https://img.shields.io/badge/version-v0.3.0--alpha-orange)
![Python](https://img.shields.io/badge/python-3.12-blue)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-black)

> An automated LeetCode SQL solution archive powered by GitHub Actions, LeetCode GraphQL API synchronization, and structured metadata management.

Last updated: 2026-08-02 23:35:18 EDT

---

# Progress Statistics

| Difficulty | Count |
|---|---:|
| Easy | 37 |
| Medium | 26 |
| Hard | 2 |
| **Total** | **65** |

---

<details>
<summary>Repository Structure</summary>

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

- The hints are the notes btw :>
- Repo is based on my alt: leetcode.com/u/C1rn0_Fum0/
- Repo meant for SQL LeetCode questions until language recognition is implemented; did two sum by accident, pls ignore for now!
- Lmk if my questions solved counter ever breaks!

</details>
