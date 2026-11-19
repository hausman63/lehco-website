#!/usr/bin/env python3
"""Builds index.html and episodes.html for lehcobrand.com from episodes-data.csv and keeps the story pages in the site look.
Lives in _build/ of the lehco-website repo; writes into the repo root. Run: python3 _build/build_site.py
A GitHub Action runs it every morning after _build/update_from_youtube.py adds the newest episodes."""
import csv, html, json, re, os, sys, datetime
here = os.path.dirname(os.path.abspath(__file__))
site = sys.argv[1] if len(sys.argv) > 1 else (os.path.dirname(here) if os.path.basename(here) == '_build' else here)
repo = site
rows = sorted(csv.DictReader(open(os.path.join(here, 'episodes-data.csv'), encoding='utf-8')), key=lambda r: r['date'], reverse=True)
E = html.escape
YT = 'https://www.youtube.com/channel/UC-eUx-OY9vU2cHm58JQXDQw'
IG = 'https://www.instagram.com/lehco_pa/'
TT = 'https://www.tiktok.com/@lehco_pa'
ETSY = 'https://lehco.etsy.com'
MAIL = 'lehcohistory@gmail.com'
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Alfa+Slab+One&family=League+Gothic&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,700;1,8..60,400&display=swap" rel="stylesheet">'
def ytid(u):
    m = re.search(r'(?:v=|shorts/|youtu\.be/)([\w-]{11})', u or ''); return m.group(1) if m else ''
def nice(d): return datetime.date.fromisoformat(d).strftime('%B %-d, %Y')
def first(r):
    v = ytid(r['youtube']); return f'https://www.youtube.com/shorts/{v}' if v else (r['instagram'] or r['tiktok'])
def plate(r, lead=False):
    v = ytid(r['youtube']); t = E(r['title'])
    on = []
    if v: on.append(f'<a href="https://www.youtube.com/shorts/{v}" target="_blank" rel="noopener">YouTube</a>')
    if r['instagram']: on.append(f'<a href="{E(r["instagram"])}" target="_blank" rel="noopener">Instagram</a>')
    if r['tiktok']: on.append(f'<a href="{E(r["tiktok"])}" target="_blank" rel="noopener">TikTok</a>')
    img = f'<img {"" if lead else "loading=lazy "}src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="">' if v else ''
    body = f'<time datetime="{r["date"]}">{nice(r["date"])}</time><h3>{t}</h3><p class="on">Watch on {", ".join(on)}</p>'
    if lead:
        return f'<article class="plate lead-plate"><a class="pic" href="{E(first(r))}" target="_blank" rel="noopener" aria-label="Watch: {t}">{img}</a><div>{body}</div></article>'
    return f'<article class="plate" data-t="{t.lower()}"><a class="pic" href="{E(first(r))}" target="_blank" rel="noopener" aria-label="Watch: {t}">{img}</a>{body}</article>'
def mast(cur):
    def a(href, label, key): return f'<a href="{href}"{" aria-current=page" if key == cur else ""}>{label}</a>'
    return f'<header class="mast"><div class="wrap"><a class="name" href="/">LEHCO</a><nav aria-label="Main">{a("/episodes.html","Episodes","ep")}{a("/#stories","Stories","st")}{a(ETSY,"Shop","sh")}{a("/#write","Write to us","wr")}</nav></div></header>'
FOOT = f'<footer class="foot"><div class="wrap"><p>LEHCO Brand LLC, Lehigh County, Pennsylvania. &copy; 2026.</p><nav aria-label="Footer"><a href="/episodes.html">Episodes</a><a href="{ETSY}">Shop</a><a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a><a href="/publisher.html">Publisher</a></nav></div></footer>'
def page(title, desc, path, cur, body, extra=''):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="https://lehcobrand.com{path}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://lehcobrand.com{path}">
<meta property="og:image" content="https://lehcobrand.com/lehco_transparent.png">
{FONTS}
<link rel="stylesheet" href="/lehco.css">
{extra}
</head>
<body>
{mast(cur)}
{body}
{FOOT}
</body>
</html>
'''
STORIES = [
 ('mack-trucks.html', 'Mack Trucks', 'Born in Allentown in 1905, Mack put a snarling bulldog on the hood and Lehigh County on the map of American manufacturing.'),
 ('liberty-bell-hidden-allentown.html', "The Liberty Bell's hideout", "In 1777 the Liberty Bell went underground, hidden beneath Zion's Reformed Church in Allentown for nine months."),
 ('a-treat-soda.html', 'A-Treat soda', 'Bottled in Allentown since 1918, A-Treat is the taste of a Lehigh County summer, birch beer included.'),
 ('hess-department-store.html', "Hess's department store", "Allentown's legendary department store basically invented the mall food court, and a parade nobody who saw it ever forgot."),
 ('shankweilers-drive-in.html', "Shankweiler's Drive-In", "Running in Orefield since 1934, Shankweiler's is America's oldest continuously operating drive-in theater."),
 ('dorney-park.html', 'Dorney Park', "Dropping stomachs and building memories since 1884, Dorney Park is Lehigh County's own amusement park institution."),
 ('trexlertown-velodrome.html', 'The Trexlertown velodrome', "The T-Town Velodrome turned a quiet corner of Lehigh County into one of America's most storied cycling tracks."),
 ('lee-iacocca.html', 'Lee Iacocca', "Born and raised in Allentown, Iacocca went on to reinvent Ford's Mustang and save Chrysler from the brink."),
 ('saquon-barkley.html', 'Saquon Barkley', "Before he was breaking NFL tackles, Saquon was Whitehall's own, Lehigh County's homegrown star running back."),
]
SAID = ['You\'re not really from here until you\'ve argued about whether it\'s "Allentown" or "the Valley."',
 'There are two seasons in Lehigh County: Fair season, and "when\'s the Fair again?" season.',
 "A-Treat birch beer isn't a beverage preference. It's a personality trait.",
 'Ask someone from Trexlertown about the Velodrome. Clear your schedule.',
 "If your grandfather didn't work at Mack, did you even grow up here?",
 "We hid the Liberty Bell in a church basement once. We don't bring it up enough."]
latest, recent = rows[0], rows[1:5]
home = f'''<main>
<section class="bill"><div class="wrap"><div class="sheet">
<p class="when">Every morning at eight o'clock</p>
<div class="rule"></div>
<h1><span class="l1">Lehigh County</span><span class="l2">History</span><span class="l3">told in sixty seconds, one town at a time</span></h1>
<img class="cut" src="/lehco_transparent.png" alt="LEHCO mark: the outline of Pennsylvania with a gold star on Lehigh County" width="200" height="200">
<p class="claims"><span>Real photographs</span> <b>&#9733;</b> <span>Named sources</span> <b>&#9733;</b> <span>Corrections pinned</span></p>
<div class="rule short"></div>
<p class="fine">Allentown, Emmaus, Macungie, Slatington, Whitehall and every crossroads between. Made by a family that never left the 610.</p>
<div class="btns"><a class="btn" href="/episodes.html">Watch the episodes</a><a class="btn plain" href="{ETSY}" target="_blank" rel="noopener">Shop the gear</a></div>
</div></div></section>
<section class="sec" id="latest"><div class="wrap">
<h2>This morning's story</h2>
<p class="lead">The newest episode, and the four before it.</p>
<div class="plates">{plate(latest, True)}{''.join(plate(r) for r in recent)}</div>
<div class="btns" style="justify-content:flex-start"><a class="btn" href="/episodes.html">See every episode</a><a class="btn plain" href="{YT}?sub_confirmation=1" target="_blank" rel="noopener">Subscribe on YouTube</a></div>
</div></section>
<section class="sec"><div class="wrap"><div class="letter">
<h2>Why we started</h2>
<p style="margin-top:14px">We started LEHCO because there's a Delco shirt, a Chesco shirt, a Bucks shirt, and nothing for the county that gave the world a bulldog on a hood and a bell in a basement. Lehigh County has stories nobody else gets to tell. We just figured somebody should put them on a hoodie.</p>
<p class="sig">Dave and family, LEHCO</p>
</div></div></section>
<section class="sec" id="stories"><div class="wrap">
<h2>The long stories</h2>
<p class="lead">Every county has landmarks. Ours have plot twists. Nine to start with.</p>
<ul class="index">{''.join(f'<li><a href="/{f}"><strong>{E(t)}</strong><span>{E(d)}</span></a></li>' for f, t, d in STORIES)}</ul>
</div></section>
<section class="sec inked" id="shop"><div class="wrap">
<h2>Wear the county</h2>
<p class="lead">Every design starts with a Lehigh County story. Tees, hoodies, hats, stickers and flags, printed to order, one at a time.</p>
<a class="btn" href="{ETSY}" target="_blank" rel="noopener">Open the Etsy shop</a>
</div></section>
<section class="sec"><div class="wrap">
<h2>Overheard in the 610</h2>
<p class="lead">Things you only understand if you're from here.</p>
<div class="said">{''.join(f'<blockquote>{E(q)}</blockquote>' for q in SAID)}</div>
</div></section>
<section class="sec" id="write"><div class="wrap"><div class="letter">
<h2>Write to us</h2>
<p style="margin-top:14px">Spot a mistake? Know a story we should tell? Have old photos of Lehigh County in a shoebox? Send them. Corrections get pinned, and if we make your idea, you get the credit by name.</p>
<div class="btns" style="justify-content:flex-start"><a class="btn" href="mailto:{MAIL}">Email {MAIL}</a><a class="btn plain" href="{IG}" target="_blank" rel="noopener">Instagram</a><a class="btn plain" href="{TT}" target="_blank" rel="noopener">TikTok</a></div>
</div></div></section>
</main>'''
top = sorted(rows, key=lambda r: int(r['reach'] or 0), reverse=True)[:4]
ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "LEHCO: History of Lehigh County, PA", "itemListElement": [
  {"@type": "ListItem", "position": i + 1, "item": {"@type": "VideoObject", "name": r['title'], "description": r['title'], "uploadDate": r['date'],
   "thumbnailUrl": f"https://i.ytimg.com/vi/{ytid(r['youtube'])}/hqdefault.jpg", "embedUrl": f"https://www.youtube.com/embed/{ytid(r['youtube'])}",
   "url": f"https://www.youtube.com/shorts/{ytid(r['youtube'])}"}} for i, r in enumerate(rows) if ytid(r['youtube'])]}
eps = f'''<main>
<section class="bill" style="padding-bottom:20px"><div class="wrap">
<p class="when">Every morning at eight o'clock</p>
<div class="rule"></div>
<h1><span class="l1" style="font-size:clamp(2.4rem,8vw,5.6rem)">The Episodes</span><span class="l3">Lehigh County history, sixty seconds at a time</span></h1>
<div class="btns"><a class="btn" href="{YT}?sub_confirmation=1" target="_blank" rel="noopener">Subscribe on YouTube</a><a class="btn plain" href="{IG}" target="_blank" rel="noopener">Instagram</a><a class="btn plain" href="{TT}" target="_blank" rel="noopener">TikTok</a></div>
</div></section>
<section class="sec"><div class="wrap">
<h2>Most watched</h2>
<p class="lead">The four stories the county has watched the most.</p>
<div class="plates">{''.join(plate(r) for r in top)}</div>
</div></section>
<section class="sec"><div class="wrap">
<h2>The latest {len(rows)}</h2>
<p class="lead">Newest first. Search for your town, a street, a family name.</p>
<input class="search" id="q" type="search" placeholder="Try Emmaus, Mack, covered bridge" aria-label="Search episodes">
<div class="plates" id="all">{''.join(plate(r) for r in rows)}</div>
<p class="none" id="none">No episode on that yet. Email the idea to <a href="mailto:{MAIL}">{MAIL}</a> and if we make it, you get the credit.</p>
</div></section>
<section class="sec inked"><div class="wrap">
<h2>Got a story or an old photo?</h2>
<p class="lead">Spot a mistake, know a story we should tell, or have old photos of Lehigh County? With your OK we will use them in a video and credit you by name.</p>
<div class="btns" style="justify-content:flex-start"><a class="btn" href="mailto:{MAIL}">Email {MAIL}</a><a class="btn" href="{ETSY}" target="_blank" rel="noopener">Shop the gear</a></div>
</div></section>
</main>
<script>
var q=document.getElementById('q'),eps=[].slice.call(document.querySelectorAll('#all .plate')),none=document.getElementById('none');
q.addEventListener('input',function(){{var s=q.value.trim().toLowerCase(),n=0;eps.forEach(function(e){{var ok=!s||e.getAttribute('data-t').indexOf(s)>-1;e.style.display=ok?'':'none';if(ok)n++;}});none.style.display=n?'none':'block';}});
</script>'''
out = lambda name, text: open(os.path.join(site, name), 'w', encoding='utf-8').write(text)
out('index.html', page('LEHCO: Lehigh County history, told in sixty seconds', 'A new piece of Lehigh County, Pennsylvania history every morning at 8: real photographs, named sources, and the gear to wear it. Allentown, Emmaus, Macungie, Slatington, Whitehall and beyond.', '/', '', home))
out('episodes.html', page('LEHCO episodes: Lehigh County history in sixty seconds', f'{len(rows)} short history videos about Lehigh County, Pennsylvania. Search by town and watch on YouTube, Instagram or TikTok.', '/episodes.html', 'ep', eps, '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'))
# reskin story pages: same content, new inks and types, working links
SKIN = '''<!--lehco-skin-->''' + FONTS + '''<style>
:root{--navy:#12233f;--navy-deep:#16202f;--gold:#c2932a;--gold-bright:#c2932a;--gold-dim:#7b2219;--cream:#e7dfcb;--paper:#d8cdb2;--white:#f3eddd;--ink:#16202f}
body{font-family:'Source Serif 4',Georgia,serif;font-size:1.0625rem;background-color:#e7dfcb}
h1,h2{font-family:'League Gothic',Impact,sans-serif;font-weight:400;letter-spacing:.02em}
.topbar{background:#e7dfcb;border-bottom:3px double #16202f}
.topbar .brand{font-family:'Abril Fatface',Georgia,serif;color:#16202f;font-size:1.7rem;letter-spacing:.04em}.topbar .brand span{color:#16202f}
.topbar a.back{font-family:'League Gothic',Impact,sans-serif;font-size:1.25rem;color:#16202f;opacity:1;font-weight:400}.topbar a.back:hover{color:#7b2219}
.hero-band{background:#12233f;background-image:none}
.hero-band h1{font-family:'Abril Fatface',Georgia,serif;text-transform:none;letter-spacing:0;font-size:clamp(2rem,5.4vw,3.2rem);line-height:1.05}
.hero-image,.t-card{border-radius:0;box-shadow:none;border:2px solid #16202f}
.t-card h3,.t-year,.section-label,.merch-tease strong{font-family:'League Gothic',Impact,sans-serif;font-weight:400;font-size:1.35rem;letter-spacing:.04em}
.section-label{font-size:1.8rem}
.merch-tease{border-radius:0}
footer{background:#e7dfcb;color:#16202f;border-top:3px double #16202f}
</style>'''
for f, _, _ in STORIES:
    p = os.path.join(repo, f)
    if not os.path.exists(p): print('missing', f); continue
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!--lehco-skin-->.*?</style>\n?', '', s, flags=re.S)
    s = s.replace('../lehco-site.html#legends', '/#stories').replace('../lehco-site.html#shop', ETSY).replace('../lehco-site.html#join', '/#write').replace('../lehco-site.html', '/')
    s = s.replace('>Join the List<', '>Write to us<').replace('>History<', '>Stories<')
    s = s.replace('</head>', SKIN + '\n</head>', 1)
    open(os.path.join(site, f), 'w', encoding='utf-8').write(s)
print('built', len(rows), 'episodes')
