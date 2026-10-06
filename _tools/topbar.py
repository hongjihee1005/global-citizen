#!/usr/bin/env python3
"""모든 페이지 맨 위에 '세계시민교육' 띠를 고정하고, 누르면 첫 화면(index.html)으로 가게 합니다.

    python3 _tools/topbar.py      # 저장소 루트에서. 여러 번 실행해도 안전합니다.

hong_teacher에서 파일을 다시 복사해 왔으면 이 스크립트를 다시 돌리세요.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = '<!--gc-top-->', '<!--/gc-top-->'
CSS_ID = 'gc-top-css'

CSS = '''<style id="gc-top-css">
:root{--gct-bg:#FFF9F3;--gct-line:#EFE3D6;--gct-ink:#2A221C;--gct-tile:#FBE6DC;--gct-ico:#C0704A;--gct-hover:#FBEFE6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--gct-bg:#211B17;--gct-line:#3A302A;--gct-ink:#F4ECE4;--gct-tile:#3B2A22;--gct-ico:#F0A47E;--gct-hover:#2C241F}}
:root[data-theme="dark"]{--gct-bg:#211B17;--gct-line:#3A302A;--gct-ink:#F4ECE4;--gct-tile:#3B2A22;--gct-ico:#F0A47E;--gct-hover:#2C241F}
#gc-top{position:sticky;top:0;z-index:90;display:flex;align-items:center;min-height:64px;padding:8px max(16px,env(safe-area-inset-left));
 background:var(--gct-bg);border-bottom:1px solid var(--gct-line);box-sizing:border-box;margin:0}
#gc-top a{display:inline-flex;align-items:center;gap:14px;padding:4px 10px 4px 4px;border-radius:16px;text-decoration:none!important;color:var(--gct-ink)!important;
 font-family:"Pretendard Variable",Pretendard,system-ui,-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;font-weight:800;font-size:clamp(22px,2.4vw,28px);
 letter-spacing:-.02em;line-height:1.2;word-break:keep-all}
#gc-top a:hover{background:var(--gct-hover)}
#gc-top a:focus-visible{outline:3px solid var(--gct-ico);outline-offset:2px}
#gc-top .gct-ico{display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:15px;background:var(--gct-tile);color:var(--gct-ico);flex:none}
#gc-top .gct-ico svg{width:24px;height:24px}
html.gc-full #gc-top,body:has(#slides:not([hidden])) #gc-top{display:none}
@media print{#gc-top{display:none!important}}
</style>'''

SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
       '<circle cx="12" cy="12" r="8.4"/><path d="M3.6 12h16.8M12 3.6c2.3 2.3 3.4 5.1 3.4 8.4s-1.1 6.1-3.4 8.4c-2.3-2.3-3.4-5.1-3.4-8.4S9.7 5.9 12 3.6Z"/></svg>')

# 전체 화면(슬라이드 등)일 때는 띠를 숨김
JS = "<script>document.addEventListener('fullscreenchange',function(){document.documentElement.classList.toggle('gc-full',!!document.fullscreenElement)})</script>"


def bar(href):
    return (f'{START}<div id="gc-top"><a href="{href}" title="첫 화면으로 가요">'
            f'<span class="gct-ico">{SVG}</span><span>세계시민교육</span></a></div>{JS}{END}')


def main():
    n = 0
    for f in sorted(glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)):
        rel = os.path.relpath(f, ROOT)
        if rel.startswith('_') or rel == os.path.join('project', 'index.html'):
            continue  # project/index.html은 첫 화면으로 넘기는 안내 페이지
        s = open(f, encoding='utf-8').read()
        o = s
        depth = rel.count(os.sep)
        href = '../' * depth + 'index.html'
        s = re.sub(re.escape(START) + '.*?' + re.escape(END), '', s, flags=re.S)
        s = re.sub(r'<style id="' + CSS_ID + r'">.*?</style>', '', s, flags=re.S)
        s = s.replace('</head>', CSS + '</head>', 1)
        s = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + bar(href), s, count=1)
        if rel == 'index.html':
            # 첫 화면은 띠가 제목을 대신함
            s = re.sub(r'<h1><span class="h-ico" aria-hidden="true">🌏</span>세계시민교육</h1>\n?', '', s)
        if s != o:
            open(f, 'w', encoding='utf-8').write(s)
            n += 1
    print('고친 파일', n)


if __name__ == '__main__':
    main()
