"""CSS for each output format."""

BASE_CSS = """
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; }
body { font-family: Merriweather, Georgia, 'Times New Roman', serif; color: #111; }
.page { position: relative; overflow: hidden; page-break-after: always; break-after: page; background: #fff; }
.page:last-child { page-break-after: auto; break-after: auto; }
.img { display: block; object-fit: cover; }
.num { position: absolute; left: 0; right: 0; text-align: center; font-family: Helvetica, Arial, sans-serif; }
.wm-small { position: absolute; }
.wm-big { position: absolute; left: 50%; top: 50%; width: 82%; transform: translate(-50%, -50%); opacity: .28; z-index: 0; }
.center { text-align: center; position: relative; z-index: 1; }
.center.mid { position: absolute; left: 0; right: 0; top: 50%; transform: translateY(-50%); padding: 0 12%; }
.center p { margin: 0 0 .9em; line-height: 1.5; }
.center p.verse { margin-bottom: 1.1em; }
.center h1 { font-weight: 700; line-height: 1.2; margin: 0 0 .6em; }
.body strong { font-weight: 700; }
.moral-head { font-weight: 700; line-height: 1.1; }
.back-hook { font-weight: 700; line-height: 1.3; }
.cover-full { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.frame { border: 0.5mm dashed #b9a97f; border-radius: 4mm; }
"""

A4_CSS = """
@page { size: 210mm 297mm; margin: 0; }
.page { width: 210mm; height: 297mm; padding: 20mm 21mm 0 21mm; }
.img { width: 100mm; height: 100mm; margin: 0 auto 9mm; border-radius: 6mm; }
.body { font-size: 14.5pt; line-height: 1.55; }
.body p { margin: 0 0 4.2mm; }
.body p.verse { margin-bottom: 7mm; }
.num { bottom: 14mm; font-size: 13pt; }
.wm-small { width: 44mm; right: 14mm; bottom: 18mm; }
.title-big { font-size: 40pt; } .title-med { font-size: 24pt; }
.frontmatter { font-size: 15pt; } .legal { font-size: 12pt; }
.moral-head { font-size: 30pt; margin: 26mm 0 12mm; }
.extra .moral-head { margin-top: 10mm; }
.back-hook { font-size: 24pt; } .back-body { font-size: 14pt; }
.frame { height: 95mm; margin-bottom: 8mm; }
"""

PRINT_CSS = """
@page { size: 8.625in 8.75in; margin: 0; }
.page { width: 8.625in; height: 8.75in; padding: 0.625in 0.5in 0 0.5in; }
.page.odd { padding-left: 0.62in; padding-right: 0.625in; }
.page.even { padding-left: 0.625in; padding-right: 0.62in; }
.img { width: 4.0in; height: 4.0in; margin: 0 auto 0.22in; border-radius: 0.16in; }
.body { font-size: 12.5pt; line-height: 1.5; }
.body p { margin: 0 0 0.1in; }
.body p.verse { margin-bottom: 0.17in; }
.num { bottom: 0.5in; font-size: 11pt; }
.wm-small { width: 1.3in; right: 0.6in; bottom: 0.55in; }
.title-big { font-size: 34pt; } .title-med { font-size: 20pt; }
.frontmatter { font-size: 13pt; } .legal { font-size: 10.5pt; }
.moral-head { font-size: 26pt; margin: 0.9in 0 0.4in; }
.extra .moral-head { margin-top: 0.2in; }
.back-hook { font-size: 20pt; } .back-body { font-size: 12pt; }
.frame { height: 3.3in; margin-bottom: 0.2in; }
"""
