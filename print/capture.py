import json
import time
from pathlib import Path

import urllib.request
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
API = "http://localhost:8000"
FRONT = "http://localhost:8080"

EVENT = {
    "source": "formulario-web",
    "type": "solicitacao",
    "value": "segunda via de boleto",
    "created_at": "2026-06-01",
}


def post_event_api():
    """Garante que existe um evento + demanda gerada antes dos screenshots."""
    req = urllib.request.Request(
        f"{API}/event",
        data=json.dumps(EVENT).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())
    print("POST /event ->", body.get("message"))
    return body


def main():
    post_event_api()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        # ---- Swagger: POST /event executado (evidencias 5 e 6) ----
        page.goto(f"{API}/docs", wait_until="networkidle")
        page.wait_for_timeout(1500)
        # expandir o bloco POST /event
        page.click("#operations-default-receive_event_event_post .opblock-summary")
        page.wait_for_timeout(600)
        page.click("#operations-default-receive_event_event_post button.try-out__btn")
        page.wait_for_timeout(400)
        textarea = page.locator(
            "#operations-default-receive_event_event_post textarea.body-param__text"
        )
        textarea.fill(json.dumps(EVENT, indent=2, ensure_ascii=False))
        page.screenshot(path=str(OUT / "05_post_event_rota.png"), full_page=True)
        page.click("#operations-default-receive_event_event_post button.execute")
        page.wait_for_timeout(1800)
        page.screenshot(path=str(OUT / "06_evento_enviado.png"), full_page=True)

        # ---- Frontend com dados carregados ----
        page.goto(FRONT, wait_until="networkidle")
        page.click("#load-demands-btn")
        page.wait_for_timeout(1500)
        page.screenshot(path=str(OUT / "01_frontend.png"), full_page=True)

        # recortes por secao
        cards = page.locator("section.card")
        # 0=cadastrar, 1=resumo, 2=demandas, 3=eventos
        cards.nth(1).screenshot(path=str(OUT / "02_painel_resumo.png"))
        cards.nth(2).screenshot(path=str(OUT / "03_lista_demandas.png"))
        cards.nth(3).screenshot(path=str(OUT / "04_lista_eventos.png"))
        # demanda gerada automaticamente = ultima demanda da lista
        page.locator("#demand-list li").last.screenshot(
            path=str(OUT / "07_demanda_gerada.png")
        )

        browser.close()
    print("Screenshots salvos em", OUT)


if __name__ == "__main__":
    main()
