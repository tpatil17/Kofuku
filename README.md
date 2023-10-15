# Kufuku
Kofuku challenge

Dependancies: The Application is developed usig SQLite, FastAPI, Streamlit and Randomuser.me

Running the application: If you are running the application on a local machine, please make sure that you have the required dependancies installed for smooth functioning.

To launch the app, run BackEnd.py file in one terminal then run the streamlit_app.py in another terminal simultaneously. After Running the Streamlit file a new window on your web browser should open prompting you for two input fields; Number of users to fetch (the number of users you would like to get from randomuser.me) and next field for the number of people you want plotted on the graph. 

On clicking the start button the app will need some time to fetch the data and apply the logic to display the users table and their on map location.

Sources: 1) FastApi ( https://fastapi.tiangolo.com/tutorial/first-steps/) for understanding how to use the FastApi to get and post data to the database.

2) https://docs.streamlit.io/library/get-started/installation for understanding the use of streamlit and referancing its features

3) https://www.tutorialspoint.com/fastapi/fastapi_sql_databases.htm For linking the database with fastApi

4) https://randomuser.me/ sample user data

commands: "uvicorn BackEnd:app --host 0.0.0.0 --port 8000" for starting the backend, please use the specified command as the HTTP request from streamlit is sent to the same host and port.

streamlit run streamlit_app.py to launch the app

About the Code:

BackEnd.py: 

Users: the table in our database that stores data
UsersCreate: A base model class that is used to post user data to the table

func distance: Calculated the distance between two pairs of latitudes and longitudes using haversin formula
func get_random_users: Generates n random users from Randomuser.me
func create_item: send a post request via fastApi to add a user to the table
func startup: the input taken from streamlit is read here and then calls get_random_users() to generate n users, then gets a random number in range n
from python's random(), uses it as a uid to select a random user. Based on the selection, calls distance() the calulate the distance between selected 
user and others to create a list of touples containing uid and distance. The list of touple pair is sorted based on distance and sliced at x to get x closest users. This data is exported to streamlit.

streamlit_app.py: This file contains the streamlit api, first you will be asked to enter two values. These values will generate the list of users and find closest x users. Once the start button is clicked, a post requst containing inputs is sent to the fastapi endpoint which then starts working as explained above. The data returned is then used to display user and plot others on map.

