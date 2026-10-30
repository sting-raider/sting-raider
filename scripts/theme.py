"""Shared Undertale/Deltarune look for every profile SVG: palette, embedded pixel fonts, text."""
import base64
import html
from pathlib import Path

FONTS = Path(__file__).parent / 'fonts'
BLACK, WHITE, GRAY, YELLOW, ORANGE, RED = '#000000', '#ffffff', '#9a9a9a', '#ffff00', '#ff8c1a', '#ff0000'
# Deltarune party colours, used as per-card accents.
KRIS, SUSIE, RALSEI, NOELLE = '#00a2e8', '#ea79c8', '#b5e61d', '#ffd84a'
# Pixel Operator (CC0, by Jayvee Enaguas) subset to ASCII + a few symbols; see fonts/LICENSE-PixelOperator.txt.
# README images can't fetch web fonts, so each SVG carries the faces it uses as data URIs.
FAMILIES = {'mono': 'PixelOperatorMono', 'bold': 'PixelOperator-Bold', 'big': 'PixelOperator8-Bold'}


def font_css(*kinds):
    return ''.join(
        f'@font-face{{font-family:{k};src:url(data:font/ttf;base64,'
        f'{base64.b64encode((FONTS / (FAMILIES[k] + ".ttf")).read_bytes()).decode()})}}'
        for k in kinds)


def text(x, y, value, size=24, color=WHITE, font='mono', extra=''):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}"{extra}>'
            f'{html.escape(str(value))}</text>')
