#!/usr/bin/env python3
"""A small mutation check for the rules that matter most (money, access, verification, contact safety).

It changes one comparison, boolean or constant at a time in a file, runs the tests that should notice, and lists every
change the tests did NOT notice ("survivors"). A survivor means a rule has no test that would fail if it broke.

    python3 scripts/mutation_check.py backend/ledger/services.py backend/ledger --max 40 --seed 1

The file is restored after every run, also when interrupted. Run it on a clean working tree."""

import argparse
import random
import re
import subprocess
import sys
from pathlib import Path

SWAPS = [
    (r"==", "!="),
    (r"!=", "=="),
    (r"(?<![<>=!])>=(?!=)", ">"),
    (r"(?<![<>=!-])>(?![>=])", ">="),
    (r"<=", "<"),
    (r"(?<![<>=!-])<(?![<=])", "<="),
    (r"\band\b", "or"),
    (r"\bor\b", "and"),
    (r"\bnot\b ", ""),
    (r"\bTrue\b", "False"),
    (r"\bFalse\b", "True"),
    (r"\+ 1\b", "+ 2"),
    (r"- 1\b", "- 0"),
]
SKIP = re.compile(r"^\s*(#|\"\"\"|'''|import |from |raise |assert |@|class |def .*:\s*$|logger|audit\()")


STRING = re.compile(r"\"(?:[^\"\\\\]|\\\\.)*\"|'(?:[^'\\\\]|\\\\.)*'")


def code_only(line):
    """The line with string contents and trailing comments blanked out (same length), so only real code is mutated."""
    masked = STRING.sub(lambda m: m.group(0)[0] + " " * (len(m.group(0)) - 2) + m.group(0)[-1], line)
    cut = masked.find("#")
    return masked if cut < 0 else masked[:cut] + " " * (len(masked) - cut)


def candidates(lines):
    in_doc = False
    for n, line in enumerate(lines):
        if line.count('"""') % 2 == 1:
            in_doc = not in_doc
            continue
        if in_doc or SKIP.match(line):
            continue
        masked = code_only(line)
        for pat, rep in SWAPS:
            for m in re.finditer(pat, masked):
                yield n, m.start(), m.end(), rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("tests", nargs="+")
    ap.add_argument("--max", type=int, default=30)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    path = Path(a.file)
    original = path.read_text()
    lines = original.splitlines(keepends=True)
    cands = list(candidates(lines))
    random.Random(a.seed).shuffle(cands)
    cands = cands[: a.max]
    survivors, killed = [], 0
    try:
        for n, s, e, rep in cands:
            mutated = lines[:]
            mutated[n] = lines[n][:s] + rep + lines[n][e:]
            path.write_text("".join(mutated))
            r = subprocess.run(
                ["pytest", "-q", "-x", "-p", "no:randomly", "-p", "no:cacheprovider", "--timeout", "120", *a.tests],
                capture_output=True,
                text=True,
            )
            if r.returncode == 0:
                survivors.append((n + 1, lines[n].strip(), mutated[n].strip()))
                print(f"SURVIVED line {n + 1}: {lines[n].strip()}  ->  {mutated[n].strip()}", flush=True)
            else:
                killed += 1
    finally:
        path.write_text(original)
    print(f"{a.file}: {killed} killed, {len(survivors)} survived, of {len(cands)} tried")
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
