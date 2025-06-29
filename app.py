import streamlit as st
import requests

st.set_page_config(page_title="🔎 Buscar CTO no Ozmap", layout="centered")

st.title("🔌 Consulta de CTOs via Ozmap API (com chave API)")

st.markdown("""
Insira sua **API Key** gerada no Ozmap e o **nome exato da CTO** para buscar localização.
""")

# Campos de entrada
api_key = st.text_input("🔑 API Key Ozmap", type="password")
cto_input = st.text_input("📡 Nome da CTO (ex: FLA27-0118)")

if st.button("🔍 Buscar CTO"):
    if not api_key or not cto_input:
        st.warning("Preencha os campos acima.")
    else:
        # URL correta da API
        cto_url = f"https://sandbox.ozmap.com.br:8994/api/v2/ctos?name={cto_input}"
        headers = {"Authorization": api_key}

        try:
            res = requests.get(cto_url, headers=headers, timeout=10)

            if res.status_code == 200:
                ctos = res.json()

                if isinstance(ctos, list) and len(ctos) > 0:
                    resultado = ctos[0]
                    st.success("✅ CTO encontrada!")
                    st.write(f"📍 **Cidade:** {resultado.get('city')}")
                    st.write(f"🌐 **Latitude:** {resultado.get('latitude')}")
                    st.write(f"🌐 **Longitude:** {resultado.get('longitude')}")

                    if resultado.get("latitude") and resultado.get("longitude"):
                        st.map(data=[{
                            "lat": resultado.get("latitude"),
                            "lon": resultado.get("longitude")
                        }])
                else:
                    st.warning("CTO não encontrada. Verifique o nome exato.")
            else:
                st.error(f"Erro {res.status_code}: não foi possível acessar a API.")
                st.text(res.text)

        except requests.exceptions.RequestException as e:
            st.error("Erro de conexão com a API Ozmap.")
            st.text(str(e))
