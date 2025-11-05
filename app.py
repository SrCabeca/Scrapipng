import streamlit as st
import pandas as pd
from scraping import buscar_produtos

st.set_page_config(page_title="Scraping Mercado Livre", layout="wide")

st.title("🔎 Buscador de Produtos - Mercado Livre")

with st.form("busca_form"):
    termo = st.text_input("Digite o produto para buscar:", "")
    limite = st.number_input("Limite de produtos", min_value=1, max_value=50, value=10)
    buscar = st.form_submit_button("Buscar")

if buscar and termo:
    with st.spinner("Buscando produtos..."):
        resultado = buscar_produtos(termo, limite)
    if not resultado.empty:
        st.success(f"{len(resultado)} produtos encontrados!")
        st.dataframe(resultado, use_container_width=True)

        # Opção para exportar CSV
        csv = resultado.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar CSV", csv, file_name=f"{termo}.csv", mime="text/csv")
    else:
        st.warning("Nenhum produto encontrado ou erro na busca.")
else:
    st.info("Digite um termo e clique em Buscar para iniciar.")
