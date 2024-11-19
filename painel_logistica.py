import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
from io import BytesIO
# Certifique-se de que `st.set_page_config()` é a primeira linha de código
st.set_page_config(page_title="Análise de dados Senior", layout="wide")

st.markdown(
    """
    <style>
    
        /* Títulos principais com animação de entrada */
        h1, h2, h3{
            color: black;
            font-weight: bold;
            animation: fadeIn 1.5s ease-in-out;
        }
        /* Forçar o título da sidebar a ficar branco */
        .css-1d391kg h2 {
            color: #ffffff !important;
        }
        
        /* Fundo geral da aplicação */
        .stApp {
            background: linear-gradient(120deg, #2F4F4F, #e2ebf2);
            font-family: 'Helvetica Neue', sans-serif;
        }

        /* Botão de "Baixar Excel" */
        .stDownloadButton > button {
            display: inline-flex;
            align-items: center;
            color: white;
            background-color: #28a745;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            transition: background 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .stDownloadButton > button:hover {
            background-color: #218838;
            transform: scale(1.05);
        }
        .stDownloadButton > button::before {
            content: url('https://img.icons8.com/fluency-systems-filled/24/FFFFFF/download.png');
            display: inline-block;
            margin-right: 8px;
        }

        /* Botão de "Análise Gráfica" */
        .stButton > button {
            display: inline-flex;
            align-items: center;
            color: white;
            background-color: #28a745;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            transition: background 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .stButton > button:hover {
            background-color: #218838;
            transform: scale(1.05);
        }
        .stButton > button::before {
            content: url('https://img.icons8.com/fluency-systems-filled/24/FFFFFF/combo-chart.png');
            display: inline-block;
            margin-right: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Título principal com ícone e tooltip
st.markdown(
    """
    <h1 class="tooltip">
        <img src="https://img.icons8.com/doodle/48/000000/bar-chart.png" style="vertical-align: middle;">
        Análise de Dados Senior
        <span class="tooltiptext"></span>
    </h1>
    """,
    unsafe_allow_html=True,
)

# Título da barra lateral de filtros com ícone
st.sidebar.markdown(
    """<h2 class="tooltip"><img src="https://img.icons8.com/ios-filled/30/ffffff/filter.png" style="vertical-align: middle;">
    <span class="tooltiptext"></span></h2>""",
    unsafe_allow_html=True,
)

# Título da barra de busca com ícone
st.markdown(
    """<h3 class="tooltip"><img src="https://img.icons8.com/ios-glyphs/30/000000/search.png" style="vertical-align: middle;">
    Buscar por Nome<span class="tooltiptext"></span></h3>""",
    unsafe_allow_html=True
)


  
# Carregar os dados
file_path = 'relatorio4.xlsx'  # Atualize o caminho para o seu arquivo
df = pd.read_excel(file_path)

# Renomear colunas para visualização
df = df.rename(columns={
    'Hora Trabalhada': 'Estouro de Jornada',
    'Hora Exceção': 'Interjornada',
    'Hora Interno': 'Trabalho na Folga'
})


# Selecionar apenas as colunas necessárias
# Certifique-se de que o nome da coluna "Estouro de Jornada" está correto
df = df[['Colaborador ID', 'Nome', 'MÊS', 'Data', 'Data Início', 
         'Código Centro Custo', 'Estouro de Jornada', 'Interjornada', 
         'Trabalho na Folga', 'Faltas']]

# Manter a coluna "Data" como string no formato "YYYY-MM-DD" para facilitar os filtros
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True).dt.strftime('%Y-%m-%d')

# Definir intervalos de datas como strings para cada intervalo desejado
intervalos_mensais = {
    "janeiro_fevereiro": ("2024-01-11", "2024-02-10"),
    "fevereiro_marco": ("2024-02-11", "2024-03-10"),
    "marco_abril": ("2024-03-11", "2024-04-10"),
    "abril_maio": ("2024-04-11", "2024-05-10"),
    "maio_junho": ("2024-05-11", "2024-06-10"),
    "junho_julho": ("2024-06-11", "2024-07-10"),
    "julho_agosto": ("2024-07-11", "2024-08-10"),
    "agosto_setembro": ("2024-08-11", "2024-09-10"),
    "setembro_outubro": ("2024-09-11", "2024-10-10"),
    "outubro_novembro": ("2024-10-11", "2024-11-10")
}

# Função para aplicar filtro de datas com base no intervalo selecionado
def aplicar_filtro_mensal(df, intervalo_selecionado):
    if intervalo_selecionado in intervalos_mensais:
        inicio, fim = intervalos_mensais[intervalo_selecionado]
        return df[(df['Data'] >= inicio) & (df['Data'] <= fim)]
    return df








# Filtro por Intervalo de Mês com opção "Todos"
intervalos_unicos = ["Todos"] + list(intervalos_mensais.keys())
intervalo_selecionado = st.sidebar.selectbox("Filtrar por Intervalo de Mês", options=intervalos_unicos)

# Filtro por Código Centro Custo com opção "Todos"
centros_custo_unicos = ["Todos"] + sorted(df["Código Centro Custo"].unique())
centro_custo_selecionado = st.sidebar.selectbox("Filtrar por Centro de Custo", options=centros_custo_unicos)

# Aplicar o filtro de intervalo de mês com intervalo de datas quando necessário
if intervalo_selecionado != "Todos":
    df_filtrado = aplicar_filtro_mensal(df, intervalo_selecionado)
else:
    df_filtrado = df

# Aplicar filtro de Centro de Custo
if centro_custo_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Código Centro Custo"] == centro_custo_selecionado]

# Barra de busca
busca = st.text_input("Buscar por Nome")

# Filtrar por busca no nome
if busca:
    df_filtrado = df_filtrado[df_filtrado["Nome"].str.contains(busca, case=False, na=False)]

# Contador de linhas após filtros
st.write(f"### Total de Registros: {len(df_filtrado)}")

# Configuração do AgGrid para expandir a tabela com paginação
st.write("### Dados Interativos")
gb = GridOptionsBuilder.from_dataframe(df_filtrado)
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)  # Configuração de paginação com 20 linhas por página
gb.configure_side_bar()  # Barra lateral para filtros avançados na tabela
gb.configure_default_column(editable=True, groupable=True)

grid_options = gb.build()

# Renderizar a tabela interativa com paginação
grid_response = AgGrid(df_filtrado, gridOptions=grid_options, enable_enterprise_modules=True, height=400)

# Função para converter o DataFrame em Excel
@st.cache_data
def converter_para_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Botão para baixar a versão editada em Excel
excel_bytes = converter_para_excel(df_filtrado)
st.download_button(label="Baixar Excel", data=excel_bytes, file_name="dados_filtrados.xlsx", mime="application/vnd.ms-excel")

# Verificar e armazenar o estado do botão de análise gráfica
if "exibir_grafico" not in st.session_state:
    st.session_state.exibir_grafico = False

# Atualizar o estado do botão ao clicar
if st.button("Análise Gráfica"):
    st.session_state.exibir_grafico = True

# Exibir o gráfico apenas se o botão foi pressionado ao menos uma vez
if st.session_state.exibir_grafico:



    # Função para converter "Estouro de Jornada" de "HH:MM" para horas decimais
    def converter_para_horas_decimais(tempo_str):
        try:
            horas, minutos = map(int, tempo_str.split(':'))
            return horas + minutos / 60
        except (ValueError, AttributeError):
            return 0  # Retorna 0 se o valor não estiver no formato esperado

    # Aplicar a função de conversão para a coluna "Estouro de Jornada" no DataFrame filtrado
    df_filtrado['Estouro de Jornada'] = df_filtrado['Estouro de Jornada'].apply(converter_para_horas_decimais)

    # Agrupar por "Colaborador ID" e "Nome", somando as horas de "Estouro de Jornada"
    df_agrupado = df_filtrado.groupby(['Colaborador ID', 'Nome'])['Estouro de Jornada'].sum().reset_index()

    # Ordenar por "Estouro de Jornada" em ordem decrescente e pegar os 20 primeiros
    top_20_motoristas = df_agrupado.sort_values(by='Estouro de Jornada', ascending=False).head(20)

    # Criar o gráfico interativo com Plotly
    fig = px.bar(
        top_20_motoristas, 
        x='Estouro de Jornada', 
        y='Nome', 
        orientation='h',
        text='Estouro de Jornada',  # Rótulos de dados
        title="Top 20 Motoristas com Mais Estouro de Jornada"
    )

    # Customizar a aparência do gráfico
    fig.update_traces(marker_color='rgba(135, 206, 250, 0.6)',  # Cor azul clara com menor saturação
                    texttemplate='%{text:.2f} horas',  # Rótulo com duas casas decimais
                    textposition='outside')  # Posiciona o rótulo fora das barras
    fig.update_layout(xaxis_title="Total de Horas de Estouro de Jornada", yaxis_title="Motorista")

    # Exibir o gráfico interativo no Streamlit
    st.plotly_chart(fig)



        # 2. Gráfico de Linha - Evolução do Estouro de Jornada ao Longo do Tempo
    # Agrupar o DataFrame filtrado por data e somar as horas de estouro de jornada
    df_tempo = df_filtrado.groupby('Data')['Estouro de Jornada'].sum().reset_index()

    # Criar o gráfico de linha para visualizar a evolução do estouro de jornada
    fig_line = px.line(
        df_tempo, 
        x='Data', 
        y='Estouro de Jornada',
        title="Evolução do Estouro de Jornada ao Longo do Tempo",
        labels={"Estouro de Jornada": "Total de Horas de Estouro de Jornada", "Data": "Data"}
    )
    fig_line.update_traces(line_color='rgba(255, 127, 80, 0.8)')  # Cor laranja suave para a linha
    fig_line.update_layout(xaxis_title="Data", yaxis_title="Total de Horas de Estouro de Jornada")

    # Exibir o gráfico de linha no Streamlit
    st.plotly_chart(fig_line)
    

   
    # Função para somar múltiplos períodos de tempo em formato "HH:MM"
    def somar_periodos(tempo_str):
        if isinstance(tempo_str, str) and ':' in tempo_str:
            total_horas = 0
            periodos = tempo_str.split(':')
            for i in range(0, len(periodos) - 1, 2):
                try:
                    horas = int(periodos[i])
                    minutos = int(periodos[i + 1])
                    total_horas += horas + minutos / 60
                except ValueError:
                    pass
            return total_horas
        else:
            try:
                return float(tempo_str)
            except ValueError:
                return 0

    # Aplicar a função de soma de períodos para a coluna "Estouro de Jornada" no DataFrame filtrado
    df_filtrado['Estouro de Jornada'] = df_filtrado['Estouro de Jornada'].apply(somar_periodos)

    # Agrupar por motorista para calcular o total de horas de estouro de jornada
    df_total_estouro = df_filtrado.groupby(['Nome'])['Estouro de Jornada'].sum().reset_index()

    # Selecionar os Top 10 motoristas com maior estouro de jornada total
    top_motoristas = df_total_estouro.nlargest(15, 'Estouro de Jornada')['Nome']

    # Filtrar o DataFrame original para incluir apenas os Top 10 motoristas
    df_top_motoristas = df_filtrado[df_filtrado['Nome'].isin(top_motoristas)]

    # Agrupar os dados por "MÊS" e "Nome" (motorista), somando as horas de "Estouro de Jornada"
    df_heatmap_top = df_top_motoristas.groupby(['MÊS', 'Nome'])['Estouro de Jornada'].sum().reset_index()

    # Criar o heatmap com Plotly para os Top 10 motoristas
    fig_heatmap = px.density_heatmap(
        df_heatmap_top, 
        x='MÊS', 
        y='Nome',  
        z='Estouro de Jornada',
        color_continuous_scale='Oranges',  # Escala de cor para representar intensidade
        title="Distribuição de Estouro de Jornada por Mês para os Top 15 Motoristas",
        labels={"Estouro de Jornada": "Total de Horas de Estouro de Jornada"}
    )

    # Customizar o layout do heatmap
    fig_heatmap.update_layout(xaxis_title="Mês", yaxis_title="Motorista")
    fig_heatmap.update_coloraxes(colorbar_title="Horas")

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_heatmap)




    # Função para somar múltiplos períodos de tempo em formato "HH:MM"
    def somar_periodos(tempo_str):
        if isinstance(tempo_str, str) and ':' in tempo_str:
            total_horas = 0
            periodos = tempo_str.split(':')
            for i in range(0, len(periodos) - 1, 2):
                try:
                    horas = int(periodos[i])
                    minutos = int(periodos[i + 1])
                    total_horas += horas + minutos / 60
                except ValueError:
                    pass
            return total_horas
        else:
            try:
                return float(tempo_str)
            except ValueError:
                return 0

    # Aplicar a função de soma de períodos para a coluna "Estouro de Jornada" no DataFrame filtrado
    df_filtrado['Estouro de Jornada'] = df_filtrado['Estouro de Jornada'].apply(somar_periodos)

    # Função para categorizar os intervalos de tempo
    def categorizar_estouro(duracao):
        if duracao < 2.166:  # Até 2h10min
            return "02:00 - 02:10"
        elif duracao < 2.5:  # Até 2h30min
            return "02:10 - 02:30"
        elif duracao < 2.75:  # Até 2h45min
            return "02:30 - 02:45"
        elif duracao < 3.0:  # Até 3h
            return "02:45 - 03:00"
        elif duracao < 4.0:  # Até 4h
            return "03:00 - 04:00"
        else:
            return "Acima de 04:00"

    # Criar uma coluna de categorias de intervalos
    df_filtrado['Intervalo Estouro'] = df_filtrado['Estouro de Jornada'].apply(categorizar_estouro)

    # Contar a frequência de cada intervalo
    df_freq = df_filtrado['Intervalo Estouro'].value_counts().reset_index()
    df_freq.columns = ['Intervalo Estouro', 'Frequência']


    # Gráfico de barras para a distribuição dos intervalos de estouro de jornada
    fig_bar = px.bar(
        df_freq,
        x='Intervalo Estouro',
        y='Frequência',
        title="Distribuição de Frequência dos Intervalos de Estouro de Jornada",
        labels={"Intervalo Estouro": "Intervalo de Estouro de Jornada", "Frequência": "Frequência"}
    )

    # Customizar a aparência do gráfico
    fig_bar.update_layout(xaxis_title="Intervalo de Estouro de Jornada", yaxis_title="Frequência")
    fig_bar.update_traces(marker_color='rgba(255, 127, 80, 0.7)')  # Cor laranja com transparência

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_bar)




    # Definindo os intervalos de mês
    intervalos_mensais = {
        "janeiro_fevereiro": ("2024-01-11", "2024-02-10"),
        "fevereiro_marco": ("2024-02-11", "2024-03-10"),
        "marco_abril": ("2024-03-11", "2024-04-10"),
        "abril_maio": ("2024-04-11", "2024-05-10"),
        "maio_junho": ("2024-05-11", "2024-06-10"),
        "junho_julho": ("2024-06-11", "2024-07-10"),
        "julho_agosto": ("2024-07-11", "2024-08-10"),
        "agosto_setembro": ("2024-08-11", "2024-09-10"),
        "setembro_outubro": ("2024-09-11", "2024-10-10"),
        "outubro_novembro": ("2024-10-11", "2024-11-10")
    }

    # Função para aplicar filtro e contar as ocorrências de "Estouro de Jornada" em cada intervalo
    def contar_ocorrencias_por_mes(df, intervalos_mensais):
        ocorrencias_mensais = []
        for mes, (inicio, fim) in intervalos_mensais.items():
            total_ocorrencias = df[(df['Data'] >= inicio) & (df['Data'] <= fim)].shape[0]
            ocorrencias_mensais.append({"Mês": mes.replace("_", "/"), "Total de Ocorrências": total_ocorrencias})
        return pd.DataFrame(ocorrencias_mensais)

    # Carregar os dados
    file_path = 'relatorio4.xlsx'  # Atualize o caminho para o seu arquivo
    df = pd.read_excel(file_path)

    # Renomear colunas e formatar a coluna de data
    df = df.rename(columns={
        'Hora Trabalhada': 'Estouro de Jornada',
        'Hora Exceção': 'Interjornada',
        'Hora Interno': 'Trabalho na Folga'
    })
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True).dt.strftime('%Y-%m-%d')

    # Contar as ocorrências de "Estouro de Jornada" por mês
    df_ocorrencias = contar_ocorrencias_por_mes(df, intervalos_mensais)

    # Plotar o gráfico de barras
    fig = px.bar(
        df_ocorrencias,
        x='Mês',
        y='Total de Ocorrências',
        title="Total de Ocorrências de Estouro de Jornada por Mês",
        labels={"Total de Ocorrências": "Ocorrências", "Mês": "Mês"},
        text='Total de Ocorrências'  # Exibir as contagens diretamente nas barras
    )

    # Customizar a aparência do gráfico
    fig.update_traces(marker_color='rgba(100, 149, 237, 0.7)',  # Cor azul clara
                    textposition='outside')  # Posicionar o texto fora das barras
    fig.update_layout(xaxis_title="Mês", yaxis_title="Total de Ocorrências")

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)


    import plotly.graph_objects as go
    import pandas as pd
    import streamlit as st

    # Dados de exemplo de contagem de ocorrências mensais
    intervalos_mensais = {
        "janeiro_fevereiro": 612,
        "fevereiro_marco": 673,
        "marco_abril": 586,
        "abril_maio": 1255,
        "maio_junho": 1158,
        "junho_julho": 1190,
        "julho_agosto": 833,
        "agosto_setembro": 1280,
        "setembro_outubro": 1014
        
    }

    # Converter os dados em um DataFrame
    df_ocorrencias = pd.DataFrame(list(intervalos_mensais.items()), columns=['Mês', 'Ocorrências'])

    # Calcular as variações para o gráfico de ponte
    df_ocorrencias['Variação'] = df_ocorrencias['Ocorrências'].diff().fillna(df_ocorrencias['Ocorrências'])

    # Configuração do gráfico de ponte
    fig = go.Figure(go.Waterfall(
        name="Variação Mensal",
        orientation="v",
        measure=["absolute"] + ["relative"] * (len(df_ocorrencias) - 2) + ["total"],
        x=df_ocorrencias["Mês"],
        y=df_ocorrencias["Variação"],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        text=df_ocorrencias["Ocorrências"]
    ))

    # Customizar o layout do gráfico
    fig.update_layout(
        title="Variação Mensal de Ocorrências de Estouro de Jornada",
        xaxis_title="Mês",
        yaxis_title="Número de Ocorrências",
        waterfallgap=0.3,
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)
