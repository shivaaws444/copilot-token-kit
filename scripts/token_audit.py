#!/usr/bin/env python3
"""Estimate Copilot context cost of this kit (~4 chars/token). Zero credits.
always-on: sent every request. scoped: only when applyTo matches. on-demand: skill bodies/prompts/agents load when used
(skill name+description is always-on)."""
import glob, re, sys
T=lambda s: len(s)//4
def body(p): return open(p, encoding='utf-8').read()
rows=[]; always=0
for p in ['.github/copilot-instructions.md','AGENTS.md']:
    try: t=T(body(p)); rows.append(('always',p,t)); always+=t
    except FileNotFoundError: pass
for p in sorted(glob.glob('.github/skills/*/SKILL.md')):
    s=body(p); d=re.search(r'^description:\s*(.*)$',s,re.M); dt=T(d.group(1)) if d else 0
    always+=dt; rows.append(('on-demand',p,T(s)))
scoped=[(p,T(body(p))) for p in sorted(glob.glob('.github/instructions/*.instructions.md'))]
rows+= [('scoped',p,t) for p,t in scoped]
for p in sorted(glob.glob('.github/prompts/*.prompt.md')+glob.glob('.github/agents/*.agent.md')): rows.append(('on-demand',p,T(body(p))))
if '-v' in sys.argv:
    for k,p,t in rows: print(f'{k:9} {t:6} {p}')
alln=sum(t for _,_,t in rows)
print(f'ALWAYS-ON per request : ~{always} tokens (global rules + skill descriptions)')
print(f'SCOPED (max if all match): ~{sum(t for _,t in scoped)} tokens')
print(f'TOTAL kit if all loaded: ~{alln} tokens  -> on-demand design saves ~{alln-always} tokens/request ({100*(alln-always)//max(alln,1)}%)')
if always>3000: print('WARN: always-on > 3000 tokens; trim copilot-instructions.md or skill descriptions'); sys.exit(1)
