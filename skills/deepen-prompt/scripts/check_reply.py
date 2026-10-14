#!/usr/bin/env python3
"""Pre-send checks on a deepen-prompt reply.

Usage: python3 check_reply.py <reply.md> [workspace_root]

Checks the parts of the skill's contract a script can check, so the agent
runs them before sending instead of estimating:
  - whole reply <= 500 words, rewritten prompt <= 150 words
  - the rewrite has all five contract labels and no persona line
  - "Done when" names a failure ("fails if") and is seen failing on an input
    that does that failure, not on the unchanged work ("against itself")
  - <= 3 [brackets] in the rewrite
  - every backticked path exists relative to workspace_root; a path that
    doesn't prints where the file actually is, a bare filename must be unique
Exit status is the number of failed checks. Fix every FAIL, then re-run.
"""
import glob
import os
import re
import sys

LABELS = ["Deliverable", "Start from", "Method", "Done when", "Not in scope"]
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".next",
             "dist", "build", ".claude", "site-packages", ".mypy_cache"}
TRIVIAL_FAIL = re.compile(
    r"against itself|(vs\.?|versus) itself|scored on itself|no[- ]op\b|"
    r"unchanged (code|version|model)|before (any|the) (change|work)|not (done|implemented) yet",
    re.I)


def rewrite_block(text: str) -> str:
    """Blockquote lines following the 'Rewritten prompt' heading."""
    m = re.search(r"Rewritten prompt[^\n]*\n", text, re.I)
    if not m:
        return ""
    lines = []
    for line in text[m.end():].splitlines():
        if line.lstrip().startswith((">", "▎")):
            lines.append(line.lstrip().lstrip(">▎ ").rstrip())
        elif lines and line.strip():
            break
    return "\n".join(lines)


def words(s: str) -> int:
    return len(re.findall(r"\S+", s))


def cited_paths(text: str):
    for tok in re.findall(r"`([^`\n]+)`", text):
        tok = tok.split(":")[0].split("#")[0].strip().replace("…", "*")
        if "/" in tok or re.search(r"\.(py|md|ts|tsx|js|json|toml|ya?ml|csv|sql|html|txt|pdf)$", tok):
            if " " not in tok and not tok.startswith(("http", "--")):
                yield tok


def find_by_suffix(root: str, suffix: str):
    """Repo files whose relative path ends with suffix (dependency dirs skipped)."""
    hits = []
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            rel = os.path.relpath(os.path.join(d, f), root)
            if rel == suffix or rel.endswith("/" + suffix):
                hits.append(rel)
    return hits


def path_problems(root: str, paths):
    problems = []
    for p in paths:
        if glob.glob(os.path.join(root, p)) or glob.glob(os.path.expanduser(p)):
            continue
        if "*" in p or p.startswith(("~", "/")):
            problems.append(f"{p} (not found)")
            continue
        hits = find_by_suffix(root, p)
        if "/" not in p and len(hits) == 1:
            continue  # unique bare filename: unambiguous enough
        if not hits:
            problems.append(f"{p} (not found)")
        elif len(hits) == 1:
            problems.append(f"{p} -> use {hits[0]}")
        else:
            problems.append(f"{p} (ambiguous: {', '.join(hits[:4])})")
    return problems


def main() -> int:
    path = sys.argv[1]
    project = sys.argv[2] if len(sys.argv) > 2 else None
    text = open(path, encoding="utf-8").read().split("---TRACE---")[0]
    rw = rewrite_block(text)
    results = []

    def check(name, ok, detail=""):
        results.append((name, ok, detail))

    check("reply <= 500 words", words(text) <= 500, f"{words(text)} words")
    check("rewrite present", bool(rw))
    check("rewrite <= 150 words", 0 < words(rw) <= 150, f"{words(rw)} words")
    missing_labels = [l for l in LABELS if not re.search(re.escape(l), rw, re.I)]
    check("five contract labels", not missing_labels, f"missing: {missing_labels}" if missing_labels else "")
    check("no persona line", not re.search(r"\byou are (a|an|the) ", rw, re.I))
    i = rw.lower().find("done when")
    done = rw[i:] if i >= 0 else rw
    j = done.lower().find("not in scope")
    done = done[:j] if j > 0 else done
    check("done-when names a failure", bool(re.search(r"fails? (if|when|on)|must fail|finds nothing", done, re.I)))
    check("done-when seen failing", bool(re.search(r"(seen|shown|confirm\w*|run\w*|must) [^.]{0,60}fail|fail\w* [^.]{0,40}(first|once|planted|known-bad|parent commit|current|commit|`[0-9a-f]{7,}`)|(checked|caught|catch\w*) on a planted", done, re.I)))
    trivial = TRIVIAL_FAIL.search(done)
    check("seen failing on a real failure", not trivial,
          f"'{trivial.group(0)}' only shows the work isn't done; use a variant that does the named failure" if trivial else "")
    brackets = re.findall(r"\[[^\]]+\]", rw)
    check("<= 3 [brackets] in rewrite", len(brackets) <= 3, f"{len(brackets)}: {brackets[:4]}")
    if project:
        paths = sorted(set(cited_paths(text)))
        problems = path_problems(project, paths)
        check("cited paths exist", not problems, f"{len(paths)} cited; {'; '.join(problems)}")

    failed = 0
    for name, ok, detail in results:
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name:32} {detail}")
    return failed


if __name__ == "__main__":
    sys.exit(main())
