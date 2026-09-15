import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Dados",
    layout="wide"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* FUNDO */
.stApp {
    background: #f5f6fa;
}

/* CONTAINER */
.block-container {
    max-width: 1350px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* TÍTULO */
h1 {
    color: #17172b !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
}

/* SUBTÍTULOS */
h2, h3 {
    color: #25243a !important;
    font-weight: 700 !important;
}

/* TEXTOS */
p {
    color: #66677a;
    line-height: 1.7;
}

/* CAPTION */
[data-testid="stCaptionContainer"] {
    color: #85869a !important;
}

/* UPLOAD */
[data-testid="stFileUploader"] {
    background: white;
    border: 2px dashed #6366f1;
    border-radius: 16px;
    padding: 20px;
    margin-top: 15px;
    margin-bottom: 25px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
}

/* MÉTRICAS */
[data-testid="stMetric"] {
    background: white;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #e8e8f0;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
}

[data-testid="stMetricLabel"] {
    color: #77788b !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #17172b !important;
    font-weight: 800 !important;
}

/* TABELA */
[data-testid="stDataFrame"] {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #e8e8f0;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
}

/* EXPANDER */
[data-testid="stExpander"] {
    background: white;
    border: 1px solid #e8e8f0;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
    margin-top: 15px;
    margin-bottom: 15px;
}

/* GRÁFICOS */
.stPlotlyChart {
    background: white;
    border-radius: 16px;
    padding: 10px;
    border: 1px solid #e8e8f0;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
}

/* ALERTAS */
[data-testid="stAlert"] {
    border-radius: 14px !important;
}

/* COLUNAS */
[data-testid="column"] {
    padding: 5px;
}

/* DIVISÓRIAS */
hr {
    border: none;
    height: 1px;
    background: #e4e4ec;
    margin: 30px 0;
}

/* RESPONSIVO */
@media (max-width: 768px) {

    .block-container {
        padding: 1rem;
    }

    h1 {
        font-size: 2rem !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }

}

</style>
""", unsafe_allow_html=True)


st.title("Dashboard de Dados - Participantes do ENEM")

st.write("""
Este dashboard apresenta uma análise sobre os participantes do ENEM 2025. 

**Criado por: João Vitor Helfstein, Gabriel Willian, Kaue Santos**
""")

st.caption(
    "Fonte dos dados: Microdados do ENEM — INEP/MEC "
    "(gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem)"
)

arquivo = st.file_uploader(
    "Envie um arquivo CSV",
    type=["csv"]
)

if arquivo is not None:

    df = pd.read_csv(arquivo, sep=";")

    st.subheader("Visualização dos dados")
    st.dataframe(df.head())

    col1, col2 = st.columns(2)
    col1.metric(
        "Quantidade de registros",
        df.shape[0]
    )
    col2.metric(
        "Quantidade de colunas",
        df.shape[1]
    )

    with st.expander("Verificação da qualidade dos dados"):
        st.write("Valores ausentes por coluna:")
        st.write(df.isnull().sum())

        st.write(f"Registros duplicados encontrados: {df.duplicated().sum()}")

        st.write("Tipos de dados por coluna:")
        st.write(df.dtypes)

    linhas_antes = df.shape[0]
    df = df.drop_duplicates()
    linhas_depois = df.shape[0]

    if linhas_antes != linhas_depois:
        st.info(
            f"Foram removidos {linhas_antes - linhas_depois} registros "
            "duplicados antes da análise."
        )

    st.subheader("Análise dos dados")

    coluna_estado = "SG_UF_PROVA"
    coluna_sexo = "TP_SEXO"

    grafico_col1, grafico_col2 = st.columns(2)

    with grafico_col1:
        if coluna_estado in df.columns:
            contagem_estado = (
                df[coluna_estado]
                .value_counts()
                .reset_index()
            )
            contagem_estado.columns = ["Estado", "Quantidade"]

            fig_estado = px.bar(
                contagem_estado,
                x="Estado",
                y="Quantidade",
                title="Participantes por estado",
                text="Quantidade"
            )
            fig_estado.update_xaxes(
                tickmode="linear",
                tickangle=-45
            )
            st.plotly_chart(fig_estado, use_container_width=True)

            st.markdown("**Qual estado apresenta o maior número de participantes? /br São Paulo, com folga: 751.612 inscritos, à frente de Minas Gerais (464.937) e Bahia (427.983).**")
        else:
            st.warning(
                f"Coluna '{coluna_estado}' não encontrada na base enviada."
            )

    with grafico_col2:
        if coluna_sexo in df.columns:
            contagem_sexo = (
                df[coluna_sexo]
                .value_counts()
                .reset_index()
            )
            contagem_sexo.columns = ["Sexo", "Quantidade"]

            fig_sexo = px.bar(
                contagem_sexo,
                x="Sexo",
                y="Quantidade",
                title="Participantes por sexo",
                text="Quantidade"
            )
            st.plotly_chart(fig_sexo, use_container_width=True)

            st.markdown("**Como os participantes se distribuem por sexo?**")
        else:
            st.warning(
                f"Coluna '{coluna_sexo}' não encontrada na base enviada."
            )

    if coluna_estado in df.columns:
        st.subheader("Indicador geral")
        media_por_estado = round(
            df[coluna_estado].value_counts().mean(), 0
        )
        st.metric(
            "Média de participantes por estado analisado",
            f"{media_por_estado:,.0f}"
        )

    with st.expander( "Respostas das perguntas"):
        st.markdown(""" Respostas — Dashboard ENEM 2025 (base: PARTICIPANTES_2025.csv)
**Aula 1, perguntas de análise**

Não dá pra ver como um indicador mudou ao longo do tempo com essa base, porque ela cobre só 2025. Sem série histórica não tem comparação possível.

O estado com mais gente inscrita é São Paulo, disparado: 751.612 participantes, uns 15,6% de tudo. Minas e Bahia vêm logo atrás.

Em termos de categorias mais frequentes, pardos e brancos dominam a base (44,6% e 39,6%), e quando se olha pra renda, 71,2% dos participantes caem na faixa "baixa" do questionário socioeconômico, uma concentração bem forte.

Entre regiões a diferença é grande: Nordeste e Sudeste puxam a fila com 36% e 34% dos inscritos, enquanto o Centro-Oeste fica com pouco mais de 8%.

E o sexo dos participantes também não é equilibrado: 60% são mulheres.

**Entrega da Aula 1**
**Pergunta 1: qual estado tem mais participantes?**

São Paulo, com folga: 751.612 inscritos, à frente de Minas Gerais (464.937) e Bahia (427.983).

**Pergunta 2: como isso mudou ao longo dos anos?**

Aqui a base trava. Só temos 2025, então essa pergunta fica sem resposta com os dados que temos.

**Aula 3, retomando as perguntas**

Os cinco estados com mais participantes, na ordem, são SP, MG, BA, RJ e PA. E de novo: comparar com anos anteriores não é possível, porque a base não traz histórico.

**Aula 4, lendo os gráficos**

Os gráficos de estado e região mostram basicamente a mesma coisa vista de dois ângulos: quantos participantes cada lugar teve em 2025.

O maior valor aparece em SP no gráfico por estado (751.612) e no Nordeste no gráfico por região (1.737.630).

**Dá pra notar uma diferença bem grande entre as pontas:** o Centro-Oeste tem menos da metade dos participantes do Sul, e cerca de 4,5 vezes menos que o Nordeste.

Como é uma foto única de 2025, não tem como falar em aumento ou queda. Isso pediria dados de outros anos.

**As diferenças entre categorias são nítidas:** só os estados nordestinos juntos já superam a região Sudeste inteira em número de inscritos.

E o padrão que salta aos olhos é meio óbvio quando se para pra pensar: estados mais populosos (SP, MG, BA, RJ) puxam os maiores números. Faz sentido, já que mais gente morando lá significa mais gente prestando o exame.

**Aula 5, testando o dashboard**

O app abre, carrega o CSV com pd.read_csv(sep=";"), os dados aparecem na aba de dados brutos, e os gráficos das abas Geografia, Perfil e Socioeconômico funcionam normalmente. Os títulos batem com o que cada gráfico mostra, e os valores vêm direto de value_counts() na base, sem estimativa nem arredondamento forçado.

**Apresentação final**

O projeto investiga o perfil de quem fez o ENEM 2025: de onde vêm, sexo, cor/raça e situação socioeconômica. A base usada foi os microdados oficiais do ENEM 2025 (INEP/MEC), com 4.810.772 registros.

Os principais achados: São Paulo concentra a maior fatia de participantes (15,6%), o Nordeste é a região líder (36,1%), a maioria dos inscritos é mulher (60,1%) e a maior parte vem de famílias com renda baixa (71,2%).

A IA entrou principalmente na parte chata: pegar os códigos numéricos da base (tipo "3" na coluna de cor/raça) e transformar em algo legível ("Parda"), além de criar as colunas novas de região e nível socioeconômico que não vinham prontas no arquivo original.

**Reflexão final**

O dashboard funciona: carrega, filtra e mostra os gráficos do jeito esperado.

Ele representa bem os dados, com uma ressalva importante: não dá pra ligar os itens da prova a participantes específicos, porque o INEP usa identificadores diferentes e anonimizados em cada base, de propósito, pra proteger quem fez a prova.

As conclusões aqui vêm de contagem direta, então são sólidas. O cuidado é não confundir associação com causa. Dizer que uma região "causa" renda baixa seria forçar a mão; o que dá pra afirmar é que essas coisas aparecem juntas nos dados, nada além disso.

E sim, dá pra explicar o que foi feito numa frase: um dashboard que lê o CSV de participantes do ENEM 2025, traduz os campos usando o dicionário oficial do INEP e mostra a distribuição geográfica, demográfica e socioeconômica em gráficos que o usuário pode filtrar.""")

    with st.expander("Exemplo de como a IA ajudou no desenvolvimento"):
        st.markdown("""
        **Problema encontrado:** ao carregar o CSV com `pd.read_csv()`,
        todos os dados apareciam em uma única coluna no visualizador.

        **Prompt utilizado:** foi perguntado à IA se o arquivo deveria
        ser separado por ponto e vírgula, já que essa é a convenção dos
        microdados do INEP.

        **Sugestão da IA:** utilizar `pd.read_csv(arquivo, sep=";")`
        para indicar explicitamente o separador correto.

        **O que o grupo fez:** a sugestão foi testada e o arquivo passou
        a ser lido corretamente, com cada coluna separada de forma
        adequada. A alteração foi validada comparando o número de
        colunas exibido pelo Pandas (`df.shape[1]`) com o número de
        colunas do arquivo original.
        """)

else:
    st.info("Envie um arquivo CSV para iniciar a análise.")
