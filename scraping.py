import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin
import time  # Para adicionar delay

def buscar_produtos(termo, limite=10, salvar_csv=False):
    termo_formatado = termo.replace(" ", "-")
    url = f"https://lista.mercadolivre.com.br/{termo_formatado}"

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Levanta erro se status não for 200
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

    soup = BeautifulSoup(response.text, "html.parser")

    produtos_html = soup.select("div.ui-search-result__wrapper")[:limite]

    produtos = []
    for p in produtos_html:
        try:
            # Tenta pegar o nome do produto
            nome_tag = p.select_one("h2.ui-search-item__title") or p.select_one("h3.poly-component__title") or p.select_one("a.poly-component__title")
            preco_tag = p.select_one("span.andes-money-amount__fraction")
            centavos_tag = p.select_one("span.andes-money-amount__cents")  # Para centavos
            link_tag = p.select_one("a.ui-search-link") or p.find("a", href=True)

            nome = nome_tag.get_text(strip=True) if nome_tag else "N/A"
            
            # Preço completo (inteiro + centavos)
            preco_inteiro = preco_tag.get_text(strip=True) if preco_tag else "0"
            centavos = centavos_tag.get_text(strip=True) if centavos_tag else "00"
            preco = f"{preco_inteiro},{centavos}" if preco_inteiro != "0" else "N/A"
            
             # Link absoluto e completo
            link_relativo = link_tag["href"] if link_tag else ""
            link = urljoin(url, link_relativo) if link_relativo else "N/A"
            # Logging temporário para depurar (remova depois)
            print(f"Link extraído: {link_relativo} -> {link}")
            # Verifica se é um link válido do Mercado Livre (não truncado)
            if not link.startswith("https://www.mercadolivre.com.br") or len(link) < 50:  # Links válidos são longos
                link = "N/A"

            produtos.append({
                "Nome": nome,
                "Preço": preco,
                "Link": link
            })
        except Exception as e:
            print(f"Erro ao extrair produto: {e}")
            continue  # Pula para o próximo

        # Delay pequeno para evitar sobrecarga (1 segundo entre produtos)
        time.sleep(1)

    df = pd.DataFrame(produtos)

    # Ajusta o índice pra começar em 1
    df.index = range(1, len(df) + 1)
    df.index.name = "Nº"


    return df
    
    pd.set_option('display.max_colwidth', None)
    print(df)
    
# Exemplo de uso
if __name__ == "__main__":
    termo = input("Digite o produto para buscar: ")
    limite = int(input("Digite o limite de produtos (padrão 10): ") or 10)
    resultado = buscar_produtos(termo, limite=limite, salvar_csv=salvar)
    if not resultado.empty:
        print(resultado)
    else:
        print("Nenhum produto encontrado ou erro na busca.")