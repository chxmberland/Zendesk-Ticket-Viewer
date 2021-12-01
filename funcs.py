# Importing the necessary libraries to make a sucsessful request
import requests
from requests.auth import HTTPBasicAuth

# Importing the necessary libraries to process the request data
import json

# Importing a custom ticket class
from ticket import Ticket

# Importing a library which helps to format tables
from tabulate import tabulate



# Creating a function which tries to authenticate the user
def try_authentication():

    # Getting the users data
    user_subdomain =    input("\nPlease enter your personal Zendesk subdomain (it should look like https://\{subdomain\}.zendesk.com): ")
    user_email =        input("Now, the email related to your Zendesk account: ")
    user_pass =         input("Finally, your password (I'll keep it secret): ")

    user_url = "https://" + user_subdomain.strip() + ".zendesk.com/api/v2/tickets.json"


    print("\nGetting your data now...")

    # Using Python's requests and HTTPBasicAuth library to abstract the HTTP request from Zendesk's API using basic authentication
    response = requests.get(user_url, auth = HTTPBasicAuth(user_email, user_pass.strip()))

    # The user was not authenticated
    if response.status_code != 200:

        print("\nOur program was unable to authenticate you, or Zendesk's API is unavailable." \
            + "\nDouble check your email and password, that's most likely the issue." \
            + "\nIf this error persists, reach out to us at becha9260@gmail.com, and we'll help fix the problem." + "\n")
        return False, None

    # The user was sucsessfully authenticated
    else:

        # Congradulating the user on a sucsessful authenrication
        print("\nNice! Zendesk has given us the go ahead to display your data for you.")
        return True, response



# Defining a function that checks to see if the user would like to view the next tickets
def get_user_pref(valid_inputs, question):

    # Getting input from the user to see if they would like to see more tickets ["b", "n", "done"]
    user_input = ""

    while user_input not in valid_inputs:
        user_input = input(question)

        # Checking for valid input
        if user_input not in valid_inputs:
            print("\nInvalid input, sorry I don't understand.")

    return user_input



# Creating Ticket objects from JSON data
def create_tickets(ticket_list_JSON, fields_of_interest):

    # Creating a second list which will hold ticket objects, as defined by the Ticket class in ticket.py
    ticket_objects = []

    # Looping through the tickets in the JSON object
    for ticket in ticket_list_JSON:

        # Making the created_at and updated_at fields easier to read
        new_created_at = ticket["created_at"].replace("T", " at ").replace("Z", " ")
        new_updated_at = ticket["created_at"].replace("T", " at ").replace("Z", " ")

        # Removing the whitespace from the description
        nws_description = ticket["description"][0 : 30].split()
        nws_description = " ".join(nws_description)

        # Instantiating a new ticket based on the properties of the JSON ticket
        t = Ticket(

            # Setting all of the properties of the ticket based on the JSON ticket
            ticket["id"],
            ticket["type"],
            ticket["status"],
            nws_description,
            new_created_at,
            new_updated_at,
            None
        )

        # Adding any addtional fields specified by the user
        for interest in fields_of_interest:

            # Storing the field name and it's data in a dictionary related to the Ticket object
            t.custom_fields.update({interest : ticket[interest]})

        # Appending the Ticket object to the list of ticket objects
        ticket_objects.append(t)

    # Returning a list of ticket objects
    return ticket_objects



# Creating a function which displays tickets
def display_tickets(attribute_matrix):

    # Setting the headers of the table
    table_headers = ["Ticket ID", "Ticket Type", "Ticket Status", "Description", "Created at:", "Updated at:"]
    print("\n")

    # Displaying the tickets accoring to the user
    count, user_input = 0, ""
    while user_input != "done":

        # Adding to the count
        count += 1

        # Abstracting the tabulation of the ticket data using Python's tabulate library
        print(tabulate(attribute_matrix[(count * 25) - 25 : count * 25],    \
                       table_headers,                              \
                       tablefmt = "github"))

        # Getting the users input
        valid_inputs = ["b", "n", "done", "id"]
        question = "\nHit n to see the next 25 tickets."        \
                    + "\nHit b see the previous 25 tickets."    \
                    + "\nType id to see a specific ticket."     \
                    + "\nType done if you're done."
        
        user_input = get_user_pref(valid_inputs, question)

        # Acting accordingly
        if user_input == "b" and (count * 25) - 50 >= 0:
            count -= 2
        elif user_input == "b" and (count * 25) - 50 < 0:
            count = 0
        elif user_input == "n" and (count + 1) * 25 > len(attribute_matrix):
            count -= 1