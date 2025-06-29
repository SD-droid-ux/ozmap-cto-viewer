import streamlit as st
import requests

st.set_page_config(page_title="🔎 Buscar CTO no Ozmap", layout="centered")

st.title("🔌 Consulta de CTOs via Ozmap API")

st.markdown("""
Este aplicativo permite buscar uma CTO cadastrada no Ozmap e exibe suas informações de localização.
""")

# Campos para login
email = st.text_input("Email Ozmap")
senha = st.text_input("Senha Ozmap", type="password")

# Campo para digitar o nome da CTO
cto_input = st.text_input("Nome exato da CTO (ex: FLA27-0118)")

if st.button("🔍 Buscar CTO"):
    if not email or not senha or not cto_input:
        st.warning("Preencha todos os campos para continuar.")
    else:
        # Autenticação na API Ozmap
        login_url = "https://ozmap.com.br/api/token"
        login_payload = {"email": email, "password": senha}
        login_response = requests.post(login_url, json=login_payload)

        if login_response.status_code == 200:
            token = login_response.json().get("token")
            headers = {"Authorization": f"Bearer {token}"}

            # Buscar CTOs
            cto_url = "https://ozmap.com.br/api/cto"
            cto_response = requests.get(cto_url, headers=headers)

            if cto_response.status_code == 200:
                ctos = cto_response.json()

                # Procurar a CTO pelo nome exato
                resultado = next((cto for cto in ctos if cto.get("name") == cto_input), None)

                if resultado:
                    st.success("✅ CTO encontrada!")
                    st.write(f"📍 **Cidade:** {resultado.get('city')}")
                    st.write(f"🌐 **Latitude:** {resultado.get('latitude')}")
                    st.write(f"🌐 **Longitude:** {resultado.get('longitude')}")

                    # Exibir no mapa se tiver coordenadas
                    if resultado.get("latitude") and resultado.get("longitude"):
                        st.map(data=[{
                            "lat": resultado.get("latitude"),
                            "lon": resultado.get("longitude")
                        }])
                else:
                    st.error("CTO não encontrada. Verifique se o nome está correto.")
            else:
                st.error("Erro ao buscar CTOs.")
                st.text(cto_response.text)
        else:
            st.error("Falha no login. Verifique seu e-mail e senha.")
            st.text(login_response.text)
