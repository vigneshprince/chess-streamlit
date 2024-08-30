import requests
import streamlit as st
import pandas as pd
import time
from bs4 import BeautifulSoup
import streamlit_antd_components as sac
st.set_page_config(layout="wide")

# Sample DataFrame (replace with your actual data fetching logic)
@st.cache_data
def fetch_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table',class_="CRs1")
    table_data = []
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            row_data.append(cell.get_text().strip())
        table_data.append(row_data)
    df= pd.DataFrame(table_data[1:], columns=table_data[0])
    return df.set_index(df.columns[0])


col1, col2 = st.columns(2,vertical_alignment="bottom")

# Search box and button
search_term = col1.text_input("Paste chess link")
search_button = col2.button("Search")


# Filter and display data on button click
if search_term or search_button:
    # Placeholder for the DataFrame while data is being fetched
    placeholder = st.empty()
    
    with st.spinner(text="In progress"):
        url = "https://chess-results.com/tnr994345.aspx?lan=1".strip("&zeilen=99999")+"&zeilen=99999"
        st.session_state['df']=fetch_data(url)
        selected=sac.chip(
            items=[
                sac.ChipItem(label=x) for x in sorted(set(st.session_state['df']["Typ"]))
            ], label='Filter', index=[0], align='center', radius='md', multiple=False
        )
        data=st.session_state['df'][st.session_state['df']['Typ']==selected]
        st.markdown(f"Filtered \"**{len(data)}**\" rows")
        st.table(data)