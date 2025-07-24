import streamlit as st
import requests
import json

# Configurações da página
st.set_page_config(page_title="🔎 Buscar CTO no Ozmap", layout="centered")
st.title("🔌 Consulta de CTOs via Ozmap API")

st.markdown("Insira sua **API Key** e o **nome da CTO** para buscar sua localização.")

# Entrada da chave e nome
api_key = st.text_input("🔑 API Key Ozmap", type="password")
cto_name = st.text_input("📦 Nome da CTO (ex: NTL06-570)")

# Ação ao clicar no botão
if st.button("🔍 Buscar CTO"):
    if not api_key or not cto_name:
        st.warning("Preencha todos os campos.")
    else:
        filtro = json.dumps([
            {
                "property": "name",
                "operator": "=",
                "value": cto_name
            }
        ])

        # URL do ambiente sandbox
        url = f"https://sandbox.ozmap.com.br:9994/api/v2/boxes?filter={filtro}"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                ctos = response.json()

                if ctos:
                    st.success(f"✅ {len(ctos)} CTO(s) encontrada(s) com esse nome.")
                    for i, box in enumerate(ctos):
                        st.markdown(f"### CTO {i + 1}")
                        st.write(f"📍 **Cidade:** {box.get('city', 'Não informado')}")
                        st.write(f"🌐 **Latitude:** {box.get('latitude', 'Não informado')}")
                        st.write(f"🌐 **Longitude:** {box.get('longitude', 'Não informado')}")
                        
                        if box.get("latitude") and box.get("longitude"):
                            st.map([{
                                "lat": box["latitude"],
                                "lon": box["longitude"]
                            }])
                        else:
                            st.info("CTO encontrada, mas sem coordenadas geográficas.")
                else:
                    st.warning("Nenhuma CTO com esse nome foi encontrada.")
            else:
                st.error(f"Erro {response.status_code}: {response.reason}")
                st.text(response.text)
        except requests.exceptions.RequestException as e:
            st.error("Erro de conexão com a API do Ozmap.")
            st.text(str(e))
