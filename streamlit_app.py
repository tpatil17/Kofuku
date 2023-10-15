import streamlit as st
import requests

st.title("Rizzler")

# Define Streamlit pages
pages = ["Home", "Display Page"]

# Page navigation
st.sidebar.title("Navigation")
page_selection = st.sidebar.radio("Go to", pages, index=0)

usr_input = ""
in2 = ""
user_data_ar = []
if page_selection == "Home":
    st.title("Input Page")
    usr_input = st.text_input("Number of users to Fetch:")
    in2 = st.text_input("Desired number of people you would like to see:")

    if st.button("Start"):
        if usr_input:
            if int(usr_input) == 0:
                st.write("Number of users cannot be Zero!")
            elif in2:
                if int(usr_input) < int(in2):
                    st.write("The desired mates cannot exceed the number of users")
                elif int(in2) == 0:
                    st.write("You sure you don't want to see anyone?")
                else:
                    # Make an HTTP request to the FastAPI route
                    response = requests.post("http://0.0.0.0:8000/chosen_user?n={}&lim={}".format(int(usr_input), in2))
                    if response.status_code == 200:
                        user_data = response.json()
                        user_data_ar.append(user_data)
                        page_selection = "Display Page"
                    else:
                        st.write("Error fetching data from FastAPI.")
            else:
                st.write("Please enter the number of people you want to see")
        else:
            st.write("Please enter something first.")

if page_selection == "Display Page":
    st.title("User")
    disp_usr = user_data_ar[0][0]
    st.write("Chosen User: {} {}".format(disp_usr["first_name"], disp_usr["last_name"]))
    st.write("Nearby people:")
    for i, d in user_data_ar[0][1]:
        st.write("{} {}".format(user_data_ar[0][2][i]["name"]["first"] ,user_data_ar[0][2][i]["name"]["last"] )) 
    
    # Display user data from the response

