#!/usr/bin/env python3
"""Builds 05_taxonomy_schema_designs.md from a template, so that every code block in the note is the code that was run.
Placeholders:  {{CLASS path Name}}  {{FUNC path Name}}  {{DIFF path}}  {{LINES path start end}}  {{INCLUDE file}}
               {{FILE path}} (whole design file)  {{MIGOPS path}} (one line per operation of a migration)
Paths are relative to the design copy of backend/ (argument 1)."""
import ast
import difflib
import re
import sys

DESIGN = sys.argv[1]
ORIG = "/home/user/Alllists.org/backend"
TEMPLATE, OUT = sys.argv[2], sys.argv[3]


def seg(path, name, kind):
    src = open(f"{DESIGN}/{path}").read()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name == name:
            lines = src.splitlines()
            start = (node.decorator_list[0].lineno if node.decorator_list else node.lineno) - 1
            return "\n".join(lines[start : node.end_lineno])
    raise KeyError(name)


def diff(path):
    a = open(f"{ORIG}/{path}").read().splitlines()
    b = open(f"{DESIGN}/{path}").read().splitlines()
    d = list(difflib.unified_diff(a, b, f"a/backend/{path}", f"b/backend/{path}", lineterm="", n=2))
    return "\n".join(d)


def sub(m):
    parts = m.group(1).split()
    kind = parts[0]
    if kind in ("CLASS", "FUNC"):
        return seg(parts[1], parts[2], kind)
    if kind == "DIFF":
        return diff(parts[1])
    if kind == "LINES":
        ls = open(f"{DESIGN}/{parts[1]}").read().splitlines()
        return "\n".join(ls[int(parts[2]) - 1 : int(parts[3])])
    if kind == "FILE":
        return open(f"{DESIGN}/{parts[1]}").read().rstrip("\n")
    if kind == "MIGOPS":
        src = open(f"{DESIGN}/{parts[1]}").read()
        out = []
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "operations":
                for e in node.value.elts:
                    if isinstance(e, ast.Call) and isinstance(e.func, ast.Attribute):
                        names = [k.value.value for k in e.keywords if k.arg in ("model_name", "name") and isinstance(k.value, ast.Constant)]
                        out.append(f"{e.func.attr}({', '.join(names)})" if names else f"{e.func.attr}(...)")
                    else:
                        out.append(ast.get_source_segment(src, e).split("(")[0] + "(...)")
        return "\n".join(out)
    if kind == "INCLUDE":
        return open(parts[1]).read().rstrip("\n")
    raise ValueError(kind)


text = open(TEMPLATE).read()
text = re.sub(r"\{\{(.+?)\}\}", sub, text)
open(OUT, "w").write(text)
print("wrote", OUT, len(text.splitlines()), "lines")
