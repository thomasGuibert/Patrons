import sys, math
sys.path.insert(0, sys.argv[3] if len(sys.argv) > 3 else __import__("os").path.dirname(__file__))
from evaluer_hors_seamly import Pattern, plen
from PIL import Image, ImageDraw
p = Pattern(sys.argv[1])
mod = {}
for b in p.root.iter('draftBlock'):
    for e in b.find('modeling'):
        mod[e.get('id')] = e.get('idObject')
def nearest(pts, q):
    return min(range(len(pts)), key=lambda i: math.dist(pts[i], q))
outlines = {}
for pc in p.root.iter('piece'):
    nodes = list(pc.iter('node'))
    seq = []
    for k, n in enumerate(nodes):
        o = mod[n.get('idObject')]
        if n.get('type') == 'NodePoint':
            seq.append(('P', p.P[o], n.get('notch')))
        else:
            pts = list(p.curve_by_id[o])
            if n.get('reverse') == '1': pts = pts[::-1]
            seq.append(('C', pts, None))
    poly, notches = [], []
    for k, (t, v, notch) in enumerate(seq):
        if t == 'P':
            poly.append(v)
            if notch: notches.append(v)
        else:
            prev = next((s[1] for s in reversed(seq[:k]) if s[0] == 'P'), None)
            nxt = next((s[1] for s in seq[k+1:] if s[0] == 'P'), seq[0][1])
            i0 = nearest(v, prev) if prev else 0
            i1 = nearest(v, nxt)
            poly += v[i0:i1+1] if i1 >= i0 else v[i0:i1-1:-1]
    outlines[pc.get('name')] = (poly, notches)
s = 8
allp = [q for poly, _ in outlines.values() for q in poly]
minx = min(q[0] for q in allp) - 3; maxy = max(q[1] for q in allp) + 3
W = int((max(q[0] for q in allp) - minx + 3) * s); Hh = int((maxy - min(q[1] for q in allp) + 3) * s)
im = Image.new('RGB', (W, Hh), 'white'); d = ImageDraw.Draw(im)
tr = lambda q: ((q[0] - minx) * s, (maxy - q[1]) * s)
cols = {'Devant': 'blue', 'Dos': 'red', 'Manche': 'green', "Bande d'encolure": 'purple', 'Carré 5x5': 'black'}
for name, (poly, notches) in outlines.items():
    d.line([tr(q) for q in poly + poly[:1]], fill=cols.get(name, 'black'), width=2)
    for q in notches:
        x, y = tr(q); d.ellipse((x-4, y-4, x+4, y+4), outline='orange', width=2)
for n in ['vK','vKp','vKpp','vHp','vHpp','vE2','vC2','vF2','mE','mCrE']:
    x, y = tr(p.byname[n]); d.text((x+4, y-10), n, fill='black')
im.save(sys.argv[2])
for name, (poly, _) in outlines.items():
    print(name, 'périmètre', round(plen(poly + poly[:1]), 2))
