#!/usr/bin/env python3
"""
health.py - zero-credit code health scan for Spring Boot / Java repos.
Feeds /debt-scan and weekly reviews. Prints compact Markdown.

  python3 scripts/health.py            # scan current repo
  python3 scripts/health.py > docs/status/health-$(date +%F).md
"""
import os, re, subprocess, sys
from collections import Counter

SKIP = {"target", "build", ".git", "node_modules", ".idea", ".gradle", "out", "generated", "generated-sources"}
root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

main_files, test_files = [], []
for dp, dns, fns in os.walk(root):
    dns[:] = [d for d in dns if d not in SKIP and not d.startswith(".")]
    for f in fns:
        if f.endswith(".java"):
            p = os.path.join(dp, f)
            (test_files if os.sep + "test" + os.sep in p else main_files).append(p)

def read(p):
    try: return open(p, encoding="utf-8", errors="ignore").read()
    except OSError: return ""
def rel(p): return os.path.relpath(p, root)

checks = {
    "TODO/FIXME/HACK": r"//\s*(TODO|FIXME|HACK)|/\*\s*(TODO|FIXME|HACK)",
    "Field injection (@Autowired field)": r"@Autowired\s+(private|protected|public)?\s*[\w<>, ]+\s+\w+\s*;",
    "System.out / printStackTrace": r"System\.(out|err)\.print|\.printStackTrace\(\)",
    "Empty catch block": r"catch\s*\([^)]*\)\s*\{\s*\}",
    "Broad catch (Exception/Throwable)": r"catch\s*\(\s*(final\s+)?(Exception|Throwable)\s+\w+\s*\)",
    "@Transactional on private method": r"@Transactional[^;{]*\s+private\s",
    "Hard-coded http(s) URL": r"\"https?://[^\"]+\"",
    "Possible hard-coded secret": r"(?i)(password|secret|apikey|api_key|token)\s*=\s*\"[^\"]{4,}\"",
    "new RestTemplate() (check timeouts)": r"new\s+RestTemplate\s*\(",
    "Thread.sleep in main code": r"Thread\.sleep\(",
}
hits = {k: Counter() for k in checks}
sizes = []
for p in main_files:
    s = read(p)
    sizes.append((s.count("\n"), rel(p)))
    for k, rx in checks.items():
        n = len(re.findall(rx, s))
        if n: hits[k][rel(p)] += n

disabled = Counter()
for p in test_files:
    n = len(re.findall(r"@(Disabled|Ignore)\b", read(p)))
    if n: disabled[rel(p)] = n

test_names = {os.path.basename(p)[:-5] for p in test_files}
untested = []
for p in main_files:
    s = read(p); name = os.path.basename(p)[:-5]
    if re.search(r"@(Service|RestController|Controller|Component)\b", s) and "@Configuration" not in s:
        if not any(t.startswith(name) and t[len(name):] in ("Test", "Tests", "IT", "IntegrationTest") for t in test_names):
            untested.append(rel(p))

def pom_value(rx):
    pom = read(os.path.join(root, "pom.xml"))
    m = re.search(rx, pom, re.S)
    return m.group(1).strip() if m else "?"
boot = pom_value(r"<parent>.*?spring-boot-starter-parent</artifactId>\s*<version>([^<]+)")
java = pom_value(r"<java\.version>([^<]+)") if boot else "?"

churn = Counter()
try:
    out = subprocess.run(["git", "-C", root, "log", "--since=90.days", "--name-only", "--pretty=format:"], capture_output=True, text=True, timeout=30).stdout
    for line in out.splitlines():
        if line.endswith(".java") and "/test/" not in line: churn[line] += 1
except Exception:
    pass

L = ["# Code Health", "", f"- Java files: {len(main_files)} main, {len(test_files)} test",
     f"- Spring Boot parent: {boot} | java.version: {java}", ""]
L += ["## Findings", "", "| Check | Count | Top files |", "|---|---|---|"]
for k in checks:
    c = hits[k]
    if c: L.append(f"| {k} | {sum(c.values())} | " + ", ".join(f"`{f}`({n})" for f, n in c.most_common(3)) + " |")
if disabled: L.append(f"| @Disabled/@Ignore tests | {sum(disabled.values())} | " + ", ".join(f"`{f}`({n})" for f, n in disabled.most_common(3)) + " |")
L.append("")
L += ["## Largest classes (lines)", ""] + [f"- {n} `{f}`" for n, f in sorted(sizes, reverse=True)[:8]] + [""]
if untested:
    L += [f"## Services/controllers/components without a matching test ({len(untested)})", ""] + [f"- `{f}`" for f in sorted(untested)[:15]]
    if len(untested) > 15: L.append(f"- ... {len(untested) - 15} more")
    L.append("")
if churn:
    L += ["## Hot spots (most changed in 90 days)", "", "Big + frequently changed + untested = top refactor/test candidates.", ""]
    L += [f"- {n} commits `{f}`" for f, n in churn.most_common(8)] + [""]
print("\n".join(L))
