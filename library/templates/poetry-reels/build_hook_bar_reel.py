import html
E_=html.escape; TOTAL=21.5
SH=[("a",0,3.9,1.0,1.06),("b",3.8,11.7,1.08,1.0),("c",11.6,16.9,1.0,1.1),("d",16.8,TOTAL,1.12,1.0)]
CAP=[(3.95,7.6,"Sab se baat karta hai, sab ki sunta hai,"),(7.7,11.55,"bas apni baat kisi se nahi kehta."),
     (11.75,14.15,"Khamosh hoon to yeh na samajh ke haar gaya,"),(14.25,16.75,"kuch jung mard chup reh kar ladte hain. 🖤"),
     (16.95,TOTAL,"Aur ek din... sab theek ho jata hai. 🤍")]
b,j=[],[]
def show(s,t0,t1):
    j.append(f'gsap.set("{s}",{{visibility:"hidden"}});tl.set("{s}",{{visibility:"visible"}},{t0});')
    if t1<TOTAL: j.append(f'tl.set("{s}",{{visibility:"hidden"}},{t1});')
for n,t0,t1,z0,z1 in SH:
    d=round(t1-t0,2)
    b.append(f'<div id="s{n}" style="position:absolute;left:0;top:330px;width:1080px;height:1590px;overflow:hidden;"><div id="s{n}z" style="position:absolute;inset:0;"><video id="v{n}" src="assets/clips/{n}.mp4" data-start="{t0}" data-duration="{d}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div></div>')
    show(f"#s{n}",t0,t1); j.append(f'tl.fromTo("#s{n}z",{{scale:{z0}}},{{scale:{z1},duration:{d},ease:"none"}},{t0});')
j.append('tl.fromTo("#sb",{opacity:0},{opacity:1,duration:0.35},3.8);')
j.append('tl.fromTo("#sd",{opacity:0,filter:"blur(16px)"},{opacity:1,filter:"blur(0px)",duration:0.5},16.8);')
b.append('<div style="position:absolute;left:0;top:330px;width:1080px;height:1590px;background:linear-gradient(180deg,rgba(0,0,0,0) 45%,rgba(0,0,0,0.65) 100%);pointer-events:none;"></div>')
b.append('<div id="fl" style="position:absolute;left:0;top:330px;width:1080px;height:1590px;background:#fff;"></div>'); show("#fl",11.55,11.95)
j.append('tl.fromTo("#fl",{opacity:0.9},{opacity:0,duration:0.4},11.55);')
for i,(t0,t1,txt) in enumerate(CAP):
    ws=txt.split(" ")
    b.append(f'<div id="c{i}" class="cap">'+" ".join(f'<span id="c{i}_{k}" class="w">{E_(w)}</span>' for k,w in enumerate(ws))+'</div>'); show(f"#c{i}",t0,t1)
    for k in range(len(ws)): j.append(f'tl.fromTo("#c{i}_{k}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.3,ease:"power2.out"}},{round(t0+k*0.17,2)});')
b.append('<div id="bar" style="position:absolute;left:0;top:0;width:1080px;height:330px;background:#fff;"></div>')
b.append('<div id="h1" class="hk">Woh ladka jo sab ko<br>hasata hai...</div>'); show("#h1",0,19.0)
b.append('<div id="h2" class="hk">Ahmad Ali ✍️<br><span style="font-size:44px;color:#555;">Follow for more</span></div>'); show("#h2",19.0,TOTAL)
j.append('tl.fromTo("#h1",{opacity:0,y:20},{opacity:1,y:0,duration:0.4},0.1);tl.fromTo("#h2",{opacity:0,y:20},{opacity:1,y:0,duration:0.4},19.0);')
open("index.html","w").write(f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/vendor/gsap-3.14.2.min.js"></script><style>
@font-face{{font-family:"PB";src:url("assets/fonts/Poppins-ExtraBold.ttf");}}@font-face{{font-family:"PS";src:url("assets/fonts/Poppins-SemiBold.ttf");}}
*{{margin:0;padding:0;box-sizing:border-box;}}html,body{{width:1080px;height:1920px;overflow:hidden;background:#000;}}
.hk{{position:absolute;left:40px;right:40px;top:70px;text-align:center;font-family:PB;font-size:70px;line-height:1.1;color:#141414;}}
.cap{{position:absolute;left:70px;right:70px;top:1450px;text-align:center;font-family:PS;font-size:58px;line-height:1.25;color:#fff;text-shadow:0 3px 14px rgba(0,0,0,0.9);}}
.w{{display:inline-block;}}
</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920" style="position:absolute;inset:0;overflow:hidden;background:#000;">
{chr(10).join(b)}
</div><script>const tl=gsap.timeline({{paused:true}});
{chr(10).join(j)}
tl.to({{}},{{duration:{TOTAL}}},0);window.__timelines=window.__timelines||{{}};window.__timelines["main"]=tl;</script></body></html>''')
print("ok")
