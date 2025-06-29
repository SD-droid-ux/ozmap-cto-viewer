import streamlit as st
import requests

st.set_page_config(page_title="🔎 Buscar CTO no Ozmap", layout="centered")

st.title("🔌 Consulta de CTOs via Ozmap API")

st.markdown("""
Este aplicativo permite buscar uma CTO cadastrada no Ozmap e exibe suas informações de localização.
""")

# Login via usuário Ozmap
usuario = st.text_input("Usuário Ozmap (sem @)")
senha = st.text_input("Senha Ozmap", type="password")

# Nome da CTO a buscar
cto_input = st.text_input("Nome exato da CTO (ex: FLA27-0118)")

if st.button("🔍 Buscar CTO"):
    if not usuario or not senha or not cto_input:
        st.warning("Preencha todos os campos para continuar.")
    else:
        # ✅ Endpoints ajustados com seu domínio e porta 9090
        login_url = "http://alaresinternet.ozmap.com.br:9090/api/token"
        cto_url = "http://alaresinternet.ozmap.com.br:9090/api/cto"

        login_payload = {"username": usuario, "password": senha}

        try:
            login_response = requests.post(login_url, json=login_payload, timeout=10)

            if login_response.status_code == 200:
                token = login_response.json().get("token")
                headers = {"Authorization": f"Bearer {token}"}

                cto_response = requests.get(cto_url, headers=headers, timeout=10)

                if cto_response.status_code == 200:
                    ctos = cto_response.json()

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
                        st.error("CTO não encontrada. Verifique o nome.")
                else:
                    st.error("Erro ao buscar CTOs:")
                    st.text(cto_response.text)
            else:
                st.error("Falha no login. Verifique o usuário e a senha.")
                st.text(login_response.text)

        except requests.exceptions.RequestException as e:
            st.error("Erro de conexão com a API Ozmap.")
            st.text(str(e))
