import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Airbnb Analysis - Lucia Rodriguez-Arias")
st.markdown("We are gonig to analyze the airbnb dataframe with what we have learned in class about streamlit")
dataf = pd.read_csv("airbnb.csv")
st.dataframe(dataf.head(5))

# Use of sidebar and columns
st.sidebar.header("Filters")
st.caption("This fitler will be used to show the specific visualizations depending on what neighbourhood you choose.")
choosen_neigh = st.sidebar.multiselect("Choose a neighbourhood", dataf["neighbourhood"].unique())

#age filtering 
input_age = st.number_input("Enter your age", min_value=0, max_value=100) 
if input_age < 18:
    st.markdown(":red[You] need someone older to help you do this proccess:")
else:
    st.markdown(":green[You] are allow to do this proccess by yourself:")

#filtering by neighbourhood to only show the chosen ones 
st.subheader("Top Neighborhoods by Listings")
st.markdown("This graph will show as much neighbourhoods as you choose.")
top = st.radio("How many neighborhoods do you want to visualize?", [3, 5, 10, 20, 50])
df_top_neigh = dataf["neighbourhood"].value_counts().reset_index().head(top)
df_top_neigh.columns = ["neighbourhood", "count"]
fig= px.bar(df_top_neigh, x="count", y="neighbourhood", orientation="h", title=f"Top {top} Neighborhoods", color="neighbourhood")
st.plotly_chart(fig, key=f"top_{top}_neighborhoods")

#update the dataframe to only include the neighbourohoods chosen 
if choosen_neigh:
    filtered_dataf = dataf[dataf["neighbourhood"].isin(choosen_neigh)]
else:
    filtered_dataf = dataf.copy()

# 2 different tabs
tab1,tab2 = st.tabs(["Visualizations","Price Simulator"]) 
with tab1:
    col1,col2 = st.columns(2)
     #A graph to study the relationship between listing type and the number of people
    with col1:

        st.subheader("Relationship between type of room - number of people")
        fig1 = px.histogram(filtered_dataf,x="room_type",y="minimum_nights", histfunc="avg", color ="room_type")
        st.plotly_chart(fig1)

    with col2:

        st.subheader("Price per type of House")
        #without outliers
        fig2 = px.box(filtered_dataf[filtered_dataf["price"]<400],x="room_type",y="price", color="room_type")
        st.plotly_chart(fig2)

with tab2:
    st.subheader("Price simulator")
    input_neigh = st.selectbox("Select your desired neighbourhood", dataf["neighbourhood"].unique())
    input_room = st.selectbox("Select your desired type of room", dataf["room_type"].unique())
    input_nights = st.slider("Slide the dot to choose as many nights as you want",1,5,30)
    
    #filtering independent to sidebar filter
    price_info = dataf[(dataf["neighbourhood"]==input_neigh) & (dataf["room_type"]==input_room)]
    sugested_price = price_info["price"].median()

    if pd.notna(sugested_price):
        st.write(f"Suggested price: **{sugested_price} euros per night**")
    else:
        st.write("There is not enugh information to mkae a recomendation. ")

    
# Minimum of two more graphs of your own imagination.
    #apartments with hights reviews per month
    st.subheader("Top apartments with highest reviews pero month")
    df_top_reviews= dataf.sort_values("reviews_per_month", ascending=False).head(10)
    fig3 = px.bar(df_top_reviews, x="name", y="reviews_per_month",color="neighbourhood", title="Apartments with highest reviews pero month")
    st.plotly_chart(fig3)

    #another additional graph
    st.subheader("Relationship between number of reviews and price")
    scatter_data = dataf[dataf["neighbourhood"]==input_neigh]
    fig4 = px.scatter(scatter_data,x="reviews_per_month", y="price", color="room_type", title=f"Number of reviews vs price in {input_neigh}")
    st.plotly_chart(fig4)