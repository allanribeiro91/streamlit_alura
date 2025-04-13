import streamlit as st
import requests
import pandas as pd
import plotly.express as px

#dashboard
st.title('DASHBOARD DE VENDAS :shopping_trolley:')

#data
url = 'https://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())

# tables
receita_estados = dados.groupby('Local da compra')[['Preço']].sum()
receita_estados = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)

# graphics
fig_mapa_receita = px.scatter_geo(receita_estados, 
                                  lat= 'lat',
                                  lon= 'lon',
                                  scope='south america',
                                  size= 'Preço',
                                  template= 'seaborn',
                                  hover_name= 'Local da compra',
                                  hover_data= {'lat': False, 'lon': False},
                                  title= 'Receita por estado')

# datavizualization
aba1, aba2, aba3 = st.tabs(['Receita', 'Qtd Vendas', 'Vendedores'])

with aba1:
    ### KPIs
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        receita = dados['Preço'].sum()
        receita_formatada = f"{receita:,.2f}"
        receita_formatada = receita_formatada.replace(",", "X").replace(".", ",").replace("X", ".")
        st.metric('Receita Total R$', receita_formatada, help='Somatória da receita total')
    with coluna2:
        qtd_vendas = dados.shape[0]
        qtd_vendas = f"{qtd_vendas:,}"
        qtd_vendas = qtd_vendas.replace(",",".")
        st.metric('Qtd de Vendas', qtd_vendas)
    
with aba2:
    st.text('Teste')

with aba3:
    st.plotly_chart(fig_mapa_receita)




