import streamlit as st
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image
import seaborn as sns
import mysql.connector

dbs=mysql.connector.connect(
    host="localhost",
    user="root@localhost",
    password="Charu@9601",
    database='airbnb',
    port='3306'
)
cursor=dbs.cursor()
query='''select *From airbnb_analysis'''
cursor.execute(query)
data = cursor.fetchall()
cursor.close()



Cleaned_data=pd.DataFrame(data,columns=['name','summary','description','property_type','room_type','bed_type','minimum_nights','maximum_nights','cancellation_policy','last_scraped',
                                        'calendar_last_scraped','accommodates','bedrooms','beds','number_of_reviews','bathrooms','price','extra_people','guests_included',
                                        'get_picture_url','host_url','host_name','host_picture_url','availability_30','availability_60','availability_90',
                                        'availability_365','country_name'])


st.set_page_config(layout="wide")
st.title("Airbnb Analysis")
selected=option_menu(None,options=["About_Airbnb","Explore_data","Insights_table"],
                     icons=["rooms","bi-people","table"],
                     default_index=0,
                     orientation="horizontal",
                     styles={"container": {"width": "100%"},
                               "options": {"margin": "10px"},
                               "icon": {"color": "green", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "15px", "--hover-color": "#6F36AD"},
                               })




def country_data():
    Cou_data=Cleaned_data.groupby(["country_name"])["price"].sum()
    cou_index=Cou_data.reset_index()
    plt.bar(cou_index.index, cou_index["price"])
    plt.xticks(cou_index.index, cou_index["country_name"],rotation=90)
    plt.xlabel("country_name")
    plt.ylabel("price")
    plt.title("Bar chart for which country have highest price")
    plt.tight_layout()
    col1,col2 =st.columns(2) 
    with col1:
       st.pyplot(plt)

def Country_Property_Price(country_):
    filtered_df = Cleaned_data[Cleaned_data['country_name'] == country_]
    Price_value = filtered_df.groupby(["property_type", "country_name"])["price"].sum()
    Price_value = Price_value.reset_index()
    plt.scatter(Price_value.index, Price_value['price'])
    plt.title('Scatter Plot Outliers Visible')
   
    col1,col2 =st.columns(2)
    with col1:
        st.pyplot(plt) 
    plt.figure(figsize=(10, 8))
    plt.plot(Price_value["property_type"], Price_value["price"])
    plt.xticks(rotation=90)
    plt.xlabel("Property Type")
    plt.ylabel("Price")
    plt.title("Price vs Property Type")
    plt.tight_layout()  
    col1,col2 =st.columns(2)
    with col2:
       st.pyplot(plt)

    
def Property_price(Property):
    filtered_df = Cleaned_data[Cleaned_data['property_type'] == Property]  
    Price_value=filtered_df.groupby(["country_name","property_type"])["price"].sum()
    Price_value= Price_value.reset_index()
    plt.figure(figsize=(8, 8))
    plt.pie(Price_value["price"],labels=Price_value['country_name'],startangle=0,autopct='%1.1f%%')
    plt.title("{} level in all countries".format(Property))
    col1,col2 =st.columns(2)
    with col1:
       st.pyplot(plt)

def Booking_available():
    book_availabilty = Cleaned_data.groupby(["last_scraped", "country_name"]).size().reset_index()
    plt.pie(book_availabilty[0], labels=book_availabilty["country_name"], startangle=140, autopct='%1.1f%%')
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title("Booking_Availability")
    col1,col2 =st.columns(2)
    with col1:
       st.pyplot(plt)

def reviews_data():
    reviews=Cleaned_data.groupby(["country_name"])["number_of_reviews"].sum()
    reviews_=reviews.reset_index()
    plt.bar(reviews_.index,reviews_["number_of_reviews"])
    plt.xlabel("country_name")
    plt.ylabel("number_of_reviews")
    plt.title("Highest Review Country")
    plt.xticks(reviews_.index, reviews_["country_name"],rotation=45)
    col1,col2 =st.columns(2)
    with col1:
       st.pyplot(plt)

def avalable_days_data(available):
    data=Cleaned_data.groupby(["country_name"])[[available]].sum().reset_index()
    plt.figure(figsize=(6,6))
    plt.pie(data[available],labels=data['country_name'],startangle=140,autopct='%1.1f%%',center=(0,0))
    plt.title("Availability details for upcomig days")
    plt.axis('equal')
    col1,col2 =st.columns(2)
    with col1:
       st.pyplot(plt)  
       st.table(data) 

def Property_available(available,country_Name):
    country_vice=Cleaned_data[Cleaned_data["country_name"]==country_Name]
    data_property=country_vice.groupby(["property_type"])[[available]].sum().reset_index()
    plt.figure(figsize=(10,8))
    plt.bar(data_property.index,data_property[available])
    plt.xlabel("property_type")
    plt.ylabel(available)
    plt.xticks(data_property.index, data_property["property_type"],rotation=45)

    plt.title("Available property for {}".format(country_Name))
    col1,col2 =st.columns(2)
    with col1:
       st.pyplot(plt)
       st.table(data_property) 

def tables_Pro(Country,Pro_type):
    Table = Cleaned_data[(Cleaned_data["country_name"] == Country) & (Cleaned_data["property_type"] == Pro_type)].reset_index(drop=True,inplace=False)
    Table=Table.astype(str)
    Table_=Table.groupby(["name","summary","room_type","bed_type","minimum_nights","maximum_nights","cancellation_policy","accommodates","bedrooms",'beds', 'number_of_reviews', 'bathrooms','price',
        'extra_people', 'guests_included', 'get_picture_url','host_picture_url','host_url','host_name']).size().reset_index()
    pivot_table = Cleaned_data.pivot_table(index="country_name", columns="room_type", values="price", fill_value=0)
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, cmap="YlGnBu")
    plt.title("Heatmap of Property Data")
    plt.xlabel("Address")
    plt.ylabel("Name")
    col1,col2 =st.columns(2)
    with col1:
       st.pyplot(plt)
       
    st.table(Table_ )   

def tables_Pro1(Country,roo_type,Pro_type):
    Table = Cleaned_data[(Cleaned_data["country_name"] == Country) & (Cleaned_data["room_type"] == roo_type) &(Cleaned_data["property_type"] == Pro_type) ].reset_index(drop=True,inplace=False)
    Table=Table.astype(str)
    Table_=Table.groupby(["name","summary","bed_type","minimum_nights","maximum_nights","cancellation_policy","accommodates","bedrooms",'beds', 'number_of_reviews', 'bathrooms', 'price',
        'extra_people', 'guests_included', 'get_picture_url','host_picture_url','host_url','host_name']).size().reset_index()
    
    st.table(Table_) 

if selected=="About_Airbnb":
      col1,col2=st.columns(2)
      with col1: 
            Image_path="C:/Users/charu/OneDrive/Pictures/Airbnb.jpg"
            image_data=Image.open(Image_path)
            larger_image = image_data.resize((500, 500))
            st.image(larger_image)
      with col2:

        st.markdown(
                        """
                        <style>
                        .reportview-container .main .block-container {
                            font-family: "Times New Roman", Times, serif;
                            color: blue;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

               
                
        st.write('''
        What Is Airbnb? 

        Airbnb (ABNB) is an online marketplace that connects people who want to rent out their homes
        with people looking for accommodations in specific locales.The company has come a long way since 2007, 
        when its co-founders first came up with the idea to invite paying guests to sleep on an air mattress in their living room.

        About Airbnb:
        1) Airbnb offers a wide range of accommodation options, including apartments, houses, villas, and even unique properties like treehouses and castles.
        2) Hosts on Airbnb can earn extra income by renting out their spaces, while travelers can enjoy unique and personalized experiences.
        3) The platform provides a way for hosts and guests to communicate and review each other, building trust within the community.
        4) Airbnb has expanded its services beyond accommodations, offering experiences and activities hosted by locals in various destinations.
        5) The company has faced regulatory challenges in some cities and countries, leading to debates about the impact of short-term rentals on local housing markets and communities.''')

elif selected=="Explore_data":
     Box=st.selectbox("Select analysis data",("1,Bar chart for which country have highest price",
                                              "2,Scatter Plot Outliers Visible and Price vs Property Type",
                                              "3,Each property  level in all countries",
                                              "4,Booking_Availability for all country",
                                              "5.Highest review count of all country",
                                              "6.Availability details for upcomig days",
                                              "7.Avilability count for particular country"))   
     if Box== "1,Bar chart for which country have highest price":
          country_data()
     if Box=="2,Scatter Plot Outliers Visible and Price vs Property Type":
            country_=st.radio("Select Country_name",['Turkey', 'Portugal', 'Hong Kong', 'Brazil', 'United States',
                                                     'Canada', 'Spain', 'Australia', 'China'])
            Country_Property_Price(country_) 
     if Box=="3,Each property  level in all countries":
              Property=st.selectbox('select Property',('House', 'Apartment', 'Condominium', 'Loft', 'Guesthouse',
                                    'Serviced apartment', 'Hostel', 'Bed and breakfast', 'Treehouse',
                                    'Bungalow', 'Guest suite', 'Townhouse', 'Cabin', 'Villa', 'Other',
                                    'Boat', 'Chalet', 'Farm stay', 'Boutique hotel', 'Cottage',
                                    'Earth house', 'Aparthotel', 'Resort', 'Tiny house',
                                    'Nature lodge', 'Casa particular (Cuba)', 'Hotel', 'Camper/RV',
                                    'Hut', 'Barn', 'Heritage hotel (India)', 'Pension (South Korea)',
                                    'Campsite', 'Houseboat', 'Castle', 'Train'))
              Property_price(Property)

     if Box=="4,Booking_Availability for all country" :
            Booking_available()
     if Box=="5.Highest review count of all country":
            reviews_data() 

     if Box=="6.Availability details for upcomig days":
             available=st.radio("Select Availability",["availability_30","availability_60","availability_90","availability_365"])
             avalable_days_data(available)

     if Box=="7.Avilability count for particular country":
              country_Name= st.radio("Select Country_name",['Turkey', 'Portugal', 'Hong Kong', 'Brazil', 'United States',
                                                     'Canada', 'Spain', 'Australia', 'China'])
              available=st.radio("Select Availability",["availability_30","availability_60","availability_90","availability_365"])                                       
              Property_available(available,country_Name)       

elif selected=='Insights_table':
     Country= st.radio("Select Country_name",['Turkey', 'Portugal', 'Hong Kong', 'Brazil', 'United States',
                                                     'Canada', 'Spain', 'Australia', 'China'])
     Pro_type=st.selectbox('select Property',('House', 'Apartment', 'Condominium', 'Loft', 'Guesthouse',
                                    'Serviced apartment', 'Hostel', 'Bed and breakfast', 'Treehouse',
                                    'Bungalow', 'Guest suite', 'Townhouse', 'Cabin', 'Villa', 'Other',
                                    'Boat', 'Chalet', 'Farm stay', 'Boutique hotel', 'Cottage',
                                    'Earth house', 'Aparthotel', 'Resort', 'Tiny house',
                                    'Nature lodge', 'Casa particular (Cuba)', 'Hotel', 'Camper/RV',
                                    'Hut', 'Barn', 'Heritage hotel (India)', 'Pension (South Korea)',
                                    'Campsite', 'Houseboat', 'Castle', 'Train'))
     roo_type=st.radio("select Room_type option",['Entire home/apt', 'Private room', 'Shared room'])
     tables_Pro1(Country,roo_type,Pro_type)
     tables_Pro(Country,Pro_type)
    

      