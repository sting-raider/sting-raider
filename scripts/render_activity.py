"""Generate profile activity SVG from GitHub's public calendar and PR search."""
import datetime as dt
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import urllib.parse
import urllib.request

USER = os.environ.get('PROFILE_USER', 'sting-raider')
def fetch(url):
    headers = {'User-Agent': 'profile-activity-generator', 'Accept': 'application/vnd.github+json'}
    if url.startswith('https://api.github.com/') and os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=45) as response:
        return response.read().decode()

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}
        self.target = None
        self.buffer = ''
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and 'data-date' in a:
            self.days[a['id']] = {'date': a['data-date'], 'level': int(a['data-level'])}
        if tag == 'tool-tip' and a.get('for') in self.days:
            self.target = a['for']
            self.buffer = ''
    def handle_data(self, data):
        if self.target: self.buffer += data
    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.target:
            match = re.match(r'([\d,]+) contribution', self.buffer)
            if not match and not self.buffer.startswith('No contributions'):
                raise ValueError('Unrecognized calendar tooltip')
            self.days[self.target]['count'] = int(match[1].replace(',', '')) if match else 0
            self.target = None

def render():
    raw = fetch(f'https://github.com/users/{USER}/contributions')
    calendar = Calendar()
    calendar.feed(raw)
    days = sorted(calendar.days.values(), key=lambda d: d['date'])
    if len(days) < 350 or any('count' not in d for d in days):
        raise ValueError('Incomplete GitHub contribution calendar; keeping previous asset')
    summary = re.search(r'([\d,]+)\s+contributions\s+in the last year', raw)
    if not summary: raise ValueError('GitHub annual total missing')
    def prs(extra):
        q = urllib.parse.quote(f'is:pr author:{USER} {extra}')
        result = json.loads(fetch(f'https://api.github.com/search/issues?q={q}&per_page=1'))
        if result.get('incomplete_results'): raise ValueError('Incomplete PR results')
        return result['total_count']
    pr_total, merged = prs(''), prs('is:merged')
    recent = days[-364:]
    weeks = [sum(d['count'] for d in recent[i:i+7]) for i in range(0,364,7)]
    colors = ['#19191f','#38305f','#6655a4','#a383e6','#ffda6a']
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="630" viewBox="0 0 1000 630" role="img" aria-labelledby="title desc"><title id="title">Contribution SAVE file</title><desc id="desc">GitHub contribution calendar, weekly totals, and all-time public authored pull requests.</desc><style>text{font-family:Courier New,monospace}</style><rect width="1000" height="630" fill="#08080d"/><rect x="12" y="12" width="976" height="606" fill="none" stroke="#ffffff" stroke-width="2"/>']
    def text(x,y,value,size=17,color='#eeeeee'):
        s.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}">{html.escape(str(value))}</text>')
    text(40,50,'* SAVE FILE / CONTRIBUTION HISTORY',22,'#ffda6a')
    for x,value,label in [(40,summary[1],'CONTRIBUTIONS / LAST YEAR'),(430,pr_total,'PUBLIC PRs / ALL TIME'),(755,merged,'MERGED / ALL TIME')]:
        text(x,105,value,40,'#ffffff'); text(x,135,label,14,'#b9a8e0')
    start = dt.date.fromisoformat(days[0]['date'])
    for d in days:
        date = dt.date.fromisoformat(d['date'])
        col = (date-start).days//7; row=(date.weekday()+1)%7
        s.append(f'<rect x="{55+col*17}" y="{185+row*17}" width="13" height="13" fill="{colors[d["level"]]}"><title>{d["date"]}: {d["count"]} contributions</title></rect>')
    text(55,172,days[0]['date'],13,'#aaa5b7'); text(807,172,days[-1]['date'],13,'#aaa5b7')
    text(55,334,'LESS',12,'#aaa5b7')
    for i,c in enumerate(colors): s.append(f'<rect x="{103+i*20}" y="324" width="13" height="13" fill="{c}"/>')
    text(212,334,'MORE',12,'#aaa5b7')
    text(55,378,'* WEEKLY ACTIVITY / LAST 52 WEEKS',18,'#ffda6a')
    peak = max(weeks) or 1
    for i,value in enumerate(weeks):
        h=120*value/peak
        s.append(f'<rect x="{55+i*17}" y="{520-h:.1f}" width="12" height="{max(h,1):.1f}" fill="{colors[4] if value==peak else colors[3]}"><title>Week {i+1}: {value} contributions</title></rect>')
    s.append('<path d="M55 522H944" stroke="#484254"/>')
    text(55,548,f'Peak week: {peak:,} contributions',14,'#b9a8e0')
    text(55,580,'Source: public GitHub calendar + PR search. Contributions include more than commits.',13,'#aaa5b7')
    text(55,600,'Updated '+dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')+' / refreshes daily',13,'#aaa5b7')
    s.append('</svg>')
    dest=Path('assets/activity.svg'); dest.parent.mkdir(exist_ok=True)
    dest.write_text(''.join(s),encoding='utf-8')
    print(f'Annual contributions: {summary[1]}; authored PRs: {pr_total}; merged: {merged}')

if __name__ == '__main__': render()
