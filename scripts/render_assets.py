"""Generate the static profile SVGs (header, nav buttons, intro box, build cards). Run locally: python scripts/render_assets.py"""
from pathlib import Path
import random

from fontTools.ttLib import TTFont

from theme import BLACK, WHITE, GRAY, YELLOW, ORANGE, RED, KRIS, SUSIE, RALSEI, NOELLE, FONTS, FAMILIES, font_css, text

OUT = Path(__file__).resolve().parent.parent / 'assets'
HEART = 'M-8 -10h6v2h4v-2h6v2h2v2h2v8h-2v2H8v2H6v2H4v2H2v2h-4v-2h-2V8h-2V6h-2V4h-2V2h-2v-8h2v-2h2z'


def svg(w, h, label, body, css=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{label}"><title>{label}</title><style>{css}</style>'
            f'<rect width="{w}" height="{h}" fill="{BLACK}"/>{body}</svg>')


def width(value, size, font):
    f = TTFont(FONTS / (FAMILIES[font] + '.ttf'))
    cmap, hmtx = f.getBestCmap(), f['hmtx']
    return sum(hmtx[cmap[ord(c)]][0] for c in value) * size / f['head'].unitsPerEm


def word_platforms(x, y, value, size, font):
    """(top, left, right) of every word in a text line, so sprites can stand on the actual glyph tops."""
    f = TTFont(FONTS / (FAMILIES[font] + '.ttf'))
    cmap, glyf, upm = f.getBestCmap(), f['glyf'], f['head'].unitsPerEm
    out, start = [], 0
    for word in value.split(' '):
        if word:
            top = max(getattr(glyf[cmap[ord(c)]], 'yMax', 0) for c in word) * size / upm
            left = x + width(value[:start], size, font)
            out.append((y - top, left, left + width(word, size, font)))
        start += len(word) + 1
    return out


def pixels(rows, palette, scale, x=0, y=0, cls=''):
    """Pixel-art grid -> one <path> per colour; '.' is transparent."""
    paths = {}
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            key, run = row[c], 1
            while c + run < len(row) and row[c + run] == key: run += 1
            if key != '.': paths.setdefault(key, []).append(f'M{c} {r}h{run}v1h-{run}z')
            c += run
    inner = ''.join(f'<path fill="{palette[k]}" d="{"".join(d)}"/>' for k, d in paths.items())
    return f'<g{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} transform="translate({x} {y}) scale({scale})">{inner}</g>'


# Original pixel sprites in the spirit of the games' casts (body rows + two leg frames for the walk cycle).
SPRITES = {
    'kid': ({'h': '#6e4a26', 's': '#f5c896', 'k': '#3a2a1a', 'b': '#4a6bd2', 'm': '#c94fd1', 'p': '#3a55b0', 'o': '#7a4a26'},
            ['...hhhhhh...', '..hhhhhhhh..', '.hhhhhhhhhh.', '.hhsssssshh.', '.hsksssskshh', '..ssssssss..', '...ssssss...',
             '..bbbbbbbb..', '.sbmmmmmmbs.', '.sbbbbbbbbs.', '.sbmmmmmmbs.', '..bbbbbbbb..', '..pppppppp..'],
            ['..ppp..ppp..', '..ppp..ppp..', '.ooo....ooo.'], ['...pp..pp...', '...pp..pp...', '..ooo..ooo..']),
    'skeleton': ({'w': '#ffffff', 'k': '#000000', 'f': '#cfcfd6', 'b': '#2e66c1', 'd': '#3a3a4a', 'q': '#ff8fc8'},
                 ['...wwwwww...', '.wwwwwwwwww.', 'wwwwwwwwwwww', 'wwkkwwwwkkww', 'wwkkwwwwkkww', 'wwwwwkkwwwww', '.wwkwkwkwkw.',
                  '..wwwwwwww..', 'fbbbbbbbbbbf', 'bbbbbbbbbbbb', 'bbbbbffbbbbb', 'wbbbbffbbbbw', 'wbbbbbbbbbbw'],
                 ['.dddddddddd.', '..ww....ww..', '.qqq....qqq.'], ['.dddddddddd.', '...ww..ww...', '..qqq..qqq..']),
    'tall_skeleton': ({'w': '#ffffff', 'k': '#000000', 'r': '#e0302a', 'y': '#f2c12e', 'b': '#3b6fd9'},
                      ['...wwwwww...', '..wwwwwwww..', '..wkkwwkkw..', '..wwwwkwww..', '..wkwkwkww..', '...wwwwww...',
                       '.rrrrrrrrrr.', 'rr.wyyyyw.rr', 'r.wwwwwwww..', '..wwyyyyww..', '..wwwwwwww..', '.rwwwwwwwwr.', '..bbbbbbbb..'],
                      ['..ww....ww..', '..ww....ww..', '..ww....ww..', '.rrr....rrr.', '.rrr....rrr.'],
                      ['...ww..ww...', '...ww..ww...', '...ww..ww...', '..rrr..rrr..', '..rrr..rrr..']),
    'goat_mom': ({'h': '#f0d9a8', 'w': '#ffffff', 'k': '#000000', 'q': '#ff9aa8', 'p': '#7d4ab5'},
                 ['..h......h..', '..hh....hh..', '...wwwwww...', '..wwwwwwww..', 'wwwkwwwwkwww', 'ww.wwwwww.ww', '...wwqqww...',
                  '....wwww....', '..pppppppp..', '.pppppppppp.', 'wppppwwppppw', 'wppppppppppw', '.pppppppppp.', '.pppppppppp.'],
                 ['.pppppppppp.', '..ww....ww..'], ['.pppppppppp.', '...ww..ww...']),
    'hero': ({'h': '#5a3a22', 's': '#f2d2b8', 'g': '#3fa34d', 'y': '#f0d040', 'd': '#2b3a8f', 'o': '#6b4a2a'},
             ['...hhhhhh...', '..hhhhhhhh..', '.hhhhhhhhhh.', '.hhhhhhhhhh.', '.hhsssssshh.', '.hhsssssshh.', '..h.ssss.h..',
              '..gggggggg..', '.sggggggggs.', '.syyyyyyyys.', '.sggggggggs.', '..gggggggg..', '..dddddddd..'],
             ['..ddd..ddd..', '.ooo....ooo.'], ['...dd..dd...', '..oo...oo...']),
    'bruiser': ({'e': '#a8327a', 'u': '#8f7ccf', 'w': '#ffffff', 'j': '#565b78', 'n': '#3d3570', 'o': '#6b4a2a'},
                ['.ee.eeee.ee.', 'eeeeeeeeeeee', 'eeeeeeeeeeee', 'eeuuuuuuuuee', 'eeuuuuuuuuee', '.euuwwwwuue.', '..uuuuuuuu..',
                 '.jjjjjjjjjj.', 'jjjjjjjjjjjj', 'ujjjjjjjjjju', 'ujjjjjjjjjju', '.jjjjjjjjjj.', '..nnnnnnnn..'],
                ['..nnn..nnn..', '.ooo....ooo.'], ['...nn..nn...', '..oo...oo...']),
    'prince': ({'g': '#2fa860', 'f': '#5a5a6e', 'w': '#ffffff', 'q': '#ff73b5'},
               ['.....g......', '....ggg.....', '...ggggg....', '..ggggggg...', '.ggggggggggg', '..fffffff...', '..fwfffwf...',
                '...fffff....', '..qqqqqqq...', '.gggggggggg.', 'fggggggggggf', '.gggggggggg.', '.gggggggggg.'],
               ['.gggggggggg.', '..ff....ff..'], ['.gggggggggg.', '...ff..ff...']),
}
for _name, (_pal, _body, _a, _b) in SPRITES.items():  # self-check: every sprite row is the same width
    assert len({len(r) for r in _body + _a + _b}) == 1, _name

# A white dog driving a toy coupe, side view facing right.
CAR = ({'o': '#ff8c1a', 'y': '#ffc83d', 'w': '#ffffff', 'k': '#000000', 'g': '#6a6a6a', 'r': '#e8243c', 'd': '#a3122a'},
       ['...oooooooooooooo.....', '..oyyyyyyyyyyyyyyo....', '..oyo...........yo....', '..oyo...wwww....yo....',
        '..oyo..wwwwww...yo....', '..oyo..wkwwkw...yo....', '..oyo..wwwkkw..gyo....', '..oyo...wwww..g.yo....',
        'rrrrrrrrrrrrrrrrrrrr..', 'rrrrrrrrrrrrrrrrrrrrr.', 'rrrrrrrrrrrrrrrrrrrrrr', 'rrrrrrrdrrrrrrrrrrrrrr',
        'rrrrrrrdrrrrrrrrrrrrrr', 'drrrrrrrrrrrrrrrrrrrrd', '.ddgggddddddddddgggdd.', '..ggwgg.......ggwgg...',
        '..gwwwg.......gwwwg...', '...ggg.........ggg....'])
assert len({len(r) for r in CAR[1]}) == 1


def explosion_frames(seed=7):
    """Eight 16x16 frames: white-hot core -> yellow -> orange -> brown smoke -> scattered debris."""
    rng, frames = random.Random(seed), []
    for k, r in enumerate([1.5, 3.5, 5.5, 6.5, 7, 7.2, 7, 6]):
        rows = []
        for y in range(16):
            row = ''
            for x in range(16):
                d = ((x - 7.5) ** 2 + (y - 7.5) ** 2) ** .5 + rng.uniform(-1.2, 1.2)
                gone = d >= r or (k >= 5 and rng.random() < (k - 4) * .22)
                row += '.' if gone else '012345'[min(5, int(d / r * 2.2 + k * .6))]
            rows.append(row)
        frames.append(rows)
    return frames


BLAST = dict(zip('012345', ['#ffffff', '#fff6b0', '#ffd84a', '#ff8c1a', '#b5651d', '#6b3410']))


def sprite(name, x, ground, scale, delay):
    pal, body, a, b = SPRITES[name]
    top = ground - (len(body) + len(a)) * scale
    legs_y = top + len(body) * scale
    style = f' style="animation-delay:-{delay}s"'
    return (pixels(body, pal, scale, x, top) +
            pixels(a, pal, scale, x, legs_y, 'fa').replace('class="fa"', 'class="fa"' + style) +
            pixels(b, pal, scale, x, legs_y, 'fb').replace('class="fb"', 'class="fb"' + style))


def steps_css(name, changes, T, start):
    """Opacity keyframes that switch instantly at each (seconds, value) change."""
    frames, prev = [f'0%{{opacity:{start}}}'], start
    for t, v in changes:
        p = t / T * 100
        frames += [f'{max(p - .001, 0):.3f}%{{opacity:{prev}}}', f'{p:.3f}%{{opacity:{v}}}']
        prev = v
    return f'@keyframes {name}{{{"".join(frames)}100%{{opacity:{prev}}}}}'


def scene(names, platforms, T=60.0, seed=27, dt=.05):
    """Simulate one seamless loop: sprites hop between words; the dog-car drives along a line and anyone it touches
    explodes and respawns on the floor. Everything shares the period T so collisions stay in sync."""
    rng = random.Random(seed)
    floor = next(p for p in platforms if p[3] == 'floor')
    lines = {}
    for p in platforms: lines.setdefault(p[3], []).append(p)
    roads = [l for l in lines if l not in ('label', 'arena')]
    cw, ch, speed, scale = len(CAR[1][0]) * 3, len(CAR[1]) * 3, 260, 3
    drive_at = [5 + 7 * k for k in range(5)]  # last drive ends well before the walk home
    drives, blasts, active = [], [], None

    chars = []
    for name in names:
        pal, body, a, b = SPRITES[name]
        w, h = len(body[0]) * scale, (len(body) + len(a)) * scale
        lo, hi = floor[1] + w / 2, floor[2] - w / 2
        home = rng.uniform(lo, hi)
        chars.append(dict(name=name, w=w, h=h, lo=lo, hi=hi, home=home, x=home, y=floor[0], keys=[(0.0, home, floor[0])],
                          vis=[], dead_until=None, safe_until=0.0, seg_t=0.0, sx=home, sy=floor[0], line='floor',
                          segs=[(rng.uniform(0, 3), home, floor[0], 'floor')]))

    def arc(x0, y0, x, y):
        peak, secs = min(y0, y) - 28 - abs(x - x0) * .08, .45 + abs(x - x0) / 700
        return [(secs / 8, x0 + (x - x0) * k / 8, (1 - k / 8) ** 2 * y0 + 2 * (1 - k / 8) * k / 8 * peak + (k / 8) ** 2 * y, None)
                for k in range(1, 9)]

    def plan(c, t):
        """Next few segments (seconds, x, y, line-or-None-while-airborne) for one sprite."""
        cx, fy = c['sx'], c['sy']
        if t > T - 22:  # head home so the loop closes seamlessly
            segs = [] if c['line'] == 'floor' else arc(cx, fy, min(max(cx, c['lo']), c['hi']), floor[0])
            last = segs[-1][1] if segs else cx
            return segs + [(abs(c['home'] - last) / 55 + .01, c['home'], floor[0], 'floor'), (T, c['home'], floor[0], 'floor')]
        near = [p for p in platforms if p[3] != 'floor' and abs((p[1] + p[2]) / 2 - cx) < 320
                and fy - p[0] < 175 and abs(p[0] - fy) > 4 and p[0] - c['h'] > 16]  # reachable, head stays in frame
        top, left, right, line = rng.choice(near) if near and rng.random() < .85 else floor
        land = rng.uniform(left, right) if line != 'floor' else rng.uniform(c['lo'], c['hi'])
        segs = arc(cx, fy, land, top) + [(rng.uniform(.4, 1.6), land, top, line)]
        if right - left > 40:  # stroll along the word
            nx = min(max(rng.uniform(left, right), c['lo']), c['hi'])
            segs += [(abs(nx - land) / 55 + .01, nx, top, line), (rng.uniform(.2, 1.0), nx, top, line)]
        return segs

    for n in range(int(T / dt) + 1):
        t = n * dt
        if drive_at and t >= drive_at[0]:  # aim for the busiest line
            drive_at.pop(0)
            count = {l: sum(c['line'] == l and c['dead_until'] is None for c in chars) for l in roads}
            best = max(count.values())
            line = rng.choice([l for l in roads if count[l] == best] if best else roads)
            active = (t, line, min(p[0] for p in lines[line]))
            drives.append(active)
        car_x = -cw - 20 + speed * (t - active[0]) if active else None
        if car_x is not None and car_x > 1020: active = car_x = None
        for c in chars:
            if c['dead_until'] is not None:
                if t >= c['dead_until']:  # respawn on the floor, blinking like after a hit
                    x = rng.uniform(c['lo'], c['hi'])
                    c['keys'].append((t, x, floor[0]))
                    c['vis'] += [(t, 1), (t + .15, .2), (t + .3, 1), (t + .45, .2), (t + .6, 1), (t + .75, .2), (t + .9, 1)]
                    c.update(x=x, y=floor[0], sx=x, sy=floor[0], line='floor', seg_t=t, segs=[], dead_until=None, safe_until=t + 1.5)
                continue
            while not c['segs'] or t >= c['seg_t'] + c['segs'][0][0]:
                if c['segs']:
                    dur, ex, ey, line = c['segs'].pop(0)
                    c['seg_t'] += dur
                    c.update(sx=ex, sy=ey, line=line)
                    c['keys'].append((c['seg_t'], ex, ey))
                if not c['segs']: c['segs'] = plan(c, c['seg_t'])
            dur, ex, ey, line = c['segs'][0]
            f = (t - c['seg_t']) / dur
            c['x'], c['y'] = c['sx'] + (ex - c['sx']) * f, c['sy'] + (ey - c['sy']) * f
            c['line'] = line  # None while airborne: the car can't hit mid-jump
            if (car_x is not None and line == active[1] and t >= c['safe_until']
                    and car_x < c['x'] + c['w'] / 2 and car_x + cw > c['x'] - c['w'] / 2):
                c['keys'].append((t, c['x'], c['y']))
                c['vis'].append((t, 0))
                blasts.append((t, c['x'], c['y'] - c['h'] / 2))
                c.update(dead_until=t + 1.2, segs=[], line=None)

    css, out = [], []
    for i, c in enumerate(chars):
        keys = [k for k in c['keys'] if k[0] < T] + [(T, c['home'], floor[0])]
        frames = ''.join(f'{t / T * 100:.3f}%{{transform:translate({x - c["w"] / 2:.1f}px,{y - c["h"]:.1f}px)}}' for t, x, y in keys)
        css.append(f'.w{i}{{animation:w{i} {T}s linear infinite}}@keyframes w{i}{{{frames}}}'
                   f'.v{i}{{animation:v{i} {T}s linear infinite}}' + steps_css(f'v{i}', c['vis'], T, 1))
        out.append(f'<g class="w{i}" style="transform:translate({c["home"] - c["w"] / 2:.1f}px,{floor[0] - c["h"]}px)">'
                   f'<g class="v{i}">{sprite(c["name"], 0, c["h"], scale, rng.uniform(0, .36))}</g></g>')

    # Car: visible only while crossing; it slides back offscreen while hidden.
    cross = (1040 + cw) / speed
    ckeys = [(0.0, -cw - 20, floor[0] - ch)]
    for t0, _, y in drives: ckeys += [(t0, -cw - 20, y - ch), (t0 + cross, 1020, y - ch)]
    ckeys.append((T, -cw - 20, floor[0] - ch))
    cframes = ''.join(f'{t / T * 100:.3f}%{{transform:translate({x:.1f}px,{y:.1f}px)}}' for t, x, y in ckeys)
    css.append(f'.car{{opacity:0;animation:car {T}s linear infinite,carv {T}s linear infinite}}@keyframes car{{{cframes}}}'
               + steps_css('carv', [c for t0, _, _ in drives for c in ((t0, 1), (t0 + cross, 0))], T, 0)
               + '.bump{animation:bump .2s steps(1,end) infinite}@keyframes bump{50%{transform:translateY(-3px)}}')
    out.append(f'<g class="car"><g class="bump">{pixels(CAR[1], CAR[0], 3)}</g></g>')

    # Explosions: 8 frames, each a <use> that flashes on for one frame; animation-delay places it at the hit time.
    frames, fd = explosion_frames(), .09
    defs = ''.join(f'<g id="ex{k}">{pixels(rows, BLAST, 4)}</g>' for k, rows in enumerate(frames))
    for k in range(len(frames)):
        a, b = k * fd / T * 100, (k + 1) * fd / T * 100
        css.append(f'.e{k}{{opacity:0;animation:e{k} {T}s linear infinite}}'
                   f'@keyframes e{k}{{0%,{a:.3f}%{{opacity:0}}{a + .001:.3f}%,{b:.3f}%{{opacity:1}}{b + .001:.3f}%,100%{{opacity:0}}}}')
    for t, x, y in blasts:
        out.append(f'<g transform="translate({x - 32:.1f} {y - 32:.1f})">'
                   + ''.join(f'<use href="#ex{k}" class="e{k}" style="animation-delay:{t:.2f}s"/>' for k in range(len(frames))) + '</g>')
    print(f'{len(drives)} drives on {[d[1] for d in drives]}, {len(blasts)} explosions')
    return ''.join(css), f'<defs>{defs}</defs><g shape-rendering="crispEdges">{"".join(out)}</g>'


def typewriter(i, x, y, value, size, start, dur, cycle):
    """Cover the line with a black block that steps right one character at a time."""
    w, n = len(value) * size / 2, len(value)  # mono font: every glyph is half an em wide
    p0, p1 = start / cycle * 100, (start + dur) / cycle * 100
    css = (f'.tw{i}{{animation:tw{i} {cycle}s steps({n},end) infinite}}'
           f'@keyframes tw{i}{{0%,{p0:.2f}%{{transform:translateX(0)}}{p1:.2f}%,100%{{transform:translateX({w}px)}}}}')
    box = f'x="{x}" y="{y - size}" width="{w + 2}" height="{size * 1.3}"'
    return css, (f'<clipPath id="c{i}"><rect {box}/></clipPath>'
                 f'<g clip-path="url(#c{i})"><rect class="tw{i} cover" {box} fill="{BLACK}"/></g>')


WALK = ('.fa{animation:fa .36s infinite}.fb{opacity:0;animation:fb .36s infinite}'
        '@keyframes fa{0%,49.9%{opacity:1}50%,100%{opacity:0}}@keyframes fb{0%,49.9%{opacity:0}50%,100%{opacity:1}}')


def header():
    css = [font_css('mono', 'big'), WALK,
           'text{white-space:pre}.soul{animation:dodge 10s linear infinite}.white-bones{animation:whitewave 10s linear infinite}.blue-bone{animation:bluewave 10s linear infinite}'
           '.dodge-label{animation:dodgelabel 10s steps(1,end) infinite}.hold-label{animation:holdlabel 10s steps(1,end) infinite;opacity:0}'
           '.save{transform-box:fill-box;transform-origin:center;animation:save 3s steps(8,end) infinite}.spark{animation:spark 3s ease-out infinite}'
           '.star{animation:twinkle 4s steps(3,end) infinite}'
           '@keyframes dodge{0%,14%{transform:translate(0,-10px)}18%,24%{transform:translate(0,24px)}28%,46%{transform:translate(0,-10px)}50%,76%{transform:translate(0,0)}84%,92%{transform:translate(35px,0)}100%{transform:translate(0,-10px)}}'
           '@keyframes whitewave{0%{transform:translateX(0);opacity:1}46%{transform:translateX(-680px);opacity:1}47%,100%{transform:translateX(-680px);opacity:0}}'
           '@keyframes bluewave{0%,50%{transform:translateX(0);opacity:0}51%{transform:translateX(0);opacity:1}76%{transform:translateX(-285px);opacity:1}77%,100%{transform:translateX(-285px);opacity:0}}'
           '@keyframes dodgelabel{0%,50%{opacity:1}51%,76%{opacity:0}77%,100%{opacity:1}}@keyframes holdlabel{0%,50%{opacity:0}51%,76%{opacity:1}77%,100%{opacity:0}}'
           '@keyframes save{50%{transform:rotate(180deg) scale(.65)}100%{transform:rotate(360deg)}}'
           '@keyframes spark{0%{opacity:0;transform:translateY(0)}25%{opacity:1}100%{opacity:0;transform:translateY(-50px)}}@keyframes twinkle{50%{opacity:.2}}']
    tw_css, tw = typewriter(0, 40, 178, '* Stay determined. Keep building.', 32, .5, 2.2, 10)
    # (x, y, text, size, colour, font, line): each line is a level the sprites stand on and the car can drive along.
    words = [(40, 56, 'STING-RAIDER // AI · REINFORCEMENT LEARNING · SYSTEMS', 16, GRAY, 'mono', 'label'),
             (36, 130, 'ALI KHAN', 64, WHITE, 'big', 'title'),
             (40, 178, '* Stay determined. Keep building.', 32, YELLOW, 'mono', 'tagline'),
             (40, 222, '* Teaching machines to drive, grasp, and think.', 24, WHITE, 'mono', 'line1'),
             (40, 254, '* Making the results public, failures included.', 24, WHITE, 'mono', 'line2'),
             (40, 312, 'ALI', 24, WHITE, 'big', 'stats'), (150, 312, 'LV 27', 24, WHITE, 'big', 'stats'),
             (300, 312, 'HP', 16, WHITE, 'big', 'stats'), (468, 312, '99 / 99', 24, WHITE, 'big', 'stats'),
             (705, 82, '* BONE ENCOUNTER', 16, WHITE, 'mono', 'arena')]
    platforms = [(*p, line) for x, y, v, s, _, f, line in words for p in word_platforms(x, y, v, s, f)]
    platforms += [(290, 336, 448, 'stats'), (93, 705, 952, 'arena'), (424, 20, 980, 'floor')]  # HP bar, arena roof, floor
    roam_css, roam = scene(['kid', 'skeleton', 'tall_skeleton', 'goat_mom', 'hero', 'bruiser', 'prince'], platforms)
    css += [tw_css, roam_css]
    css.append('@media(prefers-reduced-motion:reduce){*{animation:none!important}.cover,.white-bones,.blue-bone,.hold-label{display:none}.fb{opacity:0}}')
    bone = 'M-4 0h6v2h4V0h6v6h-4v{h}h4v6H6v-2H2v2h-6v-6H0V6h-4z'
    bones = ''.join(f'<g transform="translate({x} {y})"><path d="{bone.format(h=h)}"/></g>'
                    for x, y, h in [(966, 98, 31), (966, 181, 59), (1116, 98, 66), (1116, 216, 24), (1266, 98, 31), (1266, 181, 59)])
    stars = ''.join(f'<path class="star" style="animation-delay:{d}s" d="M{x} {y}v8m-4 -4h8" stroke="{WHITE}"/>'
                    for x, y, d in [(630, 88, 2), (666, 140, 0), (560, 250, 1), (902, 40, 2), (600, 52, 1)])
    body = [
        f'<rect x="14" y="14" width="972" height="412" fill="none" stroke="{WHITE}" stroke-width="4"/>',
        *(text(*w[:6]) for w in words), tw,
        # Undertale-style battle status line.
        f'<rect x="336" y="290" width="112" height="24" fill="{RED}"/><rect x="336" y="290" width="112" height="24" fill="{YELLOW}"/>',
        # Soul arena.
        f'<defs><clipPath id="arena"><rect x="705" y="95" width="247" height="160"/></clipPath>'
        f'<path id="heart" d="{HEART}"/></defs>',
        f'<rect x="705" y="95" width="247" height="160" fill="{BLACK}" stroke="{WHITE}" stroke-width="4"/>',
        f'<g clip-path="url(#arena)" shape-rendering="crispEdges"><g class="white-bones" fill="{WHITE}">{bones}</g>'
        f'<g transform="translate(967 99)"><g class="blue-bone" fill="#14a9ff"><path d="{bone.format(h=142)}"/></g></g>'
        f'<g transform="translate(818 171)"><use class="soul" href="#heart" fill="{RED}"/></g></g>',
        text(752, 282, 'WHITE / DODGE', 16, WHITE, extra=' class="dodge-label"'),
        text(728, 282, 'BLUE / HOLD STILL', 16, '#14a9ff', extra=' class="hold-label"'),
        # SAVE point.
        f'<g transform="translate(930 300)"><path class="save" d="M0 -24h6v12h6v6h12v6H12v6H6v12H0V6h-6V0h-12v-6h12v-6H0z" fill="{YELLOW}"/></g>',
        f'<g class="spark" fill="{YELLOW}"><rect x="910" y="284" width="4" height="4"/><rect x="947" y="300" width="4" height="4"/><rect x="920" y="316" width="4" height="4"/></g>',
        stars,
        roam,
    ]
    return svg(1000, 440, 'Ali Khan — an Undertale-style battle screen: a red soul dodges bones while tiny pixel characters hop from word to word, until a dog in a toy car drives through and blows them up. Stay determined, keep building.',
               ''.join(body), ''.join(css))


ICONS = {
    'sword': ['........oo', '.......ooo', '......ooo.', '.....ooo..', '....ooo...', 'o..ooo....', '.oooo.....', '..oo......', '.o..o.....', 'o.........'],
    'paper': ['.oooooo...', '.o....oo..', '.o.oo.ooo.', '.o......o.', '.o.oooo.o.', '.o......o.', '.o.oooo.o.', '.o......o.', '.oooooooo.', '..........'],
    'bubble': ['.oooooooo.', 'o........o', 'o.oo.oo..o', 'o........o', 'o........o', '.oooooooo.', '..oo......', '.oo.......', 'o.........', '..........'],
    'mail': ['..........', 'oooooooooo', 'oo......oo', 'o.o....o.o', 'o..o..o..o', 'o...oo...o', 'o........o', 'oooooooooo', '..........', '..........'],
}


def nav(label, icon, selected=False):
    color = YELLOW if selected else ORANGE
    mark = (f'<use href="#h" transform="translate(28 30) scale(1.2)" fill="{RED}"/>' if selected
            else pixels(ICONS[icon], {'o': color}, 3, 13, 15))
    w = width(label, 32, 'bold')
    body = (f'<defs><path id="h" d="{HEART}"/></defs>'
            f'<rect x="4" y="4" width="232" height="52" fill="none" stroke="{color}" stroke-width="4"/>{mark}'
            + text(round(50 + (182 - w) / 2), 42, label, 32, color, 'bold'))
    return svg(240, 60, label, body, font_css('bold'))


def intro():
    lines = [("* I'm Ali — CS @ VIT Vellore '27.", WHITE),
             ('* I build AI systems that have to survive outside a notebook.', WHITE),
             ('* (Open to SWE / AI engineering internships.)', GRAY)]
    css, body, t = [font_css('mono'), 'text{white-space:pre}'], [], .4
    for i, (line, color) in enumerate(lines):
        y = 66 + i * 40
        c, cover = typewriter(i, 44, y, line, 24, t, len(line) / 30, 14)
        css.append(c); body += [text(44, y, line, 24, color), cover]
        t += len(line) / 30 + .4
    css.append('@media(prefers-reduced-motion:reduce){.cover{display:none}}')
    box = f'<rect x="16" y="16" width="968" height="156" fill="none" stroke="{WHITE}" stroke-width="6"/>'
    return svg(1000, 240, "About Ali: CS at VIT Vellore '27, builds AI systems that survive outside a notebook, open to SWE / AI engineering internships. Selected builds below.",
               box + ''.join(body) + text(20, 224, '* SELECTED BUILDS', 32, YELLOW), ''.join(css))


def card(title, lines, stack, status, accent):
    body = (f'<rect x="6" y="6" width="468" height="192" fill="none" stroke="{WHITE}" stroke-width="4"/>'
            f'<rect x="6" y="6" width="468" height="8" fill="{accent}"/>'
            f'<path d="{HEART}" transform="translate(34 46) scale(.9)" fill="{RED}"/>'
            + text(56, 56, title, 32, WHITE, 'bold')
            + ''.join(text(26, 96 + i * 26, line, 20) for i, line in enumerate(lines))
            + text(26, 152, stack, 20, accent) + text(26, 182, status + ' >>', 16, GRAY))
    label = f'{title}: {" ".join(lines)} {status}. {stack}'
    return svg(480, 204, label, body, font_css('bold', 'mono') + 'text{white-space:pre}')


def main():
    files = {
        'header.svg': header(),
        'nav-portfolio.svg': nav('PORTFOLIO', 'sword', selected=True),
        'nav-resume.svg': nav('RÉSUMÉ', 'paper'),
        'nav-linkedin.svg': nav('LINKEDIN', 'bubble'),
        'nav-email.svg': nav('EMAIL', 'mail'),
        'intro.svg': intro(),
        'build-roleatlas.svg': card('RoleAtlas', ['Qualification-first job discovery', 'with a Rust crawler fleet.'],
                                    'TypeScript / Rust / PostgreSQL', 'PUBLIC REPOSITORY', KRIS),
        'build-aegisflow.svg': card('AegisFlow', ['Network intrusion detection,', 'with public evaluation results.'],
                                    'Python / PyTorch / Suricata', 'PUBLIC REPOSITORY', SUSIE),
        'build-plaid.svg': card('Plaid', ['Researching N64 ROM-to-native', 'recompilation. Discovery comes first.'],
                                'Rust / Python / MIPS', 'IN PROGRESS / PUBLIC REPOSITORY', RALSEI),
        'build-arm.svg': card('6-DOF Arm RL', ['Teaching a UR10e to reach,', 'grasp, lift, and place.'],
                              'Isaac Lab / PyTorch / PPO', 'PRIVATE REPO / PUBLIC WRITE-UP', NOELLE),
    }
    for name, content in files.items():
        (OUT / name).write_text(content, encoding='utf-8')
    print('wrote', ', '.join(files))


if __name__ == '__main__':
    main()
