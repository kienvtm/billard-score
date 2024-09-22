import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import plotly.graph_objects as go

st.title('Score')

# Inject CSS
st.markdown(
    """
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 100px;
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
with col1:
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
        # col31, col32, col33 = st.columns(3)
        col21, col22, col23 = st.columns(3)
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
        
        # with col32:
        st.metric(label=player1, value=st.session_state.count1)
        
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
            
# with st.container(border=True):
with col2:
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
        # col31, col32, col33 = st.columns(3)
            
        # with col32:
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
        
        st.metric(label=player2, value=st.session_state.count2)
