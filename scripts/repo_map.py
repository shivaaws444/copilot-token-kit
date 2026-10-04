#!/usr/bin/env python3
"""
repo_map.py - scan a Spring Boot repo (no AI, zero credits) and write docs/repo-map.md:
endpoints, listeners/schedulers, call flow (controller -> service -> repo/external),
entities, external integrations, config keys, and a Mermaid component graph.

  python3 scripts/repo_map.py                # scan current repo -> docs/repo-map.md
  python3 scripts/repo_map.py --depth 5      # deeper call flow (default 4)
  python3 scripts/repo_map.py --out x.md --include-tests

Static regex-based analysis: fast and good enough for orientation; dynamic/reflective
calls, interface->multiple impls, and lambdas may be missed or simplified.
"""
import argparse, os, re, sys
from collections import defaultdict

SKIP_DIRS = {"target", "build", ".git", "node_modules", ".idea", ".gradle", "out", "generated", "generated-sources"}
MAPPINGS = {"GetMapping": "GET", "PostMapping": "POST", "PutMapping": "PUT", "DeleteMapping": "DELETE", "PatchMapping": "PATCH", "RequestMapping": None}
ENTRY_ANNOS = ["KafkaListener", "SqsListener", "JmsListener", "RabbitListener", "Scheduled", "EventListener", "StreamListener"]
EXTERNAL_TYPES = {
    "WebClient": "HTTP", "RestTemplate": "HTTP", "RestClient": "HTTP", "HttpClient": "HTTP",
    "KafkaTemplate": "Kafka", "SqsTemplate": "SQS", "SqsClient": "SQS", "SqsAsyncClient": "SQS", "AmazonSQS": "SQS",
    "SnsClient": "SNS", "S3Client": "S3", "AmazonS3": "S3", "SecretsManagerClient": "SecretsManager",
    "DynamoDbClient": "DynamoDB", "JdbcTemplate": "JDBC", "NamedParameterJdbcTemplate": "JDBC",
    "JmsTemplate": "JMS", "RabbitTemplate": "RabbitMQ", "RedisTemplate": "Redis", "StringRedisTemplate": "Redis",
}
KEYWORDS = {"if", "for", "while", "switch", "catch", "synchronized", "return", "new", "throw", "else", "try", "do", "super", "this"}

def strip(src):
    """Blank out comments and string/char literals, preserving offsets."""
    out, i, n = list(src), 0, len(src)
    while i < n:
        c = src[i]
        if src.startswith("//", i):
            j = src.find("\n", i); j = n if j < 0 else j
            for k in range(i, j): out[k] = " "
            i = j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2); j = n if j < 0 else j + 2
            for k in range(i, j):
                if out[k] != "\n": out[k] = " "
            i = j
        elif src.startswith('"""', i):
            j = src.find('"""', i + 3); j = n if j < 0 else j + 3
            for k in range(i + 1, j - 1):
                if out[k] != "\n": out[k] = " "
            i = j
        elif c in "\"'":
            j = i + 1
            while j < n and src[j] != c and src[j] != "\n":
                j += 2 if src[j] == "\\" else 1
            for k in range(i + 1, min(j, n)): out[k] = " "
            i = j + 1
        else:
            i += 1
    return "".join(out)

def match_close(s, i, open_c, close_c):
    depth = 0
    while i < len(s):
        if s[i] == open_c: depth += 1
        elif s[i] == close_c:
            depth -= 1
            if depth == 0: return i
        i += 1
    return len(s) - 1

def simple_type(t):
    t = re.sub(r"<.*>", "", t).strip().split(".")[-1]
    return t.replace("[]", "")

def split_params(p):
    parts, depth, cur = [], 0, ""
    for ch in p:
        if ch in "<(": depth += 1
        elif ch in ">)": depth -= 1
        if ch == "," and depth == 0: parts.append(cur); cur = ""
        else: cur += ch
    if cur.strip(): parts.append(cur)
    res = []
    for prm in parts:
        prm = re.sub(r"@\w+(\([^)]*\))?", "", prm).replace("final ", "").strip()
        bits = prm.rsplit(None, 1)
        if len(bits) == 2: res.append((bits[0].strip(), bits[1].strip()))
    return res

def annos(text):
    return re.findall(r"@(\w+)(?:\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\))?", text)

def first_str(args):
    m = re.search(r'(?:value|path)\s*=\s*\{?\s*"([^"]*)"', args or "") or re.search(r'"([^"]*)"', args or "")
    return m.group(1) if m else ""

class Cls:
    def __init__(s, **kw): s.__dict__.update(kw)

def parse_file(path, module):
    src = open(path, encoding="utf-8", errors="ignore").read()
    st = strip(src)
    pkg = (re.search(r"^\s*package\s+([\w.]+)\s*;", st, re.M) or [None, ""])[1] if re.search(r"^\s*package", st, re.M) else ""
    cm = re.search(r"\b(class|interface|record|enum)\s+(\w+)([^{]*)\{", st)
    if not cm: return None
    kind, name, header = cm.group(1), cm.group(2), cm.group(3)
    prev = max(st.rfind(";", 0, cm.start()), 0)
    cls_annos = annos(src[prev:cm.start()])
    body_start = cm.end()
    body_end = match_close(st, cm.end() - 1, "{", "}")
    depth = [0] * len(st); d = 0
    for i, ch in enumerate(st):
        if ch == "{": d += 1
        depth[i] = d
        if ch == "}": d -= 1
    top = depth[body_start - 1]
    fields, methods = {}, []
    # fields
    for fm in re.finditer(r"(?:(?:private|protected|public|static|final|transient|volatile)\s+)*([\w.$]+(?:<[^;{}()=]*>)?(?:\[\])?)\s+(\w+)\s*(?:=[^;]*)?;", st[body_start:body_end]):
        pos = body_start + fm.start()
        if depth[pos] == top and fm.group(1) not in ("return", "throw", "package", "import"):
            fields[fm.group(2)] = simple_type(fm.group(1))
    # methods / constructors
    sig = re.compile(r"(?:(?:public|protected|private|static|final|synchronized|abstract|default|native)\s+)*(?:<[^>]+>\s+)?(?:([\w.$]+(?:<[^;{}()]*?>)?(?:\[\])*)\s+)?(\w+)\s*\(")
    i = body_start
    while True:
        m = sig.search(st, i, body_end)
        if not m: break
        i = m.end()
        if depth[m.start()] != top or m.group(2) in KEYWORDS: continue
        rtype, mname = m.group(1), m.group(2)
        if not rtype and mname != name: continue
        if rtype in KEYWORDS: continue
        close = match_close(st, m.end() - 1, "(", ")")
        rest = st[close + 1: close + 200]
        tm = re.match(r"\s*(throws\s+[\w.,\s]+)?\s*([{;])", rest)
        if not tm: continue
        params = split_params(st[m.end(): close])
        a_start = max(st.rfind(";", body_start, m.start()), st.rfind("}", body_start, m.start()), st.rfind("{", body_start, m.start()), body_start)
        m_annos = annos(src[a_start + 1: m.start()])
        body = ""
        if tm.group(2) == "{":
            b0 = close + 1 + tm.end() - 1
            b1 = match_close(st, b0, "{", "}")
            body = st[b0:b1]
            i = b1
        if mname == name:
            for t, n in params: fields.setdefault(n, simple_type(t))
            continue
        methods.append(Cls(name=mname, params=params, rtype=rtype, annos=m_annos, body=body))
    ext = re.search(r"\bextends\s+([\w.<>, ]+?)(?:\s+implements|\s*$)", header)
    impl = re.search(r"\bimplements\s+([\w.<>, ]+)", header)
    supers = [simple_type(x) for x in re.split(r",(?![^<]*>)", (ext.group(1) if ext else "") + "," + (impl.group(1) if impl else "")) if x.strip()]
    return Cls(name=name, kind=kind, pkg=pkg, module=module, path=path, annos=cls_annos,
               anno_names={a[0] for a in cls_annos}, fields=fields, methods=methods, supers=supers, src=src)

def role(c):
    a = c.anno_names
    if a & {"RestController", "Controller"}: return "controller"
    if "FeignClient" in a: return "feign"
    if "Entity" in a: return "entity"
    if "Repository" in a or any(s.endswith("Repository") for s in c.supers): return "repository"
    if "Service" in a: return "service"
    if a & {"Component", "Configuration"}: return "component"
    if c.name.endswith("Service") or c.name.endswith("ServiceImpl"): return "service"
    return "other"

def find_module(path, root):
    d = os.path.dirname(path)
    while d.startswith(root):
        if os.path.exists(os.path.join(d, "pom.xml")) or os.path.exists(os.path.join(d, "build.gradle")) or os.path.exists(os.path.join(d, "build.gradle.kts")):
            return os.path.relpath(d, root) or "."
        nd = os.path.dirname(d)
        if nd == d: break
        d = nd
    return "."

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="docs/repo-map.md")
    ap.add_argument("--depth", type=int, default=4)
    ap.add_argument("--include-tests", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    classes = {}
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and not d.startswith(".")]
        if not a.include_tests and (os.sep + "test" + os.sep) in (dp + os.sep): continue
        for f in fns:
            if f.endswith(".java"):
                p = os.path.join(dp, f)
                c = parse_file(p, find_module(p, root))
                if c: classes.setdefault(c.name, c)
    # interface -> implementation
    impls = defaultdict(list)
    for c in classes.values():
        for s in c.supers: impls[s].append(c.name)
    def resolve(t):
        if t in classes and classes[t].kind == "interface" and role(classes[t]) != "repository" and "FeignClient" not in classes[t].anno_names and impls.get(t):
            return impls[t][0]
        return t
    def node_label(t):
        if t in EXTERNAL_TYPES: return f"[{EXTERNAL_TYPES[t]}] {t}"
        c = classes.get(t)
        if not c: return None
        r = role(c)
        if r == "feign":
            url = next((first_str(x[1]) or x[1] for x in c.annos if x[0] == "FeignClient"), "")
            return f"[HTTP Feign] {t} {url}".strip()
        if r == "repository":
            ent = re.search(r"<\s*(\w+)", c.src[c.src.find(c.name):c.src.find("{")])
            return f"[DB] {t}" + (f" ({ent.group(1)})" if ent else "")
        return t
    edges = set()
    def calls(cname, m):
        c = classes[cname]; found = []
        for cm in re.finditer(r"\b(?:this\.)?(\w+)\.(\w+)\s*\(", m.body):
            t = c.fields.get(cm.group(1))
            if t:
                t = resolve(t)
                if node_label(t): found.append((cm.start(), t, cm.group(2)))
        own = {x.name for x in c.methods}
        for cm in re.finditer(r"(?<![\w.])(\w+)\s*\(", m.body):  # same-class helpers
            n = cm.group(1)
            if n not in KEYWORDS and n in own and n != m.name: found.append((cm.start(), cname, n))
        out = []
        for _, t, meth in sorted(found):
            if (t, meth) not in out: out.append((t, meth))
        return out
    def tree(cname, mname, d, seen, lines, indent):
        c = classes.get(cname)
        if not c or d > a.depth: return
        for m in [x for x in c.methods if x.name == mname][:1]:
            for t, meth in calls(cname, m):
                if t != cname: edges.add((cname, t))
                lbl = node_label(t) or t
                lines.append(f"{'  ' * indent}- {lbl}.{meth}()" if t != cname else f"{'  ' * indent}- (self) {meth}()")
                key = (t, meth)
                if key in seen or t in EXTERNAL_TYPES: continue
                tc = classes.get(t)
                if tc and role(tc) not in ("repository", "feign"):
                    tree(t, meth, d + 1, seen | {key}, lines, indent + 1)
    # endpoints
    endpoints = []
    for c in classes.values():
        if role(c) != "controller": continue
        base = next((first_str(x[1]) for x in c.annos if x[0] == "RequestMapping"), "")
        for m in c.methods:
            for an, args in m.annos:
                if an in MAPPINGS:
                    verb = MAPPINGS[an] or (re.search(r"RequestMethod\.(\w+)", args or "") or [None, "ANY"])[1]
                    path = ("/" + base.strip("/") + "/" + first_str(args).strip("/")).replace("//", "/").rstrip("/") or "/"
                    req = [simple_type(t) for t, n in m.params]
                    endpoints.append(Cls(verb=verb, path=path, cls=c, m=m, req=req, resp=re.sub(r"[\w]+\.", "", (m.rtype or "").replace(" ", ""))))
    entries = []
    for c in classes.values():
        for m in c.methods:
            for an, args in m.annos:
                if an in ENTRY_ANNOS:
                    entries.append(Cls(kind=an, detail=first_str(args) or (args or "").strip()[:60], cls=c, m=m))
    # output
    L = ["# Repo Map", "",
         "_Generated by `scripts/repo_map.py` - static scan, regenerate after structural changes. "
         "Use this file as the starting point for questions about endpoints and flows; open source files only as needed._", ""]
    mods = sorted({c.module for c in classes.values()})
    L += ["## Modules", ""] + [f"- `{mo}` - " + ", ".join(f"{sum(1 for c in classes.values() if c.module == mo and role(c) == r)} {pl}" for r, pl in (("controller", "controllers"), ("service", "services"), ("repository", "repositories"), ("entity", "entities"))) for mo in mods] + [""]
    L += ["## Endpoints", "", "| Method | Path | Handler | Request | Response | Module |", "|---|---|---|---|---|---|"]
    for e in sorted(endpoints, key=lambda e: (e.path, e.verb)):
        L.append(f"| {e.verb} | `{e.path}` | `{e.cls.name}.{e.m.name}` | {', '.join(e.req) or '-'} | `{e.resp or '-'}` | {e.cls.module} |")
    L.append("")
    if entries:
        L += ["## Other entry points (listeners, schedulers)", "", "| Type | Detail | Handler | Module |", "|---|---|---|---|"]
        L += [f"| @{e.kind} | `{e.detail}` | `{e.cls.name}.{e.m.name}` | {e.cls.module} |" for e in entries] + [""]
    L += ["## Request flows", "", "Call chain per entry point: `[DB]` repository, `[HTTP]` outbound call, `[Kafka]`/`[SQS]` messaging.", ""]
    for e in sorted(endpoints, key=lambda e: (e.path, e.verb)):
        lines = []; tree(e.cls.name, e.m.name, 1, {(e.cls.name, e.m.name)}, lines, 0)
        L += [f"### {e.verb} {e.path}", f"`{e.cls.name}.{e.m.name}` -> returns `{e.resp or 'void'}`"] + (lines or ["- (no tracked calls)"]) + [""]
    for e in entries:
        lines = []; tree(e.cls.name, e.m.name, 1, {(e.cls.name, e.m.name)}, lines, 0)
        L += [f"### @{e.kind} {e.detail}", f"`{e.cls.name}.{e.m.name}`"] + (lines or ["- (no tracked calls)"]) + [""]
    ext = defaultdict(set)
    for c in classes.values():
        for f, t in c.fields.items():
            if t in EXTERNAL_TYPES: ext[f"{EXTERNAL_TYPES[t]} ({t})"].add(c.name)
        if role(c) == "feign":
            ext["HTTP Feign"].add(f"{c.name} -> " + next((first_str(x[1]) or x[1] for x in c.annos if x[0] == "FeignClient"), ""))
    if ext:
        L += ["## External integrations", ""] + [f"- **{k}**: {', '.join(sorted(v))}" for k, v in sorted(ext.items())] + [""]
    ents = [c for c in classes.values() if role(c) == "entity"]
    if ents:
        L += ["## Entities", "", "| Entity | Table | Module |", "|---|---|---|"]
        for c in sorted(ents, key=lambda c: c.name):
            tbl = next((first_str(x[1]) or re.sub(r'.*name\s*=\s*"([^"]+)".*', r"\1", x[1] or "") for x in c.annos if x[0] == "Table"), c.name.lower())
            L.append(f"| {c.name} | {tbl} | {c.module} |")
        L.append("")
    keys = defaultdict(set)
    for c in classes.values():
        for k in re.findall(r'@Value\s*\(\s*"\$\{([^}:]+)', c.src): keys[k].add(c.name)
        for an, args in c.annos:
            if an == "ConfigurationProperties": keys[(first_str(args) or args or "") + ".*"].add(c.name)
    if keys:
        L += ["## Config keys", ""] + [f"- `{k}` - {', '.join(sorted(v))}" for k, v in sorted(keys.items())] + [""]
    if edges:
        L += ["## Component graph", "", "```mermaid", "flowchart LR"]
        def nid(x): return re.sub(r"\W", "_", x)
        for s, t in sorted(edges)[:150]:
            lbl = (node_label(t) or t).replace("[", "").replace("]", ":").replace('"', "'")
            L.append(f'  {nid(s)}["{s}"] --> {nid(t)}["{lbl}"]')
        L += ["```", ""]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    text = "\n".join(L)
    open(a.out, "w", encoding="utf-8").write(text)
    sys.stderr.write(f"[repo_map] {len(classes)} classes, {len(endpoints)} endpoints, {len(entries)} other entry points -> {a.out} (~{len(text)//4} tokens)\n")

if __name__ == "__main__":
    main()
