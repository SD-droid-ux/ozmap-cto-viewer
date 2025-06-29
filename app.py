import streamlit as st
import requests

st.set_page_config(page_title="🔎 Buscar CTO no Ozmap", layout="centered")

st.title("🔌 Consulta de CTOs via Ozmap API (com chave API)")

st.markdown("""
Insira sua **API Key** gerada no Ozmap e o **nome exato da CTO** para buscar localização.
""")

# Campo de entrada
api_key = st.text_input("🔑 API Key Ozmap", type="password")
cto_input = st.text_input("📡 Nome da CTO (ex: FLA27-0118)")

if st.button("🔍 Buscar CTO"):
    if not api_key or not cto_input:
        st.warning("Preencha os campos acima.")
    else:
        cto_url = "http://alaresinternet.ozmap.com.br:9090/api/cto"
        headers = {"Authorization": f"Token {api_key}"}

        try:
            res = requests.get(cto_url, headers=headers, timeout=10)

            if res.status_code == 200:
                ctos = res.json()
                resultado = next((c for c in ctos if c.get("name") == cto_input), None)

                if resultado:
                    st.success("✅ CTO encontrada!")
                    st.write(f"📍 **Cidade:** {resultado.get('city')}")
                    st.write(f"🌐 **Latitude:** {resultado.get('latitude')}")
                    st.write(f"🌐 **Longitude:** {resultado.get('longitude')}")
                    if resultado.get("latitude") and resultado.get("longitude"):
                        st.map(data=[{"lat": resultado.get("latitude"), "lon": resultado.get("longitude")}])
                else:
                    st.warning("CTO não encontrada. Verifique o nome exato.")
            else:
                st.error(f"Erro {res.status_code}: não foi possível acessar a API.")
                st.text(res.text)

        except requests.exceptions.RequestException as e:
            st.error("Erro de conexão com a API Ozmap.")
            st.text(str(e))
