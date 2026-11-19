"""Rewrite the 'Now' block in README.md between the NOW markers.

Reads now.json, computes milestone countdowns, and (when GITHUB_TOKEN is set)
adds the latest public push. Standard library only. Safe to run locally.
"""
import json
import os
import re
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
START, END = "<!--NOW:START-->", "<!--NOW:END-->"


def latest_push(user: str):
    token = os.environ.get("GITHUB_TOKEN")
    req = urllib.request.Request(
        f"https://api.github.com/users/{user}/events/public?per_page=30",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-now"},
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            events = json.load(r)
    except Exception:
        return None
    for e in events:
        repo = e.get("repo", {}).get("name", "").split("/")[-1]
        if e.get("type") == "PushEvent" and repo != user:  # skip this profile repo's own bot commits
            return repo, e["created_at"][:10]
    return None


def render(cfg: dict) -> str:
    today = date.today()
    rows = [
        ("building", cfg["building"]),
        ("shipping", cfg["shipping"]),
        ("next", cfg["next"]),
    ]
    for m in cfg.get("milestones", []):
        days = (date.fromisoformat(m["date"]) - today).days
        rows.append(("countdown", f'{m["label"]} in {days} days' if days > 0 else f'{m["label"]}: live'))
    push = latest_push(cfg["user"])
    if push:
        rows.append(("last push", f"{push[0]} · {push[1]}"))
    rows.append(("refreshed", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")))
    width = max(len(k) for k, _ in rows) + 3
    body = "\n".join(f"{k.ljust(width)}{v}" for k, v in rows)
    return f"{START}\n```console\n$ agent status\n{body}\n```\n{END}"


def main():
    cfg = json.loads((ROOT / "now.json").read_text(encoding="utf-8"))
    text = README.read_text(encoding="utf-8")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), render(cfg), text, flags=re.S)
    README.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    main()
