# LeetCode Tracker

> An automated LeetCode SQL solution archive powered by GitHub Actions, LeetCode GraphQL API synchronization, and structured metadata management.

Last updated: 2026-08-02 22:12:30 EDT

---

# 📊 Progress Statistics

| Difficulty | Count |
|---|---:|
| 🟢 Easy | 37 |
| 🟡 Medium | 26 |
| 🔴 Hard | 2 |
| **Total** | **65** |

---

<details>
<summary>📁 Repository Structure</summary>

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
<summary>⚙️ How It Works</summary>

<br>

This repository automatically synchronizes accepted LeetCode submissions into organized SQL solution files.

## Workflow

1. **Automated Trigger**
   - GitHub Actions runs `sync.py` automatically on a scheduled interval.
   - The workflow can also be manually triggered through GitHub Actions.

2. **Authentication & API Connection**
   - The script authenticates with the LeetCode GraphQL API.
   - Credentials are securely stored through GitHub Actions secrets:
     - `LEETCODE_USERNAME`
     - `LEETCODE_SESSION`

3. **Submission Retrieval**
   - The script queries LeetCode's `recentAcSubmissionList`.
   - Accepted submissions are retrieved automatically.

4. **Metadata Collection**
   - Additional GraphQL requests collect:
     - Problem title
     - Difficulty
     - Runtime performance
     - First solved timestamp

5. **Solution Generation**
   - SQL files are automatically created or updated.
   - Solutions are organized into:
   
        leetcode/
        ├── easy/
        ├── medium/
        └── hard/

6. **Notes Synchronization**
   - Manual notes from `leetcode_notes.json` are injected into SQL files.
   - Notes are converted into SQL block comments.
   - Existing SQL solutions are preserved.

7. **Repository Repair**
   - Existing SQL files are scanned for missing note entries.
   - Missing entries are automatically added to `leetcode_notes.json`.

8. **Statistics Generation**
   - Solution counts are calculated.
   - `leetcode_stats.json` is updated.
   - README statistics are regenerated.

</details>

---

<details>
<summary>✨ Implemented Features</summary>

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
- [x] Organize solutions by difficulty
- [x] Clean problem titles into filenames
- [x] Preserve existing solutions
- [x] Avoid unnecessary file writes
- [x] Detect missing notes entries
- [x] Repair older solutions

## Metadata System

- [x] Store first solved timestamps
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
<summary>🚀 Incoming Features</summary>

<br>

## 🧠 Intelligent Analysis

- [ ] Automatic time complexity analysis
- [ ] Automatic space complexity analysis
- [ ] Generate solution explanations
- [ ] Generate problem summaries
- [ ] Detect inefficient queries
- [ ] Suggest SQL optimizations

## 🗂️ Organization

- [ ] Automatic solution tagging system:
  - JOIN
  - CTE
  - Window Functions
  - Subqueries
  - Aggregations
  - Ranking
  - Date Manipulation

- [ ] Search and filter system
- [ ] Detect duplicate solutions
- [ ] Detect renamed files
- [ ] Categorize solutions automatically

## 📈 Analytics

- [ ] Progress graphs
- [ ] Daily/weekly/monthly solving streaks
- [ ] Difficulty distribution charts
- [ ] Advanced README dashboard

## 🌐 Platform Expansion

- [ ] Multi-language support
- [ ] Automatically deploy a web interface/extension for browsing solutions through CI/CD
- [ ] Interactive solution explorer

</details>

---

<details>
<summary>📝 Author Notes</summary>

<br>

- Repo is based on my LeetCode alternate account: leetcode.com/u/C1rn0_Fum0/
- Notes are manually written hints that improve over time as I learn more SQL.
- Repository currently focuses on SQL LeetCode problems.
- Multi-language support and additional analysis features are planned for future updates.

</details>
