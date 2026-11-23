# Usage: python3 course/uroki/make-konspekt-pdf.py course/uroki/urok-02.md
# Turns a lesson plan (Markdown) into an A4 PDF for reading on iPad. Simple styles only, so Apple apps render it correctly.
import sys, subprocess, markdown, pathlib, re
src = pathlib.Path(sys.argv[1])
md = src.read_text()
md = md.replace('- [ ] ', '- ☐ ')
# Python-Markdown needs a blank line before a list that follows a paragraph line
lines, out = md.split('\n'), []
is_item = lambda l: bool(re.match(r'\s*([-*]|\d+\.)\s', l))
for i, l in enumerate(lines):
    if i and is_item(l) and lines[i-1].strip() and not is_item(lines[i-1]) and not lines[i-1].startswith(('|', '>', '#')) and not l.startswith(' '):
        out.append('')
    out.append(l)
md = '\n'.join(out)
html = markdown.markdown(md, extensions=['tables', 'sane_lists'])
page = f"""<!doctype html><meta charset="utf-8"><title>{src.stem}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=PT+Sans:wght@400;700&family=Oswald:wght@600&display=swap">
<style>
@page{{size:A4;margin:16mm 15mm}}
body{{font:400 10.5pt/1.5 "PT Sans",Arial,sans-serif;color:#151515}}
h1{{font:600 24pt/1.1 Oswald,Arial,sans-serif;text-transform:uppercase;color:#ff6a13;margin:0 0 4pt}}
h2{{font:600 15pt/1.2 Oswald,Arial,sans-serif;text-transform:uppercase;color:#1f86e0;margin:16pt 0 5pt;break-after:avoid}}
h3{{font:700 11.5pt/1.3 "PT Sans",Arial,sans-serif;margin:11pt 0 3pt;break-after:avoid}}
p,li{{margin:3pt 0}} ul,ol{{padding-left:16pt;margin:3pt 0}}
blockquote{{margin:6pt 0;padding:5pt 9pt;background:#eef6fd;border-left:3pt solid #1f86e0}}
blockquote p{{margin:0}}
table{{border-collapse:collapse;width:100%;margin:5pt 0;font-size:9.5pt;break-inside:auto}}
th{{background:#1f86e0;color:#fff;text-align:left;padding:4pt 6pt}}
td:first-child{{white-space:nowrap}}
td{{border-bottom:.5pt solid #cfdceb;padding:4pt 6pt;vertical-align:top}}
tr{{break-inside:avoid}}
hr{{border:0;border-top:.6pt solid #d8d8d8;margin:10pt 0}}
strong{{font-weight:700}} code{{font-family:inherit;background:#f1f1f1;padding:0 2pt}}
</style>{html}"""
tmp = src.with_suffix('.tmp.html'); tmp.write_text(page)
out = src.with_suffix('.pdf')
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{tmp.resolve()}');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
await p.pdf({{path:'{out.resolve()}',format:'A4',printBackground:true,margin:{{top:'16mm',bottom:'16mm',left:'15mm',right:'15mm'}}}});await b.close();}})();"""
subprocess.run(['node', '-e', js], check=True)
tmp.unlink(); print(out)
