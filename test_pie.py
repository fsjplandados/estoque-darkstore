import streamlit as st
import plotly.express as px
import pandas as pd

st.write("Streamlit Version:", st.__version__)

df = pd.DataFrame({"Status": ["Ruptura", "Saudável", "Ruptura", "Excesso"]})
status_counts = df['Status'].value_counts().reset_index()

if 'pie_chart' in st.session_state:
    st.write("Session State pie_chart:", st.session_state.pie_chart)

fig_pie = px.pie(status_counts, values='count', names='Status')
st.plotly_chart(fig_pie, key='pie_chart', on_select="rerun")
