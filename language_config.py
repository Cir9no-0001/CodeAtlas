LANGUAGE_CONFIG = {
    "python": {
        "extension": ".py",
        "comment": {
            "single": "#",
            "multi_start": '"""',
            "multi_end": '"""'
        }
    },

    "python2": {
        "extension": ".py",
        "comment": {
            "single": "#",
            "multi_start": '"""',
            "multi_end": '"""'
        }
    },

    "python3": {
        "extension": ".py",
        "comment": {
            "single": "#",
            "multi_start": '"""',
            "multi_end": '"""'
        }
    },

    "mysql": {
        "extension": ".sql",
        "comment": {
            "single": "--",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "mssql": {
        "extension": ".sql",
        "comment": {
            "single": "--",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "oracle": {
        "extension": ".sql",
        "comment": {
            "single": "--",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "postgresql": {
        "extension": ".sql",
        "comment": {
            "single": "--",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "cpp": {
        "extension": ".cpp",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "c": {
        "extension": ".c",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "java": {
        "extension": ".java",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "csharp": {
        "extension": ".cs",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "javascript": {
        "extension": ".js",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "typescript": {
        "extension": ".ts",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "kotlin": {
        "extension": ".kt",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "swift": {
        "extension": ".swift",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "golang": {
        "extension": ".go",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "rust": {
        "extension": ".rs",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "php": {
        "extension": ".php",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "ruby": {
        "extension": ".rb",
        "comment": {
            "single": "#",
            "multi_start": "=begin",
            "multi_end": "=end"
        }
    },

    "scala": {
        "extension": ".scala",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "dart": {
        "extension": ".dart",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "racket": {
        "extension": ".rkt",
        "comment": {
            "single": ";",
            "multi_start": "#|",
            "multi_end": "|#"
        }
    },

    "erlang": {
        "extension": ".erl",
        "comment": {
            "single": "%",
            "multi_start": None,
            "multi_end": None
        }
    },

    "elixir": {
        "extension": ".ex",
        "comment": {
            "single": "#",
            "multi_start": None,
            "multi_end": None
        }
    },

    "bash": {
        "extension": ".sh",
        "comment": {
            "single": "#",
            "multi_start": None,
            "multi_end": None
        }
    },

    "groovy": {
        "extension": ".groovy",
        "comment": {
            "single": "//",
            "multi_start": "/*",
            "multi_end": "*/"
        }
    },

    "lua": {
        "extension": ".lua",
        "comment": {
            "single": "--",
            "multi_start": "--[[",
            "multi_end": "]]"
        }
    },

    "perl": {
        "extension": ".pl",
        "comment": {
            "single": "#",
            "multi_start": None,
            "multi_end": None
        }
    },

    "clojure": {
        "extension": ".clj",
        "comment": {
            "single": ";",
            "multi_start": None,
            "multi_end": None
        }
    },

    "haskell": {
        "extension": ".hs",
        "comment": {
            "single": "--",
            "multi_start": "{-",
            "multi_end": "-}"
        }
    }
}


SUPPORTED_EXTENSIONS = {
    config["extension"]
    for config in LANGUAGE_CONFIG.values()
}
