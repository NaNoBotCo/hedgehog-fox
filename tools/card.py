"""Share card: docs/card.jpg, 1200x630, drawn with the site's own fox and hedgehog code.

    python3 tools/card.py
"""
import pathlib, re, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

src = (DOCS / "index.html").read_text()
draw = src.split("/* drawings */", 1)[1].split("$('#fox')", 1)[0]
css = re.search(r":root\{[^}]*\}", src).group(0)

PAGE = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,800&family=Nunito:wght@800&display=block">
<style>{css}
html,body{{margin:0;width:1200px;height:630px;overflow:hidden;background:radial-gradient(ellipse at 80% 15%,#2f5240 0,#14231c 65%)}}
.moon{{position:absolute;right:120px;top:50px;width:110px;height:110px;border-radius:50%;background:#fff4cf;box-shadow:0 0 80px 30px rgba(255,240,190,.25)}}
#trees{{position:absolute;left:0;bottom:0;width:1200px;height:420px}}
.t{{position:absolute;left:64px;top:70px;width:700px;font-family:Fraunces,serif;color:#fff7e6}}
.k{{font:800 24px Nunito,sans-serif;letter-spacing:.12em;color:#8fb456;text-transform:uppercase}}
h1{{font-size:86px;line-height:1;margin:12px 0 18px;text-shadow:0 4px 24px rgba(0,0,0,.6)}}
.q{{font-size:32px;color:#fdebc4;line-height:1.25;text-shadow:0 2px 14px #000}}
#fox{{position:absolute;left:560px;bottom:44px;width:330px}}
#hog{{position:absolute;right:70px;bottom:44px;width:210px}} .hog-ball{{display:none}}
.ground{{position:absolute;left:-20px;right:-20px;bottom:0;height:70px;background:#2a4a31;border-radius:50% 50% 0 0/100% 100% 0 0}}
.fly{{position:absolute;width:7px;height:7px;border-radius:50%;background:#ffe58a;box-shadow:0 0 14px 5px rgba(255,229,138,.6)}}
</style></head><body>
<div class="moon"></div><svg id="trees" viewBox="0 0 1200 600" preserveAspectRatio="xMidYMax slice"></svg>
<div class="ground"></div><div id="fox"></div><div id="hog"></div>
<div class="t"><div class="k">Archilochus · Berlin · Tetlock · a quiz</div><h1>The Hedgehog<br>and the Fox</h1><div class="q">“The fox knows many things, but the hedgehog knows one big thing.”</div></div>
<script>
const $=s=>document.querySelector(s);
let seed=7;const rnd=(a,b)=>{{seed=(seed*16807)%2147483647;return a+(seed/2147483647)*(b-a)}};
{draw}
$('#fox').innerHTML=foxSVG();$('#hog').innerHTML=hogSVG();
let g='';const cols=['#1a2e24','#203a2c','#254433'];
for(let layer=0;layer<3;layer++){{for(let i=0;i<14;i++){{const x=i*95+rnd(-30,30)+layer*40,h=rnd(220,420)-layer*60,w=h*0.42,base=600-layer*10;
g+=`<g fill="${{cols[layer]}}"><rect x="${{x-6}}" y="${{base-40}}" width="12" height="40" fill="#2b2017"/><path d="M${{x}} ${{base-h}}L${{x+w/2}} ${{base-40}}H${{x-w/2}}Z"/><path d="M${{x}} ${{base-h*0.8}}L${{x+w*0.6}} ${{base-h*0.25}}H${{x-w*0.6}}Z"/></g>`}}}}
$('#trees').innerHTML=g;
for(let i=0;i<22;i++){{const d=document.createElement('i');d.className='fly';d.style.left=rnd(0,1200)+'px';d.style.top=rnd(20,560)+'px';d.style.opacity=rnd(.3,1);document.body.appendChild(d)}}
</script></body></html>"""

with tempfile.TemporaryDirectory() as tmp:
    page = pathlib.Path(tmp) / "card.html"
    page.write_text(PAGE)
    png = pathlib.Path(tmp) / "card.png"
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--window-size=1200,630",
                    "--virtual-time-budget=4000", f"--screenshot={png}", page.as_uri()],
                   check=True, capture_output=True)
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "86", str(png),
                    "--out", str(DOCS / "card.jpg")], check=True, capture_output=True)
print("docs/card.jpg")
