#!/usr/bin/env python3
"""Builds index.html and episodes.html for lehcobrand.com from episodes-data.csv and keeps the story pages in the site look.
Lives in _build/ of the lehco-website repo; writes into the repo root. Run: python3 _build/build_site.py
A GitHub Action runs it every morning after _build/update_from_youtube.py adds the newest episodes."""
import csv, html, json, re, os, sys, datetime
here = os.path.dirname(os.path.abspath(__file__))
site = sys.argv[1] if len(sys.argv) > 1 else (os.path.dirname(here) if os.path.basename(here) == '_build' else here)
rows = sorted(csv.DictReader(open(os.path.join(here, 'episodes-data.csv'), encoding='utf-8')), key=lambda r: r['date'], reverse=True)
E = html.escape
YT = 'https://www.youtube.com/channel/UC-eUx-OY9vU2cHm58JQXDQw'
IG = 'https://www.instagram.com/lehco_pa/'
TT = 'https://www.tiktok.com/@lehco_pa'
ETSY = 'https://lehco.etsy.com'
MAIL = 'lehcohistory@gmail.com'
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&display=swap" rel="stylesheet">'
import hashlib
try:
    CSSV = hashlib.md5(open(os.path.join(site, 'lehco.css'), 'rb').read()).hexdigest()[:8]
except Exception:
    CSSV = '1'
TRI = '<span class="tri" aria-hidden="true"></span>'
def ytid(u):
    m = re.search(r'(?:v=|shorts/|youtu\.be/)([\w-]{11})', u or ''); return m.group(1) if m else ''
rows = [r for r in rows if ytid(r['youtube'])]
def nice(d): return datetime.date.fromisoformat(d).strftime('%B %-d, %Y')
def short(d): return datetime.date.fromisoformat(d).strftime('%b %-d, %Y')
def card(r, big=False):
    v = ytid(r['youtube']); t = E(r['title'])
    return (f'<a class="card{" big" if big else ""}" href="https://www.youtube.com/shorts/{v}" data-yt="{v}" data-t="{t.lower()}" target="_blank" rel="noopener" aria-label="Play: {t}">'
            f'<img {"" if big else "loading=lazy "}src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt="">'
            f'<span class="play">{TRI}</span><span class="meta"><time datetime="{r["date"]}">{short(r["date"])}</time><strong>{t}</strong></span></a>')
def top(cur, solid=False):
    def a(href, label, key): return f'<a href="{href}"{" aria-current=page" if key == cur else ""}>{label}</a>'
    return (f'<header class="top{" solid" if solid else ""}"><div class="wrap"><a class="seal" href="/"><img src="/lehco_transparent.png" alt="" width="48" height="48"><span>LEHCO</span></a>'
            f'<nav aria-label="Main">{a("/episodes.html","Episodes","ep")}{a("/#stories","Stories","st")}{a(ETSY,"Shop","sh")}{a("/#write","Write to us","wr")}</nav></div></header>')
CREDITS = ('Archive images: bird’s-eye view of Macungie, T. M. Fowler &amp; J. B. Moyer, 1893, Library of Congress; '
           'Allentown postcards, 1905 to 1935, public domain via Wikimedia Commons. Film clips from LEHCO episodes.')
FOOT = (f'<footer class="foot"><div class="wrap"><nav aria-label="Footer"><a href="/episodes.html">Episodes</a><a href="{ETSY}">Shop</a><a href="{YT}">YouTube</a><a href="{IG}">Instagram</a><a href="{TT}">TikTok</a>'
        f'<a href="/privacy.html">Privacy</a><a href="/terms.html">Terms</a><a href="/publisher.html">Publisher</a></nav><p>{CREDITS}</p><p>LEHCO Brand LLC, Lehigh County, Pennsylvania. &copy; 2026.</p></div></footer>')
PLAYER = '''<dialog class="player" id="player" aria-label="Episode player"><button class="x" aria-label="Close player">&times;</button><div class="frame"></div></dialog>
<script>
(function(){var d=document.getElementById('player');if(!d||!d.showModal)return;var f=d.querySelector('.frame');
function shut(){f.innerHTML='';if(d.open)d.close();}
document.addEventListener('click',function(e){var a=e.target.closest('[data-yt]');if(!a||e.metaKey||e.ctrlKey)return;e.preventDefault();
f.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+a.getAttribute('data-yt')+'?autoplay=1&rel=0&playsinline=1" title="LEHCO episode" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';d.showModal();});
d.addEventListener('click',function(e){if(e.target===d||e.target.classList.contains('x'))shut();});d.addEventListener('close',function(){f.innerHTML='';});
var v=document.querySelector('.hero video');if(v&&matchMedia('(prefers-reduced-motion: reduce)').matches){v.removeAttribute('autoplay');v.pause();}
})();
</script>'''
def page(title, desc, path, body, extra=''):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="https://lehcobrand.com{path}">
<meta name="theme-color" content="#0b121c">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://lehcobrand.com{path}">
<meta property="og:image" content="https://lehcobrand.com/media/hero-reel.jpg">
{FONTS}
<link rel="stylesheet" href="/lehco.css?v={CSSV}">
{extra}
</head>
<body>
{body}
{FOOT}
{PLAYER}
</body>
</html>
'''
STORIES = [
 ('mack-trucks.html', 'Mack Trucks', 'Born in Allentown in 1905, with a snarling bulldog on the hood.'),
 ('liberty-bell-hidden-allentown.html', "The Liberty Bell's hideout", "Nine months under the floor of Zion's Reformed Church, 1777."),
 ('a-treat-soda.html', 'A-Treat soda', 'Bottled in Allentown since 1918. Birch beer included.'),
 ('hess-department-store.html', "Hess's department store", 'The store that turned shopping on Hamilton Street into a show.'),
 ('shankweilers-drive-in.html', "Shankweiler's Drive-In", "Orefield, 1934. America's oldest drive-in still running."),
 ('dorney-park.html', 'Dorney Park', 'Dropping stomachs since 1884.'),
 ('trexlertown-velodrome.html', 'The Trexlertown velodrome', 'How a quiet corner of the county became a cycling capital.'),
 ('lee-iacocca.html', 'Lee Iacocca', 'The Allentown kid behind the Mustang and the Chrysler rescue.'),
 ('saquon-barkley.html', 'Saquon Barkley', "Whitehall's own, before the NFL knew his name."),
]
SAID = ['You\'re not really from here until you\'ve argued about whether it\'s "Allentown" or "the Valley."',
 'There are two seasons in Lehigh County: Fair season, and "when\'s the Fair again?" season.',
 "A-Treat birch beer isn't a beverage preference. It's a personality trait.",
 'Ask someone from Trexlertown about the Velodrome. Clear your schedule.',
 "If your grandfather didn't work at Mack, did you even grow up here?",
 "We hid the Liberty Bell in a church basement once. We don't bring it up enough."]
TOWNS = ['Allentown', 'Emmaus', 'Macungie', 'Slatington', 'Whitehall', 'Coopersburg', 'Catasauqua', 'Coplay', 'Egypt', 'Trexlertown', 'Fogelsville',
         'Alburtis', 'Center Valley', 'Orefield', 'Schnecksville', 'New Tripoli', 'Breinigsville', 'Zionsville', 'Neffs', 'Fullerton', 'Upper Saucon',
         'Upper Macungie', 'Salisbury', 'Bethlehem', 'Kutztown Road', 'Lehigh River', 'Jordan Creek']
def town_count(t): return sum(1 for r in rows if re.search(r'\b' + re.escape(t) + r'\b', r['title'], re.I))
towns = sorted([(t, town_count(t)) for t in TOWNS], key=lambda x: -x[1])
towns = [(t, n) for t, n in towns if n][:14]
latest, recent = rows[0], rows[1:11]
watched = sorted(rows, key=lambda r: int(r['reach'] or 0), reverse=True)[:5]
ticker = ''.join(f'<q>{E(q)}</q>' for q in SAID)
home = f'''{top('')}
<main>
<section class="hero">
<video autoplay muted loop playsinline preload="metadata" poster="/media/hero-reel.jpg" aria-hidden="true"><source src="/media/hero-reel.mp4" type="video/mp4"></video>
<div class="wrap">
<h1>You’ve driven past it <em>a thousand times.</em></h1>
<p>The bell hidden under a church floor. The creek that sinks into the ground. The outhouse on the National Register. Lehigh County’s stories, one minute every morning at 8.</p>
<div class="acts"><a class="btn" href="https://www.youtube.com/shorts/{ytid(latest['youtube'])}" data-yt="{ytid(latest['youtube'])}">{TRI} Play this morning’s story</a><a class="btn ghost" href="/episodes.html">Browse every episode</a></div>
</div>
</section>
<section class="sec" id="latest"><div class="wrap">
<div class="today">
{card(latest, True)}
<div><p class="when">This morning · {nice(latest['date'])}</p><h2>{E(latest['title'])}</h2>
<p class="lede">Sixty seconds, real photographs, named sources. If we get one wrong, the correction gets pinned.</p>
<div class="acts"><a class="btn" href="https://www.youtube.com/shorts/{ytid(latest['youtube'])}" data-yt="{ytid(latest['youtube'])}">{TRI} Watch now</a><a class="btn ghost" href="{YT}?sub_confirmation=1" target="_blank" rel="noopener">Subscribe on YouTube</a></div></div>
</div>
<div class="headrow" style="margin-top:clamp(50px,8vw,90px)"><h2>The last ten mornings</h2><a class="more" href="/episodes.html">All {len(rows)} episodes</a></div>
<div class="reel">{''.join(card(r) for r in recent)}</div>
</div></section>
<section class="map" id="towns"><div class="pan" aria-hidden="true"></div><div class="wrap">
<h2>Find the one about your town.</h2>
<p class="lede">Every crossroads in the county has a story it doesn’t brag about. Pick a place.</p>
<div class="towns">{''.join(f'<a href="/episodes.html?q={E(t.replace(" ", "+"))}">{E(t)}<span>{n}</span></a>' for t, n in towns)}</div>
<p class="credit">Macungie from above, drawn in 1893. Library of Congress.</p>
</div></section>
<section class="sec"><div class="wrap">
<div class="headrow"><div><h2>The ones the county couldn’t stop sharing</h2><p class="lede">Our five most-watched stories so far.</p></div></div>
<div class="grid">{''.join(card(r) for r in watched)}</div>
</div></section>
<section class="sec tight" id="stories"><div class="wrap split">
<figure><img src="/media/hamilton-1910.jpg" alt="Hand-tinted postcard of Hamilton Street in Allentown around 1910, with trolley tracks and brick storefronts" loading="lazy"><figcaption>Hamilton Street looking west from the courthouse, about 1910.</figcaption></figure>
<div><h2>The long versions</h2><p class="lede">Every county has landmarks. Ours have plot twists.</p>
<ul class="stories">{''.join(f'<li><a href="/{f}"><strong>{E(t)}</strong><span>{E(d)}</span><i aria-hidden="true">&rarr;</i></a></li>' for f, t, d in STORIES)}</ul></div>
</div></section>
<section class="shop" id="shop"><div class="wrap">
<h2>Wear the county.</h2>
<p class="lede" style="color:#e6dfcf">There’s a Delco shirt, a Chesco shirt and a Bucks shirt. We figured the county with a bulldog on the hood and a bell in the basement deserved one too. Printed to order, one at a time.</p>
<div class="acts"><a class="btn" href="{ETSY}" target="_blank" rel="noopener">Open the Etsy shop</a></div>
<p class="credit">Hamilton Street looking east, 1935 postcard.</p>
</div></section>
<div class="ticker" aria-label="Overheard in the 610"><div class="run">{ticker}{ticker}</div></div>
<section class="sec" id="write"><div class="wrap write">
<div><h2>Got a shoebox of old photos?</h2>
<p class="lede">Spot a mistake, know a story we should tell, or have pictures of Lehigh County nobody has seen in fifty years? Send them. If we make your idea, your name goes on it.</p>
<div class="acts"><a class="btn" href="mailto:{MAIL}">Email {MAIL}</a><a class="btn ghost" href="{IG}" target="_blank" rel="noopener">Instagram</a><a class="btn ghost" href="{TT}" target="_blank" rel="noopener">TikTok</a></div></div>
<div class="cards" aria-hidden="true"><img src="/media/bridge-1905.jpg" alt="" loading="lazy"><img src="/media/jordan-1905.jpg" alt="" loading="lazy"></div>
</div></section>
</main>'''
ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "LEHCO: History of Lehigh County, PA", "itemListElement": [
  {"@type": "ListItem", "position": i + 1, "item": {"@type": "VideoObject", "name": r['title'], "description": r['title'], "uploadDate": r['date'],
   "thumbnailUrl": f"https://i.ytimg.com/vi/{ytid(r['youtube'])}/hqdefault.jpg", "embedUrl": f"https://www.youtube.com/embed/{ytid(r['youtube'])}",
   "url": f"https://www.youtube.com/shorts/{ytid(r['youtube'])}"}} for i, r in enumerate(rows)]}
eps = f'''{top('ep')}
<main>
<section class="pagehead"><div class="wrap">
<h1>Every story so far.</h1>
<p class="lede" style="color:#e6dfcf">{len(rows)} mornings of Lehigh County history, newest first. Search for your town, a street, a family name.</p>
<input class="search" id="q" type="search" placeholder="Try Emmaus, Mack, covered bridge" aria-label="Search episodes">
</div></section>
<section class="sec" style="padding-top:20px"><div class="wrap">
<div class="grid" id="all" style="margin-top:0">{''.join(card(r) for r in rows)}</div>
<p class="none" id="none">No episode on that yet. Email the idea to <a href="mailto:{MAIL}">{MAIL}</a> and if we make it, you get the credit.</p>
</div></section>
</main>
<script>
var q=document.getElementById('q'),eps=[].slice.call(document.querySelectorAll('#all .card')),none=document.getElementById('none');
function f(){{var s=q.value.trim().toLowerCase(),n=0;eps.forEach(function(e){{var ok=!s||e.getAttribute('data-t').indexOf(s)>-1;e.style.display=ok?'':'none';if(ok)n++;}});none.style.display=n?'none':'block';}}
q.addEventListener('input',f);var p=new URLSearchParams(location.search).get('q');if(p){{q.value=p;f();}}
</script>'''
out = lambda name, text: open(os.path.join(site, name), 'w', encoding='utf-8').write(text)
out('index.html', page('LEHCO: the Lehigh County stories you drive past every day', 'You’ve driven past it a thousand times. One minute of Lehigh County, Pennsylvania history every morning at 8: real photographs, named sources, and the gear to wear it.', '/', home))
out('episodes.html', page('Every LEHCO episode: Lehigh County history in sixty seconds', f'{len(rows)} short history videos about Lehigh County, Pennsylvania. Search by town and watch right on the page.', '/episodes.html', eps, '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'))
# story pages: same content, site look, working links
SKIN = '''<!--lehco-skin-->''' + FONTS + '''<style>
:root{--navy:#0b121c;--navy-deep:#0b121c;--gold:#e0aa3e;--gold-bright:#e0aa3e;--gold-dim:#e0aa3e;--cream:#efe6d2;--paper:#17263a;--white:#17263a;--ink:#efe6d2}
body{font-family:'Archivo',Arial,sans-serif;font-size:1.0625rem;background:#0b121c;color:#efe6d2}
h1,h2{font-family:'Fraunces',Georgia,serif;font-weight:600;letter-spacing:-.01em;text-transform:none}
.topbar{background:#0b121c;border-bottom:1px solid rgba(239,230,210,.16)}
.topbar .brand{font-family:'Fraunces',Georgia,serif;font-weight:700;color:#efe6d2;font-size:1.35rem;letter-spacing:.06em}.topbar .brand span{color:#efe6d2}
.topbar a.back{font-family:'Archivo',Arial,sans-serif;font-weight:600;font-size:.98rem;color:#efe6d2;opacity:1;text-transform:none;letter-spacing:.02em}.topbar a.back:hover{color:#e0aa3e}
.hero-band{background:#111c2b;background-image:none}
.hero-band h1{font-size:clamp(2.1rem,5.6vw,3.6rem);line-height:1.04;text-transform:none}
.hero-image{border-radius:6px;box-shadow:0 24px 60px rgba(0,0,0,.5);border:8px solid #efe6d2;background:#efe6d2}
article>p{color:#e6dfcf}
.t-card{border-radius:12px;box-shadow:none;border:1px solid rgba(239,230,210,.16);background:#17263a}
.t-card h3{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:1.2rem;color:#efe6d2}.t-card p{color:#b9b3a3}
.t-year,.section-label,.merch-tease strong{font-family:'Archivo',Arial,sans-serif;font-weight:700;letter-spacing:.04em;color:#e0aa3e}
.merch-tease{border-radius:12px;background:#17263a}
footer{background:#0b121c;color:#b9b3a3;border-top:1px solid rgba(239,230,210,.16)}
</style>'''
for f, _, _ in STORIES:
    p = os.path.join(site, f)
    if not os.path.exists(p): print('missing', f); continue
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!--lehco-skin-->.*?</style>\n?', '', s, flags=re.S)
    s = s.replace('../lehco-site.html#legends', '/#stories').replace('../lehco-site.html#shop', ETSY).replace('../lehco-site.html#join', '/#write').replace('../lehco-site.html', '/')
    s = s.replace('>Join the List<', '>Write to us<').replace('>History<', '>Stories<')
    s = s.replace('</head>', SKIN + '\n</head>', 1)
    open(p, 'w', encoding='utf-8').write(s)
print('built', len(rows), 'episodes; towns', towns[:6])
