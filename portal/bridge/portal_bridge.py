#!/usr/bin/env python3
"""Bridge CLI between the client portal and Claude sessions (Python standard library only).

Env: PORTAL_URL (default https://editor.firecraft.fun), PORTAL_BRIDGE_TOKEN (secret, never commit it).
The token can also be a "Bearer" network secret for editor.firecraft.fun in the Claude environment settings: then
the environment adds the Authorization header itself and PORTAL_BRIDGE_TOKEN stays unset here.

  portal_bridge.py ping
  portal_bridge.py events                      # NEW work not yet taken: new orders, change requests, messages, approvals
  portal_bridge.py events --all                # also events already taken (forwarded) but not done yet
  portal_bridge.py take <event_id>             # mark taken (order shows "In editing" to the client)
  portal_bridge.py done <event_id>
  portal_bridge.py order <order_id>
  portal_bridge.py download <order_id> <dir>   # all input files of the order (resumes partial files)
  portal_bridge.py deliver <order_id> <file> [--note TEXT]   # chunked upload + new version for the client
  portal_bridge.py message <order_id> <text>   # message from the studio to the client
  portal_bridge.py link <client_id> <session_id>
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("PORTAL_URL", "https://editor.firecraft.fun").rstrip("/")
TOKEN = os.environ.get("PORTAL_BRIDGE_TOKEN", "")


def call(method, path, data=None, raw=None, headers=None, stream_to=None):
    url = f"{BASE}/api/bridge{path}"
    h = {"User-Agent": "portal-bridge/1"}
    if TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    body = None
    if raw is not None:
        body, h["Content-Type"] = raw, "application/octet-stream"
    elif data is not None:
        body, h["Content-Type"] = json.dumps(data).encode(), "application/json"
    h.update(headers or {})
    req = urllib.request.Request(url, data=body, method=method, headers=h)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                if stream_to:
                    while True:
                        buf = r.read(1 << 20)
                        if not buf:
                            return {"status": r.status}
                        stream_to.write(buf)
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            text = e.read().decode(errors="replace")
            if e.code in (429, 502, 503, 504) and attempt < 5:  # host has a 20-connection limit: back off
                time.sleep(2 ** attempt * 2)
                continue
            try:
                return {"error": json.loads(text).get("error", text), "http": e.code, **json.loads(text)}
            except ValueError:
                return {"error": text[:300], "http": e.code}
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < 5:
                time.sleep(2 ** attempt * 2)
                continue
            return {"error": str(e)}
    return {"error": "gave up"}


def out(x):
    print(json.dumps(x, indent=2, ensure_ascii=False))
    if isinstance(x, dict) and x.get("error"):
        sys.exit(1)


def download(order_id, folder):
    o = call("GET", f"/orders/{order_id}")
    if o.get("error"):
        out(o)
    os.makedirs(folder, exist_ok=True)
    saved = []
    for f in o["order"]["files"]:
        if f["kind"] != "input":
            continue
        dest = os.path.join(folder, f"{f['id']}_{os.path.basename(f['name'])}")
        have = os.path.getsize(dest) if os.path.exists(dest) else 0
        if have < f["size"]:
            with open(dest, "ab") as fh:
                r = call("GET", f"/files/{f['id']}", headers={"Range": f"bytes={have}-"} if have else None, stream_to=fh)
            if r.get("error"):
                out(r)
        saved.append({"id": f["id"], "path": dest, "size": os.path.getsize(dest)})
    out({"order": order_id, "files": saved})


def deliver(order_id, path, note):
    size = os.path.getsize(path)
    init = call("POST", "/upload/init", {"order_id": int(order_id), "name": os.path.basename(path), "size": size})
    if init.get("error"):
        out(init)
    token, chunk, offset = init["token"], init["chunk"], 0
    with open(path, "rb") as fh:
        while offset < size:
            fh.seek(offset)
            r = call("POST", f"/upload/chunk?token={token}&offset={offset}", raw=fh.read(chunk))
            if r.get("error") == "offset_mismatch":
                offset = r["received"]
                continue
            if r.get("error"):
                out(r)
            offset = r["received"]
            print(f"\r{offset * 100 // size}%", end="", file=sys.stderr)
    print(file=sys.stderr)
    fin = call("POST", f"/upload/finish?token={token}", {})
    if fin.get("error"):
        out(fin)
    out(call("POST", f"/orders/{order_id}/deliver", {"file_id": fin["file_id"], "note": note}))


def main():
    if not BASE:
        sys.exit("Set PORTAL_URL.")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd")
    p.add_argument("args", nargs="*")
    p.add_argument("--note", default="")
    p.add_argument("--all", action="store_true")
    a = p.parse_args()
    c, x = a.cmd, a.args
    if c == "ping":
        out(call("GET", "/ping"))
    elif c == "events":
        r = call("GET", "/events")
        if not a.all and isinstance(r.get("events"), list):
            r["events"] = [e for e in r["events"] if not e["event"].get("taken_at")]
        out(r)
    elif c in ("take", "done"):
        out(call("POST", f"/events/{int(x[0])}/{c}", {}))
    elif c == "order":
        out(call("GET", f"/orders/{int(x[0])}"))
    elif c == "download":
        download(int(x[0]), x[1])
    elif c == "deliver":
        deliver(int(x[0]), x[1], a.note)
    elif c == "message":
        out(call("POST", f"/orders/{int(x[0])}/message", {"body": " ".join(x[1:])}))
    elif c == "link":
        out(call("POST", f"/clients/{int(x[0])}/session", {"session": x[1]}))
    else:
        p.error(f"unknown command {c}")


if __name__ == "__main__":
    main()
