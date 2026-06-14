import base64
import html as html_mod
import subprocess
from datetime import date
from pathlib import Path

DATE = date.today().strftime("%d/%m/%Y")

import markdown
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
OUT = Path(__file__).parent

MD_CSS = """
body{font-family:Segoe UI,Arial,sans-serif;max-width:820px;margin:0 auto;padding:32px;color:#1b1f24;line-height:1.55}
h1{font-size:26px;border-bottom:2px solid #2563eb;padding-bottom:8px}
h2{font-size:20px;margin-top:24px;color:#1d4ed8}
h3{font-size:16px}
code{background:#eef2f7;padding:2px 5px;border-radius:4px;font-family:Consolas,monospace}
pre{background:#0f172a;color:#e2e8f0;padding:14px;border-radius:8px;overflow:auto}
pre code{background:none;color:inherit}
ul{margin:6px 0}
"""

TERM_CSS = """
body{margin:0;background:#0c0c0c}
pre{font-family:Consolas,'Courier New',monospace;font-size:13px;color:#d4d4d4;
background:#0c0c0c;padding:22px;margin:0;white-space:pre-wrap;line-height:1.4}
.p{color:#4ec9b0}
"""


def md_to_html(md_path):
    text = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["fenced_code", "tables"])
    return f"<html><head><meta charset='utf-8'><style>{MD_CSS}</style></head><body>{body}</body></html>"


def term_to_html(text, prompt_line=None):
    safe = html_mod.escape(text)
    head = f"<span class='p'>{html_mod.escape(prompt_line)}</span>\n" if prompt_line else ""
    return f"<html><head><meta charset='utf-8'><style>{TERM_CSS}</style></head><body><pre>{head}{safe}</pre></body></html>"


def shot(page, html, path, width=900):
    page.set_viewport_size({"width": width, "height": 700})
    page.set_content(html, wait_until="networkidle")
    page.wait_for_timeout(300)
    page.screenshot(path=str(path), full_page=True)
    print("ok", path.name)


def b64(path):
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


EVID = [
    ("01_frontend.png", "frontend personalizado"),
    ("02_painel_resumo.png", "painel resumo"),
    ("03_lista_demandas.png", "lista de demandas"),
    ("04_lista_eventos.png", "lista de eventos"),
    ("05_post_event_rota.png", "rota POST /event"),
    ("06_evento_enviado.png", "evento enviado"),
    ("07_demanda_gerada.png", "demanda gerada automaticamente"),
    ("08_readme.png", "README atualizado"),
    ("09_architecture.png", "ARCHITECTURE.md atualizado"),
    ("10_historico_git.png", "historico Git"),
    ("11_terminal.png", "terminal executando: docker compose up --build"),
]

REPORT_CSS = """
@page{margin:16mm 15mm}
*{box-sizing:border-box}
body{font-family:Segoe UI,Arial,sans-serif;color:#1e293b;margin:0}
.head{background:#0f2a5e;color:#fff;border-radius:12px;padding:26px 28px;margin-bottom:8px}
.head .tag{font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#9bbcff}
.head h1{margin:6px 0 14px;font-size:26px;font-weight:700}
.head .meta{font-size:13px;line-height:1.85;color:#dbe6ff}
.head .meta b{color:#fff}
.intro{font-size:12.5px;color:#64748b;margin:14px 2px 0;line-height:1.5}
h2.sec{font-size:19px;color:#0f2a5e;margin:30px 2px 16px;
border-left:4px solid #2563eb;padding-left:10px}
.evid{page-break-inside:avoid;margin-bottom:22px}
.evid .cap{display:flex;align-items:center;gap:10px;margin:0 0 8px}
.evid .n{display:inline-flex;align-items:center;justify-content:center;
min-width:26px;height:26px;background:#2563eb;color:#fff;border-radius:50%;
font-size:13px;font-weight:700}
.evid h3{font-size:14.5px;margin:0;color:#0f172a;font-weight:600}
.evid .frame{border:1px solid #e2e8f0;border-radius:10px;padding:8px;background:#f8fafc;
box-shadow:0 1px 3px rgba(15,42,94,.08);text-align:center}
.evid img{max-width:100%;max-height:225mm;width:auto;height:auto;
display:inline-block;border-radius:6px}
.foot{margin-top:24px;padding-top:10px;border-top:1px solid #e2e8f0;
font-size:11px;color:#94a3b8;text-align:center}
"""


def build_report():
    rows = []
    for fname, label in EVID:
        p = OUT / fname
        if p.exists():
            img = f"<img src='{b64(p)}'>"
        else:
            img = "<div style='padding:30px;border:1px dashed #cbd5e1;color:#94a3b8;text-align:center'>print pendente</div>"
        n = label  # already textual
        idx = EVID.index((fname, label)) + 1
        rows.append(
            f"<div class='evid'><div class='cap'><span class='n'>{idx}</span>"
            f"<h3>{label}</h3></div><div class='frame'>{img}</div></div>"
        )
    return f"""<html><head><meta charset='utf-8'><style>{REPORT_CSS}</style></head><body>
<div class='head'>
<div class='tag'>Projeto de Extens&atilde;o em Software Full Stack &middot; 2026/1</div>
<h1>Relat&oacute;rio de Evid&ecirc;ncias &mdash; Etapa 3</h1>
<div class='meta'>
<b>Sistema:</b> Controle de Atendimentos (Painel de Demandas e A&ccedil;&otilde;es orientado a eventos)<br>
<b>Dom&iacute;nio:</b> Atendimento<br>
<b>Integrante:</b> Marcos Moura Guedes &nbsp;&middot;&nbsp; <b>Matr&iacute;cula:</b> 2019200067
</div>
</div>
<p class='intro'>Sistema evolu&iacute;do para arquitetura orientada a eventos e especializado para o
dom&iacute;nio de atendimento. As capturas abaixo comprovam o funcionamento completo do fluxo
Evento &rarr; API &rarr; Demanda, al&eacute;m da documenta&ccedil;&atilde;o e do versionamento.</p>
<h2 class='sec'>Evid&ecirc;ncias</h2>
{''.join(rows)}
<div class='foot'>Controle de Atendimentos &middot; Etapa 3 &middot; gerado em {DATE}</div>
<!-- rodape -->
</body></html>"""


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        shot(page, md_to_html(ROOT / "README.md"), OUT / "08_readme.png", 820)
        shot(page, md_to_html(ROOT / "ARCHITECTURE.md"), OUT / "09_architecture.png", 820)

        gitlog = (OUT / "_gitlog.txt").read_text(encoding="utf-8")
        shot(page, term_to_html(gitlog, "$ git log --oneline"), OUT / "10_historico_git.png", 900)

        term = (OUT / "_terminal.txt").read_text(encoding="utf-8")
        shot(page, term_to_html(term, "$ docker compose up --build"), OUT / "11_terminal.png", 900)

        # relatorio final
        report = build_report()
        page.set_content(report, wait_until="networkidle")
        page.wait_for_timeout(400)
        page.pdf(path=str(OUT / "RELATORIO_Etapa3.pdf"), format="A4", print_background=True)
        print("PDF gerado: RELATORIO_Etapa3.pdf")
        browser.close()


if __name__ == "__main__":
    main()
