#!/usr/bin/env python3
"""Hands newsletter/latest.html to Kit as a broadcast.
Needs the KIT_API_KEY environment variable (a GitHub Actions secret; never stored in the repo).
MODE=draft (default) saves a draft in Kit. MODE=send schedules it to go out 15 minutes from now.
Skips quietly if this week's issue was already handed to Kit (newsletter/sent.json)."""
import json, os, sys, urllib.request, urllib.error, datetime
here = os.path.dirname(os.path.abspath(__file__))
site = os.path.dirname(here) if os.path.basename(here) == '_build' else here
nl = os.path.join(site, 'newsletter')
meta = json.load(open(os.path.join(nl, 'latest.json')))
html = open(os.path.join(nl, 'latest.html'), encoding='utf-8').read()
mode = (os.environ.get('MODE') or 'draft').strip().lower()
key = os.environ.get('KIT_API_KEY', '').strip()
sent_path = os.path.join(nl, 'sent.json')
sent = json.load(open(sent_path)) if os.path.exists(sent_path) else {}
if mode == 'send' and sent.get(meta['end']) == 'send':
    print('already sent for week ending', meta['end']); sys.exit(0)
if not key:
    print('KIT_API_KEY is not set; nothing sent.'); sys.exit(0 if mode == 'draft' else 1)
now = datetime.datetime.now(datetime.timezone.utc)
body = {'content': html, 'subject': meta['subject'], 'preview_text': meta['preview'],
        'description': 'The week in Lehigh County, ' + meta['start'] + ' to ' + meta['end'],
        'public': False, 'published_at': now.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'send_at': (now + datetime.timedelta(minutes=15)).strftime('%Y-%m-%dT%H:%M:%SZ') if mode == 'send' else None}
if os.environ.get('DRY_RUN'):
    print('DRY RUN', mode, json.dumps({k: (v if k != 'content' else f'<{len(v)} chars>') for k, v in body.items()})); sys.exit(0)
req = urllib.request.Request('https://api.kit.com/v4/broadcasts', data=json.dumps(body).encode(), method='POST',
                             headers={'X-Kit-Api-Key': key, 'Content-Type': 'application/json', 'Accept': 'application/json'})
try:
    res = json.load(urllib.request.urlopen(req, timeout=60))
except urllib.error.HTTPError as e:
    print('Kit refused the broadcast:', e.code, e.read().decode('utf-8', 'replace')[:600]); sys.exit(1)
b = res.get('broadcast', {})
print('Kit broadcast created: id', b.get('id'), '| status', b.get('status'), '| send_at', b.get('send_at'))
sent[meta['end']] = mode
json.dump(sent, open(sent_path, 'w'), indent=1)
