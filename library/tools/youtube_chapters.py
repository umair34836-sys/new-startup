#!/usr/bin/env python3
"""YouTube chapter list validator: first chapter 00:00, >=3 chapters, ascending, each >=10 s (rules from YouTube Help, see skills2/15 #4154)."""
import sys
# usage: chapters.py "0:Intro" "42:Rules" "95:Heart steal" ... -> YouTube description block
rows=[(float(a.split(':',1)[0]),a.split(':',1)[1]) for a in sys.argv[1:]]
assert rows[0][0]==0, "first chapter must start at 00:00"
assert len(rows)>=3, "need at least three timestamps"
for (t1,_),(t2,_) in zip(rows,rows[1:]):
    assert t2>t1 and t2-t1>=10, f"chapter at {t1}s shorter than 10 s"
for t,n in rows: print(f"{int(t//60):02d}:{int(t%60):02d} {n}")
