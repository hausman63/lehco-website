#!/usr/bin/env python3
"""Builds the weekly LEHCO email ("The Week in Lehigh County") from episodes-data.csv.
Writes newsletter/<monday-date>.html and newsletter/latest.html in the site root, plus newsletter/latest.json (subject + preview text).
Run: python3 _build/build_newsletter.py [YYYY-MM-DD end date, default = newest episode]
Kit adds the mailing address and unsubscribe link below this content when it sends."""
import csv, html, json, os, re, sys, datetime
here = os.path.dirname(os.path.abspath(__file__))
site = os.path.dirname(here) if os.path.basename(here) == '_build' else here
E = html.escape
rows = sorted(csv.DictReader(open(os.path.join(here, 'episodes-data.csv'), encoding='utf-8')), key=lambda r: r['date'])
def vid(u):
    m = re.search(r'(?:v=|shorts/|youtu\.be/)([\w-]{11})', u or ''); return m.group(1) if m else ''
rows = [r for r in rows if vid(r['youtube'])]
end = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.fromisoformat(rows[-1]['date'])
start = end - datetime.timedelta(days=6)
week = [r for r in rows if start.isoformat() <= r['date'] <= end.isoformat()]
if not week: print('no episodes in range'); sys.exit(0)
week.sort(key=lambda r: r['date'], reverse=True)
lead, rest = week[0], week[1:]
def d(s): return datetime.date.fromisoformat(s).strftime('%A, %B %-d')
def link(r): return 'https://www.youtube.com/shorts/' + vid(r['youtube'])
def thumb(r): return 'https://i.ytimg.com/vi/' + vid(r['youtube']) + '/hqdefault.jpg'
NAVY, GOLD, PAPER, INK = '#0b121c', '#e0aa3e', '#f4eedf', '#1b2433'
subject = lead['title'] if len(lead['title']) <= 78 else lead['title'][:75].rsplit(' ', 1)[0] + '...'
preview = f'Plus {len(rest)} more Lehigh County stories from this week, one minute each.'
items = ''.join(f'''<tr><td style="padding:14px 0;border-top:1px solid #d8cfb8">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
<td width="132" valign="top"><a href="{link(r)}"><img src="{thumb(r)}" width="120" alt="" style="display:block;border:0;border-radius:6px;width:120px;height:auto"></a></td>
<td valign="top" style="font-family:Georgia,serif;color:{INK}"><div style="font-family:Arial,sans-serif;font-size:12px;font-weight:bold;color:#8a6410;letter-spacing:.5px">{E(d(r['date']))}</div>
<a href="{link(r)}" style="color:{INK};text-decoration:none;font-size:18px;line-height:1.3;font-weight:bold">{E(r['title'])}</a>
<div style="font-family:Arial,sans-serif;font-size:14px;margin-top:6px"><a href="{link(r)}" style="color:#8a3a1f;font-weight:bold">Watch, 60 seconds</a></div></td>
</tr></table></td></tr>''' for r in rest)
page = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{E(subject)}</title></head>
<body style="margin:0;padding:0;background:{PAPER}">
<div style="display:none;max-height:0;overflow:hidden">{E(preview)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{PAPER}"><tr><td align="center" style="padding:0 12px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px">
<tr><td style="background:{NAVY};padding:26px 28px 22px;border-radius:0 0 0 0">
<div style="font-family:Georgia,serif;font-size:26px;font-weight:bold;letter-spacing:2px;color:#efe6d2">LEHCO</div>
<div style="font-family:Georgia,serif;font-style:italic;font-size:17px;color:{GOLD};margin-top:4px">The week in Lehigh County, {E(start.strftime('%B %-d'))} to {E(end.strftime('%B %-d'))}</div></td></tr>
<tr><td style="background:{NAVY};padding:0"><a href="{link(lead)}"><img src="{thumb(lead)}" width="600" alt="" style="display:block;border:0;width:100%;height:auto"></a></td></tr>
<tr><td style="background:{NAVY};padding:22px 28px 30px">
<div style="font-family:Arial,sans-serif;font-size:12px;font-weight:bold;color:{GOLD};letter-spacing:.5px">{E(d(lead['date']))}</div>
<a href="{link(lead)}" style="font-family:Georgia,serif;font-size:27px;line-height:1.2;font-weight:bold;color:#efe6d2;text-decoration:none">{E(lead['title'])}</a>
<div style="margin-top:18px"><a href="{link(lead)}" style="display:inline-block;background:{GOLD};color:#1a1205;font-family:Arial,sans-serif;font-weight:bold;font-size:15px;text-decoration:none;padding:12px 22px;border-radius:999px">&#9654;&nbsp; Watch the story</a></div></td></tr>
<tr><td style="padding:26px 28px 6px;font-family:Georgia,serif;font-size:22px;font-weight:bold;color:{INK}">Also this week</td></tr>
<tr><td style="padding:0 28px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">{items}</table></td></tr>
<tr><td style="padding:22px 28px 0"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="background:#ebe2cb;border-radius:10px;padding:20px 22px;font-family:Georgia,serif;color:{INK}">
<div style="font-size:19px;font-weight:bold">Got a shoebox of old photos?</div>
<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.5;margin-top:6px">Reply to this email with a story we should tell or a picture of Lehigh County nobody has seen in fifty years. If we make your idea, your name goes on it.</div></td></tr></table></td></tr>
<tr><td style="padding:22px 28px 0;font-family:Arial,sans-serif;font-size:15px;line-height:1.5;color:{INK}">Every episode, searchable by town: <a href="https://lehcobrand.com/episodes.html" style="color:#8a3a1f;font-weight:bold">lehcobrand.com/episodes</a><br>Lehigh County gear, printed to order: <a href="https://lehco.etsy.com" style="color:#8a3a1f;font-weight:bold">lehco.etsy.com</a></td></tr>
<tr><td style="padding:22px 28px 30px;font-family:Arial,sans-serif;font-size:12px;line-height:1.5;color:#6d6652">You are getting this because you signed up at lehcobrand.com. One email a week, on Sunday morning.</td></tr>
</table></td></tr></table></body></html>'''
out = os.path.join(site, 'newsletter'); os.makedirs(out, exist_ok=True)
for name in (end.isoformat() + '.html', 'latest.html'):
    open(os.path.join(out, name), 'w', encoding='utf-8').write(page)
json.dump({'subject': subject, 'preview': preview, 'start': start.isoformat(), 'end': end.isoformat(), 'episodes': len(week)}, open(os.path.join(out, 'latest.json'), 'w'), indent=1)
print('newsletter built:', subject, '|', len(week), 'episodes')
