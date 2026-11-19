#!/usr/bin/env python3
"""Adds newly PUBLISHED LEHCO videos to episodes-data.csv from the channel's public feed.
No keys or sign-in. If the feed cannot be read, it changes nothing and exits cleanly."""
import csv, os, re, sys, urllib.request, datetime
import xml.etree.ElementTree as ET
try:
    from zoneinfo import ZoneInfo
    ET_TZ = ZoneInfo('America/New_York')
except Exception:
    ET_TZ = datetime.timezone(datetime.timedelta(hours=-5))
CHANNEL = 'UC-eUx-OY9vU2cHm58JQXDQw'
FEED = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + CHANNEL
here = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(here, 'episodes-data.csv')
FIELDS = ['date', 'title', 'youtube', 'instagram', 'tiktok', 'reach']
def vid(u):
    m = re.search(r'(?:v=|shorts/|youtu\.be/)([\w-]{11})', u or ''); return m.group(1) if m else ''
def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        if src:
            data = open(src, 'rb').read()
        else:
            req = urllib.request.Request(FEED, headers={'User-Agent': 'Mozilla/5.0 (lehcobrand.com episode updater)'})
            data = urllib.request.urlopen(req, timeout=30).read()
        root = ET.fromstring(data)
    except Exception as e:
        print('feed not readable, nothing changed:', e); return
    ns = {'a': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}
    rows = list(csv.DictReader(open(path, encoding='utf-8')))
    have = {vid(r['youtube']) for r in rows}
    added = 0
    for e in root.findall('a:entry', ns):
        v = (e.findtext('yt:videoId', '', ns) or '').strip()
        title = re.sub(r'\s*#\w+', '', (e.findtext('a:title', '', ns) or '')).strip()
        pub = (e.findtext('a:published', '', ns) or '').strip()
        if not re.fullmatch(r'[\w-]{11}', v) or not title or v in have: continue
        try:
            d = datetime.datetime.fromisoformat(pub.replace('Z', '+00:00')).astimezone(ET_TZ).date().isoformat()
        except Exception:
            continue
        rows.append({'date': d, 'title': title, 'youtube': 'https://www.youtube.com/watch?v=' + v, 'instagram': '', 'tiktok': '', 'reach': '0'})
        have.add(v); added += 1
    if added:
        rows.sort(key=lambda r: r['date'])
        w = csv.DictWriter(open(path, 'w', newline='', encoding='utf-8'), fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    print('episodes added:', added, 'total:', len(rows))
main()
