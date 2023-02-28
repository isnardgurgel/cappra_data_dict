# Streamlit-Google Sheet
## Modules
import streamlit as st 
from pandas import DataFrame
import pandas as pd
import unicodedata
from sys import exit
from PIL import Image
from streamlit_searchbox import st_searchbox
from typing import List

#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process

from gspread_pandas import Spread,Client
from google.oauth2 import service_account

# 
import networkx as nx
import matplotlib.pyplot as plt

from datetime import datetime

#setup do título da página
st.set_page_config(page_title="Data Dict", page_icon=None, layout='centered', initial_sidebar_state='collapsed', menu_items=None)

# Disable certificate verification (Not necessary always)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

#credentials for running online streamlit
credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)

client = Client(scope=scope,creds=credentials)
spreadsheetname = "Dicionarios"
spread = Spread(spreadsheetname,client = client)



#call para abrir a imagem da Cappra na página
foto = Image.open('cappra-branco.png')
st.image(foto, width=300)
st.markdown("""<hr style="height:4px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

# Check the connection
#st.write(spread.url)
#@st.cache(ttl=600)
sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

# Functions 
# Get our worksheet names

def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names

# Get the sheet as dataframe
@st.cache(ttl=600)
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df
st.markdown(f"<h3 style='text-align: left; color: White;'> Este é o Data Dict </h3>", unsafe_allow_html=True)
st.markdown(f"<h5 style='text-align: left; color: darkgray;'> >> O dicionário de termos e tags do universo data driven </h6>", unsafe_allow_html=True)
# Check whether the sheets exists
what_sheets = worksheet_names()
what_sheets[0] = "Navegar pelo catálogo de termos e definições"
what_sheets[1] = "Sugerir novos termos ou tags"
what_sheets.append( "Consultar termos específicos (em breve)")


#st.sidebar.write(what_sheets)
ws_choice = st.radio('O que você deseja fazer?',what_sheets)
#df = load_the_spreadsheet(ws_choice)

st.markdown("""<hr style="height:4px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
if ws_choice == "Navegar pelo catálogo de termos e definições":
    df = DataFrame(sh.worksheet('Edição - 1').get_all_records())
    #sheets = ws_choice
    for index, row in df.iterrows():
        st.title(row['Termo'],': ')
        st.subheader(row['Descrição'])
        if row['Tag_2'] == "":
            st.write('<', row['Tag'], '>')
        elif row['Tag_2'] != "":
            st.write('<', row['Tag'],'>', ' <',row['Tag_2'], '>')
        else:
            st.write('<', row['Tag'],'>', ' <',row['Tag_2'], '>', ' <', row['Tag_3'],'>')
        st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
elif ws_choice == "Sugerir novos termos ou tags":
    with st.form('add form', clear_on_submit=True):
        terms_or_tags = st.radio('O que deseja sugerir?', ('novo termo', 'nova tag'))
        consulta = st.text_input('insira a palavra com letras minúsculas e sem acentos, depois aperte o botão [Enviar]', value='')
        submitted = st.form_submit_button("Enviar")
        if submitted:
            st.write('Estamos consultando: ', campo_consulta.split()[0],': ', consulta)
            df2 = df.copy()
            df2.iloc[:,0] = df2.iloc[:,0].apply(string_treat)
            if ws_choice == 'parceiro':
                df2.iloc[:,2] = df2.iloc[:,2].str.replace("(", "")
                df2.iloc[:,2] = df2.iloc[:,2].str.replace(")", '')
                df2.iloc[:,2] = df2.iloc[:,2].str.replace("-", '')
                df2.iloc[:,2] = df2.iloc[:,2].str.replace(" ", '')
                df2.iloc[:,2] = df2.iloc[:,2].str.strip()
            else:
                df2.iloc[:,2] = df2.iloc[:,2].astype(str)
                df2.iloc[:,2] = df2.iloc[:,2].str[-11:]
                
                
            df2.set_index(campo_consulta, inplace=True)
            if consulta not in set(df2.index):
                st.markdown("<h2 style='text-align: center; color: Red;'>Este dado não consta na base!</h1>", unsafe_allow_html=True)
                exit()
                    

            #st.write(df2)
            id = df2.loc[consulta][-1]
else:
    df_2= ""
    siba= ""
    with st.form('search form', clear_on_submit=True):
        

        search = st.text_input("Digite aqui a sua busca, depois clique em 'Procurar'")
        sub_2 = st.form_submit_button("Procurar")
        
        if sub_2:
            st.write('Estamos consultando o termo:', search)
            df_2= DataFrame(sh.worksheet('Edição - 1').get_all_records()) 
            if search in tolist(df_2.Termo):
                siba = f'Temos o termo {search}'
        
        
    st.write(siba)

            

