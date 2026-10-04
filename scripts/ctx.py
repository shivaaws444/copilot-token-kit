#!/usr/bin/env python3
"""
ctx.py - shrink what you paste into Copilot Chat.

  python3 scripts/ctx.py trace  < failure.txt     # trim Java stack traces / Maven output
  python3 scripts/ctx.py diff   [base]            # compact git diff (default: staged+unstaged vs HEAD)
  python3 scripts/ctx.py file   Path.java Method  # extract one method instead of whole file

Prints an estimated token count to stderr so you can see the savings.
Set CTX_PKG to your base package (default: com.jpmc) to keep only your frames.
"""
import os, re, subprocess, sys

PKG = os.environ.get("CTX_PKG", "com.jpmc")
NOISE = re.compile(r"^\s*at (java\.|javax\.|jdk\.|sun\.|org\.springframework\.|org\.junit\.|"
                   r"org\.mockito\.|org\.apache\.maven\.|net\.bytebuddy\.|com\.sun\.|reactor\.|io\.netty\.)")

def est(s): return max(1, len(s) // 4)

def report(before, after):
    b, a = est(before), est(after)
    sys.stderr.write(f"[ctx] ~{b} -> ~{a} tokens ({100 - 100*a//b}% saved)\n")

def trim_trace(text):
    out, skipped = [], 0
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("at "):
            if PKG in s or not NOISE.match(line):
                if skipped: out.append(f"    ... {skipped} framework frames"); skipped = 0
                out.append(line)
            else:
                skipped += 1
            continue
        if skipped: out.append(f"    ... {skipped} framework frames"); skipped = 0
        if re.match(r"^\[(INFO|DEBUG)\]", s) and not re.search(r"Tests run:.*Fail|BUILD|ERROR", s):
            continue
        if re.match(r"^(Download|Progress|\[INFO\] -+$)", s) or not s:
            continue
        out.append(line)
    if skipped: out.append(f"    ... {skipped} framework frames")
    # collapse duplicate consecutive lines
    dedup = [l for i, l in enumerate(out) if i == 0 or l != out[i-1]]
    return "\n".join(dedup[:150])

def compact_diff(base):
    cmd = ["git", "diff", "-U2", "--no-color", base] if base else ["git", "diff", "-U2", "--no-color", "HEAD"]
    raw = subprocess.run(cmd, capture_output=True, text=True).stdout
    keep, skip = [], False
    for line in raw.splitlines():
        if line.startswith("diff --git"):
            skip = bool(re.search(r"(target/|build/|\.lock|package-lock|generated|\.min\.)", line))
        if skip: continue
        if line.startswith(("index ", "new file mode", "deleted file mode")): continue
        keep.append(line)
    return raw, "\n".join(keep)

def extract_method(path, name):
    src = open(path, encoding="utf-8").read()
    m = re.search(r"(?:@[\w.]+(?:\([^)]*\))?\s*)*(?:public|protected|private|static|\s)+[\w<>\[\],\s?]+\s+"
                  + re.escape(name) + r"\s*\([^)]*\)[^{;]*\{", src)
    if not m: sys.exit(f"method {name} not found in {path}")
    i, depth = m.end(), 1
    while depth and i < len(src):
        depth += {"{": 1, "}": -1}.get(src[i], 0); i += 1
    pkg = re.search(r"^package .*;", src, re.M)
    header = f"// {path}\n" + (pkg.group(0) + "\n" if pkg else "")
    return src, header + src[m.start():i]

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    mode = sys.argv[1]
    if mode == "trace":
        raw = sys.stdin.read(); out = trim_trace(raw)
    elif mode == "diff":
        raw, out = compact_diff(sys.argv[2] if len(sys.argv) > 2 else None)
    elif mode == "file" and len(sys.argv) == 4:
        raw, out = extract_method(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
    print(out); report(raw or " ", out or " ")
