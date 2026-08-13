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

def language_to_extension(language):

    language_extensions = {
        "python": ".py",
        "python2": ".py",
        "python3": ".py",

        "mysql": ".sql",
        "mssql": ".sql",
        "oracle": ".sql",
        "postgresql": ".sql",

        "cpp": ".cpp",
        "c": ".c",
        "java": ".java",
        "csharp": ".cs",
        "javascript": ".js",
        "typescript": ".ts",
        "kotlin": ".kt",
        "swift": ".swift",
        "golang": ".go",
        "rust": ".rs",
        "php": ".php",
        "ruby": ".rb",
        "scala": ".scala",
        "dart": ".dart",
        "racket": ".rkt",
        "erlang": ".erl",
        "elixir": ".ex",
        "bash": ".sh",
        "groovy": ".groovy",
        "lua": ".lua",
        "perl": ".pl",
        "clojure": ".clj",
        "haskell": ".hs"
    }

    if language not in language_extensions:
        raise ValueError(f"Unsupported LeetCode language: {language}")
    
    return language_extensions[language]


COMMENT_SYNTAX = {
    ".py": {
        "single": "#",
        "multi_start": '"""',
        "multi_end": '"""'
    },

    ".sql": {
        "single": "--",
        "multi_start": "/*",
        "multi_end": "*/"
    },

    ".cpp": {
        "single": "//",
        "multi_start": "/*",
        "multi_end": "*/"
    },

    ".c": {
        "single": "//",
        "multi_start": "/*",
        "multi_end": "*/"
    },

    ".java": {
        "single": "//",
        "multi_start": "/*",
        "multi_end": "*/"
    },

    ".js": {
        "single": "//",
        "multi_start": "/*",
        "multi_end": "*/"
    },

    ".ts": {
        "single": "//",
        "multi_start": "/*",
        "multi_end": "*/"
    },

    ".cs": {
        "single": "//",
        "multi_start": "/*",
        "multi_end": "*/"
    },

    ".go": {
        "single": "//",
        "multi_start": "/*",
        "multi_end": "*/"
    },

    ".rs": {
        "single": "//",
        "multi_start": "/*",
        "multi_end": "*/"
    },

    ".rb": {
        "single": "#",
        "multi_start": "=begin",
        "multi_end": "=end"
    },

    ".sh": {
        "single": "#",
        "multi_start": None,
        "multi_end": None
    },

    ".lua": {
        "single": "--",
        "multi_start": "--[[",
        "multi_end": "]]"
    }
}

def repair_notes_json():

    print("\nChecking missing notes entries...")

    added = 0

    supported_extensions = set(
        COMMENT_SYNTAX.keys()
    )

    for difficulty in ["easy", "medium", "hard"]:

        folder = f"leetcode/{difficulty}"

        if not os.path.exists(folder):
            continue

        for file in os.listdir(folder):

            file_extension = os.path.splitext(file)[1]

            if file_extension not in supported_extensions:
                continue

            slug = os.path.splitext(file)[0]

            if slug not in notes:

                notes[slug] = {
                    "notes": ""
                }

                print("Added missing notes entry:", slug)
                added += 1

    if added == 0:
        print("All solution files already have notes entries.")

    else:
        print(
            f"Added {added} missing notes entries."
        )
    
def format_notes(note_text, file_extension):

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


    comment = COMMENT_SYNTAX.get(file_extension)

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

def format_header(title, slug, difficulty, first_seen, runtime, file_extension):

    comment = COMMENT_SYNTAX.get(file_extension)

    if not comment:
        raise ValueError(
            f"Unsupported comment syntax for extension: {file_extension}"
        )

    lines = [
        f"{comment['single']} {title}",
        f"{comment['single']} https://leetcode.com/problems/{slug}",
        f"{comment['single']} difficulty: {difficulty}",
        f"{comment['single']} first_seen: {first_seen}"
    ]

    if runtime is not None:
        lines.append(
            f"{comment['single']} runtime: {runtime}ms"
        )

    return lines

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
            lang
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
    print("  Language:", s.get("lang"))

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

def validate_file_extensions():

    print("\nChecking file extensions...")

    mismatches = 0

    for slug, data in meta.items():

        expected_extension = data.get("file_extension")

        if not expected_extension:
            print("Missing file extension metadata:", slug)
            continue

        found_file = None

        for difficulty in ["easy", "medium", "hard"]:

            folder = f"leetcode/{difficulty}"

            if not os.path.exists(folder):
                continue

            for file in os.listdir(folder):

                filename_without_extension, extension = os.path.splitext(file)

                if filename_without_extension == slug:
                    found_file = os.path.join(folder, file)
                    actual_extension = extension
                    break

            if found_file:
                break

        if not found_file:
            continue

        if actual_extension != expected_extension:

            print(
                f"Extension mismatch: {found_file} "
                f"(expected {expected_extension}, "
                f"found {actual_extension})"
            )

            mismatches += 1

    if mismatches == 0:
        print("All existing file extensions match metadata.")

    else:
        print(f"Found {mismatches} extension mismatch(es).")

def repair_file_extensions():

    print("\nRepairing file extensions...")

    repaired = 0

    for slug, data in meta.items():

        expected_extension = data.get("file_extension")

        if not expected_extension:
            continue

        found_file = None
        actual_extension = None

        for difficulty in ["easy", "medium", "hard"]:

            folder = f"leetcode/{difficulty}"

            if not os.path.exists(folder):
                continue

            for file in os.listdir(folder):

                filename_without_extension, extension = os.path.splitext(file)

                if filename_without_extension == slug:

                    found_file = os.path.join(folder, file)
                    actual_extension = extension

                    break

            if found_file:
                break

        if not found_file:
            continue

        if actual_extension == expected_extension:
            continue

        new_file = os.path.splitext(found_file)[0] + expected_extension

        if os.path.exists(new_file):
            print(
                f"Cannot repair {found_file}: "
                f"{new_file} already exists."
            )
            continue

        os.rename(found_file, new_file)

        print(
            f"Renamed: {found_file} -> {new_file}"
        )

        repaired += 1

    if repaired == 0:
        print("No file extensions needed repair.")

    else:
        print(f"Repaired {repaired} file extension(s).")


def find_notes_block(content, comment):
    """
    Find the CodeAtlas-generated Notes block.

    Returns:
        (notes_start, notes_end)
        where notes_start is the beginning of the multiline
        comment and notes_end is the end of the multiline
        comment.

        Returns (None, None) if no CodeAtlas Notes block exists.
    """

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

    for slug, data in notes.items():

        note_text = data.get("notes", "")

        if slug not in meta:
            print("No metadata found:", slug)
            continue

        expected_extension = meta[slug].get("file_extension")

        if not expected_extension:
            print("No file extension metadata:", slug)
            continue

        found_file = None

        for difficulty in ["easy", "medium", "hard"]:

            folder = f"leetcode/{difficulty}"

            if not os.path.exists(folder):
                continue

            expected_filename = f"{slug}{expected_extension}"
            path = os.path.join(folder, expected_filename)

            if os.path.exists(path):
                found_file = path
                break

        if not found_file:
            print("Solution file not found:", slug)
            continue

        with open(found_file, "r", encoding="utf-8") as f:
            content = f.read()

        comment = COMMENT_SYNTAX.get(expected_extension)

        if not comment:
            print(
                f"Unsupported comment syntax: "
                f"{expected_extension} ({slug})"
            )
            continue

        notes_start, notes_end = find_notes_block(
            content,
            comment
        )
        
        if notes_start is not None:
        
            before_notes = content[:notes_start]
        
            code = content[notes_end:].lstrip("\n")
        
            if code:
                code = "\n\n" + code
            else:
                code = ""
        
        else:
        
            lines = content.split("\n")
        
            insert_position = 0
        
            for i, line in enumerate(lines):
        
                if not line.startswith(comment["single"]):
                    insert_position = i
                    break
        
            before_notes = (
                "\n".join(lines[:insert_position])
                + "\n"
            )
        
            code = "\n".join(
                lines[insert_position:]
            )

        new_content = before_notes

        for line in format_notes(
            note_text,
            expected_extension
        ):
            new_content += line + "\n"

        new_content += code

        if new_content != content:

            with open(found_file, "w", encoding="utf-8") as f:
                f.write(new_content)

            print("Updated notes:", found_file)

        else:
            print("Already correct:", found_file)

validate_file_extensions()
repair_file_extensions()

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
            "first_seen": now(),
            "file_extension": language_to_extension(
                submission["lang"]
            )
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

    path = f"{folder}/{clean(title)}{meta[slug]['file_extension']}"


    content = format_header(
        title,
        slug,
        difficulty,
        meta[slug]["first_seen"],
        runtime,
        meta[slug]["file_extension"]
    )
    
    content.extend([
        ""
    ])
    
    content.extend(
        format_notes(
            notes[slug]["notes"],
            meta[slug]["file_extension"]
        )
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

repair_notes_json()
update_notes_in_files()

supported_extensions = set(COMMENT_SYNTAX.keys())

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
            if os.path.splitext(file)[1] in supported_extensions
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
