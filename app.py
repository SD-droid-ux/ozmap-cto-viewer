import streamlit as st
import requests

st.set_page_config(page_title="🔎 Buscar CTO no Ozmap", layout="centered")

st.title("🔌 Consulta de CTOs via Ozmap API (com chave API)")

st.markdown("""
Este aplicativo permite buscar uma CTO cadastrada no Ozmap e exibe suas informações de localização.
""")

# Campo para chave de API
api_key = st.text_input("🔑 Chave da API Ozmap", type="password")
cto_input = st.text_input("📡 Nome exato da CTO (ex: FLA27-0118)")

if st.button("🔍 Buscar CTO"):
    if not api_key or not cto_input:
        st.warning("Preencha todos os campos.")
    else:
        # 🔗 Endpoint ajustado com seu domínio e porta 9090
        cto_url = "http://alaresinternet.ozmap.com.br:9090/api/cto"

        headers = {
            "Authorization": f"Token {api_key}"
        }

        try:
            response = requests.get(cto_url, headers=headers, timeout=10)

            if response.status_code == 200:
                ctos = response.json()

                resultado = next((cto for cto in ctos if cto.get("name") == cto_input), None)

                if resultado:
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
                    st.warning("CTO não encontrada.")
            else:
                st.error("Erro ao acessar API.")
                st.text(response.text)

        except requests.exceptions.RequestException as e:
            st.error("Erro de conexão.")
            st.text(str(e))
