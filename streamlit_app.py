import streamlit as st
import pandas as pd

st.set_page_config(page_title="Formatador de Contatos CSV", layout="centered")
st.title("Formatador de contatos para o OPA!")

uploaded_file = st.file_uploader("Envie seu arquivo CSV", type=["csv"])

# Contatos fixos
contatos_fixos = [
    {"name": "Matheus Mendes", "whatsapp": "(11) 94887-6252"},
]

# Inicializa estado para contatos extras (manuais)
if "contatos_extras" not in st.session_state:
    st.session_state["contatos_extras"] = []

def encontrar_indice_padrao(colunas, palavras_chave, default=0):
    for i, col in enumerate(colunas):
        lower = str(col).lower()
        if any(k in lower for k in palavras_chave):
            return i
    return default if 0 <= default < len(colunas) else 0

if uploaded_file:
    try:
        try:
            df = pd.read_csv(uploaded_file, sep=None, engine="python")
        except Exception:
            # Recomeça leitura com separador padrão
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, sep=",")
        st.subheader("Colunas encontradas:")
        st.write(df.columns.tolist())

        # Seleção das colunas
        st.info("Selecione as colunas de Nome/Razão Social e WhatsApp/Celular abaixo:")
        colunas = df.columns.tolist()
        idx_nome = encontrar_indice_padrao(colunas, ["razão", "razao", "nome", "nome/"])
        idx_wh = encontrar_indice_padrao(colunas, ["whatsapp", "celular", "telefone"], default=1 if len(colunas) > 1 else 0)

        col_nome = st.selectbox("Coluna de Nome/Razão Social", colunas, index=idx_nome)
        col_whatsapp = st.selectbox("Coluna de WhatsApp/Celular", colunas, index=idx_wh)

        st.subheader("Adicionar contato manualmente")
        with st.form("adicionar_contato", clear_on_submit=True):
            nome_extra = st.text_input("Nome do contato")
            whatsapp_extra = st.text_input("WhatsApp do contato")
            adicionar = st.form_submit_button("Adicionar contato")
            if adicionar:
                if nome_extra.strip() and whatsapp_extra.strip():
                    st.session_state["contatos_extras"].append(
                        {"name": nome_extra.strip(), "whatsapp": whatsapp_extra.strip()}
                    )
                    st.success("Contato adicionado.")
                    st.experimental_rerun()
                else:
                    st.error("Preencha nome e WhatsApp antes de adicionar.")

        # Remover contatos manuais
        if st.session_state["contatos_extras"]:
            st.subheader("Contatos manuais adicionados")
            for idx, contato in enumerate(st.session_state["contatos_extras"]):
                col1, col2 = st.columns([4,1])
                col1.write(f"{contato['name']} — {contato['whatsapp']}")
                if col2.button("Remover", key=f"remover_{idx}"):
                    st.session_state["contatos_extras"].pop(idx)
                    st.experimental_rerun()

        # Verifica seleção e formata saída
        if col_nome and col_whatsapp:
            df_formatado = df[[col_nome, col_whatsapp]].copy()
            df_formatado.columns = ["name", "whatsapp"]

            contatos_df = pd.DataFrame(contatos_fixos + st.session_state["contatos_extras"])
            df_final = pd.concat([contatos_df, df_formatado], ignore_index=True)

            csv = df_final.to_csv(index=False)
            st.download_button(
                label="📥 Baixar CSV formatado",
                data=csv.encode("utf-8"),
                file_name="contatos_formatado.csv",
                mime="text/csv"
            )

            st.success("Colunas selecionadas com sucesso!")
            st.subheader("Pré-visualização:")
            st.dataframe(df_final)

            st.subheader("Resultado Formatado (texto com vírgula):")
            resultado_texto = "\n".join(f"{row['name']}, {row['whatsapp']}" for _, row in df_final.iterrows())
            st.code(resultado_texto, language="text")
        else:
            st.error("Selecione as colunas corretamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

st.markdown(
    """
    <style>
        .stButton>button {background-color: #01B1F2; color: white; font-weight: bold;}
        .stDataFrame {border-radius: 10px;}
    </style>
    """,
    unsafe_allow_html=True
)
