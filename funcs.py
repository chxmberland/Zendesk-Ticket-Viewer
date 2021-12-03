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
def try_authentication(user_subdomain, user_email, user_pass):

    # Handling invalid inputs
    bad_input = False
    if None in [user_subdomain, user_email, user_pass]:
        
        print("The input is invalid, either your subdomain, email or password was\n \
               null, meaning we can't make the request.")
        return False, None

    # Making sure input is valid before performing an expensive operation
    if not bad_input:

        # Creating the users URL to make a sucsessful API request
        user_url = "https://" + user_subdomain.strip() + ".zendesk.com/api/v2/tickets.json"

        print("\nGetting your data now...")

        # Using Python's requests and HTTPBasicAuth library to abstract the HTTP request from Zendesk's API using basic authentication
        response = requests.get(user_url, auth = HTTPBasicAuth(user_email, user_pass.strip()))

    # Dealing with common RESTful API errors
    errors = {

        401 : "\nZendesk's API was contacted, but it seems as though your username or password is incorrect. A typo, perhaps?",
        
        403 : "\nWe found your account with Zendesk, but it seems like you don't have acsess to their API.\n \
               Unfortunately, we can't help you view your tickets until your Zendesk account has acsess to the API.",

        404 : "\nWe couldn't find your Zendesk domain, you likely made a typo, or ther server is down.",

        408 : "\nThe request timed out, the server might be experiencing high traffic.",
        
        429 : "\nYou've made too many requests too quickly, give the server a second or so to recover."

    }

    # The user was authenticated and the data has been retrieved
    if response.status_code == 200:

        # Congradulating the user on a sucsessful authenrication
        print("\nNice! Zendesk has given us the go ahead to display your data for you.")
        return True, response

    # Checking to see if there was some error that I've created a custom message for
    elif response.status_code in list(errors.keys()):

        print(errors[response.status_code])
        return False, None

    # Some other error occured
    else:

        print("There seems to be some sort of issue. If this issue persists, contact me at lemurwebsites@gmail.com.\n \
               Make the subject line \"ERROR 901 Zendesk\" and I'll try and help!")

        



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
        nws_description = ticket["description"].split()
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
            if interest in ticket:
                t.custom_fields.update({interest : ticket[interest]})
            else: 
                t.custom_fields.update({interest : "No value was given by the API."})

        # Appending the Ticket object to the list of ticket objects
        ticket_objects.append(t)

    # Returning a list of ticket objects
    return ticket_objects



# Creating a function which displays tickets
def display_tickets(attribute_matrix, ticket_objects):

    # Handling bad input
    if (attribute_matrix == None or ticket_objects == None) or (0 in [len(attribute_matrix), len(ticket_objects)]):

        print("There are no tickets related to your account.")
        return False

    # Setting the headers of the table
    table_headers = ["Ticket ID", "Ticket Type", "Ticket Status", "Description", "Created at:", "Updated at:"]
    print("\n")

    # Displaying the tickets accoring to the user
    count = 0
    user_input = ""
    display_next = True
    while user_input != "done":

        # This gateway prevents tickets from displaying directly after the user requests a specific ticket
        if display_next:

            # Adding to the count
            count += 1

            # Abstracting the tabulation of the ticket data using Python's tabulate library
            print(tabulate(attribute_matrix[(count * 25) - 25 : count * 25],    \
                        table_headers,                                          \
                        tablefmt = "github"))
        
        else:

            display_next = True

        # Getting the users input
        valid_inputs = ["b", "n", "done", "id"]
        question = "\nHit n to see the next 25 tickets."        \
                 + "\nHit b see the previous 25 tickets."       \
                 + "\nType id to see a specific ticket."        \
                 + "\nType done if you're done."
        
        user_input = get_user_pref(valid_inputs, question)

        # Acting accordingly
        if user_input == "b" and (count * 25) - 50 >= 0:
            count -= 2
        elif user_input == "b" and (count * 25) - 50 < 0:
            count = 0
        elif user_input == "n" and (count + 1) * 25 > len(attribute_matrix):
            count -= 1
        
        # The user has requested to view an id of a specific ticket
        elif user_input == "id":

            # Getting the id of the specific ticket you're looking for
            valid_inputs = []

            # Changing the numbers to strings
            counter = 0
            while counter < len(ticket_objects):
                valid_inputs.append(str(counter))
                counter += 1

            # Preparing to get input from the user
            question = "\nEnter the id of the ticket you would like to see: "
            req_id = int(get_user_pref(valid_inputs, question))

            # Getting the specific ticket
            ticket_objects[int(req_id) - 1].print_ticket()

            # Preventing the table from being printed again for the sake of a cleaner UI
            display_next = False

    print("\n\nThank you for using my program! Have a great day.")
    return True