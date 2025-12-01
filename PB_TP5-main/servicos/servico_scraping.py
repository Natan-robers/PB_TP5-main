import requests, re, pandas as pd
from bs4 import BeautifulSoup
from utilidades.arquivos import caminho_produtos_csv, caminho_produtos_url

def extrair_produtos_flexivel(html_text):
    soup = BeautifulSoup(html_text, "html.parser")

    produtos = []
    next_id = 1
    cards = soup.find_all("div", class_="product-card")

    if cards:
        for idx, card in enumerate(cards, 1):
            try:
                titulo = card.find("h5", class_="card-title")
                nome = titulo.get_text(strip=True) if titulo else f"Produto {idx}"

                preco_elem = card.find("p", class_="card-price")
                preco_raw = preco_elem.get("data-preco", "R$ 0,00") if preco_elem else "R$ 0,00"
                preco = float(preco_raw.replace("R$", "").strip().replace(",", "."))

                qtd_elem = card.find("p", attrs={"data-qtd": True})
                quantidade = int(qtd_elem.get("data-qtd", "0")) if qtd_elem else 0

                produtos.append({
                    "id": next_id,
                    "nome": nome,
                    "quantidade": quantidade,
                    "preco": preco
                })
                next_id += 1

            except:
                continue

        if produtos:
            return produtos

    elementos_com_preco = soup.find_all(string=re.compile(r'R\$\s*[\d\.,]+'))

    for elemento_preco in elementos_com_preco:
        parent = elemento_preco.parent
        if parent:
            texto_completo = parent.get_text(separator=" ", strip=True)
            preco_match = re.search(r"R\$\s*([\d\.,]+)", texto_completo)
            if not preco_match:
                continue

            preco = float(preco_match.group(1).replace('.', '').replace(',', '.'))
            qtd_match = re.search(r"(\d+)\s*(?:un|unidade)", texto_completo, re.IGNORECASE)
            quantidade = int(qtd_match.group(1)) if qtd_match else 0

            texto_sem_preco = re.sub(r'R\$\s*[\d\.,]+', '', texto_completo)
            palavras = re.findall(r'[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ\s\-]{2,}', texto_sem_preco)

            nomes_validos = [p.strip() for p in palavras if len(p.strip()) > 2]

            if nomes_validos:
                produtos.append({
                    "id": next_id,
                    "nome": nomes_validos[0],
                    "quantidade": quantidade,
                    "preco": preco
                })
                next_id += 1

    vistos = set()
    result = []
    for p in produtos:
        chave = (p["nome"].lower(), p["preco"])
        if chave not in vistos:
            vistos.add(chave)
            result.append(p)

    return result


def executar_scraping_e_gerar_csv():
    url = caminho_produtos_url()
    print(f"Buscando produtos em: {url}")

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Erro ao acessar a página: {e}")
        return pd.DataFrame()

    lista = extrair_produtos_flexivel(resp.text)

    df = pd.DataFrame(lista)
    df.to_csv(caminho_produtos_csv(), index=False)

    print(f"{len(df)} produtos escritos em {caminho_produtos_csv()}")
    return df


