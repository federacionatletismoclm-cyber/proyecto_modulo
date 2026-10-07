import re, json, os
base = os.path.dirname(os.path.abspath(__file__))
live = os.path.join(base, '..', 'deck_pub', 'project')
order = json.load(open(os.path.join(live, 'deck.json'), encoding='utf-8'))['order']
blob = {'e89149e6f449d98f173b1a860eca0256': 'antes.jpg', 'e8cf135e02e33058e7360737a5c15265': 'logo_ayto.png',
        'eb84ed1ea9d4b4b0b0a5b9aadc0f0561': 'logo_deporte.png', '2d5361146f1b2b363bdda74291bf9bae': 'r_ext.jpg',
        '1a8ef46b99927379a91ad6b841399350': 'r_int.jpg', '59bce7d2b685216ae58a7029d9d79dc7': 'r_atl2.jpg',
        '0b20d112a1c70fd6b47dc0aa655be8a1': 'r_cancha.jpg', 'ea9f176d1c8184eeb564ca2af98bfcf5': 'r_atl.jpg',
        'c7f31533d775e75be2464d9c850b0f17': 'r_planta.jpg',
        '85c7bf986819b59e3f7e63173908b7f8': 'sup_tartan.jpg', '8d378dc8d52c1bbd1f16e1828f743b8b': 'sup_pvc.jpg'}
icons = {'Warning': '<path d="M12 3 22 20H2Z"/><path d="M12 10v5"/><path d="M12 17.5v.5"/>',
         'Cloud': '<path d="M7 18a4 4 0 0 1-.5-8 5.5 5.5 0 0 1 10.6-1A4.5 4.5 0 0 1 17 18Z"/>',
         'Users': '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.5 3-6 6-6s6 2.5 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14c3 0 5 2 5 5"/>',
         'Home': '<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/>',
         'Lightbulb': '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3Z"/>',
         'Verified': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6Z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
         'Activity': '<path d="M2 12h4l3-8 6 16 3-8h4"/>',
         'Star': '<path d="M12 2l3 7 7 .5-5.5 4.5 2 7L12 17l-6.5 4 2-7L2 9.5 9 9Z"/>'}
def icon(m):
    st = m.group(2); col = re.search(r'color:(#[0-9A-Fa-f]{6})', st).group(1); w = re.search(r'width:(\d+)px', st).group(1)
    return f'<svg viewBox="0 0 24 24" width="{w}" height="{w}" fill="none" stroke="{col}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="flex:none">{icons[m.group(1)]}</svg>'
out = []
for sid in order:
    h = open(os.path.join(live, 'slides', sid + '.html'), encoding='utf-8').read()
    h = re.sub(r'<aside>.*?</aside>', '', h, flags=re.S)
    h = re.sub(r'<x-icon name="(\w+)" style="([^"]*)"></x-icon>', icon, h)
    for k, v in blob.items(): h = h.replace('/_blob/' + k, '../presentacion_img/' + v)
    h = re.sub(r'<section id="[^"]+"[^>]*? style="', '<div class="slide" style="position:relative;width:1920px;height:1080px;overflow:hidden;box-sizing:border-box;', h, count=1)
    h = h.replace('</section>', '</div>')
    out.append(h)
html = '''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Mejora de Pistas Multideporte</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Public+Sans:wght@400;600;700&display=swap">
<style>@page{size:1920px 1080px;margin:0}html,body{margin:0;padding:0;background:#fff}.slide{page-break-after:always;break-after:page}p,h1,h2,h3{margin:0}ul{margin:0}.slide>*:not([style*="position:absolute"]){position:relative;z-index:2}.slide>[style*="position:absolute"]{z-index:1}</style></head><body>''' + '\n'.join(out) + '</body></html>'
open(os.path.join(base, 'presentacion.html'), 'w', encoding='utf-8').write(html)
print(len(out), 'diapositivas')
