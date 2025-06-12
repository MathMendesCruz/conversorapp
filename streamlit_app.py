import streamlit as st
import pandas as pd

st.set_page_config(page_title="Formatador de Contatos CSV", layout="centered")
st.title("Formatador de Contatos CSV by Math Netfit")

uploaded_file = st.file_uploader("Envie seu arquivo CSV", type=["csv"])

if uploaded_file:
    try:
        # Tentar ler o CSV com separador correto
        try:
            df = pd.read_csv(uploaded_file, sep=None, engine='python')
        except Exception:
            df = pd.read_csv(uploaded_file, sep=',')
        st.subheader("Colunas encontradas:")
        st.write(df.columns.tolist())

        # Permitir ao usuário selecionar as colunas de nome e WhatsApp
        st.info("Selecione as colunas de Nome/Razão Social e WhatsApp/Celular abaixo:")
        colunas = df.columns.tolist()
        col_nome = st.selectbox("Coluna de Nome/Razão Social", colunas, index=next((i for i, col in enumerate(colunas) if any(x in col.lower() for x in ['razão', 'nome'])), 0))
        col_whatsapp = st.selectbox("Coluna de WhatsApp/Celular", colunas, index=next((i for i, col in enumerate(colunas) if any(x in col.lower() for x in ['whatsapp', 'celular'])), 1 if len(colunas) > 1 else 0))

        if col_nome and col_whatsapp:
            df_formatado = df[[col_nome, col_whatsapp]].copy()
            df_formatado.columns = ["name", "whatsapp"]

            st.success("Colunas selecionadas com sucesso!")
            st.subheader("Pré-visualização:")
            st.dataframe(df_formatado)

            st.subheader("Resultado Formatado (texto com vírgula):")
            resultado_texto = "\n".join(f"{row['name']}, {row['whatsapp']}" for _, row in df_formatado.iterrows())
            st.code(resultado_texto, language="text")

            csv = df_formatado.to_csv(index=False)
            st.download_button(
                label="📥 Baixar CSV formatado",
                data=csv.encode("utf-8"),
                file_name="contatos_formatado.csv",
                mime="text/csv"
            )
        else:
            st.error("Selecione as colunas corretamente.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

st.markdown(
    """
    <style>
    /* Seu CSS aqui */
    .stButton>button {background-color: #01B1F2; color: white; font-weight: bold;}
    .stDataFrame {border-radius: 10px;}
    </style>
    """,
    unsafe_allow_html=True
)
