#!/usr/bin/env python3
"""Finds the existing Claude session of a portal client (library/clients/portal-sessions.json).

  match_client.py "<name>" "<email>" [--extra "<brand / channel / business name from the order>"]
Prints JSON: {"session": ..., "key": ..., "by": "domain"|"alias", "confidence": "high"|"check"} or {"session": null}.
Any match is only a SUGGESTION: anyone can register with any email or name, so the owner confirms before an order goes
to an existing client's session (security review 2026-10-30; portal_bridge.py route prints the question).
"""
import argparse
import json
import os
import re

FREE_MAIL = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com", "icloud.com", "proton.me",
             "protonmail.com", "aol.com", "yandex.com", "mail.com", "gmx.com", "msn.com", "ymail.com"}
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "library", "clients", "portal-sessions.json")


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def load_clients():
    with open(DATA) as fh:
        return json.load(fh)["clients"]


def match(name, email, extra=""):
    clients = load_clients()
    domain = email.lower().rsplit("@", 1)[-1] if "@" in email else ""
    if domain and domain not in FREE_MAIL:
        for c in clients:
            if any(domain == d or domain.endswith("." + d) for d in c["domains"]):
                return {"session": c["session"], "key": c["key"], "by": "domain", "confidence": "high"}
    hay = " " + norm(" ".join([name, extra, email.split("@")[0]])) + " "
    hay_tight = hay.replace(" ", "")
    for c in clients:
        for a in c["aliases"]:
            a_n = norm(a)
            # Whole-word alias, or the alias written without spaces (e.g. "mraloo").
            if (" " + a_n + " ") in hay or (len(a_n.replace(" ", "")) >= 6 and a_n.replace(" ", "") in hay_tight):
                return {"session": c["session"], "key": c["key"], "by": "alias", "confidence": "check"}
    return {"session": None}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("name")
    p.add_argument("email")
    p.add_argument("--extra", default="")
    a = p.parse_args()
    print(json.dumps(match(a.name, a.email, a.extra)))
