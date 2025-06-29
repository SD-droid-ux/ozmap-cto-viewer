import streamlit as st
import requests
import json

# Configurações da página
st.set_page_config(page_title="🔎 Buscar CTO no Ozmap", layout="centered")
st.title("🔌 Consulta de CTOs via Ozmap API (com chave API)")

st.markdown("Insira sua **API Key** e o **nome da CTO (box)** para buscar localização no Ozmap.")

# Entradas do usuário
api_key = st.text_input("🔑 API Key Ozmap", type="password")
cto_input = st.text_input("📦 Nome da CTO (ex: NTL06-570)")

# Quando clicar no botão
if st.button("🔍 Buscar CTO"):
    if not api_key or not cto_input:
        st.warning("Preencha todos os campos acima.")
    else:
        # Monta o filtro no formato exigido pela API
        filtro = json.dumps([{
            "property": "name",
            "operator": "=",
            "value": cto_input
        }])

        # URL da API com filtro aplicado
        url = f"https://sandbox.ozmap.com.br:8994/api/v2/boxes?filter={filtro}"

        # Cabeçalho com a chave da API
        headers = {
            "Authorization": api_key
        }

        try:
            # Requisição com timeout de 60 segundos
            response = requests.get(url, headers=headers, timeout=60)

            if response.status_code == 200:
                data = response.json()

                if data:
                    box = data[0]
                    st.success("✅ CTO encontrada!")

                    st.write(f"📍 **Cidade:** {box.get('city', 'Não informado')}")
                    st.write(f"🌐 **Latitude:** {box.get('latitude', 'Não informado')}")
                    st.write(f"🌐 **Longitude:** {box.get('longitude', 'Não informado')}")

                    if box.get("latitude") and box.get("longitude"):
                        st.map([{
                            "lat": box["latitude"],
                            "lon": box["longitude"]
                        }])
                    else:
                        st.info("Localização indisponível para essa CTO.")
                else:
                    st.warning("CTO não encontrada. Verifique se o nome está correto.")
            else:
                st.error(f"Erro {response.status_code}: não foi possível buscar a CTO.")
                st.text(response.text)

        except requests.exceptions.RequestException as e:
            st.error("Erro de conexão com a API Ozmap.")
            st.text(str(e))
