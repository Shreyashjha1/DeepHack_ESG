import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv("cleaned_esg_dataset.csv")

df = load_data()

st.title("ESG & Financial Performance Explorer")

# Filters
years = sorted(df['Year'].unique())
industries = df['Industry'].unique()

sel_year = st.sidebar.selectbox("Year", [None] + years)
sel_ind = st.sidebar.multiselect("Industry", industries)

q = df.copy()
if sel_year:
    q = q[q['Year']==sel_year]
if sel_ind:
    q = q[q['Industry'].isin(sel_ind)]

# Charts
st.subheader("ESG by Industry")
fig = px.box(q, x="Industry", y="ESG_Overall", color="Industry")
st.plotly_chart(fig)

st.subheader("Carbon vs ESG")
fig2 = px.scatter(q, x="CarbonEmissions", y="ESG_Overall", color="Industry", hover_data=["CompanyName"])
st.plotly_chart(fig2)

st.subheader("ESG Trend Over Time")
trend = q.groupby("Year")["ESG_Overall"].mean().reset_index()
fig3 = px.line(trend, x="Year", y="ESG_Overall", title="Average ESG Over Years")
st.plotly_chart(fig3)

st.subheader("Filtered Data")
st.dataframe(q)