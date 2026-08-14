# Changelog

All notable changes to CodeAtlas are documented in this file.

The changelog records changes beginning with version `0.1.0`. Changes made before
formal version tracking was introduced are not retroactively assigned versions.

---

## [0.2.0] — 2026-08-14

### Added

- Added multi-language solution synchronization.
- Added `language_config.py` to centralize supported LeetCode languages, file extensions, and comment syntax.
- Added support for storing solutions for the same LeetCode problem as separate files when they are submitted in different programming languages.
- Added language-aware submission retrieval so CodeAtlas selects the submission matching the language reported by `recentAcSubmissionList`.
- Added language-aware notes tracking, allowing each language-specific solution to maintain its own notes entry.
- Added support for language-specific comment formatting when generating headers and notes.
- Added automatic file-extension repair for language-specific solution files.

### Changed

- Changed solution identity from the LeetCode problem slug alone to `slug + file extension`.
- Changed metadata keys from problem slugs to language-specific solution filenames.
- Changed notes keys from problem slugs to language-specific solution filenames.
- Changed submission history retrieval to search multiple recent submissions and select the matching language instead of always using the most recent submission for a problem.
- Moved language extensions and comment syntax out of `sync.py` into `language_config.py`, reducing duplicated language-specific logic.
- Changed file-extension repair to detect ambiguous mismatches and skip automatic repairs when the intended mapping cannot be determined safely.
- Changed notes synchronization to locate solutions using their complete language-specific filename rather than only the problem slug.

### Fixed

- Fixed an issue where solving the same LeetCode problem in multiple languages could cause one solution to overwrite or conflict with another.
- Fixed submission retrieval incorrectly selecting a submission in a different language from the accepted submission being synchronized.
- Fixed notes and metadata collisions between solutions for the same problem written in different languages.

---

## [0.1.0] — 2026-08-12

### Added

- Added formal version tracking using `MAJOR.MINOR.PATCH` version numbers.
- Added `VERSION.md` to record the current CodeAtlas version and define the versioning rules.
- Added `CHANGELOG.md` to record changes made after formal version tracking began.

### Changed

- Established `0.1.0` as the initial tracked version of CodeAtlas.
