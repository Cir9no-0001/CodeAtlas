# LeetCode Tracker

> An automated LeetCode SQL solution archive powered by GitHub Actions, LeetCode GraphQL API synchronization, and structured metadata management.

Last updated: 2026-08-02 21:55:06 EDT

---

# 📊 Progress Statistics

| Difficulty | Count |
|---|---:|
| Easy | 37 |
| Medium | 26 |
| Hard | 2 |
| **Total** | **65** |

---

# 📁 Repository Structure
.
├── sync.py
├── leetcode_meta.json
├── leetcode_notes.json
├── leetcode_stats.json
├── README.md
│
└── leetcode/
├── easy/
├── medium/
└── hard/

---

# ⚙️ How It Works

This repository automatically synchronizes accepted LeetCode submissions into organized SQL solution files.

## Workflow

1. GitHub Actions runs `sync.py` automatically on a scheduled interval.
2. The script authenticates with the LeetCode GraphQL API.
3. Accepted submissions are retrieved.
4. Solution metadata is collected:
   - Problem title
   - Problem difficulty
   - Runtime performance
   - First solved timestamp
5. SQL solution files are created or updated automatically.
6. Manual notes from `leetcode_notes.json` are injected into each SQL file.
7. Missing notes entries are automatically detected and repaired.
8. Repository statistics and README progress tracking are regenerated.

## Architecture

LeetCode GraphQL API
|
v
sync.py
|
+------+------+
| |
v v
SQL Solutions Metadata
(.sql files) (.json files)

      |
      v

README Dashboard

---

# ✨ Implemented Features

<details>
<summary>Click to expand implemented features</summary>

## Automation & CI/CD

- [x] GitHub Actions automated synchronization
- [x] Scheduled workflow execution
- [x] Automatic repository updates through CI/CD
- [x] Secure credential handling through environment variables

## LeetCode Integration

- [x] Fetch accepted submissions through LeetCode GraphQL API
- [x] Automatically retrieve submitted SQL code
- [x] Automatically retrieve problem difficulty
- [x] Track LeetCode runtime performance
- [x] Cache repeated difficulty requests
- [x] Handle API errors and missing responses

## Solution File Management

- [x] Automatically create SQL solution files
- [x] Organize solutions by difficulty
- [x] Automatically clean problem titles into valid filenames
- [x] Preserve existing SQL solutions while updating metadata
- [x] Avoid unnecessary file writes when no changes occur
- [x] Detect missing solution note entries
- [x] Repair missing metadata connections from existing files

## Metadata Tracking

- [x] Store first solved timestamps
- [x] Maintain separate solution metadata (`leetcode_meta.json`)
- [x] Maintain separate manual notes (`leetcode_notes.json`)
- [x] Generate repository statistics (`leetcode_stats.json`)
- [x] Use timezone-aware timestamps

## Notes System

- [x] Separate generated data from manually written notes
- [x] Automatically create missing notes entries
- [x] Inject notes into SQL solutions
- [x] Convert notes into SQL block comments
- [x] Preserve SQL code while modifying comments
- [x] Automatically wrap long notes for readability
- [x] Update SQL comments when notes change
- [x] Support migration from previous comment formats

</details>

---

# Incoming Features

Potential future improvements:

## Intelligent Analysis

- [ ] Automatic time complexity analysis
- [ ] Automatic space complexity analysis
- [ ] Generate solution explanations
- [ ] Generate problem summaries
- [ ] Detect inefficient solutions
- [ ] Suggest SQL query optimizations

## File Organization

- [ ] Automatic solution tagging system:
  - JOIN
  - CTE
  - Window Functions
  - Subqueries
  - Aggregations
  - Ranking
  - Date Manipulation

- [ ] Search and filter system for solutions
- [ ] Detect duplicate solutions or renamed files
- [ ] Add solution categorization

## Data Analytics

- [ ] Generate progress graphs
- [ ] Track daily/weekly/monthly solving streaks
- [ ] Difficulty distribution charts
- [ ] Advanced README statistics dashboard

## Platform Expansion

- [ ] Support multiple programming languages
- [ ] Automatically create and deploy a web interface/extension for browsing solutions through CI/CD
- [ ] Build an interactive solution explorer

---

# Author Notes

- Repo is based on my LeetCode alternate account: leetcode.com/u/C1rn0_Fum0/
- Notes are manually written hints that improve over time as I learn more SQL.
- Repository currently focuses on SQL LeetCode problems.
- Multi-language support and additional analysis features are planned for future updates.

