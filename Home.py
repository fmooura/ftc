######## IMPORTAR BIBLIOTECAS ########

from haversine import haversine
import plotly.express as px
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from PIL import Image
import inflection

st.set_page_config(page_title="Visão Geral", layout="wide")


######## FUNÇÕES ########

def clean_code(df1):

    COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
    }

    COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }
    def color_name(color_code):
        return COLORS[color_code]

    def country_name(country_id):
        return COUNTRIES[country_id]

    def rename_columns(df1):
        df1 = df.copy()
        title = lambda x: inflection.titleize(x)
        snakecase = lambda x: inflection.underscore(x)
        spaces = lambda x: x.replace(" ", "")
        cols_old = list(df1.columns)
        cols_old = list(map(title, cols_old))
        cols_old = list(map(spaces, cols_old))
        cols_new = list(map(snakecase, cols_old))
        df1.columns = cols_new
        return df1

    
    ######## RENOMEAR COLUNAS ########

    df1 = rename_columns(df1)

    ######## REMOVER DUPLICADOS ########

    df1 = df1.drop_duplicates('restaurant_id')

    ######## RENOMEAR PAÍSES ########

    df1['country_code'] = df1['country_code'].apply(country_name)

    ######## RENOMEAR CORES ########

    df1['rating_color'] = df1['rating_color'].apply(color_name)

    ######## SPLIT CULINÁRIAS ########

    df1["cuisines"] = df1.loc[:, "cuisines"].astype(str).apply(lambda x: x.split(",")[0])
    df1.head()
    
    df1 = df1.drop(df1[df1['cuisines'] == 'nan'].index)
    df1 = df1.drop(df1[df1['cuisines'] == 'Mineira'].index)
    
    return df1

    
######## CARREGAR DATAFRAME ########

df = pd.read_csv('zomato.csv')

############ lIMPANDO OS DADOS ############################

df1 = clean_code(df)


#=====================================================================
# LAYOUT NO STREAMLIT
#=====================================================================

st.header('Culinárias')

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('### Análise de restaurantes, regiões e muito mais')
st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Países',
   ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
    default=['Brazil', 'India', 'Canada', 'England', 'New Zeland', 'United States of America'])

st.sidebar.markdown("""---""")

st.sidebar.markdown('##### Powered by Comunidade DS')


#filtro de Paises
linhas_selecionadas = df1['country_code'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#=============================
# Layout no Streamlit
#======================

tab1, tab2 = st.tabs(['Visão Gerencial', '-'])

with tab1:
    with st.container():
        
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            contagem_restaurantes = df1['restaurant_id'].nunique()
            col1.metric('Restaurantes', contagem_restaurantes)
            
        with col2:
            contagem_paises = df1['country_code'].nunique()
            col2.metric('Países', contagem_paises)
            
        with col3:
            contagem_cidades = df1['city'].nunique()
            col3.metric('Cidades', contagem_cidades)
                    
            
        with col4:
            culinarias_ofertadas = df1['cuisines'].nunique()
            col4.metric('Culinárias', culinarias_ofertadas)


       

    with st.container():
        
        st.markdown('# Mapa de endereços')
    
        df_aux = (df1.loc[:, ['city', 'aggregate_rating', 'latitude',         
            'longitude']]
                  .groupby(['city', 'aggregate_rating']).median().reset_index())
        map = folium.Map()
        for index, location_info in df_aux.iterrows():
            folium.Marker([location_info['latitude'], 
            location_info['longitude']], popup=location_info[['city',                                                 'aggregate_rating']]).add_to(map)
        folium_static(map, width=1024, height=600)
                            

            
            
            
           
            