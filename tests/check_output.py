#!/usr/bin/env python3
"""Objective checks on a deepen-prompt reply.

Usage: python3 tests/check_output.py <reply.md> [project_dir]

Scores the parts of the skill's contract that can be checked mechanically, so
a run is judged by something other than the agent that produced it:
  - whole reply <= 500 words, rewritten prompt <= 150 words
  - no persona line in the rewrite
  - "Done when" names a failure ("fails if") and a known-bad input ("seen failing")
  - [bracket] count (unresolved user-supplied facts)
  - every backticked path the reply cites exists under project_dir
Exit status is the number of failed checks.
"""
import glob
import os
import re
import sys


def rewrite_block(text: str) -> str:
    """Blockquote lines following the 'Rewritten prompt' heading."""
    m = re.search(r"Rewritten prompt[^\n]*\n", text, re.I)
    if not m:
        return ""
    lines = []
    for line in text[m.end():].splitlines():
        if line.startswith(">"):
            lines.append(line.lstrip("> ").rstrip())
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
    check("no persona line", not re.search(r"\byou are (a|an|the) ", rw, re.I))
    done = rw[rw.lower().find("done when"):] if "done when" in rw.lower() else rw
    check("done-when names a failure", bool(re.search(r"fails? (if|when|on)|must fail|finds nothing", done, re.I)))
    check("done-when shown failing", bool(re.search(r"(seen|shown|confirm\w*|run\w*|must) [^.]{0,60}fail|fail\w* [^.]{0,40}(first|once|planted|known-bad|parent commit|current|commit|`[0-9a-f]{7,}`)|(checked|caught|catch\w*) on a planted", done, re.I)))
    brackets = re.findall(r"\[[^\]]+\]", rw)
    check("<= 3 [brackets] in rewrite", len(brackets) <= 3, f"{len(brackets)}: {brackets[:4]}")
    if project:
        paths = sorted(set(cited_paths(text)))
        missing = [p for p in paths if not glob.glob(os.path.join(project, p)) and not glob.glob(os.path.expanduser(p))]
        check("cited paths exist", not missing, f"{len(paths)} cited, missing: {missing}")

    failed = 0
    for name, ok, detail in results:
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name:28} {detail}")
    return failed


if __name__ == "__main__":
    sys.exit(main())
