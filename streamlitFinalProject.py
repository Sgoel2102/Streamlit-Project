'''

Name: Sia Goel
CS230: SN1
Data: Used cars for sale on Craigslist

Description:

This program creates a home page with a sidebar with multiple options as to what the user can see and access.  The options are a bar chart of the condition of the cars, a pie chart showing the paint colors of the car, a scatter plot graphing the relationship between the price and years, and finally a map of the latitude and longitude of different manufacturers of the cars list.

'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pydeck as pdk

def pivot(df):

    pivot1 = pd.pivot_table(df, values= "price", index= ["manufacturer"], columns= ["year"])

    return pivot1

def scatter_plot(df):
    st.title("Relationship Between the Price of Used Cars and Time")
    st.write("This graph displays the increase in price of used as the years go on.  The results may indicate the increased inflation over time or the increase in demand of used cars.")
    x = df["year"]
    y = df["price"]
    plt.scatter(x,y,marker = "*", color= "g")
    plt.xlabel("Time in Years")
    plt.ylabel("Prices")

    return plt

def bar_chart(conditions):
    st.title("Condition of Cars")
    st.write("This bar chart takes each manufacturer in the data set and counts the frequency of each condition type of the used car.  It then graphs the type of condition on the x-axis and its frequency for that specific manufacturer on the y-axis.  This graph shows what type of condition you will most likely get for a specific manufacturer of a used car.  This is useful for someone who is interested in getting a specific type of used car.")
    counts = conditions.value_counts()
    condition_dict = counts.to_dict()

    plt.bar(condition_dict.keys(),condition_dict.values(), color= "pink")
    plt.xlabel("Condition Types")
    plt.ylabel("Frequency of Condition Type")
    return plt


def pie_chart(colorsdf):
    st.title("Color of Cars")
    st.write("This pie chart takes the series paint_color and counts the amount of cars painted in each color and plots it into a pie chart format.  This pie chart is useful if a customer would like to purchase a specific color used car and see which color has the most availabilities.")
    paintcount = colorsdf.value_counts()
    paint_dict = paintcount.to_dict()
    plt.subplots(figsize= (10,8))
    plt.pie(paint_dict.values(), labels=None, autopct="%.2f%%",pctdistance=1.1, radius=1.2)
    plt.title("Frequency of Colors of Used Cars")
    plt.legend(labels= paint_dict.keys(), loc= 'upper right', fontsize= "x-small")


    return plt


def map(locations, manuselection1):


    st.write("This map asks the user to select a car manufacturer and then shows the first ten coordinates of the used car postings of that car manufacturer.  This map is useful for narrowing down which car manufacturers are in your area and which will be the easiest for you to purchase.")
    st.write("Customized Map of Used Car Locations")

    view_state = pdk.ViewState(
        latitude=locations["lat"].mean(),
        longitude=locations["long"].mean(),
        zoom = 11,
        pitch = 50)

    layer1 = pdk.Layer('ScatterplotLayer',
                  data = locations,
                  get_position = '[long, lat]',
                  get_radius = 100,
                  get_color = [0,0,255],
                  pickable = True,
                  )

    tool_tip = {"html": "Car Type:<br/> <b>{manuselection1}</b> ",
            "style": { "backgroundColor": "steelblue",
                        "color": "white"}}

    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer1],
        tooltip=tool_tip)

    return map



def main():

    df = pd.read_csv("finalprojectdata.csv")

    side = st.sidebar.radio("Options:", ["home", "bar chart", "pie chart","pivot", "scatter plot", "map"])

    manufacturer_name_list =[]
    for manufacturer in df["manufacturer"]:
        if manufacturer not in manufacturer_name_list:
            manufacturer_name_list.append(manufacturer)


    if side == "home":
        st.title("Welcome to Used Cars Data from Craigslist")
        st.header("On this webpage you will see three different graphs and a map of the Used Cars Data.  Please select which one you would like to see on the sidebar.")
        describe_df = df[["manufacturer", "year","price", "odometer"]]
        manuselection2 = st.selectbox("Choose which car manufacturer's odometer reading you would like to see:", manufacturer_name_list)
        newdataframe2 = describe_df[describe_df["manufacturer"] == manuselection2]
        st.write(newdataframe2.describe())
        st.write("The odometer reading tells the buyer how many miles the car has driven and approximately how many miles are left on the car.  This is extremely useful information when deciding which used car to purchase.")

    elif side == "bar chart":
        manuselection = st.selectbox("Choose which car manufacturer's conditions you would like to see:", manufacturer_name_list)
        newdataframe = df[df["manufacturer"] == manuselection]
        conditions = newdataframe["condition"]
        st.pyplot(bar_chart(conditions), clear_figure=True)
    elif side == "pivot":
        st.write(pivot(df))
        st.write("This pivot table shows Nan for manufacturers which do not have listings in some specific years.  To see specific data you will have to scroll the year that you want to see.")
    elif side == "pie chart":
        colorsdf = df["paint_color"]
        st.pyplot(pie_chart(colorsdf),clear_figure=True)
    elif side == "scatter plot":
        st.pyplot(scatter_plot(df), clear_figure=True)
    elif side == "map":
        manuselection1 = st.selectbox("Choose which car manufacturers' coordinates you would like to see:", manufacturer_name_list)
        newdataframe1 = df[df["manufacturer"] == manuselection1]
        locations = newdataframe1[['lat','long']]
        st.pydeck_chart(map(locations.head(10), manuselection1))


main()


