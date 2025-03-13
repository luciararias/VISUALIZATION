import streamlit as st
import pandas as pd
st.text("hola")

df =pd.read_csv("airbnb.csv")
st.title("AirBNB Analysis")
st.table(df.head())
st.subheader("Top host in madrid")
df_host = df.groupby(["host_id","host_name"]).size().reset_index()
df_host_sorted = df_host.sort_values(by=0,ascending=False).head(10) 

st.dataframe(df_host_sorted)

import plotly.express as px

fig = px.bar(df_host_sorted,x="host_name",y=0)
st.plotly_chart(fig)

#selecting top host

host_selecting=st.radio("How many host do you want to visualize?",[5,10,20,50])
df_host_sorted= df_host.sort_values(by=0,)