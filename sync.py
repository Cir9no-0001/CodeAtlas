"""
FIle Name: sync.py
Author: Stanley Chen
Last Upd: CHECK README.template.md


Sections:
    # IMPORTS
    # CONSTANTS / CONFIGURATION
    # ENVIRONMENT + API CONFIGURATION
    # LEETCODE API QUERIES
    # FORMATTER FUNCTIONS
    # FILE / NOTES MANAGEMENT
    # EXECUTION

"""


# IMPORTS

import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

from language_config import LANGUAGE_CONFIG, SUPPORTED_EXTENSIONS


# CONSTANTS / CONFIGURATION

LOCAL_TZ = ZoneInfo("America/Toronto")

META_FILE = "leetcode_meta.json"
NOTES_FILE = "leetcode_notes.json"

username = os.environ.get("LEETCODE_USERNAME")
session = os.environ.get("LEETCODE_SESSION")


if not username or not session:
    raise Exception("Missing LEETCODE_USERNAME or LEETCODE_SESSION")


# ENVIRONMENT + API CONFIGURATION
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


# LEETCODE API QUERIES
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


def get_submission(slug, lang):

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
                    lang
                    statusDisplay
                }
            }
        }
        """,
        "variables": {
            "offset": 0,
            "limit": 20,
            "questionSlug": slug
        }
    })

    try:
        submissions = history["data"]["submissionList"]["submissions"]
    except Exception:
        print("No submission history:", slug)
        return {"code": "", "runtime": None}

    submission_id = None
    for s in submissions:
        if s.get("lang") == lang and s.get("statusDisplay") == "Accepted":
            submission_id = s["id"]
            break

    if submission_id is None:
        print(f"No matching accepted submission found: {slug} ({lang})")
        return {"code": "", "runtime": None}

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

    result = detail.get("data", {}).get("submissionDetails")

    if not result:
        print("No code returned:", slug)
        return {"code": "", "runtime": None}

    return {
        "code": result.get("code", ""),
        "runtime": result.get("runtime")
    }


# FORMATTER FUNCTIONS

def language_to_extension(language):  # Validates and formats file ext
    if language not in LANGUAGE_CONFIG:
        raise ValueError(
            f"Unsupported LeetCode language: {language}"
        )

    return LANGUAGE_CONFIG[language]["extension"]


# Formats header according to file ext
def format_header(title, slug, difficulty, first_seen, runtime, file_extension):
    comment = next(
        (
            config["comment"]
            for config in LANGUAGE_CONFIG.values()
            if config["extension"] == file_extension
        ),
        None
    )

    if not comment:
        raise ValueError(
            f"Unsupported comment syntax for extension: {file_extension}")

    lines = [
        f"{comment['single']} {title}",
        f"{comment['single']} https://leetcode.com/problems/{slug}",
        f"{comment['single']} difficulty: {difficulty}",
        f"{comment['single']} first_seen: {first_seen}"
    ]

    if runtime is not None:
        lines.append(f"{comment['single']} runtime: {runtime}ms")

    return lines


# Formats and wraps notes into multi/single line comments  according to file ext
def format_notes(note_text, file_extension):

    line_limit = 90
    formatted_lines = []

    if note_text:
        for paragraph in note_text.split("\n"):
            words = paragraph.split(" ")
            current_line = ""

            for word in words:
                if len(current_line) + len(word) + 1 <= line_limit:
                    current_line += word + " "

                else:
                    formatted_lines.append(current_line.rstrip())
                    current_line = word + " "

            if current_line:
                formatted_lines.append(current_line.rstrip())

    else:
        formatted_lines.append("")

    comment = next(
        (
            config["comment"]
            for config in LANGUAGE_CONFIG.values()
            if config["extension"] == file_extension
        ),
        None
    )

    if not comment:
        raise ValueError(
            f"Unsupported comment syntax for extension: {file_extension}"
        )

    if comment["multi_start"] and comment["multi_end"]:

        return [
            comment["multi_start"],
            "Notes:",
            *formatted_lines,
            comment["multi_end"]
        ]

    return [
        comment["single"] + " Notes:",
        *[
            comment["single"] + " " + line
            if line
            else comment["single"]
            for line in formatted_lines
        ]
    ]


# Combines formatted comments and main code
def assemble_body(note_text, extension, code):

    notes_str = "\n".join(format_notes(note_text, extension))

    body = notes_str + "\n"

    if code:
        body += "\n" + code.lstrip("\n")

    return body


# FILE / NOTES MANAGEMENT

def repair_file_extensions():

    print("\nChecking file extensions...")

    slug_keys = {}
    key_location = {}

    for key in meta:
        slug = os.path.splitext(key)[0]
        slug_keys.setdefault(slug, []).append(key)

        found = None
        for difficulty in ["easy", "medium", "hard"]:
            candidate = f"leetcode/{difficulty}/{key}"
            if os.path.exists(candidate):
                found = candidate
                break
        key_location[key] = found

    repaired = 0

    for slug, keys in slug_keys.items():

        missing_keys = [k for k in keys if key_location[k] is None]

        if not missing_keys:
            continue

        stray_files = []

        for difficulty in ["easy", "medium", "hard"]:
            folder = f"leetcode/{difficulty}"
            if not os.path.exists(folder):
                continue

            for file in os.listdir(folder):
                stem, ext = os.path.splitext(file)
                if stem != slug or ext not in SUPPORTED_EXTENSIONS:
                    continue
                if file in keys:
                    continue
                stray_files.append(os.path.join(folder, file))

        if len(missing_keys) == 1 and len(stray_files) == 1:

            expected_key = missing_keys[0]
            stray_path = stray_files[0]
            new_path = os.path.join(os.path.dirname(stray_path), expected_key)

            if os.path.exists(new_path):
                print(
                    f"Cannot repair {stray_path}: {new_path} already exists.")
                continue

            os.rename(stray_path, new_path)
            print(f"Renamed: {stray_path} -> {new_path}")
            repaired += 1

        elif missing_keys or stray_files:
            print(
                f"Ambiguous mismatch for '{slug}', skipping automatic repair "
                f"(missing: {missing_keys}, stray: {stray_files})"
            )

    if repaired == 0:
        print("No file extensions needed repair.")
    else:
        print(f"Repaired {repaired} file extension(s).")


def repair_notes_json():

    print("\nChecking missing notes entries...")

    added = 0

    for difficulty in ["easy", "medium", "hard"]:

        folder = f"leetcode/{difficulty}"

        if not os.path.exists(folder):
            continue

        for file in os.listdir(folder):

            if os.path.splitext(file)[1] not in SUPPORTED_EXTENSIONS:
                continue

            key = file

            if key not in notes:
                notes[key] = {"notes": ""}
                print("Added missing notes entry:", key)
                added += 1

    if added == 0:
        print("All solution files already have notes entries.")
    else:
        print(f"Added {added} missing notes entries.")


def find_notes_block(content, comment):

    if not comment["multi_start"] or not comment["multi_end"]:
        return None, None

    notes_marker = (
        comment["multi_start"]
        + "\n"
        + "Notes:"
    )

    notes_start = content.find(notes_marker)

    if notes_start == -1:
        return None, None

    notes_end = content.find(
        comment["multi_end"],
        notes_start + len(notes_marker)
    )

    if notes_end == -1:
        return None, None

    notes_end += len(comment["multi_end"])

    return notes_start, notes_end


def update_notes_in_files():

    print("\nUpdating notes from leetcode_notes.json...")

    for key, data in notes.items():

        note_text = data.get("notes", "")
        extension = os.path.splitext(key)[1]
        comment = next(
            (
                config["comment"]
                for config in LANGUAGE_CONFIG.values()
                if config["extension"] == extension
            ),
            None
        )

        if not comment:
            print(f"Unsupported comment syntax: {extension} ({key})")
            continue

        found_file = None

        for difficulty in ["easy", "medium", "hard"]:
            candidate = f"leetcode/{difficulty}/{key}"
            if os.path.exists(candidate):
                found_file = candidate
                break

        if not found_file:
            print("Solution file not found:", key)
            continue

        with open(found_file, "r", encoding="utf-8") as f:
            content = f.read()

        notes_start, notes_end = find_notes_block(content, comment)

        if notes_start is not None:
            before_notes = content[:notes_start]
            code = content[notes_end:].lstrip("\n")

        else:
            lines = content.split("\n")
            insert_position = 0
            for i, line in enumerate(lines):
                if not line.startswith(comment["single"]):
                    insert_position = i
                    break
            before_notes = "\n".join(lines[:insert_position]) + "\n"
            code = "\n".join(lines[insert_position:])

        new_content = before_notes + assemble_body(note_text, extension, code)

        if new_content != content:
            with open(found_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("Updated notes:", found_file)
        else:
            print("Already correct:", found_file)


# EXECUTION
if os.path.exists(META_FILE):  # Load meta file
    with open(META_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
else:
    meta = {}

if os.path.exists(NOTES_FILE):  # Load notes file
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        notes = json.load(f)
else:
    notes = {}

repair_file_extensions()

response = post({
    "query": """
    query recentSubmissions($username:String!, $limit:Int){
        recentSubmissionList(username:$username, limit:$limit){
            title
            titleSlug
            lang
            statusDisplay
        }
    }
    """,
    "variables": {
        "username": username,
        "limit": 40
    }
})

raw_subs = response.get("data", {}).get("recentSubmissionList", [])

if not raw_subs:
    raise Exception("No submissions returned")

seen = set()
subs = []
for s in raw_subs:
    if s.get("statusDisplay") != "Accepted":
        continue
    dedupe_key = (s["titleSlug"], s["lang"])
    if dedupe_key in seen:
        continue
    seen.add(dedupe_key)
    subs.append(s)

if not subs:
    raise Exception("No accepted submissions returned")

print("\nAccepted submissions:")

for s in subs:
    print("-", s["title"])
    print("  Language:", s.get("lang"))


for submission in subs:

    title = submission["title"]
    slug = submission["titleSlug"]
    lang = submission["lang"]

    difficulty = get_difficulty(slug)

    if difficulty not in ["easy", "medium", "hard"]:
        print("Unknown difficulty:", title)
        continue

    extension = language_to_extension(lang)
    key = f"{slug}{extension}"

    data = get_submission(slug, lang)

    code = data["code"]
    runtime = data["runtime"]

    if not code:
        print("Skipped:", title)
        continue

    if key not in meta:
        meta[key] = {
            "first_seen": now()
        }

    if key not in notes:
        notes[key] = {
            "notes": ""
        }

    folder = f"leetcode/{difficulty}"

    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/{key}"

    content = format_header(
        title,
        slug,
        difficulty,
        meta[key]["first_seen"],
        runtime,
        extension
    )

    header_str = "\n".join(content)
    new_content = header_str + "\n\n" + \
        assemble_body(notes[key]["notes"], extension, code)
    old_content = ""

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            old_content = f.read()

    if new_content != old_content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated:", title)

repair_notes_json()
update_notes_in_files()

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
            if os.path.splitext(file)[1] in SUPPORTED_EXTENSIONS
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

with open("README.template.md", "r", encoding="utf-8") as f:
    readme = f.read()

readme_values = {
    "{{LAST_UPDATED}}": stats["last_updated"],
    "{{EASY}}": str(stats["easy"]),
    "{{MEDIUM}}": str(stats["medium"]),
    "{{HARD}}": str(stats["hard"]),
    "{{TOTAL}}": str(stats["total"])
}

for placeholder, value in readme_values.items():
    readme = readme.replace(placeholder, value)

if "{{" in readme or "}}" in readme:
    raise Exception("README contains unresolved template placeholders")

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)


print("\nSync complete")
