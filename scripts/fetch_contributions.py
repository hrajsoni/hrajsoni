#!/usr/bin/env python3
"""
fetch_contributions.py
Fetches public GitHub contribution calendar data for a user without requiring a GitHub token,
computes streaks and stats, and saves the output to data/contributions.json.
"""

import sys
import os
import json
import re
from datetime import datetime, date, timezone

try:
    import requests
except ImportError:
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

import urllib.request

USERNAME = os.environ.get("GITHUB_USER", "hrajsoni")
if len(sys.argv) > 1:
    USERNAME = sys.argv[1]

URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    if requests is not None:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.text
    else:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as res:
            return res.read().decode("utf-8")


def parse_contributions(html: str):
    days = []
    
    if BeautifulSoup is not None:
        soup = BeautifulSoup(html, "html.parser")
        
        # Tooltips map: id -> text description (e.g. "5 contributions on September 21st.")
        tt_map = {}
        for tt in soup.find_all("tool-tip"):
            for_id = tt.get("for")
            if for_id:
                tt_map[for_id] = tt.get_text(strip=True)
                
        # Find all day cells
        cells = soup.find_all("td", attrs={"data-date": True})
        for cell in cells:
            dt_str = cell["data-date"]
            level = int(cell.get("data-level", 0))
            cid = cell.get("id", "")
            tt_text = tt_map.get(cid, cell.get_text(strip=True))
            
            # Extract count from tooltip
            m = re.search(r"(\d+)\s+contribution", tt_text)
            count = int(m.group(1)) if m else 0
            
            # Parse weekday: 0=Mon, ..., 6=Sun in Python; or datetime weekday
            dt = datetime.strptime(dt_str, "%Y-%m-%d").date()
            # 0=Sunday in GitHub calendar standard (Sun=0..Sat=6)
            gh_weekday = (dt.weekday() + 1) % 7
            
            days.append({
                "date": dt_str,
                "count": count,
                "level": level,
                "weekday": gh_weekday,
                "description": tt_text or f"{count} contributions on {dt_str}"
            })
    else:
        # Fallback regex parser
        cell_matches = re.findall(
            r'<td[^>]*data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="(\d+)"[^>]*id="([^"]+)"',
            html
        )
        tt_matches = dict(re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]+)</tool-tip>', html))
        for dt_str, lvl, cid in cell_matches:
            level = int(lvl)
            tt_text = tt_matches.get(cid, "")
            m = re.search(r"(\d+)\s+contribution", tt_text)
            count = int(m.group(1)) if m else 0
            dt = datetime.strptime(dt_str, "%Y-%m-%d").date()
            gh_weekday = (dt.weekday() + 1) % 7
            days.append({
                "date": dt_str,
                "count": count,
                "level": level,
                "weekday": gh_weekday,
                "description": tt_text or f"{count} contributions on {dt_str}"
            })

    days.sort(key=lambda d: d["date"])
    
    # Calculate statistics
    total_contributions = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    
    # Longest streak & Current streak
    longest_streak = 0
    temp_streak = 0
    for d in days:
        if d["count"] > 0:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 0
            
    # Current streak calculation (backwards from most recent day)
    current_streak = 0
    today_str = date.today().isoformat()
    # If today has 0 contributions so far, check if yesterday was part of a streak
    check_days = list(reversed(days))
    if check_days and check_days[0]["count"] == 0 and len(check_days) > 1:
        # Check if the last day is today
        if check_days[0]["date"] == today_str:
            check_days = check_days[1:]

    for d in check_days:
        if d["count"] > 0:
            current_streak += 1
        else:
            break
            
    # Best day
    best_day = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}
    
    # Group into weeks (53 weeks)
    weeks = []
    current_week = []
    
    # Align starting weekday: pad first week if needed
    if days:
        first_weekday = days[0]["weekday"] # 0 = Sunday
        for _ in range(first_weekday):
            current_week.append(None)
            
    for d in days:
        current_week.append(d)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        while len(current_week) < 7:
            current_week.append(None)
        weeks.append(current_week)
        
    # Month headers with column indices
    month_labels = []
    seen_months = set()
    for col_idx, week in enumerate(weeks):
        for day in week:
            if day:
                dt = datetime.strptime(day["date"], "%Y-%m-%d")
                m_key = dt.strftime("%Y-%m")
                m_name = dt.strftime("%b")
                if m_key not in seen_months:
                    seen_months.add(m_key)
                    month_labels.append({
                        "name": m_name,
                        "col": col_idx
                    })
                break

    return {
        "username": USERNAME,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": total_contributions,
        "active_days": active_days,
        "longest_streak": longest_streak,
        "current_streak": current_streak,
        "best_day": {
            "date": best_day["date"],
            "count": best_day["count"]
        },
        "weeks": weeks,
        "month_labels": month_labels,
        "days": days
    }


def main():
    print(f"Fetching contribution data for {USERNAME} from {URL}...")
    html = fetch_html(URL)
    data = parse_contributions(html)
    
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "contributions.json")
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully saved {len(data['days'])} days to {out_path}!")
    print(f"Stats: Total={data['total_contributions']}, Longest Streak={data['longest_streak']}d, Current Streak={data['current_streak']}d")


if __name__ == "__main__":
    main()
