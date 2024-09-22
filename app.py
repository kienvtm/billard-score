import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import plotly.graph_objects as go
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from datetime import datetime
import pytz

# Get the local time using pytz for timezone awareness
local_timezone = pytz.timezone('Asia/Ho_Chi_Minh')  # Example: Vietnam timezone



scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

skey = st.secrets["service_account"]
credentials = Credentials.from_service_account_info(
    skey,
    scopes=scopes,
)
client = gspread.authorize(credentials)

st.title('Score')

# Inject CSS
st.markdown(
    """
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 80px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("Clear All"):
    # Clear values from *all* all in-memory and on-disk data caches:
    # i.e. clear values from both square and cube
    st.cache_data.clear()
    st.session_state.clear()

if 'count1' not in st.session_state:
    st.session_state.count1 = 0
    st.session_state.count2 = 0

def increment_counter1(increment_value=0):
    st.session_state.count1 += increment_value

def decrement_counter1(decrement_value=0):
    st.session_state.count1 -= decrement_value

def increment_counter2(increment_value=0):
    st.session_state.count2 += increment_value

def decrement_counter2(decrement_value=0):
    st.session_state.count2 -= decrement_value

col1, col2 = st.columns(2)
with col1:
    player1 = st.text_input(label='Nhap ten Player 1', placeholder ='Player 1 name', value ='Player 1')
with col2:
    player2 = st.text_input(label='Nhap ten Player 2', placeholder ='Player 2 name', value ='Player 2')

# with st.container(border=True):
# with col1:
with stylable_container(
        key="green_button",
        css_styles="""
            button {
                background-color: green;
                color: white;
                border-radius: 20px;
            }
            """,
    ):
    col11, col12, col13 = st.columns(3)
    col21, col22, col23 = st.columns(3)
    col31, col32, col33 = st.columns(3)
    # col11, col12 = st.columns(2)
    with col11:
        st.button('+1', on_click=increment_counter1,
            kwargs=dict(increment_value=1))
    with col12:
        st.button('+2', on_click=increment_counter1,
            kwargs=dict(increment_value=2))
    with col13:
        st.button('+3', on_click=increment_counter1,
            kwargs=dict(increment_value=3))
    
    
    # with col12:
    with col21:
        st.button('+9', on_click=increment_counter1,
            kwargs=dict(increment_value=9))
    with col22:
        st.button('-3', on_click=decrement_counter1,
            kwargs=dict(decrement_value=3))
    with col23:
        st.button('-2', on_click=decrement_counter1,
            kwargs=dict(decrement_value=2))
        
    # with col32:
            
# with st.container(border=True):
# with col2:
col3, col4 = st.columns(2)
with stylable_container(
        key="orange_button",
        css_styles="""
            button {
                background-color: orange;
                color: white;
                border-radius: 20px;
            }
            """,
    ):
    col11, col12, col13 = st.columns(3)
    with col11:
        st.button('+1', key='button21', on_click=increment_counter2,
            kwargs=dict(increment_value=1))
    with col12:
        st.button('+2', key='button22', on_click=increment_counter2,
            kwargs=dict(increment_value=2))
    with col13:
        st.button('+3', key='button23', on_click=increment_counter2,
            kwargs=dict(increment_value=3))
    
    # # with col13:
        
    # fig = go.Figure()
    # fig.add_trace(go.Indicator(
    #         mode = "number",
    #         value = st.session_state.count1,
    #         # domain = {'row': 0, 'column': 1}
    #         )
    #         )
    # st.plotly_chart(fig)
    
    col21, col22, col23 = st.columns(3)
    with col21:
        st.button('+9', key='button24', on_click=increment_counter2,
            kwargs=dict(increment_value=9))
    with col22:
        st.button('-3', key='button25', on_click=decrement_counter2,
            kwargs=dict(decrement_value=3))
    with col23:
        st.button('-2', key='button26', on_click=decrement_counter2,
            kwargs=dict(decrement_value=2))
    
    col31, col32, col33 = st.columns(3)
    # with col32:

with col3:
    with st.container(border=True):
        col31, col32, col33 = st.columns(3)
        with col32:
            st.metric(label=player1, value=st.session_state.count1)
with col4:
    with st.container(border=True):
        col31, col32, col33 = st.columns(3)
        with col32:
            st.metric(label=player2, value=st.session_state.count2)

@st.cache_data(ttl=600)
def load_data(key, sheet_name="Sheet1"):
    sh = client.open_by_key(key)
    df = pd.DataFrame(sh.worksheet(sheet_name).get_all_records())
    return df

def update_data(worksheet, df):
    # Find the first non-blank row by checking the length of the sheet
    sh = client.open_by_key(key)
    worksheet = sh.worksheet(worksheet)
    str_list = list(filter(None, worksheet.col_values(1)))
    first_empty_row = len(str_list) + 1
    set_with_dataframe(worksheet, df, row=first_empty_row, col=1, include_index=False, include_column_header=False)
# st.write(st.secrets)
key = st.secrets.connections.gsheets.spreadsheet
st.write(key)

sheet_name='Sheet1'
if st.button("End Game"):
    df = pd.DataFrame({
        'date_time':[datetime.now(local_timezone)],
        'player1':[player1],
        'player1_score':[st.session_state.count1],
        'player2':[player2],
        'player2_score':[st.session_state.count2],
    })
    update_data(sheet_name, df)
    st.cache_data.clear()
    st.rerun()

with st.expander('Historical results', expanded=False):
    df = load_data(key, sheet_name='Sheet1')
    st.dataframe(df)